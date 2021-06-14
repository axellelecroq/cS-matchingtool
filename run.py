from app.app import app, config_app


if __name__ == "__main__":
    app = config_app("production")
    app.run(debug=True)