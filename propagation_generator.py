# 13 rib sections, lowest-numbered starting at tail. HEAD is section 14
# -2 means there is no valve at that index
# -1 means there is a valve there but the valve is not involved in the animation
import sys
import pyperclip as pc
import random

# ARRAY OF ORDERS, TAIL IS LOWEST
muscle_offsets_beckhoff = [[],[3,1,0,0],[1,2,-2,-2,-2,-2,-2,-2],[],[4,5,6,9,10,8,7,-2],[],[14,14,14,14,14,14,13,11],[14,14,14,14],[12,-2,-2,-2]]
muscle_offsets = [3,1,0,0,1,2,-2,-2,-2,-2,-2,-2,4,5,6,9,10,8,7,-2,14,14,14,14,14,14,13,11,14,14,14,14,12,-2,-2,-2]

# "starting at [X] rib and radiating outwards with [Y] propagation delay"
# find indices of X
# subtract the X from every entry - - this gets you "distance" in postiion from X radiating out from X
# then find the min in the whole set and re-adjust all offsets 
# multiply this distance by the propagation

# can -2 just be 0, nd we don't care? ANSWER, no we don't - just have the system fire on these blank channels too for simplicity.

if len(sys.argv) > 1:
 initial = int(sys.argv[1])
 delay = int(sys.argv[2])
 isRandom = int(sys.argv[3])
else:
	initial = 0
	delay = 0
print('starting at rib {}, radiate a waveform with propagation delay {}'.format(initial, delay))


for module in muscle_offsets_beckhoff:
	for index, i in enumerate(module):
		if isRandom:
			module[index] = (random.randint(10,100)*delay)
		else:
			module[index] = (abs(module[index] - initial)*delay)

pc.copy(str(muscle_offsets_beckhoff))
print(muscle_offsets_beckhoff)