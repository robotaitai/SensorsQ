"""
This Listener simply prints to stdout / the terminal or a file.
"""

import logging
import math
from can.listener import Listener
from .generic import BaseIOHandler

log = logging.getLogger("can.io.printer")


class Parser(BaseIOHandler, Listener):


    def __init__(self, file=None, append=False):
        """
        :param file: an optional path-like object or as file-like object to "print"
                     to instead of writing to standard out (stdout)
                     If this is a file-like object, is has to opened in text
                     write mode, not binary write mode.
        :param bool append: if set to `True` messages are appended to
                            the file, else the file is truncated
        """

        self.write_to_file = file is not None
        mode = "a" if append else "w"
        self.CAN_dic = {}
        super().__init__(file, mode=mode)





    def relevant_data(self, msg):
        if msg.is_extended_id:
            arbitration_id_string = "ID: {0:08x}".format(msg.arbitration_id)
        else:
            arbitration_id_string = "ID: {0:04x}".format(msg.arbitration_id)

        length = "DLC: {0:2d}".format(msg.dlc)

        data_strings = []
        if msg.data is not None:
            for index in range(0, min(msg.dlc, len(msg.data))):
                data_strings.append("{0:02x}".format(msg.data[index]))
        if data_strings:  # if not empty
            data_string = " ".join(data_strings).ljust(24, " ")
        else:
            data_string = " " * 24
        print(arbitration_id_string, length, data_strings)


        # if (msg.data is not None) and (msg.data.isalnum()):
        #     field_strings.append("'{}'".format(self.data.decode("utf-8", "replace")))

    def on_message_received(self, msg):
        # if self.write_to_file:
        #     self.file.write(str(msg) + "\n")
        # else:

        # self.relevant_data(msg)

        #Parse ID

        if msg.is_extended_id:
            arbitration_id_string = "{0:08x}".format(msg.arbitration_id)
        else:
            arbitration_id_string = "{0:04x}".format(msg.arbitration_id)
        # Parse length

        length = "{0:2d}".format(msg.dlc)

        # Parse Data
        data_strings = []
        if msg.data is not None:
            for index in range(0, min(msg.dlc, len(msg.data))):
                data_strings.append("{0:02x}".format(msg.data[index]))
        if data_strings:  # if not empty
            data_string = " ".join(data_strings).ljust(24, " ")
        else:
            data_string = " " * 24

        # Parse Timestamp
        timestamp = msg.timestamp


        #first time appearance
        if arbitration_id_string not in self.CAN_dic:
            values = [length, data_string, timestamp, 0]
            self.CAN_dic.update({ arbitration_id_string : values })
            self.CAN_dic[arbitration_id_string][3] = 0
            print("adding: ", arbitration_id_string)
            #TODO raise fact

            for i in self.CAN_dic.keys():
                print(i," : ", self.CAN_dic[i])
        else:
            # If already appeared before, don't need to update
            if self.CAN_dic[arbitration_id_string][1] == data_string:
                pass
                # print (self.CAN_dic[arbitration_id_string][1], data_string)
                # print("same")
            else:
                # If the status of a relevant
                # update time stamp
                self.CAN_dic[arbitration_id_string][3] = math.fsum([timestamp, -self.CAN_dic[arbitration_id_string][3]])
                print("- - - - - - - - - - - - - - - - - - - - - - -")
                print("diffrences, ",arbitration_id_string)
                print("changed from: ", self.CAN_dic[arbitration_id_string][1])
                print("          to: ", data_string)
                print("- - - - - - - - - - - - - - - - - - - - - - -")
                self.CAN_dic[arbitration_id_string][1] = data_string
                # print(self.CAN_dic[arbitration_id_string][1], data_string)
                for i in self.CAN_dic.keys():
                  print(i," : ", self.CAN_dic[i])

            if arbitration_id_string == "0610":
                list620 = data_string.split()
                # print("1b: ",list620[1],", 1a: ",hex(int(list620[1],16)-0x10))
                # print("3b: ",list620[3],", 3a: ",hex(int(list620[3],16)-0x10))
                # print("5b: ",list620[5],", 5a: ",hex(int(list620[5],16)-0x10))
                print(int(list620[1],2))
















    def __str__(self) -> str:
        field_strings = ["Timestamp: {0:>15.6f}".format(self.timestamp)]
        if self.is_extended_id:
            arbitration_id_string = "ID: {0:08x}".format(self.arbitration_id)
        else:
            arbitration_id_string = "ID: {0:04x}".format(self.arbitration_id)
        field_strings.append(arbitration_id_string.rjust(12, " "))

        flag_string = " ".join(
            [
                "X" if self.is_extended_id else "S",
                "E" if self.is_error_frame else " ",
                "R" if self.is_remote_frame else " ",
                "F" if self.is_fd else " ",
                "BS" if self.bitrate_switch else "  ",
                "EI" if self.error_state_indicator else "  ",
            ]
        )

        field_strings.append(flag_string)

        field_strings.append("DLC: {0:2d}".format(self.dlc))
        data_strings = []
        if self.data is not None:
            for index in range(0, min(self.dlc, len(self.data))):
                data_strings.append("{0:02x}".format(self.data[index]))
        if data_strings:  # if not empty
            field_strings.append(" ".join(data_strings).ljust(24, " "))
        else:
            field_strings.append(" " * 24)

        if (self.data is not None) and (self.data.isalnum()):
            field_strings.append("'{}'".format(self.data.decode("utf-8", "replace")))

        if self.channel is not None:
            try:
                field_strings.append("Channel: {}".format(self.channel))
            except UnicodeEncodeError:
                pass

        return "    ".join(field_strings).strip()
