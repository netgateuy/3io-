# run.py

import os

from app import create_app
from instance.config import CONFIG_NAME

app = create_app(CONFIG_NAME)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"), debug=True)