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
    cv2.imwrite('output/' + name + "_normalized.png", edge_int)


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
    # generate the threshholded image
    edge_normalized = (edge_image - np.min(edge_image)) / (np.max(edge_image) - np.min(edge_image)) * 255
    thresh_edge_image = edge_normalized.astype('uint8')
    thresh_edge_image[thresh_edge_image >= edge_thresh] = 255
    thresh_edge_image[thresh_edge_image < edge_thresh] = 0

    # calculate the accumulation array
    height, width, num_r = edge_image.shape[0], edge_image.shape[1], len(radius_values)
    accum_array = np.zeros([num_r, height, width])
    edge_points = np.where(thresh_edge_image == 255)
    num_points = len(edge_points[0])
    dist_to_points = np.zeros([num_points, height, width])
    for i in range(num_points):
        dist_to_points[i] = calculate_distance(height, width, edge_points[1][i], edge_points[0][i])
    for i in range(num_r):
        for j in range(num_points):
            accum_array[i] += np.exp(-1 * np.abs(dist_to_points[j] - radius_values[i]))
        save_normalized_edges(accum_array[i], "circle_centers/radius_" + str(radius_values[i]))
    return thresh_edge_image, accum_array


def calculate_distance(height, width, x, y):
    """
    generate a map which shows the distance of each point to a circle centered at point (x, y) with  given radius
    """
    dist = np.zeros([height, width])
    for i in range(height):
        for j in range(width):
            dist[i][j] = np.sqrt((i - y) ** 2 + (j - x) ** 2)
    return dist


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
    # default parameters
    color = (0, 255, 0)
    thickness = 2
    # center positions
    pos = np.where(accum_array > hough_thresh)
    num_circles = len(pos[0])
    # generate all possible circles, they may share same centers
    circles_multiple = []
    for i in range(num_circles):
        circles_multiple.append((radius_values[pos[0][i]], pos[1][i], pos[2][i]))
    # NMS operation to save a single circle for each position
    circles_multiple.sort(key=lambda x: x[2])
    circles = [circles_multiple[0]]
    for i in range(num_circles-1):
        if circles_multiple[i+1][2] - circles_multiple[i][2] > 5:
            circles.append(circles_multiple[i+1])
    # draw those circles
    for i in range(len(circles)):
        image = cv2.circle(image, (circles[i][2] + 1, circles[i][1]), circles[i][0], color, thickness)
    return circles, image


def main(argv):
    img_name = argv[0]
    img = cv2.imread('data/' + img_name + '.png', cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Q1
    edge_magnitude = detect_edges(gray_img)

    # Q2
    radius = [i for i in range(24, 31)]
    edge_thresh = 140
    edge_binary, accum_arr = hough_circles(edge_magnitude, edge_thresh, radius)
    cv2.imwrite("output/coins_edges.png", edge_binary)

    # Q3
    hough_thresh = 60
    circle_list, img_with_circle = find_circles(gray_img, accum_arr, radius, hough_thresh)
    print(circle_list)
    cv2.imwrite("output/coins_circles.png", img_with_circle)


if __name__ == '__main__':
    main(sys.argv[1:])