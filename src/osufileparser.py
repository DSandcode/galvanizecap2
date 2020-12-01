import re
from collections import defaultdict
from itertools import zip_longest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats


def convert_osufile(file):

    osufile_txt = open(file, "r")
    read_osu = osufile_txt.read()
    read_osu = (
        read_osu[: read_osu.find("[Colours]") - 1]
        + read_osu[read_osu.find("[Colours]") :]
    )
    sections = read_osu[:-1].split("\n\n")

    r_dict = {}

    time_keys = [
        "time",
        "beatlength",
        "meter",
        "sampleset",
        "sampleindex",
        "volume",
        "uninherited",
        "effects",
    ]
    hit_keys = ["x", "y", "time", "type", "hitsound", "hitsample", "objectparams"]

    col_lst = ["general", "editor", "metadata", "difficulty", "colours"]
    dataframe_lst = ["timingpoints", "hitobjects"]
    for sect in sections:

        sect_lst = sect.split("\n")
        key = ((sect_lst[0].replace("[", "")).replace("]", "")).lower()

        r_dict[key] = (
            {}
            if key in col_lst
            else []
            if key == "events"
            else {}
            if key in dataframe_lst
            else None
        )

        if key == "timingpoints":
            for timei in time_keys:
                r_dict[key][timei] = []

        if key == "hitobjects":
            for hiti in hit_keys:
                r_dict[key][hiti] = []

        for i, line in enumerate(sect_lst):

            if i == 0:
                continue

            if key in col_lst:

                split = line.split(":")
                s_key = (split[0].strip()).lower()

                if s_key == "bookmarks":
                    r_dict[key][s_key] = [int(x) for x in (split[1].strip()).split(",")]

                elif key == "colours":
                    r_dict[key][s_key] = [int(x) for x in (split[1].strip()).split(",")]

                else:
                    try:
                        r_dict[key][s_key] = int(split[1].strip())
                    except:
                        try:
                            r_dict[key][s_key] = float(split[1].strip())
                        except:
                            r_dict[key][s_key] = split[1].strip()

            if key == "events":
                r_dict[key].append(line)

            if key == "timingpoints":

                for t_info, t_key in zip(line.split(","), time_keys):

                    if t_key in [
                        "time",
                        "meter",
                        "sampleset",
                        "sampleindex",
                        "volume",
                        "uninherited",
                        "effects",
                    ]:
                        r_dict[key][t_key].append(int(t_info))
                    else:
                        r_dict[key][t_key].append(float(t_info))

            if key == "hitobjects":

                h_split = line.split(",")
                h_split.insert(5, h_split[-1])
                h_split.pop()
                type = 0

                for h_info, h_key in zip_longest(h_split, hit_keys):

                    if h_key in ["x", "y", "time", "type", "hitsound"]:
                        r_dict[key][h_key].append(int(h_info))
                        if h_key == "type":
                            type = int(h_info)

                    if h_key == "objectparams":
                        print(h_info, h_key, type)
                        if type == 0:
                            r_dict[key][h_key].append(0)

                    if h_key == "hitsample":

                        samp_key = [
                            "normalset",
                            "additionset",
                            "index",
                            "volume",
                            "filename",
                        ]

                        hit_dict = dict.fromkeys(samp_key, 0)

                        for samp, sa_key in zip(h_info.split(":"), samp_key):
                            if sa_key == "filename":
                                hit_dict[sa_key] = samp
                            else:
                                hit_dict[sa_key] = int(samp)
                        r_dict[key][h_key].append(hit_dict)

    for aaaaa in r_dict["hitobjects"]:
        print(len(r_dict["hitobjects"][aaaaa]))
    # for df_key in dataframe_lst:
    #     r_dict[df_key] = pd.DataFrame(r_dict[df_key])

    return r_dict


if __name__ == "__main__":
    file = "data/songs_osu_files/1272018/BUMP OF CHICKEN - Acacia (Sotarks) [Basen's Normal].osu"
    osu_data = convert_osufile(file)
    # print(osu_data)
