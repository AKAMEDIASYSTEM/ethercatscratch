"""Toggles the state of a digital output on an EL1259.

Usage: python basic_example.py <adapter>

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


class BasicExample:

    BECKHOFF_VENDOR_ID = 0x0002
    EK1100_PRODUCT_CODE = 0x044c2c52
    EL3002_PRODUCT_CODE = 0x0bba3052
    EL1259_PRODUCT_CODE = 0x04eb3052
    EL4102_PRODUCT_CODE = 0x10063052 # 2-chan 16-bit
    EL4008_PRODUCT_CODE = 0x0FA83052 # 8-chan 12-bit

    def __init__(self, ifname):
        self._ifname = ifname
        self._pd_thread_stop_event = threading.Event()
        self._ch_thread_stop_event = threading.Event()
        self._actual_wkc = 0
        self._master = pysoem.Master()
        self._master.in_op = False
        self._master.do_check_state = False
        SlaveSet = namedtuple('SlaveSet', 'name product_code config_func')
        self._expected_slave_layout = {0: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),
                                       1: SlaveSet('EL4102', self.EL4102_PRODUCT_CODE, None)
                                    }

    def el4102_setup(self, slave_pos):
        slave = self._master.slaves[slave_pos]
        # print(self._expected_slave_layout[slave_pos].extra_value)
        # well it turns out no SDO setup is required if we are not changing default behavior!
        print('done setup EL4102')

    def el4008_setup(self, slave_pos):
        slave = self._master.slaves[slave_pos]
        # print(self._expected_slave_layout[slave_pos].extra_value)
        # well it turns out no SDO setup is required if we are not changing default behavior!
        slave.sdo_write(0x1c12, 0, struct.pack('B', 0))
        map_1c13_bytes = struct.pack('BxH', 1, 0x00)
        slave.sdo_write(0x1c13, map_1c13_bytes, True)
        # slave.sdo_write(0x1011, 1, struct.pack('L',1684107116 ))
        # slave.dc_sync(0, 10000000)
        print('done setup EL4008')

    def ek1100_setup(self, slave_pos):
        slave = self._master.slaves[slave_pos]
        # print(self._expected_slave_layout[slave_pos].extra_value)
        # well it turns out no SDO setup is required if we are not changing default behavior!
        print('done setup EK1100')

    def el1259_setup(self, slave_pos):
        slave = self._master.slaves[slave_pos]
        # from the XML reference:

        # writing "1" to 0x8001:register 2 means "enable manual operation"
        # this makes sense because later in the demo code we toggle this output "manually"


        # <AlternativeSmMapping>
        #                                 <Name>Multi-Timestamping 8 Ch. 1x</Name>
        #                                 <Sm No="2">
        #  ...the rx_map_obj payload corresponds to this multi-timesampling preset

        slave.sdo_write(0x8001, 2, struct.pack('B', 1))

        rx_map_obj = [0x1603,
                      0x1607,
                      0x160B,
                      0x160F,
                      0x1611,
                      0x1617,
                      0x161B,
                      0x161F,
                      0x1620,
                      0x1621,
                      0x1622,
                      0x1623,
                      0x1624,
                      0x1625,
                      0x1626,
                      0x1627]
        rx_map_obj_bytes = struct.pack(
            'Bx' + ''.join(['H' for i in range(len(rx_map_obj))]), len(rx_map_obj), *rx_map_obj)
        slave.sdo_write(0x1c12, 0, rx_map_obj_bytes, True)

        slave.dc_sync(1, 10000000)

    def _processdata_thread(self):
        while not self._pd_thread_stop_event.is_set():
            self._master.send_processdata()
            self._actual_wkc = self._master.receive_processdata(10000)
            if not self._actual_wkc == self._master.expected_wkc:
                print('incorrect wkc')
            time.sleep(0.001)

    def _pdo_update_loop(self):
        print('in PDO update_loop')
        self._master.in_op = True
        for i in range(len(self._master.slaves)):
            output_len = len(self._master.slaves[i].output)
            print(self._master.slaves[i].output)
        tmp = bytearray([0])
        rx_map_obj = [0x3fff, 0x3fff]
        toggle = True
        counter = 0
        MAX_SAMPLES = len(luts.sin_lut)
        phase = len(luts.sin_lut) / 4
        try:
            while 1:
                counter = counter +1
                if counter >= MAX_SAMPLES:
                    counter = 0
                rx_map_obj[0] = luts.sin_lut[counter]
                rx_map_obj[1] = luts.sin_lut[int(max(0, counter - phase))]
                tmp = struct.pack('2h', rx_map_obj[0], rx_map_obj[1])
                # bigtmp = struct.pack('8h', rx_map_obj[0], rx_map_obj[1], rx_map_obj[0], rx_map_obj[1], rx_map_obj[0], rx_map_obj[1], rx_map_obj[0], rx_map_obj[1])
                self._master.slaves[1].output = tmp
                time.sleep(0.001)

        except KeyboardInterrupt:
            # ctrl-C abort handling
            print('stopped')

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

    print('aka_basic_example started')

    if len(sys.argv) > 1:
        try:
            BasicExample(sys.argv[1]).run()
        except BasicExampleError as expt:
            print('aka_basic_example failed: ' + expt.message)
            sys.exit(1)
    else:
        print('usage: aka_basic_example ifname')
        sys.exit(1)
