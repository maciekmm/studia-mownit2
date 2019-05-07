import itertools

import imutils as imutils
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from PIL import Image, ImageFont, ImageDraw, ImageEnhance


def bbox(img):
    img = (img > 0)
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.argmax(rows), img.shape[0] - np.argmax(np.flipud(rows))
    cmin, cmax = np.argmax(cols), img.shape[1] - np.argmax(np.flipud(cols))
    return np.s_[rmin:rmax, cmin:cmax]


def generate_test_case(font):
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vehicula lacus eu orci varius, " \
           "in euismod dui consequat. Aliquam erat volutpat. In hac habitasse platea dictumst. Vivamus augue justo, " \
           "faucibus a ante ac, pharetra auctor lectus. Nullam eleifend nunc in justo condimentum cursus sed quis " \
           "sem. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In tincidunt " \
           "vestibulum turpis sed ultrices. Quisque semper est nunc, nec egestas mi vulputate at. Duis lacinia ante " \
           "in dignissim vestibulum. Maecenas iaculis mollis augue, non laoreet neque dignissim vel. Praesent " \
           "ullamcorper finibus tincidunt. "
    text_size = font.getsize(text)
    char = Image.new('L', text_size, "white")
    imdr = ImageDraw.Draw(char)
    imdr.text((0, 0), text, font=font)
    char = cv2.threshold(np.bitwise_not(np.array(char)), 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return np.bitwise_not(np.array(char))


def load_font_characters(font):
    characters = {}
    #
    for i in itertools.chain(range(ord('a'), ord('z') + 1), range(ord('A'), ord('Z') + 1),
                             range(ord('0'), ord('9') + 1),
                             [ord('"'), ord('.'), ord(','), ord('!')]):
        text_size = font.getsize(chr(i))
        char = Image.new('L', text_size, "white")
        imdr = ImageDraw.Draw(char)
        imdr.text((0, 0), chr(i), font=font)
        char = cv2.threshold(np.bitwise_not(np.array(char)), 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        characters[chr(i)] = char
    return characters


def is_same_line(rect0, rect1):
    mid1 = rect1[1] + rect1[3] // 2
    return rect0[1] < mid1 < rect0[1] + rect0[3]


def extract_words(ref):
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 5))
    sq_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # apply tophat transform for lightning equalization
    # https://en.wikipedia.org/wiki/Top-hat_transform
    tophat = cv2.morphologyEx(ref, cv2.MORPH_TOPHAT, rect_kernel)
    # Compute gradient
    grad_x = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
                       ksize=-1)
    grad_x = np.absolute(grad_x)
    (minVal, maxVal) = (np.min(grad_x), np.max(grad_x))
    grad_x = (255 * ((grad_x - minVal) / (maxVal - minVal)))
    grad_x = grad_x.astype("uint8")
    # Apply closing operation for tophat transformation
    grad_x = cv2.morphologyEx(grad_x, cv2.MORPH_CLOSE, rect_kernel)

    # apply threshold to extract words
    thresh = cv2.threshold(grad_x, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sq_kernel)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # grab words
    contours = imutils.grab_contours(cnts)

    # grow word "selection" by 8 pixels to make sure to include whole words
    shift = 8
    locs = []
    for contour in contours:
        rect = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 40 or cv2.contourArea(contour) > 2000:
            continue
        x, y, w, h = rect
        xs, ys, ws, hs = max(x - shift, 0), max(y - shift, 0), min(w + 2 * shift, orig.shape[0]), min(h + 2 * shift,
                                                                                                      orig.shape[1])
        locs.append((xs, ys, ws, hs))
    locs = sorted(locs, key=lambda x: x[1])

    lines = [[]]
    line = 0

    # sorts words as they appear in image by heuristically guessing whether the word is still in the same line
    for i, cont in enumerate(locs):
        if i != 0 and is_same_line(locs[i - 1], cont) is False:
            # ltr sort
            lines[line] = sorted(lines[line], key=lambda x: x[0])
            # next line
            lines.append([])
            line += 1
        (xs, ys, ws, hs) = cont
        lines[line].append(cont)

    # sort horizontally
    lines[line] = sorted(lines[line], key=lambda x: x[0])
    return [word for row in lines for word in row]


def extract_characters(word):
    """
    Extracts characters by looking for empty columns.
    """
    char_bbs = []
    column = 0
    char_start = -1
    while column < word.shape[1]:
        while not word[:, column].any():
            if char_start != -1:
                char_bbs.append(np.s_[:, char_start:column])
                char_start = -1
            column += 1
        if char_start == -1:
            char_start = column
        column += 1
    if char_start != -1:
        char_bbs.append(np.s_[:, char_start:column])
    return char_bbs


font_file = "fonts/baskvl.ttf"
font = ImageFont.truetype(font_file, size=33)
fig = plt.figure()
characters = load_font_characters(font)
# Pillow draw text -> bitmap -> korelacja ->


orig = cv2.imread("tests/palatino-03.jpg")
# ref = generate_test_case(font)
orig = imutils.resize(orig, width=600)
ref = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(ref)
rotat = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

words = extract_words(ref)

for i, word in enumerate(words):
    (xs, ys, ws, hs) = word
    cv2.putText(orig, str(i), (xs, ys + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, [125])
    cv2.rectangle(orig, (xs, ys), (xs + ws, ys + hs), (255, 255, 255), 1)

plt.imshow(orig)
plt.show()
cv2.waitKey()

threshold = 169

for word in words:
    cropped = rotat[word[1]:word[1] + word[3], word[0]:word[0] + word[2]]
    cropped = cropped[bbox(cropped)]

    word_chars = extract_characters(cropped)

    for word_char in word_chars:
        cropped_char = cropped[word_char]
        cropped_char = cropped_char[bbox(cropped_char)]
        scores = []
        for character, bitmap in characters.items():
            bitmap = bitmap[bbox(bitmap)]
            test = cv2.resize(cropped_char, (bitmap.shape[1], bitmap.shape[0]))
            test[test > threshold] = 255
            test[test <= threshold] = 0
            result = cv2.matchTemplate(test, bitmap, cv2.TM_CCOEFF_NORMED)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append((character, score))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        sys.stdout.write(scores[0][0])
    sys.stdout.write(' ')

sys.stdout.flush()
# grab the (x, y) coordinates of all pixel values that
# are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all
# coordinates
# coords = np.transpose(np.where(thresh > 0))
# print(coords)
# rect = cv2.minAreaRect(coords)
# print()
# box = cv2.boxPoints(rect)  # cv2.boxPoints(rect) for OpenCV 3.x
# box = np.int0(box)
# print(rect)
# cv2.drawContours(thresh, [box], 0, (255, 255, 255), 2)

# fft = np.fft.fft2(rotat)
# max_peak = np.max(np.abs(fft))
#
# # Threshold the lower 25% of the peak
# fft[fft < (max_peak * 0.25)] = 0
#
# # Log-scale the data
# abs_data = 1 + np.abs(fft)
# c = 255.0 / np.log(1 + max_peak)
# log_data = c * np.log(abs_data)
# # Find two points within 90% of the max peak of the scaled image
# max_scaled_peak = np.max(log_data)
#
# # Determine the angle of two high-peak points in the image
# rows, cols = np.where(log_data > (max_scaled_peak * 0.905))
# min_col, max_col = np.min(cols), np.max(cols)
# min_row, max_row = np.min(rows), np.max(rows)
# dy, dx = max_col - min_col, max_row - min_row
# theta = np.arctan(dy / float(dx))
# print(180*theta/np.pi)
# # Translate and scale the image by the value we found
# width, height = thresh.shape
# cx, cy = width / 2, height / 2
# new_image = np.zeros(thresh.shape)
#
# for x, row in enumerate(thresh):
#     for y, value in enumerate(row):
#         xp = cx + (x - cx) * np.cos(theta) - (y - cy) * np.sin(theta)
#         yp = cy + (x - cx) * np.sin(theta) + (y - cy) * np.cos(theta)
#         if xp < 0 or yp < 0 or xp > width or yp > height:
#             continue
#         new_image[int(xp), int(yp)] = thresh[x, y]
# cv2.imshow('', orig)
# cv2.imshow('', thresh)
