"""Send commands to a network of Beckhoff controllers. Input comes from luts.py, a table of look-up tables that describe animations.

Usage: python aka_teacing_tree.py

Gratefully adapted from the pysoem library examples at https://github.com/bnjmnp/pysoem

This script expects a physical slave layout according to _expected_slave_layout, see below.

2022 AKA for Muhannad Shono
"""

import sys
import struct
import time
import threading
import ctypes

from collections import namedtuple

import pysoem
import random
import luts_finalcandidates as luts
import logging
import json
import outputs
import datetime as dt



class BasicExample:

    BECKHOFF_VENDOR_ID = 0x0002
    EK1100_PRODUCT_CODE = 0x044c2c52
    EL3002_PRODUCT_CODE = 0x0bba3052
    EL1259_PRODUCT_CODE = 0x04eb3052
    EL4024_PRODUCT_CODE = 0x0FB83052 # 4-chan 4mA-20mA 12-bit
    EL4102_PRODUCT_CODE = 0x10063052 # 2-chan 0-10V 16-bit, need different message format so avoid using
    EL4008_PRODUCT_CODE = 0x0FA83052 # 8-chan 0-10V 12-bit
    DAY_BEGIN_HOUR = 10
    DAY_BEGIN_MINUTE = 42


    def __init__(self, ifname):
        self._ifname = ifname
        self._pd_thread_stop_event = threading.Event()
        self._ch_thread_stop_event = threading.Event()
        self._actual_wkc = 0
        self._master = pysoem.Master()
        self._master.in_op = False
        self._master.do_check_state = False
        self._current_lut = luts.day_luts
        self._morning_triggered = False
        self._daytime_triggered = False
        self._special_triggered = False
        self._demoday_triggered = False
        self._currently_playing = False
        self._plays_remaining = 0
        self._should_play_shake = True
        SlaveSet = namedtuple('SlaveSet', 'name product_code config_func')
        # 56 outputs with 4024s ganged together on one DIN
        self._expected_slave_layout = {0: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),
                                       1: SlaveSet('EL4024', self.EL4024_PRODUCT_CODE, None),
                                       2: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None),
                                       3: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),
                                       4: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None),
                                       5: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),
                                       6: SlaveSet('EL4008', self.EL4008_PRODUCT_CODE, None),
                                       7: SlaveSet('EL4024', self.EL4024_PRODUCT_CODE, None),
                                       8: SlaveSet('EL4024', self.EL4024_PRODUCT_CODE, None)
                                       }

    def _processdata_thread(self):
        while not self._pd_thread_stop_event.is_set():
            self._master.send_processdata()
            self._actual_wkc = self._master.receive_processdata(10000)
            if not self._actual_wkc == self._master.expected_wkc:
                print('incorrect wkc')
            time.sleep(0.001)

    def _pdo_update_loop(self):
        logging.debug('in update_loop')
        self._master.in_op = True
        sample_counter = 0
        # currentlyPlaying = False
        shouldAlternate = True
        set_to_play = [1] # -4 'sigh_4_6_8_note1_response_this_is_good' is the good one
        play_counter = 0
        currentAnimation = self._current_lut[0]
        self._plays_remaining = 0 # when we choose an animation we set this to random.randint(min_plays, min_plays*3)
        try:
            while 1:
                # self.check_time() # removing all check_time logic, as we decided to go back to simpler form
                if(self._currently_playing):
                    for module_index, this_module in enumerate(currentAnimation['muscle_offsets']):
                        # logging.debug('this module is {}'.format(this_module))
                        if len(currentAnimation['muscle_offsets'][module_index]): # ie, ignore EK1100 modules
                            output_buffer = []
                            # logging.debug('module {} has offsets to handle.'.format(module_index))
                            for phase_index, c_phase_offset in enumerate(currentAnimation['muscle_offsets'][module_index]):
                                # logging.debug('phase_offset_value is {}'.format(currentAnimation['muscle_offsets'][module_index][phase_index]))
                                if int(currentAnimation['muscle_offsets'][module_index][phase_index]) > -1:
                                    # logging.debug('buffer is {}'.format(output_buffer))
                                    output_buffer.append(currentAnimation['lut'][int(max(0, sample_counter - c_phase_offset))])
                                else:
                                    # logging.debug('ignoring muscle {} in module {} for animation {}'.format(phase_index, module_index, currentAnimation['name']))
                                    output_buffer.append(0)
                            # logging.debug('trying to send {}'.format(output_buffer))
                            self._master.slaves[module_index].output = struct.pack('{}h'.format(len(output_buffer)), *output_buffer)
                    sample_counter = sample_counter +1
                    if(sample_counter >= MAX_SAMPLES):
                        sample_counter = 0
                        self._currently_playing = False
                        self._plays_remaining = self._plays_remaining - 1
                        self.all_zero()
                        sleep_interval = 1.5
                        logging.debug('sleep for {} seconds'.format(sleep_interval))
                        time.sleep(sleep_interval)
                    
                else:
                    if self._plays_remaining == 0:
                        if (currentAnimation['name'] == 'bshake_30_5_25_100'):
                            logging.debug('playing shake next')
                            currentAnimation = luts.shake[0] # the only shake in the luts file is played after bshake_30_5_25_100shake_comes_next
                            self._plays_remaining = currentAnimation['min_play']
                        else:
                            logging.debug('choosing a new animation') 
                            currentAnimation = self.pickone(random.random())
                            logging.debug('chose {}'.format(currentAnimation['name']))
                            self._plays_remaining = random.randint(int(currentAnimation['min_play']), int(currentAnimation['max_play'])) 
    
                    logging.debug('playing {}, self._plays_remaining is {}'.format(currentAnimation['name'], self._plays_remaining))
                    MAX_SAMPLES = len(currentAnimation['lut'])
                    self._currently_playing = True

                time.sleep(0.001)
                

        except KeyboardInterrupt:
            # ctrl-C abort handling
            print('stopped')

    def pickone(self, randNum):
        ''' respect each animation's play_frequency by rolling dice.'''
        drawn = random.choice(self._current_lut)
        logging.debug('considering {} with play_frequency {} versus randNum {}'.format(drawn['name'], drawn['play_frequency'], randNum))
        if drawn['play_frequency'] >= randNum:
            logging.debug('returning {}'.format(drawn['name']))
            return drawn
        else:
            logging.debug('rejected {} and rechoosing'.format(drawn['name']))
            return self.pickone(random.random())

    def all_zero(self):
        # logging.debug('all_zero()')
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
            print(i, slave)
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

    print('aka_teaching_tree started')
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    for module in outputs.installed:
        logging.debug(module['name'])
        if len(module['phase_offsets']):
            # logging.debug(module['name'])
            pass

    try:
        BasicExample('eth0').run()
    except BasicExampleError as expt:
        print('aka_basic_example failed: ' + expt.message)
        sys.exit(1)
    else:
        print('usage: aka_basic_example ifname')
        sys.exit(1)
