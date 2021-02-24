import os
import glob
import ntpath
import cv2

from settings import CUR_DIR


def collect_rotated_images(img_dir):
    image_paths = glob.glob(os.path.join(img_dir, "*.jpg"))
    for i_path in image_paths:
        image_name = ntpath.basename(i_path).replace(".jpg", "")
        image = cv2.imread(i_path)
        clock_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        counter_clock_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        horizontal_image = cv2.rotate(image, cv2.ROTATE_180)
        cv2.imwrite(os.path.join(img_dir, f"{image_name}_clocked.jpg"), clock_image)
        cv2.imwrite(os.path.join(img_dir, f"{image_name}_counter_clocked.jpg"), counter_clock_image)
        cv2.imwrite(os.path.join(img_dir, f"{image_name}_180.jpg"), horizontal_image)

    return


def create_training_images(origin_img_dir):
    image_paths = glob.glob(os.path.join(origin_img_dir, "*.*"))
    cnt = 0
    for i_path in image_paths:
        image = cv2.imread(i_path)
        cv2.imwrite(os.path.join(CUR_DIR, 'training_dir', f"image{cnt}.jpg"), image)
        cnt += 1

    return


if __name__ == '__main__':
    create_training_images(origin_img_dir="/media/main/Data/Task/StampDetectorArduino/Examples2")
