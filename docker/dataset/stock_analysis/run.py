"""Application entry point."""
from webapp import init_app

app = init_app()

# Using a development configuration
app.config.from_object('config.DevConfig')
# print(app.config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)