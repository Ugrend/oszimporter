import io
from struct import pack

class Writer:

    def __init__(self, writer: io.FileIO):
        self.writer = writer

    def write_byte(self, v: int):
        self.writer.write(pack('b', v))

    def write_int32(self, v: int):
        self.writer.write(pack('i', v))

    def write_int16(self, v: int):
        self.writer.write(pack('H', v))

    def write_boolean(self, v: bool):
        self.writer.write(pack('?', v))

    def write_ticks(self, v: int):
        self.writer.write(pack('q', v))

    def write_float32(self, v: int):
        self.writer.write(pack('f', v))

    def write_float64(self, v: int):
        self.writer.write(pack('d', v))

    def write_string(self, v: str):
        if v is None:
            v = ""
        length = len(v)
        if length == 0:
            self.write_byte(0x0B)
            self.write_byte(0)
            return

        _bStr = pack('b', 0x0B)
        while length != 0:
            _b = (length & 0x7F)
            length >>= 7
            if length != 0:
                _b |= 0x80
            _bStr += pack('B', _b)
        _bStr += pack(str(len(v))+'s', bytes(v, encoding='utf-8'))
        self.writer.write(_bStr)

