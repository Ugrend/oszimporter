__author__ = 'Ugrend'

from datetime import datetime
from reader import Reader

class Beatmap:

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
    StarRating: list
    DrainTimeSeconds: int
    Length: int
    PreviewTime: int
    TimingPoints: list
    BeatmapID: int
    BeatmapSetID: int
    ranks: list
    Offset: int
    StackLeniency: int
    GameMode: int
    Source: str
    Tags: str
    OffsetOnline: int
    TitleFont: str
    not_played: bool
    last_played: datetime
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



    @staticmethod
    def from_reader(reader: Reader):
        beatmap = Beatmap()
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
        beatmap.AR = reader.read_float_single()
        beatmap.CS = reader.read_float_single()
        beatmap.HP = reader.read_float_single()
        beatmap.OD = reader.read_float_single()
        beatmap.SliderVelocity = reader.read_float_double()
        beatmap.StarRating = [reader.read_dictionary() for x in range(0,4)]
        beatmap.DrainTimeSeconds = reader.read_int32()
        beatmap.Length = reader.read_int32()
        beatmap.PreviewTime = reader.read_int32()
        beatmap.TimingPoints = reader.read_timing_points()
        beatmap.BeatmapID = reader.read_int32()
        beatmap.BeatmapSetID = reader.read_int32()
        beatmap.TopicId = reader.read_int32()
        beatmap.ranks = [reader.read_byte() for x in range (0,4)]
        beatmap.Offset = reader.read_int16()
        beatmap.StackLeniency = reader.read_float_single()
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