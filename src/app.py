from flask import Flask
import pkgutil
import blueprints
import os
from typing import Sequence


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
