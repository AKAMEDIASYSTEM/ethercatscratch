# run through all the muscles and apply phase offset, elongating the animation by the maximum phase offset so we don't index-error

import sys
import struct
import time
import threading
import ctypes

from collections import namedtuple
import random
import luts
import logging
import json
import outputs

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.debug('starting phase test')
currentAnimation = luts.luts[0] 
sample_counter = 0
MAX_SAMPLES = len(luts.luts[0])
while True:
	muscleCounter = 0
	for module_index, this_module in enumerate(currentAnimation['muscle_offsets']):
	    output_buffer = []
	    for module_index, current_phase_offset in enumerate(this_module):
	        logging.debug('muscleCounter is {} and phase offset is {}'.format(muscleCounter, current_phase_offset))
	        muscleCounter = muscleCounter + 1
	        output_buffer.append(currentAnimation['lut'][int(max(0, sample_counter - current_phase_offset))])
	    logging.debug('done with module {} the buffer is {}'.format(module_index, output_buffer))
		# logging.debug('done with module {} the buffer is {}'.format(module_index, struct.pack('{}h'.format(len(output_buffer)), *output_buffer)))
		# self._master.slaves[module_index].output = struct.pack('{}h'.format(len(output_buffer)), *output_buffer)
	sample_counter= sample_counter + 1

	if(sample_counter>= MAX_SAMPLES):
	    sample_counter= 0
	    sleep_interval = random.randint(5,10)
	    logging.debug('sleep for {} seconds'.format(sleep_interval))
	    currentAnimation = random.choice(luts.luts)
	    # currentAnimation = luts.luts[5]
	    logging.debug('chose {}'.format(currentAnimation['name']))
	    MAX_SAMPLES = len(currentAnimation['lut'])
	    time.sleep(sleep_interval)