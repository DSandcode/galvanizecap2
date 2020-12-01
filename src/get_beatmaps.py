import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import urllib.request, json
import requests
import zipfile
import glob, os, shutil


def get_user_beatmaps(userid):
    r_data = []
    s_len = 1
    while s_len != len(r_data):
        s_len = len(r_data)
        with urllib.request.urlopen(
            f"https://osu.ppy.sh/users/{userid}/beatmapsets/ranked_and_approved?offset={len(r_data)}&limit=51"
        ) as url:
            r_data.extend(json.loads(url.read().decode()))
    return r_data


def store_mapids(userid, beatmaps_json):
    np.save(f"data/mapids/{userid}.npy", np.array([i["id"] for i in beatmaps_json]))


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def unzip(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)


def move_osu_files(source_dir, dest_dir):
    os.mkdir(dest_dir)
    files = glob.iglob(os.path.join(source_dir, "*.osu"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, dest_dir)


if __name__ == "__main__":
    userid = "4452992"
    beatmaps_json = get_user_beatmaps(userid)

    # store_mapids(userid, beatmaps_json)

    # download_url("https://bloodcat.com/osu/s/1272018", "data/osz/1272018.osz")

    # https://bloodcat.com/osu/s/1272018

    # unzip("data/osz/1272018.osz", "data/unzipped_osz/1272018")

    # move_osu_files("data/unzipped_osz/1272018", "data/songs_osu_files/1272018")

