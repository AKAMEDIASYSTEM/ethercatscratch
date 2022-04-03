# take NUM_SAMPLES samples to generate NUM_CYCLES cycles of triangle wave amplitude AMPLITUDE
# arg 1 is time-unit in samples; arg2 is breathe-in time, arg3 is breathe-out time
import math
from numpy import interp
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


if len(sys.argv) > 1:
	CHUNK_TIME = int(sys.argv[3])
	IN_TIME = int(sys.argv[1])
	OUT_TIME = int(sys.argv[2])
	logging.debug('Generating a sigh of beat {} samples that breathes in for {} and out for {}'.format(CHUNK_TIME, IN_TIME, OUT_TIME))
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
INIT_EXHALE_DUR = 2048
INIT_HOLD_DUR = 5000
HOLD_BREATH_TIME = 500

MAX_BREATHE_RATE = 3*AMPLITUDE/5
MAX_EXHALE_RATE = 2*AMPLITUDE/5

# INIT_HOLD_START = INIT_EXHALE_DUR
# INIT_HOLD_END = INIT_EXHALE_DUR + INIT_HOLD_DUR
# BREATHE_IN_START = INIT_HOLD_END
BREATHE_IN_START = 0
# print(BREATHE_IN_START)
BREATHE_IN_END = BREATHE_IN_START + (CHUNK_TIME*IN_TIME)
# print(BREATHE_IN_END)
BREATHE_OUT_START = BREATHE_IN_END + HOLD_BREATH_TIME
# print(BREATHE_OUT_START)
BREATHE_OUT_END = BREATHE_OUT_START + (OUT_TIME*CHUNK_TIME)
# print(BREATHE_OUT_END)
RESET_TIME = 2048

out_lut = [0]*(BREATHE_OUT_END + RESET_TIME)

# # exhale
# for sampleNumber in range(0,INIT_EXHALE_DUR):
# 	out_lut[sampleNumber] = int(interp(sampleNumber, [0,INIT_EXHALE_DUR], [0,(AMPLITUDE/2-AMPLITUDE/5)]))

# # hold the exhale to silently let muscles elongate
# for sampleNumber in range(INIT_HOLD_START, INIT_HOLD_END):
# 	out_lut[sampleNumber] = int(AMPLITUDE/2-AMPLITUDE/10)

# breathe in
for sampleNumber in range(BREATHE_IN_START,BREATHE_IN_END):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_IN_START,BREATHE_IN_END], [0,MAX_BREATHE_RATE]))
# hold it
for sampleNumber in range(BREATHE_IN_END, BREATHE_OUT_START):
	out_lut[sampleNumber] = int(MAX_BREATHE_RATE)
# breathe out
for sampleNumber in range( BREATHE_OUT_START,BREATHE_OUT_END):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_OUT_START,BREATHE_OUT_END], [MAX_BREATHE_RATE, MAX_EXHALE_RATE]))
# reset to mid-amplitude
for sampleNumber in range(BREATHE_OUT_END, BREATHE_OUT_END+ RESET_TIME):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_OUT_END, BREATHE_OUT_END+ RESET_TIME], [MAX_EXHALE_RATE, 0]))

print(out_lut)
