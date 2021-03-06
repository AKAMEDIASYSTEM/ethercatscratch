"""CLI script to play a slow sine wave through a single muscle.

Usage: python single.py <adapter> <muscle_number>

This example expects a physical slave layout according to
_expected_slave_layout, see below.
"""

import sys
import struct
import time
import threading
import ctypes

from collections import namedtuple

import pysoem
import random
import luts
import logging
import json
import outputs



class BasicExample:

    BECKHOFF_VENDOR_ID = 0x0002
    EK1100_PRODUCT_CODE = 0x044c2c52
    EL3002_PRODUCT_CODE = 0x0bba3052
    EL1259_PRODUCT_CODE = 0x04eb3052
    EL4024_PRODUCT_CODE = 0x0FB83052 # 4-chan 4mA-20mA 12-bit
    EL4102_PRODUCT_CODE = 0x10063052 # 2-chan 0-10V 16-bit
    EL4008_PRODUCT_CODE = 0x0FA83052 # 8-chan 0-10V 12-bit


    def __init__(self, ifname, theMuscle):
        self._ifname = ifname
        self._muscle = theMuscle
        self._pd_thread_stop_event = threading.Event()
        self._ch_thread_stop_event = threading.Event()
        self._actual_wkc = 0
        self._master = pysoem.Master()
        self._master.in_op = False
        self._master.do_check_state = False
        self.currentAnimation = {}
        SlaveSet = namedtuple('SlaveSet', 'name product_code config_func')
        # 56 outputs with 4024s ganged together on one DIN
        self._expected_slave_layout = {0: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),
                                       1: SlaveSet('EL4024', self.EL4024_PRODUCT_CODE, None),
                                       2: SlaveSet('EL4024', self.EL4024_PRODUCT_CODE, None),
                                       3: SlaveSet('EL4024', self.EL4024_PRODUCT_CODE, None),
                                       4: SlaveSet('EL4024', self.EL4024_PRODUCT_CODE, None),
                                       5: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None),
                                       6: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),
                                       7: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None),
                                       8: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None),
                                       9: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None),
                                       10: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None)
                                       }

    def _processdata_thread(self):
        while not self._pd_thread_stop_event.is_set():
            self._master.send_processdata()
            self._actual_wkc = self._master.receive_processdata(10000)
            if not self._actual_wkc == self._master.expected_wkc:
                print('incorrect wkc')
            time.sleep(0.001)

    def _pdo_update_loop(self):
        print('in update_loop')
        self._master.in_op = True
        counter = 0
        muscleCounter = 0
        currentlyPlaying = False
        try:
            while 1:
                if(currentlyPlaying):
                    # logging.debug('looking for {}'.format(self._muscle))
                    muscleCounter = 0
                    for module_index, this_module in enumerate(outputs.installed):
                        output_buffer = []
                        for phase_index, c_phase_offset in enumerate(this_module['phase_offsets']):
                            # logging.debug('muscleCounter is {}'.format(muscleCounter))
                            muscleCounter = muscleCounter + 1
                            if (muscleCounter==int(self._muscle)):
                                # logging.debug('muscleCounter MATCH {}'.format(muscleCounter))
                                output_buffer.append(currentAnimation['lut'][int(max(0, counter - c_phase_offset))])
                            else:
                                # logging.debug('muscleCounter NONMATCH {} {}'.format(muscleCounter, self._muscle))
                                output_buffer.append(0x00)
                        self._master.slaves[module_index].output = struct.pack('{}h'.format(len(output_buffer)), *output_buffer)
                    counter = counter +1
                    if(counter >= MAX_SAMPLES):
                        counter = 0
                        currentlyPlaying = False
                        self.all_zero()
                        sleep_interval = random.randint(1,2)
                        logging.debug('sleep for {} seconds'.format(sleep_interval))
                        time.sleep(sleep_interval)
                    
                else:
                    # currentAnimation = random.choice(luts.luts)
                    currentAnimation = luts.luts[0]
                    logging.debug('chose {}'.format(currentAnimation['name']))
                    MAX_SAMPLES = len(currentAnimation['lut'])
                    currentlyPlaying = True

                time.sleep(0.001)
                

        except KeyboardInterrupt:
            # ctrl-C abort handling
            print('stopped')

    def all_zero(self):
        logging.debug('all_zero()')
        for module_index, this_module in enumerate(outputs.installed):
            output_buffer = [0]*len(this_module['phase_offsets'])
            # if it turns out current-driven valves need a middle value to be "off", that logic should
            # go here
            self._master.slaves[module_index].output = struct.pack('{}h'.format(len(output_buffer)), *output_buffer)
                    
    def run(self):

        self._master.open(self._ifname)

        if not self._master.config_init() > 0:
            self._master.close()
            raise BasicExampleError('no slave found')

        for i, slave in enumerate(self._master.slaves):
            # logging.debug('Enumerating {} module as slave {}'.format(i, slave))
            if not ((slave.man == self.BECKHOFF_VENDOR_ID) and
                    (slave.id == self._expected_slave_layout[i].product_code)):
                self._master.close()
                raise BasicExampleError('unexpected slave layout')
            slave.config_func = self._expected_slave_layout[i].config_func
            slave.is_lost = False

        self._master.config_map()

        if self._master.state_check(pysoem.SAFEOP_STATE, 500000) != pysoem.SAFEOP_STATE:
            self._master.close()
            raise BasicExampleError('not all slaves reached SAFEOP state')

        self._master.state = pysoem.OP_STATE

        check_thread = threading.Thread(target=self._check_thread)
        check_thread.start()
        proc_thread = threading.Thread(target=self._processdata_thread)
        proc_thread.start()
        
        # send one valid process data to make outputs in slaves happy
        self._master.send_processdata()
        self._master.receive_processdata(2000)
        # request OP state for all slaves
        
        self._master.write_state()

        all_slaves_reached_op_state = False
        for i in range(40):
            self._master.state_check(pysoem.OP_STATE, 50000)
            if self._master.state == pysoem.OP_STATE:
                all_slaves_reached_op_state = True
                break

        if all_slaves_reached_op_state:
            self._pdo_update_loop()

        self._pd_thread_stop_event.set()
        self._ch_thread_stop_event.set()
        proc_thread.join()
        check_thread.join()
        self._master.state = pysoem.INIT_STATE
        # request INIT state for all slaves
        self._master.write_state()
        self._master.close()

        if not all_slaves_reached_op_state:
            raise BasicExampleError('not all slaves reached OP state')

    @staticmethod
    def _check_slave(slave, pos):
        if slave.state == (pysoem.SAFEOP_STATE + pysoem.STATE_ERROR):
            print(
                'ERROR : slave {} is in SAFE_OP + ERROR, attempting ack.'.format(pos))
            slave.state = pysoem.SAFEOP_STATE + pysoem.STATE_ACK
            slave.write_state()
        elif slave.state == pysoem.SAFEOP_STATE:
            print(
                'WARNING : slave {} is in SAFE_OP, try change to OPERATIONAL.'.format(pos))
            slave.state = pysoem.OP_STATE
            slave.write_state()
        elif slave.state > pysoem.NONE_STATE:
            if slave.reconfig():
                slave.is_lost = False
                print('MESSAGE : slave {} reconfigured'.format(pos))
        elif not slave.is_lost:
            slave.state_check(pysoem.OP_STATE)
            if slave.state == pysoem.NONE_STATE:
                slave.is_lost = True
                print('ERROR : slave {} lost'.format(pos))
        if slave.is_lost:
            if slave.state == pysoem.NONE_STATE:
                if slave.recover():
                    slave.is_lost = False
                    print(
                        'MESSAGE : slave {} recovered'.format(pos))
            else:
                slave.is_lost = False
                print('MESSAGE : slave {} found'.format(pos))
    
    def _check_thread(self):

        while not self._ch_thread_stop_event.is_set():
            if self._master.in_op and ((self._actual_wkc < self._master.expected_wkc) or self._master.do_check_state):
                self._master.do_check_state = False
                self._master.read_state()
                for i, slave in enumerate(self._master.slaves):
                    if slave.state != pysoem.OP_STATE:
                        self._master.do_check_state = True
                        BasicExample._check_slave(slave, i)
                if not self._master.do_check_state:
                    print('OK : all slaves resumed OPERATIONAL.')
            time.sleep(0.01)


class BasicExampleError(Exception):
    def __init__(self, message):
        super(BasicExampleError, self).__init__(message)
        self.message = message


if __name__ == '__main__':

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.debug('testing single muscle {}'.format(sys.argv[1]))

    for module in outputs.installed:
        if len(module['phase_offsets']):
            logging.debug(module['name'])

    try:
        BasicExample('eth0', sys.argv[1]).run()
    except BasicExampleError as expt:
        print('aka_basic_example failed: ' + expt.message)
        sys.exit(1)
    else:
        print('usage: aka_basic_example ifname')
        sys.exit(1)
