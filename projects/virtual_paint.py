# webcam
import sys

import cv2
import numpy as np

frame_w = 640
frame_h = 480
cap = cv2.VideoCapture(0)
cap.set(3, frame_w)
cap.set(4, frame_h)
cap.set(10, 150)
CIRCLE_SIZE = 8

ERASER = [89, 15, 0, 179, 255, 77]
COLORS = [[70, 89, 30, 87, 255, 255],  # green
             [161, 77, 97, 179, 254, 255],  # pink
             [107, 86, 99, 125, 255, 255],  # blue
             [23, 79, 153, 43, 255, 255]  # yellow
             ]  #

COLOR_VALUES = [[45, 187, 0],  # green          # BGR format
                   [100, 0, 255],  # pink
                   [170, 45, 0],  # blue
                   [90, 255, 250]  # yellow
                   ]


def detect_contours(im):
    contours, hierarchy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for ct in contours:  # ct is vector of points
        area = cv2.contourArea(ct)
        arc = cv2.arcLength(ct, True)
        if area < 50 or arc < 100:
            continue  # filter underscores
        cv2.drawContours(IMG_RES, ct, -1, (255, 255, 0), 4)
        app_thresh = 0.01  # 0.01-> 7angle detects 8angle, 0.15-> fewer points for circles
        approx = cv2.approxPolyDP(ct, app_thresh * arc, True)
        x, y, w, h = cv2.boundingRect(approx)

    return x + w // 2, y


def find_eraser() -> tuple:
    img_hsv = cv2.cvtColor(IMG, cv2.COLOR_BGR2HSV)
    lower = np.array(ERASER[:3])
    upper = np.array(ERASER[3:6])
    mask = cv2.inRange(img_hsv, lower, upper)
    x, y = detect_contours(mask)
    cv2.circle(IMG_RES, (x, y), 20, (255, 0,0), cv2.FILLED)
    return x, y


def find_color() -> dict:
    img_hsv = cv2.cvtColor(IMG, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = {}
    for color in COLORS:
        lower = np.array(color[:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(img_hsv, lower, upper)
        # cv2.imshow(str(color[0]), mask)
        x, y = detect_contours(mask)
        # cv2.circle(img_res, (x, y), circle_size, my_color_values[count], cv2.FILLED)
        if x != 0 and y != 0:
            new_points[(x, y)] = count
        count += 1
    return new_points


def draw_on_canvas(points: dict):
    for point, color_id in points.items():
        cv2.circle(IMG_RES, point, CIRCLE_SIZE, COLOR_VALUES[color_id], cv2.FILLED)


if __name__ == '__main__':

    my_points = dict()  # {(x,y): colorID}
    while True:
        success, IMG = cap.read()
        if IMG is None:
            sys.exit("Could not read the image.")

        IMG = cv2.flip(IMG, 1)
        IMG_RES = IMG.copy()

        new_points_dict = find_color()
        if len(new_points_dict) != 0:
            for new_point, clr in new_points_dict.items():
                my_points[new_point] = clr

        if len(my_points) != 0:
            draw_on_canvas(my_points)

        cv2.imshow("Video", IMG_RES)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # TODO
        # erase_point = find_eraser()
        # if erase_point[1] != 0:
        #     print(erase_point)
        # for key, item in my_points.items():
        #     if erase_point[0] + 10 < key[0] < erase_point[0] + 10 or
        #     erase_point[1] + 10 < key[1] < erase_point[1] + 10:
        #         print('YEAAAAAAAH')
        #         my_points.pop(erase_point)
