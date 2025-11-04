from werkzeug.middleware.proxy_fix import ProxyFix
from src.app import create_app

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)