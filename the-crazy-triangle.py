import itertools

#  3 - Body white
#  2 - Body green
#  1 - Body orange
# -1 - Head orange
# -2 - Head green
# -3 - Head white
triangles = [
	( 3, -1, -3),
	( 2, -2, -3),
	(-1, -2,  2),
	( 2, -1,  3),
	( 2, -1,  1),
	( 2,  2, -3),
	(-1,  1,  3),
	(-1,  2, -2),
	(-1,  2,  1)]

checks = [
	((0, 1),(2, 1)),
	((1, 2),(2, 2)),
	((1, 1),(5, 1)),
	((2, 0),(3, 0)),
	((3, 1),(7, 1)),
	((4, 2),(5, 2)),
	((5, 0),(6, 0)),
	((6, 2),(7, 2)),
	((7, 0),(8, 0))]


def check_configuration(triangles):
	for c in checks:
		t0 = triangles[c[0][0]]
		t1 = triangles[c[1][0]]
		is_valid = (t0[c[0][1]] + t1[c[1][1]]) == 0
		if not is_valid:
			return False

	return True


def shift(iterable, count):
	"""Shift elements left (neg. values) or right (pos. values)

	    shift((1,2,3), -2) -> (3,1,2)
	    shift((1,2,3),  2) -> (2,3,1)
	"""
	
	# Convert left shifts (neg. values) to their equivalent right shifts
	# (avoids problems with negative indices)
	n = len(iterable)
	while count < 0:
		count += n
	
	shifted = [0] * len(iterable)
	for i in range(n):
		shifted[(i + count) % n] = iterable[i]

	return tuple(shifted)


def solve():
	spatial_configurations = [x for x in itertools.permutations(range(9))]
	rotational_configurations = [x for x in itertools.product([0,1,2], repeat=len(triangles))]

	valid_configurations = []
	for s in range(len(spatial_configurations)):
		print "s = %i (%6.2f%%), found: %i" % (s + 1, float(s + 1)/len(spatial_configurations), len(valid_configurations))
		triangles_s = [triangles[i] for i in spatial_configurations[s]]
		
		for r in range(len(rotational_configurations)):
			triangles_r = []
			for i in range(len(triangles)):
				x = shift(triangles_s[i], rotational_configurations[r][i])
				triangles_r.append(shift(triangles_s[i], rotational_configurations[r][i]))
			
			is_valid = check_configuration(triangles_r)
			if is_valid:
				print "valid configuration: s = %s, r = %s" % (s, r)
				valid_configurations.append((s, r))

	print valid_configurations


if __name__ == "__main__":
	solve()
