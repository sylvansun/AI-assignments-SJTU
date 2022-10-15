#!/usr/bin/env python3
import cv2
import numpy as np
import sys


def binarize(gray_image, thresh_val):
    # TODO: 255 if intensity >= thresh_val else 0
    binary_image = np.zeros(gray_image.shape, dtype='uint8')
    binary_image[gray_image >= thresh_val] = 255
    return binary_image


def label(binary_image):
    """
    Note that this method always assume that the pixels in the first row and first column are backgrounds
    for code simplicity. Since this is a computer vision task which processes actual images, this method
    assume that the information on the edges of the image is not important, hence can be omitted
    """
    # global variables
    parent = [0]  # for union-find operation
    num_types = 0  # number of types during the first pass
    inf = int(1e10)  # denote the regions where are backgrounds, for simplicity of codes
    height, width = binary_image.shape[0], binary_image.shape[1]

    # initialization
    labeled_img = np.ones(binary_image.shape, dtype='int') * inf

    # first pass
    for i in range(height-1):
        for j in range(width-1):
            if binary_image[i+1][j+1] == 0:
                labeled_img[i + 1][j + 1] = inf
            else:
                neighbour_type = min(labeled_img[i][j], labeled_img[i][j+1], labeled_img[i+1][j])
                if neighbour_type == inf:
                    num_types += 1
                    parent.append(num_types)
                    labeled_img[i + 1][j + 1] = num_types
                    # print(num_types, i, j)
                else:
                    if i==227 and j==200:
                        print(neighbour_type)
                        print(labeled_img[i][j], labeled_img[i][j+1], labeled_img[i+1][j])
                        print(parent)
                    labeled_img[i + 1][j + 1] = neighbour_type
                    if labeled_img[i][j] < inf:
                        parent[labeled_img[i][j]] = min(neighbour_type, parent[labeled_img[i][j]])
                    if labeled_img[i+1][j] < inf:
                        parent[labeled_img[i+1][j]] = min(neighbour_type, parent[labeled_img[i+1][j]])
                    if labeled_img[i][j+1] < inf:
                        parent[labeled_img[i][j+1]] = min(neighbour_type, parent[labeled_img[i][j+1]])
                    if i==227 and j==200:
                        print(parent)

    print(parent)

    # union find set
    for i in range(len(parent)):
        p = parent[i]
        while p != parent[p]:
            p = parent[p]
        parent[i] = p
        # print(i, parent[i])
    print(set(parent))
    # second pass

    return labeled_img


def get_attribute(labeled_image):
    # TODO
    return attribute_list


def main(argv):
    img_name = argv[0]
    thresh_val = int(argv[1])
    img = cv2.imread('data/' + img_name + '.png', cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    binary_image = binarize(gray_image, thresh_val=thresh_val)
    labeled_image = label(binary_image)
    attribute_list = get_attribute(labeled_image)

    cv2.imwrite('output/' + img_name + "_gray.png", gray_image)
    cv2.imwrite('output/' + img_name + "_binary.png", binary_image)
    cv2.imwrite('output/' + img_name + "_labeled.png", labeled_image)
    print(attribute_list)


if __name__ == '__main__':
    main(sys.argv[1:])