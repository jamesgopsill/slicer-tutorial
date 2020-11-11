import vtk
import pyx
import matplotlib.pyplot as plt

import slicer


if __name__ == "__main__":

	# 3D printer stl file
	file_name = "stls/plate_with_hole.stl"

	# Read in the STL
	stl_file = vtk.vtkSTLReader()
	stl_file.SetFileName(file_name)
	stl_file.Update()
	stl_poly = stl_file.GetOutput()

	# Get the min/max bounds for the STL
	x_min, x_max, y_min, y_max, z_min, z_max = stl_poly.GetBounds()
	print(
		"X min:",
		x_min,
		"X max:",
		x_max,
		"Y min:",
		y_min,
		"Y max:",
		y_max,
		"Z min:",
		z_min,
		"Z max:",
		z_max,
	)

	# Generate internal mesh structure of stl
	stl_tree = vtk.vtkOBBTree()
	stl_tree.SetDataSet(stl_poly)
	stl_tree.BuildLocator()

	# Set a slice level
	level = (z_min + z_max) / 2

	# Create intersecting plane
	plane = vtk.vtkPlane()
	plane.SetOrigin(0, 0, level)
	plane.SetNormal(0, 0, 1)

	# Create cutter
	cutter = vtk.vtkCutter()
	cutter.SetCutFunction(plane)
	cutter.SetInputConnection(stl_file.GetOutputPort())
	cutter.Update()

	# Get the lines from the cutter
	cut_strips = vtk.vtkStripper()
	cut_strips.SetInputConnection(cutter.GetOutputPort())
	cut_strips.Update()

	# Create polys from the lines
	cut_polys = vtk.vtkPolyData()
	cut_polys.SetPoints(cut_strips.GetOutput().GetPoints())
	cut_polys.SetPolys(cut_strips.GetOutput().GetLines())

	print(cut_polys.GetPolys())

	# Our amazing functions

	shells = slicer.shell.exterior(cut_polys, 3)

	# TODO: create shells for any interntal geometry (e.g. holes through the part)

	shells_int = slicer.shell.interior(cut_polys, 3)

	print(shells_int)

	# Select the inner shells
	# N.b. could build to handle multiple inner shells
	mesh_width = 0.4
	linear_x_lines = slicer.infill.linear_x(
		shells[-1], x_min - 10, x_max + 10, y_min - 10, y_max + 10, mesh_width
	)
	linear_y_lines = slicer.infill.linear_y(
		shells[-1], x_min - 10, x_max + 10, y_min - 10, y_max + 10, mesh_width
	)

	# Draw out the print lines

	c = pyx.canvas.canvas()
	for shell in shells:
		c.stroke(shell, [pyx.style.linewidth(0.05)])

	# Draw out internal shell
	for shell in shells_int:
		c.stroke(shell, [pyx.style.linewidth(0.05)])

	c.writePDFfile("out/shells.pdf")

	for line in linear_x_lines:
		c.stroke(line, [pyx.style.linewidth(0.05), pyx.color.rgb.red])

	c.writePDFfile("out/shells+linear_x.pdf")

	for line in linear_y_lines:
		c.stroke(line, [pyx.style.linewidth(0.05), pyx.color.rgb.blue])

	c.writePDFfile("out/shells+linear_x+linear_y.pdf")
