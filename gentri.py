# take NUM_SAMPLES samples to generate NUM_CYCLES cycles of triangle wave amplitude AMPLITUDE
import math
from numpy import interp

NUM_SAMPLES = 512
NUM_CYCLES = 8
AMPLITUDE = 32766

out_lut = [0]*NUM_SAMPLES
for cycleNumber in range(NUM_CYCLES):
	print('cycleNumber is {}'.format(cycleNumber))
	for counter in range(int(NUM_SAMPLES/NUM_CYCLES)):
		# print('counter is {}'.format(counter))
		if counter < int(NUM_SAMPLES/NUM_CYCLES)/2:
			out_lut[(cycleNumber*int(NUM_SAMPLES/NUM_CYCLES)) + counter] = int(interp(counter, [0,int(NUM_SAMPLES/NUM_CYCLES)], [0,2*AMPLITUDE]))
		else:
			out_lut[(cycleNumber*int(NUM_SAMPLES/NUM_CYCLES)) + counter] = int(interp(counter, [0,int(NUM_SAMPLES/NUM_CYCLES)], [2*AMPLITUDE,0]))

print(out_lut)