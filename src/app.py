from flask import Flask
import pkgutil
import blueprints
import os
from typing import Sequence
from authlib.integrations.flask_client import OAuth


def register_blueprints(app: Flask) -> None:

    path: Sequence[str] = getattr(blueprints, "__path__")
    modules = pkgutil.iter_modules(path)

    for _, module_name, __ in modules:
        module = __import__(f"blueprints.{module_name}", fromlist=[""])
        blueprint = module.create_blueprint()
        app.register_blueprint(blueprint)


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("APP_SECRET")

    gamma_root = "https://auth.chalmers.it"
    client_id = os.getenv("GAMMA_CLIENT_ID", "")
    client_secret = os.getenv("GAMMA_CLIENT_SECRET", "")


    # Initialize OAuth with the Flask app
    oauth = OAuth(app)

    # Register Gamma OAuth client with proper JWKS URI
    oauth.register(
        name="gamma",
        client_id=client_id,
        client_secret=client_secret,
        api_base_url=gamma_root,
        client_kwargs={
            "scope": "openid profile",
        },
        server_metadata_url=f"{gamma_root}/.well-known/openid-configuration",
    )
    
    register_blueprints(app)

    return app


def main() -> None:
    app = create_app()

    app.run(
        host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_RUN_PORT", 5000)),
    )


if __name__ == "__main__":
    main()
