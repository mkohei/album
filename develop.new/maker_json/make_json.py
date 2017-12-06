# -*- coding: utf-8 -*-

"""
# 処理概要
* 'images/'内画像
    - thumbnail
    - resize
    - .setting.json
* Memo
    - SETTING周りの処理メモ
        + JSONに存在していない画像名を追加分とする
        + 画像それぞれにID付与(入力順で同時は撮影時刻順)
        + 追加分のid, exif取得 & JSON追加
        + JSON撮影時刻ソート
    - SETTING.JSON構造
        [
            {
                "id" : id,
                "Y" : year,
                "m" : month,
                "d" : day,
                "H" : hour,
                "M" : minute,
                "S" : second,
                "is360v" : [0,1]
            }
        ]
* TODO
    - [ ] 画像ファイルの認識を正規表現に
"""

import os                       # 画像ファイル取得
#import glob                    # 画像ファイルパス取得
from PIL import Image           # 画像リサイズ
from PIL.ExifTags import TAGS   # EXIFデータ取得
from datetime import datetime   # 日付操作
from tqdm import tqdm           # 進捗バー
import numpy as np              # argsort
import sys                      # command line arguments
import shutil                   # deepcopy
import json                     # json



###############################
########## CONSTANTS ##########
###############################
# 画像ファイルとして認識する拡張子
IMG_EXTS = ['.JPG', '.jpg', '.PNG', '.png']
# リサイズ後画像サイズの最大辺長
MAX_RESIZE_LEN = 980
# サムネイル用画像サイズ
THUMB_LEN = 300
# 画像保存ディレクトリ名
IMG_DIR = 'images'
# リサイズ画像出力先ディレクトリ名
RSZ_DIR = 'images_resize'
# サムネ用画像出力先ディレクトリ名
THUMB_DIR = 'images_thumb'
# 360viewerページ出力先ディレクトリ名
VIEWER360_DIR = 'viewer360'
# 設定ファイル名
SETTING = "setting.json"
# EXIFデータID
EXIF_MODEL = 272
EXIF_ORIENTATION = 274
EXIF_DATETIME = 306



###################################
########## MAIN FUNCTION ##########
###################################
def main():
    ### save path (from command line arguments)
    savepath = get_save_path()

    ### directory path
    img_path   = savepath + IMG_DIR
    rsz_path   = savepath + RSZ_DIR
    thumb_path = savepath + THUMB_DIR

    ### get img file (name)
    files = get_files(img_path)

    ### load SETTING
    set_json = load_set_json(savepath)

    ### remake SETTING
    set_json = remake_set_json(img_path, files, set_json)

    ### rename addings
    rename_addings(img_path, set_json)

    ### save SETTING
    svae_setting(savepath, set_json)

    ### image processing
    # comfirm to directory existing
    exists_paths([rsz_path, thumb_path])
    # get img file again (because of rename)
    files = get_files(img_path)
    # exec
    image_processing(files, img_path, rsz_path, thumb_path)




###############################
########## FUNCTIONS ##########
###############################
# 保存先ディレクトリの取得(from command line arguments)
def get_save_path():
    path = "."
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            path = sys.argv[1]
    return path + "/"


# ディレクトリ存在確認(無ければ作成)
def exists_paths(dir_array):
    for d in dir_array:
        if not os.path.exists(d):
            os.mkdir(d)


# 画像ファイルの取得
def get_files(filepath):
    try:
        files = os.listdir(filepath)
        files = [f for f in files if f[-4:] in IMG_EXTS]
        return files
    except FileNotFoundError:
        print("There is no 'images' directory!!!")
        sys.exit(0)


# 画像出力
def image_processing(files, img_dir, rsz_dir, thumb_dir):
    rfiles = os.listdir(rsz_dir)
    tfiles = os.listdir(thumb_dir)

    pbar = tqdm(files)
    for file in pbar:
        pbar.set_description("image processing")
        # load
        img = Image.open(img_dir + "/" + file)
        # resize
        if file not in rfiles:
            resize(img, rsz_dir + "/" + file)
        # thumbnail
        if file not in tfiles:
            thumbnail(img, thumb_dir + "/" + file)


# resize
def resize(img, outname, LEN=MAX_RESIZE_LEN, a=0):
    if a==0:
        r = LEN / max(img.width, img.height)
    else:
        r = LEN / min(img.width, img.height)
    # resize
    img_rsz = img.resize((int(img.width*r), int(img.height*r)), Image.LANCZOS)
    # orientation
    orientation = img._getexif()[EXIF_ORIENTATION]
    img_rsz = convert_image[orientation](img_rsz)
    # save
    if outname is not None:
        img_rsz.save(outname)
    return img_rsz


# thumbnail
def thumbnail(img, outname, LEN=THUMB_LEN):
    # resize
    rsz = resize(img, None, LEN=THUMB_LEN, a=1)
    # 正方形化
    if rsz.width > rsz.height:
        s = int(rsz.width//2 - LEN//2)
        box = (s, 0, s+LEN, rsz.height)
    elif rsz.width < rsz.height:
        s = int(rsz.height//2 - LEN//2)
        box = (0, s, rsz.width, s+LEN)
    else:
        box = (0, 0, rsz.width, rsz.height)
    thumb = rsz.crop(box)
    # save
    if outname is not None:
        thumb.save(outname)
    return thumb


# rotate
convert_image = {
    # そのまま
    1: lambda img: img,
    # 左右反転
    2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    # 180度回転
    3: lambda img: img.transpose(Image.ROTATE_180),
    # 上下反転
    4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    # 左右反転＆反時計回りに90度回転
    5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90),
    # 反時計回りに270度回転
    6: lambda img: img.transpose(Image.ROTATE_270),
    # 左右反転＆反時計回りに270度回転
    7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270), 
    # 反時計回りに90度回転
    8: lambda img: img.transpose(Image.ROTATE_90),
}


# load .setting.json
def load_set_json(path):
    path_json = path + SETTING
    if os.path.exists(path_json):
        f = open(path_json)
        data = json.load(f)
        f.close()
        return data
    else:
        return []


# remake SETTING
def remake_set_json(path, files, set_json):
    ### 追加画像(名)の取得
    addings = get_adding_img(files, set_json)
    # 画像データの取得
    data_dicts = get_data_dicts(path, files)
    # 画像データからID取得 % set_json追加
    add_set_json(data_dicts, set_json)
    # 作成時刻順にソート
    set_json = sort_by_datetime(set_json)

    return set_json



# 追加画像(名)の取得
def get_adding_img(files, set_json):
    addings = []
    added = [i["id"] for i in set_json]
    for file in files:
        if file[:-4] not in added:
            addings.append(file)
    return addings


# get_exif_set
def get_data_dicts(path, addings):
    data_dicts = []
    for file in addings:
        # 準備
        data = {"name" : file}
        # load exif
        exif = Image.open(path + "/" + file)._getexif()
        # datetime
        dt = datetime.strptime(exif[EXIF_DATETIME][:19], '%Y:%m:%d %H:%M:%S')
        data['Y'] = dt.year
        data['m'] = dt.month
        data['d'] = dt.day
        data['H'] = dt.hour
        data['M'] = dt.minute
        data['S'] = dt.second
        # model
        model = del_tail_space(exif[EXIF_MODEL])
        data['model'] = model
        # is 360v
        data['is360v'] = int(is_360v(model))
        # append
        data_dicts.append(data)
    return data_dicts


def is_360v(model):
    return "THETA" in model


# add .setting.json
def add_set_json(data_dicts, set_json):
    for data in data_dicts:
        ## idの取得
        # date_str
        y_str = "%04d" % (data['Y'])
        # count
        cnt = sum([i["id"][:4]==y_str for i in set_json])
        ## add
        # id追加
        data["id"] = y_str + "%04d" % cnt
        # add
        set_json.append(data)
    return set_json


# sort by datetime
def sort_by_datetime(set_json):
    return sorted(set_json, key=lambda i: datetime(i['Y'], i['m'], i['d'], i['H'], i['M'], i['S']), reverse=True)


# 画像のrename
def rename_addings(path, set_json):
    for data in set_json:
        if "name" in data:
            # rename
            os.rename(path+"/"+data["name"], path+"/"+data["id"] + data["name"][-4:])
            # name削除
            del data["name"]


# SETTINGの保存
def svae_setting(path, set_json):
    f = open(path + "/" + SETTING, 'w')
    json.dump(set_json, f)
    f.close()


def del_tail_space(s):
    while s[-1] == ' ':
        s = s[:-1]
    return s



###########################
########### MAIN ##########
###########################
if __name__ == '__main__':
    main()
