# take NUM_SAMPLES samples to generate NUM_CYCLES cycles of triangle wave amplitude AMPLITUDE
# arg 1 is time-unit in samples; arg2 is breathe-in time, arg3 is breathe-out time
import math
from numpy import interp
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


if len(sys.argv) > 1:
	logging.debug('Generating a sigh of beat {} samples that breathes in for {} and out for {}'.format(sys.argv[1], sys.argv[2], sys.argv[3]))
	CHUNK_TIME = int(sys.argv[1])
	IN_TIME = int(sys.argv[2])
	OUT_TIME = int(sys.argv[3])
else:
	logging.debug('no args, so displaying a single-cycle 2048-sample triangle wave')
	CHUNK_TIME = 1024
	IN_TIME = 3
	OUT_TIME = 2
AMPLITUDE = 32766
'''
interpolate from mid-to zero slowly, over 2048 seconds
THEN
interpolate from mid-amplitude to full aplitude over CHUNK_TIME*IN_TIME cycles
then interpolate from full aplitude to zero over CHUNK_TIME*OUT_TIME cycles
then interpolate from zero to mid-amplitude over CHUNK_TIME*(IN_TIME+OUT_TIME) cycles

'''
INITEXHALE_TIME = 20000
HOLD_BREATH_TIME = 500

BREATHE_IN_START = INITEXHALE_TIME
print(BREATHE_IN_START)
BREATHE_IN_END = BREATHE_IN_START + (CHUNK_TIME*IN_TIME)
print(BREATHE_IN_END)
BREATHE_OUT_START = BREATHE_IN_END + HOLD_BREATH_TIME
print(BREATHE_OUT_START)
BREATHE_OUT_END = BREATHE_OUT_START + (OUT_TIME*CHUNK_TIME)
print(BREATHE_OUT_END)
RESET_TIME = 2048

out_lut = [0]*(BREATHE_OUT_END+ RESET_TIME)

# exhale
for sampleNumber in range(INITEXHALE_TIME):
	out_lut[sampleNumber] = int(interp(sampleNumber, [0,INITEXHALE_TIME], [AMPLITUDE/2,0]))
# breathe in
for sampleNumber in range(BREATHE_IN_START,BREATHE_IN_END):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_IN_START,BREATHE_IN_END], [0,AMPLITUDE]))

# hold it
for sampleNumber in range(BREATHE_IN_END, BREATHE_OUT_START):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_IN_END, BREATHE_OUT_START], [AMPLITUDE,AMPLITUDE]))
# breathe out
for sampleNumber in range( BREATHE_OUT_START,BREATHE_OUT_END):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_OUT_START,BREATHE_OUT_END], [AMPLITUDE, 0]))
# reset to mid-amplitude
for sampleNumber in range(BREATHE_OUT_END, BREATHE_OUT_END+ RESET_TIME):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_OUT_END, BREATHE_OUT_END+ RESET_TIME], [0, AMPLITUDE/2]))

# for i, j in enumerate(out_lut):
	# logging.debug('index {} value {}'.format(i,j))

print(out_lut)
