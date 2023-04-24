
from os.path import exists


class PacketStream:
    def __init__(self, file_location, function, permissions="rb", encoding="utf-8"):
        try:
            exists(file_location)
        except OSError as err:
            print("OS error: {0}".format(err))

        self.__f__ = open(file_location,  permissions, encoding=encoding, buffering=256)
        self.__packet_buffer__ = []
        self.__save__ = 'w' in permissions

