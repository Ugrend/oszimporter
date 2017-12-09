from argparse import ArgumentParser
import zipfile
import os
from database import Database
from beatmap import Beatmap
from typing import List
import traceback


def extract_zip(file_path, destination)->str:
    folder_name = os.path.splitext(os.path.basename(file_path))[0]
    extract_to = os.path.join(destination, folder_name)
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(file_path, 'r') as zf:
        zf.extractall(extract_to)
    return extract_to


def process_osu_files(map_dir)->List[Beatmap]:
    folder_name = os.path.basename(map_dir)
    map_files = [os.path.join(map_dir, f) for f in os.listdir(map_dir) if f.endswith('.osu')]
    beatmaps = []
    for map_file in map_files:
        beatmap = Beatmap.from_osu_file(map_file, folder_name)
        beatmaps.append(beatmap)
    return beatmaps


def import_osz(osz_file, destination, database:Database):
    extract_path = extract_zip(osz_file, destination)
    database.add_set(process_osu_files(extract_path))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-d', "--database", dest="database", type=str, help="path to osu!.db")
    parser.add_argument('-e', "--extract_path", dest="extract_path", type=str, help="where to extract files to")
    parser.add_argument('osz_files', metavar='.osz', nargs="+", type=str, help='osz file(s) to import')
    args = parser.parse_args()
    database = Database.load(args.database)
    for osz in args.osz_files:
        try:
            import_osz(osz, args.extract_path, database)
        except:
            traceback.print_exc()
    database.save(args.database)
