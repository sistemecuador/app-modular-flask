import os

BASE_DIR_P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_FOLDER = os.path.abspath(os.getcwd()) + r"\uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
BASE_STATIC_ROOT = os.path.join(BASE_DIR_P, 'static')
BASE_TEMPLATE_ROOT = os.path.join(BASE_DIR_P, 'templates')