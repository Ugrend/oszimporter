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
    Artist: str = ""
    ArtistUnicode: str = ""
    Title: str = ""
    TitleUnicode: str = ""
    Creator: str = ""
    Version: str = ""
    AudioFileName: str = ""
    BeatmapChecksum: str = ""
    BeatmapFileName: str = ""
    RankedStatus: bool = False
    Circles: int = 0
    Sliders: int = 0
    Spinners: int = 0
    Modified: int = 0
    AR: int = 7
    CS: int
    HP: int
    OD: int
    SliderMultiplier: int = 1
    starRatings: list = [{}, {}, {}, {}]
    DrainTimeSeconds: int = 0
    Length: int
    PreviewTime: int = 0
    TimingPoints: list = []
    BeatmapID: int
    BeatmapSetID: int
    TopicId: int = 0
    ranks: list = [9, 9, 9, 9]
    Offset: int = 0
    StackLeniency: int
    GameMode: int
    Source: str
    Tags: str
    OffsetOnline: int = 0
    TitleFont: str = ""
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
        w.write_string(self.Artist)
        w.write_string(self.ArtistUnicode)
        w.write_string(self.Title)
        w.write_string(self.TitleUnicode)
        w.write_string(self.Creator)
        w.write_string(self.Version)
        w.write_string(self.AudioFileName)
        w.write_string(self.BeatmapChecksum)
        w.write_string(self.BeatmapFileName)
        w.write_boolean(self.RankedStatus)
        w.write_int16(self.Circles)
        w.write_int16(self.Sliders)
        w.write_int16(self.Spinners)
        w.write_ticks(self.Modified)
        w.write_float32(self.AR)
        w.write_float32(self.CS)
        w.write_float32(self.HP)
        w.write_float32(self.OD)
        w.write_float64(self.SliderMultiplier)

        for starRating in self.starRatings:
            w.write_int32(len(starRating))
            for k,v in starRating.items():
                # TODO: store type in dict so we programmatically know how to store the dictionary
                w.write_byte(8)
                w.write_int32(k)
                w.write_byte(13)
                w.write_float64(v)

        w.write_int32(self.DrainTimeSeconds)
        w.write_int32(self.Length)
        w.write_int32(self.PreviewTime)

        w.write_int32(len(self.TimingPoints))
        for timingPoint in self.TimingPoints:
            w.write_float64(timingPoint['bpm'])
            w.write_float64(timingPoint['offset'])
            w.write_boolean(timingPoint['timing_change'])

        w.write_int32(self.BeatmapID)
        w.write_int32(self.BeatmapSetID)
        w.write_int32(self.TopicId)

        for rank in self.ranks:
            w.write_byte(rank)

        w.write_int16(self.Offset)
        w.write_float32(self.StackLeniency)
        w.write_byte(self.GameMode)
        w.write_string(self.Source)
        w.write_string(self.Tags)
        w.write_int16(self.OffsetOnline)
        w.write_string(self.TitleFont)
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
        b.BeatmapChecksum = hashlib.md5(open(osu_file, 'rb').read()).hexdigest()
        b.BeatmapFileName = os.path.basename(osu_file)
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
                    b.TimingPoints.append({
                        'bpm': float(point[1]),
                        'offset': float(point[0]),
                        'timing_change': (float(point[1]) > 0)
                    })

                if parsing_hitobjects:
                    if line == "":
                        continue
                    hit_object = line.split(",")
                    b.Length = int(hit_object[2])
                    hit_object = HitObject(line)
                    b.Circles += 1 if hit_object.is_circle else 0
                    b.Sliders += 1 if hit_object.is_slider else 0
                    b.Spinners += 1 if hit_object.is_spinner else 0

                if line.startswith("AudioFilename"):
                    b.AudioFileName = parse_value(line)
                    continue
                if line.startswith("PreviewTime"):
                    b.PreviewTime = int(parse_value(line))
                    continue
                if line.startswith("StackLeniency"):
                    b.StackLeniency = float(parse_value(line))
                    continue
                if line.startswith("Mode"):
                    b.GameMode = int(parse_value(line))
                    continue
                if line.startswith("Title"):
                    b.Title = parse_value(line)
                    continue
                if line.startswith("TitleUnicode"):
                    b.TitleUnicode = parse_value(line)
                    continue
                if line.startswith("Artist"):
                    b.Artist = parse_value(line)
                    continue
                if line.startswith("ArtistUnicode"):
                    b.ArtistUnicode = parse_value(line)
                    continue
                if line.startswith("Creator"):
                    b.Creator = parse_value(line)
                    continue
                if line.startswith("Version"):
                    b.Version = parse_value(line)
                    continue
                if line.startswith("Source"):
                    b.Source = parse_value(line)
                    continue
                if line.startswith("Tags"):
                    b.Tags = parse_value(line)
                    continue
                if line.startswith("BeatmapID"):
                    b.BeatmapID = int(parse_value(line))
                    continue
                if line.startswith("BeatmapSetID"):
                    b.BeatmapSetID = int(parse_value(line))
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
        beatmap.Artist = reader.read_string()
        beatmap.ArtistUnicode = reader.read_string()
        beatmap.Title = reader.read_string()
        beatmap.TitleUnicode = reader.read_string()
        beatmap.Creator = reader.read_string()
        beatmap.Version = reader.read_string()
        beatmap.AudioFileName = reader.read_string()

        beatmap.BeatmapChecksum = reader.read_string()
        beatmap.BeatmapFileName = reader.read_string()
        beatmap.RankedStatus = reader.read_boolean()
        beatmap.Circles = reader.read_int16()
        beatmap.Sliders = reader.read_int16()
        beatmap.Spinners = reader.read_int16()
        beatmap.Modified = reader.read_ticks()
        beatmap.AR = reader.read_float32()
        beatmap.CS = reader.read_float32()
        beatmap.HP = reader.read_float32()
        beatmap.OD = reader.read_float32()
        beatmap.SliderMultiplier = reader.read_float64()
        beatmap.starRatings = [reader.read_dictionary() for x in range(0, 4)]
        beatmap.DrainTimeSeconds = reader.read_int32()
        beatmap.Length = reader.read_int32()
        beatmap.PreviewTime = reader.read_int32()
        beatmap.TimingPoints = reader.read_timing_points()
        beatmap.BeatmapID = reader.read_int32()
        beatmap.BeatmapSetID = reader.read_int32()
        beatmap.TopicId = reader.read_int32()
        beatmap.ranks = [reader.read_byte() for x in range (0,4)]
        beatmap.Offset = reader.read_int16()
        beatmap.StackLeniency = reader.read_float32()
        beatmap.GameMode = reader.read_byte()
        beatmap.Source = reader.read_string()
        beatmap.Tags = reader.read_string()
        beatmap.OffsetOnline = reader.read_int16()
        beatmap.TitleFont = reader.read_string()
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
