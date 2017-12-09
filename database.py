from reader import Reader
from Beatmap import Beatmap
from helpers import json_parser
from writer import Writer
import json
from typing import List
__author__ = 'Ugrend'


class Database:
    version: int
    folder_count: int
    account_unlocked: bool
    unlock_date: int
    username: str
    beatmap_count: int
    beatmaps: List[Beatmap]
    user_level: int

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
        db.user_level = r.read_int16()
        return db

    def add_set(self, beatmaps: List[Beatmap]):
        if len(beatmaps) == 0:
            return
        if not any(b.folder_name == beatmaps[0].folder_name for b in self.beatmaps):
            self.folder_count += 1
        for beatmap in beatmaps:
            self.add_beatmap(beatmap)

    def add_beatmap(self, beatmap: Beatmap):
        if not any(b.BeatmapID == beatmap.BeatmapID for b in self.beatmaps):
            self.beatmaps.append(beatmap)
            self.beatmap_count += 1

    def save(self, w: Writer):
        w.write_int32(self.version)
        w.write_int32(self.folder_count)
        w.write_boolean(self.account_unlocked)
        w.write_ticks(self.unlock_date)
        w.write_string(self.username)
        w.write_int32(len(db.beatmaps))
        for beatmap in db.beatmaps:
            beatmap.save(w)
        w.write_int16(db.user_level)


if __name__ == "__main__":
    f = open('osu!.db', 'rb')
    r = Reader(f)
    db = Database.from_reader(r)
    print(json.dumps(db.beatmaps[0].Version,default=json_parser,indent=4))
    f.close()
    #f2 = open('test.db', 'wb')
    #w = Writer(f2)
    #db.write_binary(w)
