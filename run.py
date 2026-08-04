from dotenv import load_dotenv

load_dotenv()

from web.app import app
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
)

if __name__ == "__main__":
    app.run(debug=True)
