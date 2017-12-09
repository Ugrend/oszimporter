from reader import Reader
from beatmap import Beatmap
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
        if not any(b.beatmap_id == beatmap.beatmap_id for b in self.beatmaps):
            self.beatmaps.append(beatmap)
            self.beatmap_count += 1

    def save(self, osu_db_file: str):
        f = open(osu_db_file, 'wb')
        w = Writer(f)
        w.write_int32(self.version)
        w.write_int32(self.folder_count)
        w.write_boolean(self.account_unlocked)
        w.write_ticks(self.unlock_date)
        w.write_string(self.username)
        w.write_int32(len(self.beatmaps))
        for beatmap in self.beatmaps:
            beatmap.save(w)
        w.write_int16(self.user_level)
        f.close()

    def to_json(self, **kwargs):
        return json.dumps(self, default=json_parser, **kwargs)

    @staticmethod
    def load(osu_db_file: str):
        f = open(osu_db_file, 'rb')
        r = Reader(f)
        db = Database.from_reader(r)
        f.close()
        return db


if __name__ == "__main__":
    db = Database.load('test.db')
    print(db.to_json(indent=4))
