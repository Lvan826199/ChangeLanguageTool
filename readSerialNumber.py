import os
class adbDevices():


    def __init__(self):
        pass

    def readSN(self):

        text = os.popen("adb devices | findstr /v List").read()

        Sn = text.split('d')[0].split()[0]

        return Sn

