"""
 The crazy triangle:

            /0\  
           /   \ 
          /     \
          -------       
        /1\     /3\    
       /   \   /   \  
      /     \2/     \  
      ------- ------- 
    /4\     /6\     /8\    
   /   \   /   \   /   \ 
  /     \5/     \7/     \ 
  ------- ------- ------- 


 Edge labels:
                   c
      /X\       -------    X = [1, 2, 4, 5, 7, 9]
   a /   \ b    \     /    Y = [3, 6, 8]
    /     \    b \   / a
    -------       \Y/   
       c


 Cards:
  * HO - Head orange
  * HG - Head green
  * HW - Head white
  * BO - Body orange
  * BG - Body green
  * BW - Body white
"""

# from multiprocessing.dummy import Pool # Threads
from multiprocessing import Pool # Processes
import itertools as it
import time

cards = [
	("HO", "BW", "HW"), # 0.
	("HG", "BG", "HW"), # 1.
	("BG", "HG", "HO"), # 2.
	("HO", "BG", "BW"), # 3.
	("BO", "BG", "HO"), # 4.
	("BO", "HO", "BG"), # 5.
	("HG", "BG", "HO"), # 6.
	("BW", "BG", "HW"), # 7.
	("HO", "BW", "BO")] # 8.

#
# Lists of all
#   * permutations of the nine triangles inside the large triangle
#   * possible rotations of the triangles (0, 120, 240 deg.) for each
#     of the permutations.
#
# Note: a single list of all possible combinations won't be constructed
#       explicitly because it is quite large. Nested for-loops will be
#       used instead.
#
permutations = [x for x in it.permutations(range(len(cards)))]
rotations = [x for x in it.product([0,1,2], repeat=len(cards))]

def is_valid_triangle(cards):
	"""Returns true if a configuration is valid, i.e. if all neighboring
	triangles match. A pair of triangles match, if the body parts 
	printed on the neighboring sides of the triangles are complements 
	(head and body), i.e. if they are not equal, and if the colors are
	the same."""

	checks = [
		((0,2),(2,2)), # ((1,c),(3,c)),
		((1,1),(2,1)), # ((2,b),(3,b)),
		((1,2),(5,2)), # ((2,c),(6,c)),
		((2,0),(3,0)), # ((3,a),(4,a)),
		((3,2),(7,2)), # ((4,c),(8,c)),
		((4,1),(5,1)), # ((5,b),(6,b)),
		((5,0),(6,0)), # ((6,a),(7,a)),
		((6,1),(7,1)), # ((7,b),(8,b)),
		((7,0),(8,0))] # ((8,a),(9,a))]

	for c in checks:
		t0 = cards[c[0][0]]
		s0 = t0[c[0][1]]

		t1 = cards[c[1][0]]
		s1 = t1[c[0][1]]

		is_match = s0[0] != s1[0] and s0[1] == s1[1]
		if not is_match:
			return False

	return True


def rotate_card(card, count):
	"""Rotate a card CCW (neg. values) or CW (pos. values) in multiples of 120 degrees.

	rotate((1,2,3), -2) -> (3,1,2)
	rotate((1,2,3),  2) -> (2,3,1)

Rotations:

	count = 0           1           2
	        (no rot.)   (120 deg)   (240 deg)
	        *
	       / \         / \         / \  
	      /   \       /   \       /   \ 
	     /     \     /     \     /     \
	     -------     -------*   *-------"""

	# Convert CCW rotations (neg. values) to equivalent CW rorations
	# (avoids problems with negative indices)
	n = len(card)
	while count < 0:
		count += n
	
	rotated = [0] * len(card)
	for i in range(n):
		rotated[(i + count) % n] = card[i]

	return tuple(rotated)

def process_permutation(index):
	print "%6i (%6.2f%%)" % (index, float(index+1) / float(len(permutations)) * 100.,)

	results = []
	perm = [cards[i] for i in permutations[index]]

	for r in range(len(rotations)):
		rot = [rotate_card(perm[i], rotations[r][i]) for i in range(len(perm))]
		is_valid = is_valid_triangle(rot)

		if is_valid:
			print "Found a triangle: p = %s, r = %s" % (index, r)
			print permutations[index]
			print rot
			with open('p%06i_r%05i.txt' % (index, r), 'wb') as logfile:
				logfile.write('perm=%s\nrot=%s\ncards=%s\n' % (permutations[index], rotations[r][i], rot))
			results.append((index, r, permutations[index], rotations[r][i], rot))

	return results

if __name__ == "__main__":
def render_triangle_ascii(p, r):
	"""Render a configuration as (human-readable) ASCII art."""
	print "p = %6i, r = %5i" % (p, r)
	labels = [('%s' % (i+1), ' ', ' ') for i in permutations[p]]
	labels = [rotate_card(labels[i], rotations[r][i]) for i in range(len(labels))]
	labels = [j for i in labels for j in i]

	shuffle =   [
		 0,  1,  2, # 0
		 3,  7,  8, # 1
		 9,  5,  4, # 2
		 6, 10, 11, # 3
		12, 19, 20, # 4
		21, 14, 13, # 5
		15, 22, 23, # 6
		24, 17, 16, # 7
		18, 25, 26] # 8

	l = [' '] * len(labels)
	for i in range(len(labels)):
		l[shuffle[i]] = labels[i]
	labels = l

	triangle = """            /%s\ 
           /   \ 
          /%s   %s\ 
          -------
        /%s\%s   %s/%s\ 
       /   \   /   \ 
      /%s   %s\%s/%s   %s\ 
      ------- -------
    /%s\%s   %s/%s\%s   %s/%s\ 
   /   \   /   \   /   \ 
  /%s   %s\%s/%s   %s\%s/%s   %s\ 
  ------- ------- -------\n""" % tuple(labels)

	return triangle

	pool = Pool()
	indices = range(len(permutations))
	indices = indices[7500:]
	# indices = range(5000) # Debug
	results = pool.map(process_permutation, indices, 1)
	pool.close()
	pool.join()

	for res in results:
		if len(res) > 0:
			print res
