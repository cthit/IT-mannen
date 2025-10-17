from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    current_app,
    g,
    request,
)
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os
import requests



def devmode_active():
    return os.getenv("DEV_ENV", "False").lower() in ("true", "1", "t")


# Allow HTTP for local development (required for OAuth2Session)
# if devmode_active():

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

gamma_root = "https://auth.chalmers.it"
auth_header = os.getenv("AUTH_HEADER", "")
client_api_root = f"{gamma_root}/api/client/v1"
client_api_groups = f"{client_api_root}/groups"
client_api_groups_for = f"{client_api_groups}/for"


_auth = Blueprint("auth", __name__)


def get_gamma():
    oauth: OAuth = current_app.extensions["authlib.integrations.flask_client"]
    return oauth.gamma


def is_authenticated():
    return session.get("authenticated", False)


def set_user_in_g():
    g.user = session.get("user")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for("auth.login"))
        set_user_in_g()
        return f(*args, **kwargs)

    return decorated_function


@_auth.route("/login")
def login():
    if session.get("authenticated"):
        return redirect(url_for("home.index"))
    return render_template("login.html")


@_auth.route("/authorize")
def authorize():
    gamma = get_gamma()
    return gamma.authorize_redirect(url_for("auth.callback", _external=True))


@_auth.route("/gamma/callback")
def callback():
    gamma = get_gamma()

    token = gamma.authorize_access_token()

    try:
        user_info_response = gamma.get("/oauth2/userinfo", token=token)
        user_info = user_info_response.json()
    except Exception as e:
        user_info = {
            "message": f"UserInfo unavailable: {e}",
            "scopes": token.get("scope", "N/A"),
        }

    if "scope" not in user_info and token.get("scope"):
        user_info["scopes"] = token.get("scope")


    try:
        id = user_info.get("sub")
        r = requests.Session()
        r.headers.update({"Authorization": auth_header})
        groups_response = r.get(f"{client_api_groups_for}/{id}").json()

        # Filter groups to only include committees
        active_groups = [
            {
                "prettyName": group.get("prettyName", {}),
                "name": group.get("superGroup", {}).get("name"),
                "post": group.get("post", {}).get("enName"),
            }
            for group in groups_response
            if group.get("superGroup", {}).get("type") != "alumni"
        ]
    # {
    #     "id": "ab44f720-8ed9-48b4-ba2a-6fb2a03db8f6",
    #     "name": "digit25",
    #     "prettyName": "digIT 25",
    #     "superGroup": {
    #         "id": "dea3493e-66e4-44b2-a657-cb57a6840dab",
    #         "name": "digit",
    #         "prettyName": "digIT",
    #         "type": "committee",
    #         "svDescription": "Digitala system",
    #         "enDescription": "Digital systems"
    #     },
    #     "post": {
    #         "id": "2cf9773d-da45-4532-8203-b085baaaf413",
    #         "version": 30,
    #         "svName": "Vice Ordförande",
    #         "enName": "Vice Chairman"
    #     }
    # }

    except Exception as e:
        print(f"Failed to get api information: {e}")
        active_groups = []

    essential_user_info = {
        "name": user_info.get("name"),
        "cid": user_info.get("cid"),
        "groups": active_groups
    }

    # Store user info in session
    session["user"] = essential_user_info
    # Don't store the full token to save space
    session["authenticated"] = True
    #session["admin"] = is_admin()
    #return essential_user_info
    return redirect(url_for("home.index"))


def clear_auth_session():
    """
    Clear authentication-related session data.

    `user` and `authenticated` keys are removed from the session.
    """
    session.pop("user", None)
    session.pop("authenticated", None)


@_auth.route("/logout")
def logout():
    clear_auth_session()
    return redirect(url_for("home.index"))

def create_blueprint() -> Blueprint:
    return _auth