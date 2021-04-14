import os

from utils.folder_file_manager import make_directory_if_not_exists


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(CUR_DIR, 'utils', 'model')
OUTPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'output'))

CREDENTIAL_PATH = os.path.join(CUR_DIR, 'utils', 'credential', 'vision_key.txt')
STAMP_MODEL_PATH = os.path.join(MODEL_DIR, 'stamp_detector_v2.pb')
SIDE_MODEL_PATH = os.path.join(MODEL_DIR, 'side_classifier.pkl')
CONFIG_FILE_PATH = os.path.join(CUR_DIR, 'user_config.cfg')
TOP_IMAGE_PATH = os.path.join(CUR_DIR, 'top.jpg')
BOTTOM_IMAGE_PATH = os.path.join(CUR_DIR, 'bottom.jpg')

ROTATION_Y_THREAD = 50
CONFIDENCE = 0.9
BAUD_RATE = 115200
STAMP_AREA_THRESH = 0.02
PIXEL_TO_MM = 11.2
PAPER_WIDTH = 210
PAPER_HEIGHT = 290

COLLECTION_PATH = ""
