
import os
import sys
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + '..')
from app.manage import app

if __name__ == "__main__":
    app.run()
