import os

LIBRARY_NAME = 'ebel_rest'
HOME = os.path.expanduser('~')

pics_path = os.path.join(HOME, LIBRARY_NAME, 'pics/algorithms/')
os.makedirs(pics_path, exist_ok=True)
