import vtk
from slicer.generate_shells import generate_shells
import slicer.linear_mesh as linear_mesh
import pyx
import matplotlib.pyplot as plt

if __name__ == "__main__":
	
	# 3D printer stl file
	file_name = "stls/solid_beam.stl"

	stl_file = vtk.vtkSTLReader()
	stl_file.SetFileName(file_name)
	stl_file.Update()
	stl_poly = stl_file.GetOutput()

	x_min, x_max, y_min, y_max, z_min, z_max = stl_poly.GetBounds()
	print("X min:", x_min, "X max:", x_max, "Y min:", y_min, "Y max:", y_max, "Z min:", z_min, "Z max:", z_max)

	# generate internal mesh structure of stl
	stl_tree = vtk.vtkOBBTree()
	stl_tree.SetDataSet(stl_poly)
	stl_tree.BuildLocator()

	# Set a slice level and mesh width
	level = ( z_min + z_max ) / 2

	# Create intersecting line
	plane = vtk.vtkPlane()
	plane.SetOrigin(0, 0, level)
	plane.SetNormal(0, 0, 1)

	# Create cutter
	cutter = vtk.vtkCutter()
	cutter.SetCutFunction(plane)
	cutter.SetInputConnection(stl_file.GetOutputPort())
	cutter.Update()

	# get the lines from the cutter
	cut_strips = vtk.vtkStripper()
	cut_strips.SetInputConnection(cutter.GetOutputPort())
	cut_strips.Update()

	# create polys from the lines
	cut_polys = vtk.vtkPolyData()
	cut_polys.SetPoints(cut_strips.GetOutput().GetPoints())
	cut_polys.SetPolys(cut_strips.GetOutput().GetLines())

	shells = generate_shells(cut_polys, 3)

	# Select the inner shells
	# N.b. could build to handle multiple inner shells
	mesh_width = 0.4
	linear_x_lines = linear_mesh.linear_x(shells[-1], x_min-10, x_max+10, y_min-10, y_max+10, mesh_width)
	linear_y_lines = linear_mesh.linear_y(shells[-1], x_min-10, x_max+10, y_min-10, y_max+10, mesh_width)

	c = pyx.canvas.canvas()
	for shell in shells:
		c.stroke(shell, [pyx.style.linewidth(0.05)])

	for line in linear_x_lines:
		c.stroke(line, [pyx.style.linewidth(0.05), pyx.color.rgb.red])

	for line in linear_y_lines:
		c.stroke(line, [pyx.style.linewidth(0.05), pyx.color.rgb.blue])

	c.writePDFfile("out/shells.pdf")