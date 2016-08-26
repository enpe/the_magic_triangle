""" The Magic Triangle

                / \    
               /   \   
              /0a 0b\  
             /   0   \ 
            /    0c   \ 
            ----------- 
          / \    1c   / \     
         /   \   7   /   \    
        /2a 2b\1b 1a/8b 8a\   
       /   8   \   /   1   \ 
      /    2c   \ /    8c   \ 
      ----------- ----------- 
    / \    3c   / \    6c   / \     
   /   \   4   /   \   3   /   \    
  /4a 4b\3b 3a/5a 5b\6b 6a/7a 7b\   
 /   2   \   /   6   \   /   5   \ 
/    4c   \ /    5c   \ /    7c   \ 
----------- ----------- ----------- 
"""

# Deck of cards
#
# HO - Head orange
# HG - Head green
# HW - Head white
# BO - Body orange
# BG - Body green
# BW - Body white
#
# Cf. doc/snoopy-the-magic-triangle.jpg
deck = [
	# a     b     c
	("HO", "BW", "HW"), # 0
	("HG", "BG", "HW"), # 1
	("BG", "HG", "HO"), # 2
	("HO", "BG", "BW"), # 3
	("BO", "BG", "HO"), # 4
	("BO", "HO", "BG"), # 5
	("HG", "BG", "HO"), # 6
	("BW", "BG", "HW"), # 7
	("HO", "BW", "BO")] # 8

# Sides of neighboring triangles that need to be checked. These are
# expressed as the edges of a dual graph.
#
# Cf. doc/triangle-checks.png
edge_matches = [
	#+--------- card 
	#|  +------ neighboring card
	#|  |  +--- shared side (a=0, b=1, c=2)
	#|  |  |
	#V  V  V
	(0, 1, 2),
	(1, 2, 1),
	(2, 3, 2),
	(3, 4, 1),
	(3, 5, 0),
	(5, 6, 1),
	(6, 7, 0),
	(6, 8, 2),
	(1, 8, 0)]


def rotate(card, count):
	"""Rotate a card CCW (neg. values) or CW (pos. values) in multiples 
	of 120 degrees.

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

	# Convert CCW rotations (neg. values) to equivalent CW rotations
	# (avoids problems with negative indices)
	n = len(card)
	while count < 0:
		count += n
	
	rotated = [0] * len(card)
	for i in range(n):
		rotated[(i + count) % n] = card[i]

	return tuple(rotated)


def shuffle_deck(c):
	"""Shuffle the deck of cards as specified by the configuration c."""
	return [rotate(deck[x[0]], x[1]) if x is not None else None for x in c]


def is_complete(c):
	"""Returns true if the configuration contains all cards from the deck, otherwise false."""
	if c is None:
		return False
	else:
		return None not in c and len(c) == len(deck)


def is_solution(c, partial=False):
	"""Returns true if the configuration is a valid solution, otherwise false. A pair of triangles
	match, if the body parts  printed on the neighboring sides of the triangles are complements 
	(head and body), i.e. if they are not equal, and if the colors are the same."""
	if c is None:
		print "c is None"
		return False

	shuffled = shuffle_deck(c)

	for edge in edge_matches:
		card0 = shuffled[edge[0]]
		card1 = shuffled[edge[1]]
		if None in [card0, card1]:
			if partial:
				continue
			else:
				return False

		# Reminder: body parts must be different while colors must match
		side = edge[2]
		side0 = card0[side]
		side1 = card1[side]
		# print "s0 = %s, s1 = %s " % (side0, side1) # Debug
		is_match = side0[0] != side1[0] and side0[1] == side1[1]
		if not is_match:
			return False

	return True


def reject(c):
	"""Return true if configuration isn't complete and edge tests already fail, otherwise false."""
	return not is_solution(c, partial=True)


def output(c):
	"""Returns string containing a configuration in a human-readablea form."""

	# Debug
	# s = ""
	# d = ""
	# labels = ('0a', '0b',  '0', '0c',
	# 	      '1c',  '1', '2a', '2b',
	# 	      '1b', '1a', '8a', '8b',
	# 	       '2',  '8', '2c', '8c',
	# 	      '3c', '6c',  '3',  '6',
	# 	      '4a', '4b', '3b', '3a',
	# 	      '5a', '5b', '6b', '6a',
	# 	      '7a', '7b',  '4',  '5',
	# 	       '7', '4c', '5c', '7c')
	s = shuffle_deck(c)
	d = [card[0] for card in c]
	labels = (s[0][0], s[0][1], d[0],    s[0][2],
		      s[1][2], d[1],    s[2][0], s[2][1],
		      s[1][1], s[1][0], s[8][0], s[8][1],
		      d[2],    d[8],    s[2][2], s[8][2],
		      s[3][2], s[6][2], d[3],    d[6],
		      s[4][0], s[4][1], s[3][1], s[3][0],
		      s[5][0], s[5][1], s[6][1], s[6][0],
		      s[7][0], s[7][1], d[4],    d[5],
		      d[7],    s[4][2], s[5][2], s[7][2])

	triangle = """
                / \    
               /   \   
              /%s %s\  
             /   %s   \ 
            /    %s   \ 
            ----------- 
          / \    %s   / \     
         /   \   %s   /   \    
        /%s %s\%s %s/%s %s\   
       /   %s   \   /   %s   \ 
      /    %s   \ /    %s   \ 
      ----------- ----------- 
    / \    %s   / \    %s   / \     
   /   \   %s   /   \   %s   /   \    
  /%s %s\%s %s/%s %s\%s %s/%s %s\   
 /   %s   \   /   %s   \   /   %s   \ 
/    %s   \ /    %s   \ /    %s   \ 
----------- ----------- ----------- 
""" % labels

	msg = "config = %s\ndeck   = %s\n%s" % (c, s, triangle)

	return msg


def first(c):
	"""Generate a first extension of the current configuration; find the first empty element in the 
	configuration (None), which will be filled with the next free card. If no empty elements exist, 
	the return value will be None"""
	try:
		first_empty = (x for x in range(len(c)) if c[x] == None).next()
	except StopIteration:
		return None

	# Find the next free card that can be added to the configuration at the location determined 
	# above.
	new_c = c[:]
	used_cards = [card[0] for card in new_c if card != None]
	for i in range(len(deck)):
		if i not in used_cards:
			new_c[first_empty] = (i, 0) # Add the i-th card, with no rotation (0)
			break

	return new_c


def next(c):
	"""Returns the next possible configuration given the current configuration; will return None if 
	no next configuration exists."""
	try:
		first_empty = (x for x in range(len(c)) if c[x] == None).next()
	except StopIteration:
		first_empty = len(deck)

	# Avoid negative indices
	last_non_empty = first_empty - 1
	if last_non_empty < 0:
		return None

	# Determine the next configuration. If possible, rotate the current
	# last card, otherwise choose and select a new card.
	new_c = c[:]
	current_card = c[last_non_empty][0]
	current_rotation = c[last_non_empty][1]
	if current_rotation < 2:
		new_c[last_non_empty] = (current_card, current_rotation + 1)
	else:
		# No next card exists, if the current card is the last card in
		# the deck. Abort the search.
		if current_card >= len(deck) - 1:
			return None

		# Determine the next possible card for testing; ignore all cards
		# that already have been tested before.
		used_cards = [card[0] for card in new_c if card != None]
		for i in range(current_card, len(deck)):
			if i not in used_cards:
				new_c[last_non_empty] = (i, 0) # Add the i-th card, with no rotation (0)
				break
	
	# If the configuration didn't change until now, a next item doesn't
	# exist and that will be indicated by returning None.
	if new_c == c:
		return None

	return new_c

def backtrack(c):
	"""Text-book backtracking, cf. https://en.wikipedia.org/wiki/Backtracking"""
	if reject(c):
		return

	if is_solution(c):
		print output(c)

	cur = first(c)
	while cur != None:
		backtrack(cur)
		cur = next(cur)


if __name__ == "__main__":
	c = [None] * len(deck)
	backtrack(c)
