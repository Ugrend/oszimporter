__author__ = 'Ugrend'
import io
from datetime import datetime, timedelta
import struct


class Reader:

    def __init__(self, file_handle: io.FileIO):
        self.file = file_handle

    def parse_dict_value(self):
        t = int.from_bytes(self.file.read(1), byteorder='little')
        if t == 0:
            return None
        if t == 1:
            return self.read_boolean()
        if t == 8:
            return self.read_int32()
        if t == 13:
            return self.read_float64()

        raise Exception("I don't know what this byte means %d" %t)

    def read_byte(self)->int:
        return int.from_bytes(self.file.read(1), byteorder='little')

    def read_int32(self)->int:
        return int.from_bytes(self.file.read(4), byteorder='little', signed=True)

    def read_int16(self)->int:
        return int.from_bytes(self.file.read(2), byteorder='little', signed=False)

    def read_boolean(self)->bool:
        return bool(int.from_bytes(self.file.read(1), byteorder='little'))

    def read_ticks(self)->int:
        # TODO: convert to datetime
        ticks = int.from_bytes(self.file.read(8), byteorder='little', signed=True)
        return ticks

    def read_float32(self)-> int:
        return struct.unpack('f', self.file.read(4))[0]

    def read_float64(self)->int:
        return struct.unpack('d', self.file.read(8))[0]

    def read_string(self)->(str, None):

        start = self.file.read(1)
        if int.from_bytes(start, byteorder='little') == 0:
            return None

        length = 0
        s = 0
        while True:
            byte = self.read_byte()
            length |= ((byte & 0x7F) << s)
            if(byte & 0x80) == 0:
                break
            s += 7
        return self.file.read(length).decode('utf-8')

    def read_dictionary(self)->(dict, None):
        length = self.read_int32()
        if length < 0:
            return None
        count = 0
        dictionary = {}
        while count != length:
            count += 1
            key = self.parse_dict_value()
            dictionary[key] = self.parse_dict_value()
        return dictionary

    def read_timing_points(self)-> list:
        result = []
        length = self.read_int32()
        count = 0
        while count != length:
            count += 1
            result.append({
                "beat_length": self.read_float64(),
                "offset": self.read_float64(),
                "timing_change": self.read_boolean()
            })
        return result
