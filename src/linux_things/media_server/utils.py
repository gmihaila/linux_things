import os
import re
import warnings
import shutil

ALLOWED_FORMATS = ['mkv', 'srt', 'avi']

REG_EXP = '[sS.]?(\d){1,2}[eE.xX]?(\d){1,2}'


def move_folder(files, show_name, use_season, use_path, target_path_, dry_run):
    for file_ in files:
        if os.path.isdir(os.path.join(use_path, file_)):
            # Each file is in a folder.
            for actual_file in os.listdir(os.path.join(use_path, file_)):
                format_ = actual_file.split('.')[-1]
                if format_ in ALLOWED_FORMATS:
                    get_paths(actual_file, show_name, use_season, format_, target_path_,
                              os.path.join(use_path, file_, dry_run))
                else:
                    warnings.warn(f"Format '{format_}' not found in '{ALLOWED_FORMATS}'", Warning)

        else:
            format_ = file_.split('.')[-1]
            if format_ in ALLOWED_FORMATS:
                get_paths(file_, show_name, use_season, format_, target_path_, use_path, dry_run)
            else:
                warnings.warn(f"Format '{format_}' not found in '{ALLOWED_FORMATS}'", Warning)


def get_paths(use_file, show_name, use_season, format_, target_path_, use_path, dry_run):
    # print(file_)
    season_episode = re.search(REG_EXP, use_file).group()
    season_episode = re.sub("[^0-9]", "", season_episode)  # .lstrip('0')
    if len(season_episode) == 3:
        season_ = f'0{season_episode[0]}'
    elif len(season_episode) == 4:
        season_ = season_episode[:2]
    else:
        raise ValueError(f"Value for season_episode '{season_episode}' not recognized!")

    if use_season != season_:
        raise ValueError(
            f"Value for season '{use_season}' should be same as season episode '{season_}' from {season_episode}")

    # assert season is season_episode[0:len(season)]
    episode = season_episode[len(use_season):].lstrip('0')
    episode = f'0{episode}' if len(episode) == 1 else episode
    new_name = f"{show_name} - s{use_season}e{episode}.{format_}"
    # print(new_name)
    current_file = os.path.join(use_path, use_file) if os.path.isdir(use_path) else use_path
    target_file = os.path.join(target_path_, new_name)
    shutil.move(current_file, target_file) if not dry_run else None

    print(f"File '{current_file}' was moved to '{target_file}'")
