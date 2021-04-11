import cv2

from src.image_processing.utils import ImageUtils
from settings import COLLECTION_PATH


image_utils = ImageUtils()
image = cv2.imread(COLLECTION_PATH)
processed_image = image_utils.run(frame=image)
cv2.imshow("Processed Image", processed_image)
cv2.waitKey()