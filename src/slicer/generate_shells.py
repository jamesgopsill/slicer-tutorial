import vtk
import numpy as np
import pyx

def generate_shells(cut_polys, n):

	# Identify the outer shell
	# This would be for the generation of the shell G-Code
	shells = []
	for i in range(0, cut_polys.GetNumberOfCells()): # Run through each poly that has been generated

		poly = cut_polys.GetCell(i)

		#print 'Poly:', i, 'Edges:', poly.GetNumberOfEdges()

		# get the initial line
		from_x, from_y, _ = poly.GetEdge(0).GetPoints().GetData().GetTuple(0)
		to_x, to_y, _ = poly.GetEdge(0).GetPoints().GetData().GetTuple(1)

		shell = pyx.path.line(from_x, from_y, to_x, to_y)

		# run through the remaining polys
		for j in range(1, poly.GetNumberOfEdges()):

			to_x, to_y, _ = poly.GetEdge(j).GetPoints().GetData().GetTuple(1)

			shell.append(pyx.path.lineto(to_x, to_y))

		# Append the shell to the list
		shells.append(shell)

		# Now deform the path to add the additional shells
		if n != 0:
			for i in range(1, n):
				shells.append(pyx.deformer.parallel(i*0.1).deform(shell))


	return shells