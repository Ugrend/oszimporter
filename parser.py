__author__ = 'Ugrend'

from reader import Reader
from Beatmap import Beatmap

if __name__ == "__main__":
    database = {

        "beatmaps": []

    }
    f = open('osu!.db', 'rb')
    r = Reader(f)
    print(r.read_int32())
    print(r.read_int32())
    print(r.read_boolean())
    print(r.read_ticks())
    print(r.read_string())
    length = r.read_int32()
    print(length)
    count = 0
    while count <= length:
        entry_length = r.read_int32()
        b = Beatmap.from_reader(r)
        database["beatmaps"].append(b.__dict__)
        count += 1
    print(database)
    f.close()
