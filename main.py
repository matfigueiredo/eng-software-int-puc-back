from config import settings
from core.app_factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=False)