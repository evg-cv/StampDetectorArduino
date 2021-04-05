import math
import numpy as np
import cv2

from settings import PIXEL_TO_MM


def order_points(pts):
    # sort the points based on their x-coordinates
    pts_x_sorted = pts[np.argsort(pts[:, 0]), :]
    left_most = pts_x_sorted[:2, :]
    right_most = pts_x_sorted[2:, :]

    left_most = left_most[np.argsort(left_most[:, 1]), :]
    (tl, bl) = left_most

    right_most = right_most[np.argsort(right_most[:, 1]), :]
    (tr, br) = right_most

    return [tl.tolist(), bl.tolist(), br.tolist(), tr.tolist()]


def get_stamp_contour(roi_frame):
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    _, thresh_frame = cv2.threshold(gray_frame, 200, 255, cv2.THRESH_BINARY_INV)
    st_contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    stamp_contour = sorted(st_contours, key=cv2.contourArea, reverse=True)[0]

    return stamp_contour


def rotate_stamp(frame):
    stamp_contour = get_stamp_contour(roi_frame=frame)
    stamp_rect = cv2.minAreaRect(stamp_contour)
    stamp_box = np.int0(cv2.boxPoints(stamp_rect))
    stamp_box[stamp_box < 0] = 0
    ordered_points = order_points(pts=stamp_box)
    width = int(math.sqrt((ordered_points[1][0] - ordered_points[2][0]) ** 2 +
                          (ordered_points[1][1] - ordered_points[2][1]) ** 2))
    height = int(math.sqrt((ordered_points[0][0] - ordered_points[1][0]) ** 2 +
                           (ordered_points[0][1] - ordered_points[1][1]) ** 2))

    origin_pts = np.float32(ordered_points)
    trans_pts = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
    trans = cv2.getPerspectiveTransform(origin_pts, trans_pts)
    trans_frame = cv2.warpPerspective(frame, trans, (width, height))
    white_image = np.ones([height + round(PIXEL_TO_MM * 2), width + round(2 * PIXEL_TO_MM), 3], dtype=np.uint8) * 255
    stamp_image = white_image.copy()
    stamp_image[round(PIXEL_TO_MM):round(PIXEL_TO_MM) + height, round(PIXEL_TO_MM):round(PIXEL_TO_MM) + width] = \
        trans_frame
    trans_contour = get_stamp_contour(roi_frame=stamp_image)
    black_image = np.zeros([height + round(PIXEL_TO_MM * 2), width + round(2 * PIXEL_TO_MM), 3], np.uint8)
    mask = cv2.drawContours(black_image, [trans_contour], -1, (255, 255, 255), -1)
    blur_edge_frame = (mask / 255.0 * stamp_image).astype(np.uint8)
    final_stamp = blur_edge_frame + white_image
    # cv2.imwrite("test50.jpg", final_stamp)

    # cv2.imshow("Rotated Frame", final_stamp)
    # cv2.waitKey()

    return final_stamp


if __name__ == '__main__':
    rotate_stamp(frame=cv2.imread(""))
