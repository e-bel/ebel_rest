import os

from pathlib import Path

HOME = str(Path.home())
PROJECT = '.ebel_rest'
PROJECT_PATH = os.path.join(HOME, PROJECT)

pics_path = os.path.join(PROJECT_PATH, 'pics/algorithms/')
os.makedirs(pics_path, exist_ok=True)
