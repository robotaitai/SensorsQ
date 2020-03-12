

#IP = "192.168.1.16"  # ofri
#IP = "192.168.100.181" #bench
# IP = "192.168.10.106"
IPs = {0: "192.168.10.75",
       1: "192.168.1.17" }

Shields = {0: "Sensors",
            1: "CAN"}


class Configurations:

    def __init__(self):
        self.shield = Shields[1]
        print(self.shield, " Shield was chosen")

        self.ip = IPs[1]

