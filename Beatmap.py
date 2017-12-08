__author__ = 'Ugrend'

from datetime import datetime
from reader import Reader
from writer import  Writer
from io import BytesIO

class Beatmap:

    data_length: int
    Artist: str
    ArtistUnicode: str
    Title: str
    TitleUnicode: str
    Creator: str
    Version: str
    AudioFileName: str
    BeatmapChecksum: str
    BeatmapFileName: str
    RankedStatus: bool
    Circles: int
    Sliders: int
    Spinners: int
    Modified: int
    AR: int
    CS: int
    HP: int
    OD: int
    SliderVelocity: int
    starRatings: list
    DrainTimeSeconds: int
    Length: int
    PreviewTime: int
    TimingPoints: list
    BeatmapID: int
    BeatmapSetID: int
    TopicId: int
    ranks: list
    Offset: int
    StackLeniency: int
    GameMode: int
    Source: str
    Tags: str
    OffsetOnline: int
    TitleFont: str
    not_played: bool
    last_played: int
    osz2: bool
    folder_name: str
    last_checked_osu: int
    ignore_beatmap_sounds: bool
    ignore_beatmap_skin: bool
    disable_story_board: bool
    disable_video: bool
    visual_override: bool
    edited: int
    mania_scroll_speed: int

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
        w.write_float64(self.SliderVelocity)

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
    def from_reader(reader: Reader):
        beatmap = Beatmap()
        beatmap.data_length = reader.read_int32()
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
        beatmap.SliderVelocity = reader.read_float64()
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
