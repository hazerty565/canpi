from math import ceil

from . import CanBus
from constances import CAN_CFG


class Cvm(CanBus):
    CVM = CAN_CFG.get('CVM')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
  
    def _get_data(self, timeout, msg_send):
        data_zero, data, multiline  = 0x21, bytearray(), -1
        while timeout != 0 and multiline != 0:
            msg_recv = self.recv(0.1)
            if msg_recv and msg_recv.arbitration_id == self.ID_REPLY:
                if msg_recv.data[0] == 0x10 and msg_recv.data[3] == msg_send[2] and msg_recv.data[4] == msg_send[3]:
                    multiline = ceil((int(msg_recv.data[1]) + 1) / 7) - 1
                    print(multiline)
                    data.extend(msg_recv.data[1:])
                    self.send_messages(self.ID_DIAG, self.DATA_EXT, True)
                elif msg_recv.data[0] == data_zero:
                    data.extend(msg_recv.data[1:])
                    data_zero += 1
                    multiline -= 1
                elif multiline == -1 and msg_recv.dlc != 0:
                    data =  msg_recv.data
                self.data_print(msg_recv)
            timeout -= 1
        return data