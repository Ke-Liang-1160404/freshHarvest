from flask import Flask
from freshHarvest import app

import os

if __name__ == "__main__":
    # Only start the scheduler if the app is not in debug modes
    app.run(debug=False)
   