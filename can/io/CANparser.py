"""
This Listener simply prints to stdout / the terminal or a file.
"""

import logging
import math
from can.listener import Listener
from scripts.utils import UtilityFunctions
from .generic import BaseIOHandler
from Shields import CANShield

log = logging.getLogger("can.io.printer")


class Parser(BaseIOHandler, Listener):


    def __init__(self, CANShield, file=None, append=False):
        """
        :param file: an optional path-like object or as file-like object to "print"
                     to instead of writing to standard out (stdout)
                     If this is a file-like object, is has to opened in text
                     write mode, not binary write mode.
        :param bool append: if set to `True` messages are appended to
                            the file, else the file is truncated
        """
        # self.publisher = CANShield.CANShield
        self.write_to_file = file is not None
        mode = "a" if append else "w"

        self.CAN_dictionary = {}
        self.filtered_CAN_dict ={}
        self.old_filtered_CAN_dict = {}

        super().__init__(file, mode=mode)
        self.list620_4 = ["None", "None", "None", "None", "None", "KeyOn", "None", "None"]
        self.list620_5 = ["None", "None", "BLDoor", "BRDoor", "FRDoor", "FLDoor", "None", "Cargo"]
        self.list620_7 = ["None", "None", "None", "None","HandBreak", "None", "FLSB", "None" ]

        self.sensorsDict = {"BLDoor":0, "BRDoor":0, "FRDoor":0, "FLDoor":0,  "frontSB":0, "HandBreak":0, "None":0}
        self.list2C1_7 =0 #Throttle in 7H
        self.list3BB_5 =0 #Breaks in 7H
        self.need_to_be_updated = {}
        self.CANShield = CANShield







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
            stringID = "{0:08x}".format(msg.arbitration_id)
        else:
            stringID = "{0:04x}".format(msg.arbitration_id)
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
        if stringID not in self.CAN_dictionary:                                                       #if it a message from a new ID
            address_data = [length, data_string, timestamp, 0]
            self.CAN_dictionary.update({stringID : address_data})
            self.CAN_dictionary[stringID][3] = 0

            if stringID == "0620":
                self.updateFilteredDict (data_string)            # print("adding: ", stringID)
            # #TODO raise fact
            #
            # for i in self.CAN_dic.keys():
            #     print(i," : ", self.CAN_dic[i])
        else:                                                                                  #if it a message from a known ID
            # If already appeared before, don't need to update
            if self.CAN_dictionary[stringID][1] == data_string:
                return
                # print (self.CAN_dic[stringID][1], data_string)
                # print("same")
            else:                                                                              #if it change in a message from a known ID
                # If the status of a relevant
                # update time stamp
                self.CAN_dictionary[stringID][3] = math.fsum([timestamp, -self.CAN_dictionary[stringID][3]])
                # print("- - - - - - - - - - - - - - - - - - - - - - -")
                # print("diffrences, ",stringID)
                # print("changed from: ", self.CAN_dic[stringID][1])
                # print("          to: ", data_string)
                # print("- - - - - - - - - - - - - - - - - - - - - - -")
                self.CAN_dictionary[stringID][1] = data_string
                # print(self.CAN_dic[stringID][1], data_string)
                # for i in self.CAN_dic.keys():
                #   print(i," : ", self.CAN_dic[i])

            # if stringID == "0610":
            #
            #     list620 = data_string.split()
            #     bin3list620 = int(bin(int(list620[3])),2)
            #     for b in range(8):
            #         if bin3list620>>b & list620[b] == 1:
            #             print("i'm here! this is b: ")
            if stringID == "0620":
                list_data = data_string.split()
                if(list_data[1]=="80"): # "80" means that there was a change on this ID
                    self.updateFilteredDict(data_string)

                # print("620! ", data_string)
                # list620 = data_string.split()
                # # binlist620_5 = int(bin(int(list620[5])), 2)
                # print(list620)
                #
                # binlist620_5 = int(list620[5], 16)
                #
                # print(bin(binlist620_5))
                # for b in range(8):
                #     andResult = binlist620_5>>b & 1
                #     print("b = ",b," bin is: ",binlist620_5>>b, " and in dict we have: ",self.sensorsDict[self.list620_5[b]]," and method: ",andResult)
                #
                #     if andResult:
                #         # print("Change in: ", self.list620_5[b], "from: ", self.sensorsDict[self.list620_5[b]], " to: ", binlist620_5>>b )
                #         self.sensorsDict[self.list620_5[b]] = andResult


                # print("1b: ",list620[1],", 1a: ",hex(int(list620[1],16)-0x10))
                # print("3b: ",list620[3],", 3a: ",hex(int(list620[3],16)-0x10))
                # print("5b: ",list620[5],", 5a: ",hex(int(list620[5],16)-0x10))
                # print(int(list620[0],2))
                # print(int(list620[5]))







    def updateFilteredDict(self, data_string):

        bin_list_620_5 = UtilityFunctions.decodeBinMsg(data_string, 5)
        bin_list_620_7 = UtilityFunctions.decodeBinMsg(data_string, 7)
        self.filtered_CAN_dict.update(UtilityFunctions.compareLists(self.list620_5, bin_list_620_5))
        self.filtered_CAN_dict.update(UtilityFunctions.compareLists(self.list620_7, bin_list_620_7))
        self.need_to_be_updated = UtilityFunctions.compareDicts(self.filtered_CAN_dict, self.old_filtered_CAN_dict)
        self.CANShield.onChange(self.need_to_be_updated)
        self.old_filtered_CAN_dict.update(self.filtered_CAN_dict) #update the "old" dict   for further comparisions

        ##TODO if succeeded
        self.need_to_be_updated = {}
