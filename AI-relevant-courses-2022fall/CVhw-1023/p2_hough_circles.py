#!/usr/bin/env python3
import cv2
import numpy as np
import sys


def detect_edges(image):
    """Find edge points in a grayscale image.

      Args:
      - image (2D uint8 array): A grayscale image.

      Return:
      - edge_image (2D float array): A heat map where the intensity at each point
          is proportional to the edge magnitude.
    """
    pad_img = np.pad(image, ((1, 1), (1, 1)), 'constant')  # actually we do not use this
    sobel_x = np.array([-1, 0, 1, -2, 0, 2, -1, 0, 1]).reshape(3, -1)
    sobel_y = np.array([1, 2, 1, 0, 0, 0, -1, -2, -1]).reshape(3, -1)
    grad_x, grad_y = cv2.filter2D(image, -1, sobel_x), cv2.filter2D(image, -1, sobel_y)
    edge_image = np.sqrt(grad_x ** 2 + grad_y ** 2)
    return edge_image


def save_edges_as_image(edges, name):
    """

    Args:
        - edges (2D float array): A heat map where the intensity at each point
            is proportional to the edge magnitude.
        - name (string): file name

    Returns:
        - None
    """
    scale = int(255/np.max(edges))
    cv2.imwrite('output/' + name + "_edge.png", edges.astype('uint8') * scale)


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
    save_edges_as_image(edge, img_name)

    # Q2


if __name__ == '__main__':
    main(sys.argv[1:])

