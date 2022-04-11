# take NUM_SAMPLES samples to generate NUM_CYCLES cycles of triangle wave amplitude AMPLITUDE
import math
from numpy import interp
import sys
import logging
import pyperclip as pc

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


if len(sys.argv) > 1:
	logging.debug('Generating a {} cycle triangle wave {} samples long'.format(sys.argv[1], sys.argv[2]))
	NUM_SAMPLES = int(sys.argv[2])
	NUM_CYCLES = int(sys.argv[1])
else:
	logging.debug('no args, so displaying a single-cycle 2048-sample triangle wave')
	NUM_SAMPLES = 2048
	NUM_CYCLES = 1
AMPLITUDE = 32766

out_lut = [0]*NUM_SAMPLES
for cycleNumber in range(NUM_CYCLES):
	for counter in range(int(NUM_SAMPLES/NUM_CYCLES)):
		if counter < int(NUM_SAMPLES/NUM_CYCLES)/2:
			out_lut[(cycleNumber*int(NUM_SAMPLES/NUM_CYCLES)) + counter] = int(interp(counter, [0,int(NUM_SAMPLES/NUM_CYCLES)], [0,2*AMPLITUDE]))
		else:
			out_lut[(cycleNumber*int(NUM_SAMPLES/NUM_CYCLES)) + counter] = int(interp(counter, [0,int(NUM_SAMPLES/NUM_CYCLES)], [2*AMPLITUDE,0]))

pc.copy(str(out_lut))
# print(out_lut)