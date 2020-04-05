

class UtilityFunctions:


    @staticmethod
    def check_user_input(exit_program):
        pass

        var = ""
        # while not exit_program:
        #     var = input("")
        #     exit_program = (var == 'q' or var == 'Q')

    """
    This function will help us compare the bits of a certain byte
    IN: data_strin of a certain message and the desired byte location (from 8 b)
    OUT: list of 0s and 1s
    """
    @staticmethod
    def decodeBinMsg(data_string, byte_pos, data_len = 8):
        bin_list = []
        list_data =  data_string.split()
        bin_data = int(list_data[byte_pos],16)
        for b in range(data_len):
            bin_list.append(bin_data >> b & 1)

        return bin_list



    """
    This func receives the list of features of a specific car area, and a list of bools according to each feature, (i.e Doors)
    and what happen if the bool is tru or false ("open, close")
    
    and gives back a dict with the features and their status.
    """
    @staticmethod
    def compareLists(features_list, bin_list, same = True):
        true_false_dict = {}
        for i in range(len(features_list)):
            if features_list[i] == "None":
                pass
            elif bin_list[i]:
                d = {features_list[i]:1 & same}
                true_false_dict.update(d)
            else:
                d = {features_list[i]: 0 & same}
                true_false_dict.update(d)

        return true_false_dict


    """
    compare 2 dicts a nd return updated dic with only the added values or the changed ones
    """


    @staticmethod
    def compareDicts(newDict, oldDict):
        diffDict = {}
        for key in newDict:
            # if key not in oldDict:
            #     diffDic.update({key: newDict[key]})
            # if newDict[key] != oldDict[key]:
            #     diffDic.update({key:newDict[key]})
            if key not in oldDict or newDict[key] != oldDict[key]: #first if is for new commers, second for changes in dicts
                # print("new", newDict[key], "old", oldDict[key])
                d = {key:newDict[key]}
                diffDict.update(d)

        return diffDict
