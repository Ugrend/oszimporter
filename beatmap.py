__author__ = 'Ugrend'

from reader import Reader
from writer import  Writer
from io import BytesIO
import hashlib
import os


class HitObject:

    is_circle: bool = False
    is_slider: bool = False
    is_spinner: bool = False

    def __init__(self, line):
        object_val = int(line.split(",")[3])
        if object_val & 1:
            self.is_circle = True
            return
        if object_val & 2:
            self.is_slider = True
            return
        if object_val & 8:
            self.is_spinner = True
            return

        self.is_circle = True


class Beatmap:

    _data_length: int = 0
    artist: str = ""
    artist_unicode: str = ""
    title: str = ""
    title_unicode: str = ""
    creator: str = ""
    version: str = ""
    audio_file_name: str = ""
    md5sum: str = ""
    beatmap_file_name: str = ""
    ranked: bool = False
    circles: int = 0
    sliders: int = 0
    spinners: int = 0
    modified: int = 0
    AR: int = 7
    CS: int
    HP: int
    OD: int
    slider_multi: int = 1
    star_ratings: list = [{}, {}, {}, {}]
    drain_time_seconds: int = 0
    map_length: int
    preview_time: int = 0
    timing_points: list = []
    beatmap_id: int
    beatmap_set_id: int
    topic_id: int = 0
    ranks: list = [9, 9, 9, 9]
    offset: int = 0
    stack_leniency: int
    game_mode: int
    source: str
    tags: str
    offset_online: int = 0
    title_font: str = ""
    not_played: bool = False
    last_played: int = 0
    osz2: bool = False
    folder_name: str
    last_checked_osu: int = 0
    ignore_beatmap_sounds: bool = False
    ignore_beatmap_skin: bool = False
    disable_story_board: bool = False
    disable_video: bool = False
    visual_override: bool = False
    edited: int = 0
    mania_scroll_speed: int = 0

    def save(self, w: Writer):
        binary_self = self.to_binary()
        w.write_int32(binary_self.getbuffer().nbytes)
        w.writer.write(binary_self.getvalue())

    def to_binary(self)->BytesIO:
        b = BytesIO()
        w = Writer(b)
        w.write_string(self.artist)
        w.write_string(self.artist_unicode)
        w.write_string(self.title)
        w.write_string(self.title_unicode)
        w.write_string(self.creator)
        w.write_string(self.version)
        w.write_string(self.audio_file_name)
        w.write_string(self.md5sum)
        w.write_string(self.beatmap_file_name)
        w.write_boolean(self.ranked)
        w.write_int16(self.circles)
        w.write_int16(self.sliders)
        w.write_int16(self.spinners)
        w.write_ticks(self.modified)
        w.write_float32(self.AR)
        w.write_float32(self.CS)
        w.write_float32(self.HP)
        w.write_float32(self.OD)
        w.write_float64(self.slider_multi)

        for starRating in self.star_ratings:
            w.write_int32(len(starRating))
            for k,v in starRating.items():
                # TODO: store type in dict so we programmatically know how to store the dictionary
                w.write_byte(8)
                w.write_int32(k)
                w.write_byte(13)
                w.write_float64(v)

        w.write_int32(self.drain_time_seconds)
        w.write_int32(self.map_length)
        w.write_int32(self.preview_time)

        w.write_int32(len(self.timing_points))
        for timingPoint in self.timing_points:
            w.write_float64(timingPoint['bpm'])
            w.write_float64(timingPoint['offset'])
            w.write_boolean(timingPoint['timing_change'])

        w.write_int32(self.beatmap_id)
        w.write_int32(self.beatmap_set_id)
        w.write_int32(self.topic_id)

        for rank in self.ranks:
            w.write_byte(rank)

        w.write_int16(self.offset)
        w.write_float32(self.stack_leniency)
        w.write_byte(self.game_mode)
        w.write_string(self.source)
        w.write_string(self.tags)
        w.write_int16(self.offset_online)
        w.write_string(self.title_font)
        w.write_boolean(self.not_played)
        w.write_ticks(self.last_played)
        w.write_boolean(self.osz2)
        w.write_string(self.folder_name)
        w.write_ticks(self.last_checked_osu)
        w.write_boolean(self.ignore_beatmap_sounds)
        w.write_boolean(self.ignore_beatmap_skin)
        w.write_boolean(self.disable_story_board)
        w.write_boolean(self.disable_video)
        w.write_boolean(self.visual_override)
        w.write_int32(self.edited)
        w.write_byte(self.mania_scroll_speed)
        return b




    @staticmethod
    def from_osu_file(osu_file: str, folder: str):
        def parse_value(line: str):
            return ''.join(line.split(":")[1:]).lstrip(" ")

        b = Beatmap()
        b.folder_name = folder
        b.md5sum = hashlib.md5(open(osu_file, 'rb').read()).hexdigest()
        b.beatmap_file_name = os.path.basename(osu_file)
        parsing_timing = False
        parsing_hitobjects = False
        with open(osu_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if parsing_timing:
                    if line == "":
                        parsing_timing = False
                        continue
                    point = line.split(",")
                    b.timing_points.append({
                        'bpm': float(point[1]),
                        'offset': float(point[0]),
                        'timing_change': (float(point[1]) > 0)
                    })

                if parsing_hitobjects:
                    if line == "":
                        continue
                    hit_object = line.split(",")
                    b.map_length = int(hit_object[2])
                    hit_object = HitObject(line)
                    b.circles += 1 if hit_object.is_circle else 0
                    b.sliders += 1 if hit_object.is_slider else 0
                    b.spinners += 1 if hit_object.is_spinner else 0

                if line.startswith("AudioFilename"):
                    b.audio_file_name = parse_value(line)
                    continue
                if line.startswith("PreviewTime"):
                    b.preview_time = int(parse_value(line))
                    continue
                if line.startswith("StackLeniency"):
                    b.stack_leniency = float(parse_value(line))
                    continue
                if line.startswith("Mode"):
                    b.game_mode = int(parse_value(line))
                    continue
                if line.startswith("Title"):
                    b.title = parse_value(line)
                    continue
                if line.startswith("TitleUnicode"):
                    b.title_unicode = parse_value(line)
                    continue
                if line.startswith("Artist"):
                    b.artist = parse_value(line)
                    continue
                if line.startswith("ArtistUnicode"):
                    b.artist_unicode = parse_value(line)
                    continue
                if line.startswith("Creator"):
                    b.creator = parse_value(line)
                    continue
                if line.startswith("Version"):
                    b.version = parse_value(line)
                    continue
                if line.startswith("Source"):
                    b.source = parse_value(line)
                    continue
                if line.startswith("Tags"):
                    b.tags = parse_value(line)
                    continue
                if line.startswith("BeatmapID"):
                    b.beatmap_id = int(parse_value(line))
                    continue
                if line.startswith("BeatmapSetID"):
                    b.beatmap_set_id = int(parse_value(line))
                    continue
                if line.startswith("HPDrainRate"):
                    b.HP = float(parse_value(line))
                    continue
                if line.startswith("CircleSize"):
                    b.CS = float(parse_value(line))
                    continue
                if line.startswith("OverallDifficulty"):
                    b.OD = float(parse_value(line))
                    continue
                if line.startswith("ApproachRate"):
                    b.AR = float(parse_value(line))
                    continue
                if line.startswith("SliderMultiplier"):
                    b.AR = float(parse_value(line))
                    continue

                if line.startswith("[TimingPoints]"):
                    parsing_timing = True
                    continue
                if line.startswith("[HitObjects]"):
                    parsing_hitobjects = True
                    continue

        return b

    @staticmethod
    def from_reader(reader: Reader):
        beatmap = Beatmap()
        beatmap._data_length = reader.read_int32()
        beatmap.artist = reader.read_string()
        beatmap.artist_unicode = reader.read_string()
        beatmap.title = reader.read_string()
        beatmap.title_unicode = reader.read_string()
        beatmap.creator = reader.read_string()
        beatmap.version = reader.read_string()
        beatmap.audio_file_name = reader.read_string()

        beatmap.md5sum = reader.read_string()
        beatmap.beatmap_file_name = reader.read_string()
        beatmap.ranked = reader.read_boolean()
        beatmap.circles = reader.read_int16()
        beatmap.sliders = reader.read_int16()
        beatmap.spinners = reader.read_int16()
        beatmap.modified = reader.read_ticks()
        beatmap.AR = reader.read_float32()
        beatmap.CS = reader.read_float32()
        beatmap.HP = reader.read_float32()
        beatmap.OD = reader.read_float32()
        beatmap.slider_multi = reader.read_float64()
        beatmap.star_ratings = [reader.read_dictionary() for x in range(0, 4)]
        beatmap.drain_time_seconds = reader.read_int32()
        beatmap.map_length = reader.read_int32()
        beatmap.preview_time = reader.read_int32()
        beatmap.timing_points = reader.read_timing_points()
        beatmap.beatmap_id = reader.read_int32()
        beatmap.beatmap_set_id = reader.read_int32()
        beatmap.topic_id = reader.read_int32()
        beatmap.ranks = [reader.read_byte() for x in range (0,4)]
        beatmap.offset = reader.read_int16()
        beatmap.stack_leniency = reader.read_float32()
        beatmap.game_mode = reader.read_byte()
        beatmap.source = reader.read_string()
        beatmap.tags = reader.read_string()
        beatmap.offset_online = reader.read_int16()
        beatmap.title_font = reader.read_string()
        beatmap.not_played = reader.read_boolean()
        beatmap.last_played = reader.read_ticks()
        beatmap.osz2 = reader.read_boolean()
        beatmap.folder_name = reader.read_string()
        beatmap.last_checked_osu = reader.read_ticks()
        beatmap.ignore_beatmap_sounds = reader.read_boolean()
        beatmap.ignore_beatmap_skin = reader.read_boolean()
        beatmap.disable_story_board = reader.read_boolean()
        beatmap.disable_video = reader.read_boolean()
        beatmap.visual_override = reader.read_boolean()
        beatmap.edited = reader.read_int32()
        beatmap.mania_scroll_speed = reader.read_byte()

        return beatmap
