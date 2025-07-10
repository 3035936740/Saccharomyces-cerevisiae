import os
import csv

import numpy as np
from xml.etree.cElementTree import parse

from .common import decode_b64, jis_2_utf, amend_jis
from update.data.__db_data import csv_data

from utli.dir import local_dir


# WHY USING SHIFT-JIS???!!!
def update_db(game_dir, map_size):
    mods_path = f"{os.path.dirname(game_dir)}/data_mods/_cache/others/music_db.xml"
    
    jis_path = game_dir + '/others/music_db.xml'
    
    is_mod_path = False
    
    if os.path.isfile(mods_path):
        jis_path = mods_path
        is_mod_path = True
    
    utf_path = local_dir + '/data/music_db.xml'

    # Set up music_db encoded with UTF-8
    jis_2_utf(jis_path, utf_path, is_mod_path)

    # Get music information from xml, then saved as npy file
    tree = parse(utf_path)
    root = tree.getroot()

    music_map = [[''] * 26 for _ in range(map_size)]

    for music in root.findall('music'):
        # 举例获取属性或子标签内容
        mid = music.get('id')  # 获取属性
        
        # info
        info = music.find('info')
        name = amend_jis(info.findtext('title_name'))  # 获取子标签内容
        name_yo = info.findtext('title_yomigana')
        artist = amend_jis(info.findtext("artist_name"))
        artist_yo = info.findtext("artist_yomigana")
        music_ascii = info.findtext("ascii").replace('_', ' ')
        bpm_max = int(info.findtext("bpm_max"))
        bpm_min = int(info.findtext("bpm_min"))
        date = int(info.findtext("distribution_date"))
        version = int(info.findtext("version"))
        inf_ver = int(info.findtext("inf_ver"))

        # level
        difficulty = music.find('difficulty')
        novice = difficulty.find('novice')
        nov_lv = int(novice.findtext("difnum"))
        nov_ill = amend_jis(novice.findtext("illustrator"))
        nov_eff = amend_jis(novice.findtext("effected_by"))
        advanced = difficulty.find('advanced')
        adv_lv = int(advanced.findtext("difnum"))
        adv_ill = amend_jis(advanced.findtext("illustrator"))
        adv_eff = amend_jis(advanced.findtext("effected_by"))
        exhaust = difficulty.find('exhaust')
        exh_lv = int(exhaust.findtext("difnum"))
        exh_ill = amend_jis(exhaust.findtext("illustrator"))
        exh_eff = amend_jis(exhaust.findtext("effected_by"))
        try:
            infinite = difficulty.find('infinite')
            if infinite is None:
                raise ValueError("infinite not found")
            inf_lv = int(infinite.findtext("difnum"))
            inf_ill = amend_jis(infinite.findtext("illustrator"))
            inf_eff = amend_jis(infinite.findtext("effected_by"))
        except Exception:
            inf_lv = 0
            inf_ill = 'dummy'
            inf_eff = 'dummy'
        try:
            maximum = difficulty.find('maximum')
            if maximum is None:
                raise ValueError("maximum not found")
            mxm_lv = int(maximum.findtext("difnum"))
            mxm_ill = amend_jis(maximum.findtext("illustrator"))
            mxm_eff = amend_jis(maximum.findtext("effected_by"))
        except Exception:
            mxm_lv = 0
            mxm_ill = 'dummy'
            mxm_eff = 'dummy'
        
        music_map[int(mid)] = [
                mid, name, name_yo, artist, artist_yo,
                bpm_max, bpm_min, date, version, inf_ver,
                nov_lv, nov_ill, nov_eff,
                adv_lv, adv_ill, adv_eff,
                exh_lv, exh_ill, exh_eff,
                inf_lv, inf_ill, inf_eff,
                mxm_lv, mxm_ill, mxm_eff,
                music_ascii
            ]
        
    """


    for index in range(map_size):
        try:
            # Fill up each line of level_table.npy
            mid = int(root[index].attrib['id'])
            name = amend_jis(root[index][0][1].text)
            name_yo = root[index][0][2].text
            artist = amend_jis(root[index][0][3].text)
            artist_yo = root[index][0][4].text
            music_ascii = root[index][0][5].text.replace('_', ' ')
            bpm_max = int(root[index][0][6].text)
            bpm_min = int(root[index][0][7].text)
            date = int(root[index][0][8].text)
            version = int(root[index][0][13].text)
            inf_ver = int(root[index][0][15].text)

            nov_lv = int(root[index][1][0][0].text)
            nov_ill = amend_jis(root[index][1][0][1].text)
            nov_eff = amend_jis(root[index][1][0][2].text)
            adv_lv = int(root[index][1][1][0].text)
            adv_ill = amend_jis(root[index][1][1][1].text)
            adv_eff = amend_jis(root[index][1][1][2].text)
            exh_lv = int(root[index][1][2][0].text)
            exh_ill = amend_jis(root[index][1][2][1].text)
            exh_eff = amend_jis(root[index][1][2][2].text)
            inf_lv = int(root[index][1][3][0].text)
            inf_ill = amend_jis(root[index][1][3][1].text)
            inf_eff = amend_jis(root[index][1][3][2].text)
            try:
                mxm_lv = int(root[index][1][4][0].text)
                mxm_ill = amend_jis(root[index][1][4][1].text)
                mxm_eff = amend_jis(root[index][1][4][2].text)
            except IndexError:
                mxm_lv = 0
                mxm_ill = 'dummy'
                mxm_eff = 'dummy'
            music_map[int(mid)] = [
                mid, name, name_yo, artist, artist_yo,
                bpm_max, bpm_min, date, version, inf_ver,
                nov_lv, nov_ill, nov_eff,
                adv_lv, adv_ill, adv_eff,
                exh_lv, exh_ill, exh_eff,
                inf_lv, inf_ill, inf_eff,
                mxm_lv, mxm_ill, mxm_eff,
                music_ascii
            ]

        except IndexError:
            break
    """

    # Save level table
    try:
        os.remove(utf_path)
    except FileNotFoundError:
        pass
    music_map = np.array(music_map)
    np.save(local_dir + '/data/level_table.npy', music_map)

    # Decompress csv data from __db_data.py
    csv_path = local_dir + '/data/raw_search_db.csv'
    decode_b64(csv_data, csv_path)

    temp_list = []
    search_csv = csv.reader(open(local_dir + '/data/raw_search_db.csv', encoding='utf-8'))
    __index = 0
    for csv_record in search_csv:
        temp_list.append(' '.join(csv_record))

    # Set up search database
    search_list = [' ' for _ in range(map_size)]
    search_list[:len(temp_list)] = temp_list
    for index in range(map_size):
        if search_list[index][0] == ' ':
            search_list[index] = ' '.join(_get_raw_search_record(music_map[index]))

    # Save search database
    search_list = np.array(search_list)
    np.save(local_dir + '/data/search_db.npy', search_list)


def _get_raw_search_record(_record) -> list:
    mid = _record[0]
    name = _record[1]
    artist = _record[3]
    music_ascii = _record[25]
    return [mid, name, artist, music_ascii]
