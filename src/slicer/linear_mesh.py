import pyx
import numpy as np


def linear_x(shell, x_min, x_max, y_min, y_max, inc):

	mesh_lines = []

	for x in np.arange(x_min, x_max, inc):

		line = pyx.path.line(x, y_min, x, y_max)
		intersects, _ = line.intersect(shell)

		if len(intersects) == 2:

			x1, y1 = line.at(intersects[0])
			x2, y2 = line.at(intersects[1])

			mesh_lines.append(pyx.path.line(x1, y1, x2, y2))

	return mesh_lines


def linear_y(shell, x_min, x_max, y_min, y_max, inc):

	mesh_lines = []

	for y in np.arange(y_min, y_max, inc):

		line = pyx.path.line(x_min, y, x_max, y)
		intersects, _ = line.intersect(shell)

		if len(intersects) == 2:

			x1, y1 = line.at(intersects[0])
			x2, y2 = line.at(intersects[1])

			mesh_lines.append(pyx.path.line(x1, y1, x2, y2))

	return mesh_lines
