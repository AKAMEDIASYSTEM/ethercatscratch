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
INITEXHALE_TIME = 1024

BREATHE_IN_START = INITEXHALE_TIME

BREATHE_IN_END = BREATHE_IN_START + (CHUNK_TIME*IN_TIME)

BREATHE_OUT_START = BREATHE_IN_END + HOLD BREATH_TIME

BREATHE_OUT_END = BREATHE_OUT_START + (OUT_TIME*CHUNK_TIME)

out_lut = [0]*(IN_TIME*CHUNK_TIME + OUT_TIME*CHUNK_TIME + CHUNK_TIME*(IN_TIME+OUT_TIME))

for sampleNumber in range(0,INITEXHALE_TIME):
	out_lut[sampleNumber] = int(interp(sampleNumber, [0,(INITEXHALE_TIME)], [AMPLITUDE/2,0]))

for sampleNumber in range(INITEXHALE_TIME,(IN_TIME*CHUNK_TIME)):
	out_lut[sampleNumber] = int(interp(sampleNumber, [INITEXHALE_TIME,INITEXHALE_TIME+(IN_TIME*CHUNK_TIME)], [0,AMPLITUDE]))

for sampleNumber in range((INITEXHALE_TIME+(IN_TIME*CHUNK_TIME)), (INITEXHALE_TIME +(IN_TIME*CHUNK_TIME) + (OUT_TIME*CHUNK_TIME))):
	out_lut[sampleNumber] = int(interp(sampleNumber, [(INITEXHALE_TIME+(IN_TIME*CHUNK_TIME)),(INITEXHALE_TIME +(IN_TIME*CHUNK_TIME)+(OUT_TIME*CHUNK_TIME))], [AMPLITUDE, 0]))

for sampleNumber in range( ((IN_TIME*CHUNK_TIME) + (OUT_TIME*CHUNK_TIME)),(2*CHUNK_TIME*(IN_TIME+OUT_TIME))):
	out_lut[sampleNumber] = int(interp(sampleNumber, [(INITEXHALE_TIME+(OUT_TIME*CHUNK_TIME)+(IN_TIME*CHUNK_TIME)),(INITEXHALE_TIME+2*CHUNK_TIME*(IN_TIME+OUT_TIME))], [0, AMPLITUDE/2]))
	# print(out_lut[sampleNumber])

# for i, j in enumerate(out_lut):
	# logging.debug('index {} value {}'.format(i,j))

print(out_lut)