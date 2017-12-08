from reader import Reader
from Beatmap import Beatmap
from helpers import json_parser
import json
__author__ = 'Ugrend'


class Database:
    version: int
    folder_count: int
    account_unlocked: bool
    unlock_date: int
    username: str
    beatmap_count: int
    beatmaps: list

    @staticmethod
    def from_reader(r: Reader):
        db = Database()
        db.version = r.read_int32()
        db.folder_count = r.read_int32()
        db.account_unlocked = r.read_boolean()
        db.unlock_date = r.read_ticks()
        db.username = r.read_string()
        db.beatmap_count = r.read_int32()
        db.beatmaps = [Beatmap.from_reader(r) for x in range(db.beatmap_count)]
        return db

if __name__ == "__main__":
    f = open('osu!.db', 'rb')
    r = Reader(f)
    db = Database.from_reader(r)
    print(json.dumps(db,default=json_parser,indent=4))
    f.close()
