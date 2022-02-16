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


class BasicExample:

    BECKHOFF_VENDOR_ID = 0x0002
    EK1100_PRODUCT_CODE = 0x044c2c52
    EL3002_PRODUCT_CODE = 0x0bba3052
    EL1259_PRODUCT_CODE = 0x04eb3052
    EL4102_PRODUCT_CODE = 0x10063052 # 2-chan 16-bit
    EL4008_PRODUCT_CODE = 0x0fa83052 # 8-chan 12-bit

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
                                       # 1: SlaveSet('EL4102', self.EL4102_PRODUCT_CODE, None)
                                       1: SlaveSet('EL4102', self.EL4102_PRODUCT_CODE, self.el4102_setup),
                                       2: SlaveSet('EL4102', self.EL4102_PRODUCT_CODE, self.el4102_setup),
                                       3: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),
                                       4: SlaveSet('EL4102', self.EL4102_PRODUCT_CODE, self.el4102_setup)
                                       }

    def el4102_setup(self, slave_pos):
        slave = self._master.slaves[slave_pos]
        # slave.sdo_write(0x8001, 2, struct.pack('B', 1))
        # 0x3fff is 5v, 0x7fff is 10v
        # https://infosys.beckhoff.com/english.php?content=../content/1033/el41xx/1851316619.html#1714645131&id=
        # 0x4061:05 is write an abs val to ch1
        # 0x40a1:05 is write abs val to ch2
        # (I think)
        # rx_map_obj = [0x3fff]
        # rx_map_obj_bytes = struct.pack(
        #     'Bx' + ''.join(['H' for i in range(len(rx_map_obj))]), len(rx_map_obj), *rx_map_obj)
        # slave.sdo_write(0x8010, 2, rx_map_obj_bytes, True)
        # slave.sdo_write(0x1c12, 0, struct.pack('B', 2))
        # If this object is set to “0x64616F6C” in the set value dialog, all backup objects are reset to their delivery state
        # slave.sdo_write(0x1011, 0, struct.pack('B', 1))
        
        # sending this is supposed to factory-default the unit
        # slave.sdo_write(0x1011, 1, bytes(ctypes.c_uint32(0x64616F6C)))
        # sending this should 
        # slave.sdo_write(0x1c12, 0, struct.pack('B', 2))
        # slave.dc_sync(1, 10000000)
        rx_map_obj = [0x1600]
        rx_map_obj_bytes = struct.pack(
            'Bx' + ''.join(['H' for i in range(len(rx_map_obj))]), len(rx_map_obj), *rx_map_obj)
        slave.sdo_write(0x1c12, 0, struct.pack('I', 0), True)
        slave.sdo_write(0x1c13, 0, struct.pack('I', 0), True)
        slave.sdo_write(0x1c12, 0x01, struct.pack('I', 0x1600), True)
        slave.sdo_write(0x1c12, 0x02, struct.pack('I', 0x1601), True)
        slave.sdo_write(0x1c12, 0, struct.pack('I', 0x02), True)
        # slave.dc_sync(1, 10000000)
        # slave.dc_sync(1, 1000000)
        print('done setup EL4102')

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
        print('in update_loop')
        self._master.in_op = True
        for i in range(len(self._master.slaves)):
            output_len = len(self._master.slaves[i].output)
            print(self._master.slaves[i].output)
        # tmp = bytearray([0 for i in range(2*output_len)])
        tmp = bytearray([0])
        rx_map_obj = [0x3fff, 0x3fff,0,0]
        toggle = True
        counter = 0x0000
        step = 1000 # 6400 step size at sleep=0.0005 gets us 1ch of 120hz
        try:
            while 1:
                if toggle:
                    counter = counter + step
                else:
                    counter = counter - step
                
                if counter >= 0x7ffe:
                    counter = 0x7ffe
                    toggle ^= True
                    print(rx_map_obj)
                    # print(struct.unpack(tmp))
                if counter <= 0x0001:
                    counter = 0x001
                    toggle ^= True
                    print(rx_map_obj)
                rx_map_obj[0] = counter
                rx_map_obj[1] = max(0x7ffe - counter, 0)
                rx_map_obj[2] = counter
                rx_map_obj[3] = max(0x7ffe - counter, 0)
                # tmp = struct.pack('Bx' + ''.join(['H' for i in range(len(rx_map_obj))]), len(rx_map_obj), *rx_map_obj)
                tmp = struct.pack('Bx' + ''.join(['H' for i in range(len(rx_map_obj))]), len(rx_map_obj), *rx_map_obj)
                self._master.slaves[1].output = tmp
                self._master.slaves[2].output = tmp
                self._master.slaves[4].output = tmp
                # print(rx_map_obj)
                # print(tmp)
                # self._master.slaves[1].output = rx_map_obj_bytes
                # self._master.slaves[1].sdo_write(0x8010, 2, bytes(0x3fff), True)
                # time.sleep(0.0005)
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
