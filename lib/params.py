"""Defines the basic parameters of this app"""

import os

BASE_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TMP_PATH: str = os.path.abspath(os.path.join(BASE_PATH, 'tmp'))

PAUSE_TIME: int = 1