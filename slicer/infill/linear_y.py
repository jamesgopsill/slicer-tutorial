import numpy as np
import pyx


def linear_y(shell, x_min: float, x_max: float, y_min: float, y_max: float, inc: float):
	""" Creates a linear infill along the y axis """

	mesh_lines = []

	for y in np.arange(y_min, y_max, inc):

		line = pyx.path.line(x_min, y, x_max, y)
		intersects, _ = line.intersect(shell)

		if len(intersects) == 2:

			x1, y1 = line.at(intersects[0])
			x2, y2 = line.at(intersects[1])

			mesh_lines.append(pyx.path.line(x1, y1, x2, y2))

	return mesh_lines
