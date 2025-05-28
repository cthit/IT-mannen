from flask import Flask
import pkgutil
import blueprints


def register_blueprints(app: Flask) -> None:

    modules = pkgutil.iter_modules(blueprints.__path__)

    for _, module_name, __ in modules:
        module = __import__(f"blueprints.{module_name}", fromlist=[""])
        blueprint = module.create_blueprint()
        app.register_blueprint(blueprint)


def create_app() -> Flask:
    app = Flask(__name__)

    register_blueprints(app)

    return app


def main() -> None:
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
