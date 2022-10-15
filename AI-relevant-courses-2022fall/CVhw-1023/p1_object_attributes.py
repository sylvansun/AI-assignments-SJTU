#!/usr/bin/env python3
import cv2
import numpy as np
import sys


def binarize(gray_image, thresh_val):
  # TODO: 255 if intensity >= thresh_val else 0
  return binary_image

def label(binary_image):
  # TODO
  return labeled_image

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
