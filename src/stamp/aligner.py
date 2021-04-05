import os
import ntpath
import glob
import configparser
import numpy as np
import cv2

from src.image_processing.utils import ImageUtils
from settings import PIXEL_TO_MM, PAPER_HEIGHT, PAPER_WIDTH, CONFIG_FILE_PATH, OUTPUT_DIR


class StampAligner:
    def __init__(self):
        params = configparser.ConfigParser()
        params.read(CONFIG_FILE_PATH)
        # self.collection_num = params.get('DEFAULT', 'collection_number')
        self.image_utils = ImageUtils()
        self.paper_width = int(PAPER_WIDTH * PIXEL_TO_MM)
        self.paper_height = int(PAPER_HEIGHT * PIXEL_TO_MM)
        self.align_status = "Init"
        self.current_width = 0
        self.current_height = 0
        self.row_height = 0
        self.row_stamps = {"row_stamp": [], "width": 0, "height": 0}
        self.stamp_status = []

    def align_stamps(self, stamp_frame):
        height, width = stamp_frame.shape[:2]
        if self.paper_width - self.current_width - width < int(4 * PIXEL_TO_MM):
            self.row_stamps["width"] = self.current_width
            self.row_stamps["height"] = self.row_height
            self.current_height += self.row_height
            self.stamp_status.append(self.row_stamps.copy())
            self.current_width = 0
            self.row_height = 0
            self.row_stamps["row_stamp"] = []
            if self.paper_height - self.current_height - height < int(2 * PIXEL_TO_MM * (len(self.stamp_status) + 1)):
                self.align_status = "Complete"
            else:
                self.row_stamps["row_stamp"].append(stamp_frame)
                self.current_width += width
                self.row_height = max(self.row_height, height)
        else:
            self.row_stamps["row_stamp"].append(stamp_frame)
            self.current_width += width
            self.row_height = max(self.row_height, height)

        if self.align_status == "Complete":
            stamp_paper_image = np.ones([self.paper_height, self.paper_width, 3], dtype=np.uint8) * 255
            height_spacing = int((self.paper_height - self.current_height) / (len(self.stamp_status) + 1))
            height_pos = 0
            for i, r_stamps in enumerate(self.stamp_status):
                width_pos = int((self.paper_width - r_stamps["width"]) / 2)
                height_pos += height_spacing
                for r_stamp in r_stamps["row_stamp"]:
                    r_height, r_width = r_stamp.shape[:2]
                    r_height_spacing = r_stamps["height"] - r_height
                    pos_x = width_pos
                    pos_y = height_pos + r_height_spacing
                    stamp_paper_image[pos_y:pos_y + r_height, pos_x:pos_x + r_width] = r_stamp
                    width_pos += r_width
                height_pos += r_stamps["height"]
            processed_image = self.image_utils.run(frame=stamp_paper_image)
            output_images = glob.glob(os.path.join(OUTPUT_DIR, "*.jpg"))
            output_indices = []
            for o_image in output_images:
                image_index = int(ntpath.basename(o_image).replace("StampPaper", "").replace(".jpg", ""))
                output_indices.append(image_index)
            if output_indices:
                cnt_index = max(output_indices) + 1
            else:
                cnt_index = 0
            cv2.imwrite(os.path.join(OUTPUT_DIR, f'StampPaper{cnt_index}.jpg'), processed_image)
            print(f"[INFO] Successfully saved the final StampPaper Image into "
                  f"{os.path.join(OUTPUT_DIR, f'StampPaper{cnt_index}.jpg')}")
            self.stamp_status = []

            return "complete"
        else:
            return "retry"


if __name__ == '__main__':
    stamp_aligner = StampAligner()
    image_paths = glob.glob(os.path.join("", "*.jpg"))
    for i_path in image_paths:
        res = stamp_aligner.align_stamps(stamp_frame=cv2.imread(i_path))
        print(f"[INFO] Image: {ntpath.basename(i_path)}, Res: {res}")
        if res == "Complete":
            break
