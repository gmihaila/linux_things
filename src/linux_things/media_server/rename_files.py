"""
Need to rename and structure files in the following order:

/TV Shows
  /My Show
    /Season 01
      My Show - s01e01.format
      My Show - s01e02-03.format

Run:


python src/linux_things/media_server/rename_files.py --show_name 'My Show' --target_path 'where to move' --use_path 'where is the show' --dry_run

"""

import os
import re
import argparse
import warnings
from utils import move_folder


def main():
    parser = argparse.ArgumentParser(description='Description')
    parser.add_argument('--show_name', help='Name of the TV Show.', type=str)
    parser.add_argument('--target_path', help='Where to move the renamed files.', type=str)
    parser.add_argument('--use_path', help='Where to find the files that need to be renamed.', type=str)
    parser.add_argument('--dry_run', help='Perform dry run before moving files.', default=False, action='store_true')

    # parse arguments
    args = parser.parse_args()
    print(args)

    # Add show name to target path
    target_path = os.path.join(args.target_path, args.show_name)
    os.mkdir(target_path) if not os.path.isdir(target_path) else print(
        f"Folder '{args.show_name}' already exists in '{target_path}'")

    # Deal with each season.
    folder_content = os.listdir(args.use_path)
    # Keep only folders and not files.
    all_folders = [folder for folder in folder_content if os.path.isdir(os.path.join(args.use_path, folder))]

    for folder in all_folders:
        folder_path = os.path.join(args.use_path, folder)

        season = re.search('[sS]\d{1,2}', folder_path).group()
        season = re.sub('[sS]', '', season).lstrip('0')
        season = f'0{season}' if len(season) < 2 else season

        print(f"For season '{season}'")

        addon_target_path = f'Season {season}'
        seaon_target_path = os.path.join(target_path, addon_target_path)
        os.mkdir(seaon_target_path) if not os.path.isdir(seaon_target_path) else print(
            f"Folder '{addon_target_path}' already existst in '{target_path}'")
        files = os.listdir(folder_path)
        # import pdb; pdb.set_trace()
        move_folder(files, args.show_name, season, folder_path, seaon_target_path, args.dry_run)

        if args.dry_run:
            warnings.warn("This was a dry run! No files were moved yer! Don't use --dry_run in order to move files!",
                          Warning)


if __name__ == '__main__':
    main()
