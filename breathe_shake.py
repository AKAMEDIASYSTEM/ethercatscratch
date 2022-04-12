# breathe out and then shake, once. to do this you have to subtly breathe in first
# arg 1 is time-unit in samples; arg2 is breathe-in time, arg3 is breathe-out time
import math
from numpy import interp
import sys
import logging
import pyperclip as pc

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if len(sys.argv) > 1:
	CHUNK_TIME = int(sys.argv[4])
	IN_TIME = int(sys.argv[1])
	HOLD_BREATH_TIME = int(sys.argv[2])
	OUT_TIME = int(sys.argv[3])
	logging.debug('Generating a sigh of beat {} samples that breathes in for {} and out for {}'.format(CHUNK_TIME, IN_TIME, OUT_TIME))
else:
	logging.debug('no args. should be IN_TIME - HOLD_BREATH_TIME - OUT_TIME - CHUNK_TIME')
	CHUNK_TIME = 1024
	IN_TIME = 3
	OUT_TIME = 2
	HOLD_BREATH_TIME = 500
AMPLITUDE = 32766
'''
interpolate from mid-to zero slowly, over 2048 seconds
THEN
interpolate from mid-amplitude to full aplitude over CHUNK_TIME*IN_TIME cycles
then interpolate from full aplitude to zero over CHUNK_TIME*OUT_TIME cycles
then interpolate from zero to mid-amplitude over CHUNK_TIME*(IN_TIME+OUT_TIME) cycles


tempnotes
inhale too fast
gap after exhale too long
'''
# INIT_EXHALE_DUR = 2048
# INIT_HOLD_DUR = 5000

# note1 good used 5/9 amplitude for MAX_INHALE_RATE
# note1 good used 5/11 for MAX_EXHALE_RATE

MAX_INHALE_RATE = int(0.75*AMPLITUDE) # 6*AMPLITUDE/11 a little too subtle, 3/5 a little too phaser-y, try 4/7?
MAX_EXHALE_RATE = int(0.45*AMPLITUDE)
'''
0.51 in is silent and motionless
0.45 out
'''

# INIT_HOLD_START = INIT_EXHALE_DUR
# INIT_HOLD_END = INIT_EXHALE_DUR + INIT_HOLD_DUR
# BREATHE_IN_START = INIT_HOLD_END
BREATHE_IN_START = 0
# print(BREATHE_IN_START)
BREATHE_IN_END = BREATHE_IN_START + (CHUNK_TIME*IN_TIME)
# print(BREATHE_IN_END)
BREATHE_OUT_START = BREATHE_IN_END + (HOLD_BREATH_TIME*CHUNK_TIME)
# print(BREATHE_OUT_START)
BREATHE_OUT_END = BREATHE_OUT_START + (OUT_TIME*CHUNK_TIME)
# print(BREATHE_OUT_END)
RESET_TIME = 125
PROPAGATION_DELAY = 50 # ms propagation delay
PROPAGATION_TIME = 13 * PROPAGATION_DELAY  # 13 is the number of rib-zones along which signal propagates

out_lut = [0]*(BREATHE_OUT_END +1)

# # exhale
# for sampleNumber in range(0,INIT_EXHALE_DUR):
# 	out_lut[sampleNumber] = int(interp(sampleNumber, [0,INIT_EXHALE_DUR], [0,(AMPLITUDE/2-AMPLITUDE/5)]))

# # hold the exhale to silently let muscles elongate
# for sampleNumber in range(INIT_HOLD_START, INIT_HOLD_END):
# 	out_lut[sampleNumber] = int(AMPLITUDE/2-AMPLITUDE/10)

# breathe in
for sampleNumber in range(BREATHE_IN_START,BREATHE_IN_END):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_IN_START,BREATHE_IN_END], [0,MAX_INHALE_RATE]))
# hold it
for sampleNumber in range(BREATHE_IN_END, BREATHE_OUT_START):
	out_lut[sampleNumber] = int(MAX_INHALE_RATE)
# breathe out
for sampleNumber in range( BREATHE_OUT_START,BREATHE_OUT_END):
	out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_OUT_START,BREATHE_OUT_END], [MAX_INHALE_RATE, 0]))
# # reset to mid-amplitude
# for sampleNumber in range(BREATHE_OUT_END, BREATHE_OUT_END + RESET_TIME):
	# out_lut[sampleNumber] = int(interp(sampleNumber, [BREATHE_OUT_END, BREATHE_OUT_END+ RESET_TIME], [AMPLITUDE/2, 0]))

pc.copy(str(out_lut))
print('ok, check your clipboard')


# note 1, 4/11/2022
# slower exhale, harder inhale, even less time after exhale

# note 2
# try a big long "inhale" (exhale for me) and a quick exhale