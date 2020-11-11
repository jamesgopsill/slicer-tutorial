import vtk
import pyx


def exterior(cut_polys, n: int, spacing=0.1):
	"""Returns the external shell path for a slice times by the number of shells"""

	shells = []

	n_cells = cut_polys.GetNumberOfCells()
	poly = cut_polys.GetCell(0)

	test_cell = cut_polys.GetCell(0)
	
	print(test_cell.GetPoints())

	print("Poly area = ", poly.ComputeArea())

	# If there are more than one polys from the cutter
	if n_cells != 1:

		# Run through each poly that has been generated
		for i in range(0, n_cells):

			print("Cut Poly Area = ", cut_polys.GetCell(i).ComputeArea())
			print("Cell Dimensions = ", cut_polys.GetCell(i).GetCellDimension())
			print(cut_polys.GetCell(i).PrintSelf())
			print("Cut Poly Area = ", cut_polys.GetCell(i).ComputeArea())

			# Update poly if the next one is bigger
			if cut_polys.GetCell(i).ComputeArea() > poly.ComputeArea():
				poly = cut_polys.GetCell(i)

	poly = cut_polys.GetCell(1)
	print("Poly area = ", poly.ComputeArea())

	# get the initial line
	from_x, from_y, _ = poly.GetEdge(0).GetPoints().GetData().GetTuple(0)
	to_x, to_y, _ = poly.GetEdge(0).GetPoints().GetData().GetTuple(1)

	# Add line to start the shell
	shell = pyx.path.line(from_x, from_y, to_x, to_y)

	# run through the remaining polys
	for j in range(1, poly.GetNumberOfEdges()):

		# Extend the line
		to_x, to_y, _ = poly.GetEdge(j).GetPoints().GetData().GetTuple(1)

		# Append to the shell
		shell.append(pyx.path.lineto(to_x, to_y))

	# Append the shell to the list
	shells.append(shell)

	# Now deform the path to add the additional shells
	#if n != 0:
	#	for i in range(1, n):
	#		shells.append(pyx.deformer.parallel(i * spacing).deform(shell))

	return shells
