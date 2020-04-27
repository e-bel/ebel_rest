import os

LIBRARY_NAME = 'ebel_rest'
HOME = os.path.expanduser('~')
LIBRARY_PATH = os.path.join(HOME, LIBRARY_NAME)

pics_path = os.path.join(LIBRARY_PATH, 'pics/algorithms/')
os.makedirs(pics_path, exist_ok=True)
