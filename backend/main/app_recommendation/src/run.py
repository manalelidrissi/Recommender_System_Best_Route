from app_recommendation.src.app import appli
import os

APP_PORT = int(os.environ.get("APP_PORT", default=5000))

if __name__ == "__main__":
    appli.run(host="0.0.0.0", port=5000, debug=True)