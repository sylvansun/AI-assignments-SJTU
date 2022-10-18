#!/usr/bin/env python3
import cv2
import numpy as np
import sys


def detect_edges(image, stride=1):
    """Find edge points in a grayscale image.

      Args:
      - image (2D uint8 array): A grayscale image.

      Return:
      - edge_image (2D float array): A heat map where the intensity at each point
          is proportional to the edge magnitude.
    """
    pad_img = np.pad(image, ((stride, stride), (stride, stride)), 'constant')
    up, down, left, right = img_shift(pad_img, 'up', stride), img_shift(pad_img, 'down', stride),\
                            img_shift(pad_img, 'left', stride), img_shift(pad_img, 'right', stride)
    ul, ur, dl, dr = img_shift(up, 'left', stride), img_shift(up, 'right', stride),\
                     img_shift(down, 'left', stride), img_shift(down, 'right', stride),
    tool_imgs = [ul, up, ur, left, pad_img, right, dl, down, right]

    sobel_x = np.array([-1, 0, 1, -2, 0, 2, -1, 0, 1])
    sobel_y = np.array([1, 2, 1, 0, 0, 0, -1, -2, -1])

    # calculate the gradients

    grad_x, grad_y = np.zeros(pad_img.shape), np.zeros(pad_img.shape)
    for i in range(len(sobel_x)):
        grad_x += sobel_x[i] * tool_imgs[i]
        grad_y += sobel_y[i] * tool_imgs[i]
    edge_image = np.sqrt(grad_x[stride:-stride, stride:-stride] ** 2 + grad_y[stride:-stride, stride:-stride] ** 2)
    return edge_image


def img_shift(img, direction, stride):
    """

    Args:
        img: original image, need to be padded with zeros
        stride: step size of shift
        direction: shift direction

    Returns:
        the shifted image (2D int array)

    """
    result = np.zeros(img.shape)
    if direction == 'up':
        result[0:-2 * stride, stride:-stride] = img[stride:-stride, stride:-stride]
    if direction == 'down':
        result[2*stride:, stride:-stride] = img[stride:-stride, stride:-stride]
    if direction == 'left':
        result[stride:-stride, 0:-2 * stride] = img[stride:-stride, stride:-stride]
    if direction == 'right':
        result[stride:-stride, 2 * stride:] = img[stride:-stride, stride:-stride]
    return result


def save_normalized_edges(edges, name):
    """

    Args:
        - edges (2D float array): A heat map where the intensity at each point
            is proportional to the edge magnitude.
        - name (string): file name

    Returns:
        - None
    """
    edge_normalized = (edges - np.min(edges)) / (np.max(edges) - np.min(edges)) * 255
    edge_int = edge_normalized.astype('uint8')
    cv2.imwrite('output/' + name + "_normalized_edges.png", edge_int)


def save_binary_edges(edges, name, thresh=116):
    """

    Args:
        - edges (2D float array): A heat map where the intensity at each point
            is proportional to the edge magnitude.
        - name (string): file name

    Returns:
        - None
    """
    edge_normalized = (edges - np.min(edges)) / (np.max(edges) - np.min(edges)) * 255
    edge_int = edge_normalized.astype('uint8')
    edge_int[edge_int >= thresh] = 255
    edge_int[edge_int < thresh] = 0
    cv2.imwrite('output/' + name + "_edges.png", edge_int)


def hough_circles(edge_image, edge_thresh, radius_values):
  """Threshold edge image and calculate the Hough transform accumulator array.

  Args:
  - edge_image (2D float array): An H x W heat map where the intensity at each
      point is proportional to the edge magnitude.
  - edge_thresh (float): A threshold on the edge magnitude values.
  - radius_values (1D int array): An array of R possible radius values.

  Return:
  - thresh_edge_image (2D bool array): Thresholded edge image indicating
      whether each pixel is an edge point or not.
  - accum_array (3D int array): Hough transform accumulator array. Should have
      shape R x H x W.
  """
  raise NotImplementedError  #TODO


def find_circles(image, accum_array, radius_values, hough_thresh):
  """Find circles in an image using output from Hough transform.

  Args:
  - image (3D uint8 array): An H x W x 3 BGR color image. Here we use the
      original color image instead of its grayscale version so the circles
      can be drawn in color.
  - accum_array (3D int array): Hough transform accumulator array having shape
      R x H x W.
  - radius_values (1D int array): An array of R radius values.
  - hough_thresh (int): A threshold of votes in the accumulator array.

  Return:
  - circles (list of 3-tuples): A list of circle parameters. Each element
      (r, y, x) represents the radius and the center coordinates of a circle
      found by the program.
  - circle_image (3D uint8 array): A copy of the original image with detected
      circles drawn in color.
  """
  raise NotImplementedError  #TODO


def main(argv):
    img_name = argv[0]
    img = cv2.imread('data/' + img_name + '.png', cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Q1
    edge = detect_edges(gray_img)
    save_normalized_edges(edge, img_name)
    save_binary_edges(edge, img_name)

    # Q2


if __name__ == '__main__':
    main(sys.argv[1:])

