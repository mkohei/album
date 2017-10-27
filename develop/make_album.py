# -*- coding: utf-8 -*-
"""
# 処理概要
1. 'images/'ディレクトリ内の指定拡張子を画像ファイルとして取得
2. 'images_resize/'ディレクトリ内にリサイズした画像ファイルを保存
3. HTMLコード生成・作成
4. その他必要ファイル(.js, .css, etc...)をコピー(作成)
"""

import os                       # 画像ファイル取得
#import glob                    # 画像ファイルパス取得
from PIL import Image           # 画像リサイズ
from PIL.ExifTags import TAGS   # EXIFデータ取得
from datetime import datetime   # 日付操作
from tqdm import tqdm           # 進捗バー
import numpy as np              # argsort
import album_html as html       # HTMLコード定数

###############################
########## CONSTANTS ##########
###############################
# 画像ファイルとして認識する拡張子
IMG_EXTS = ['.JPG', '.jpg', '.PNG', '.png']
# リサイズ後画像サイズの最大辺長
MAX_RESIZE_LEN = 980
# 画像保存ディレクトリ名
IMG_DIR = 'images'
# リサイズ画像出力先ディレクトリ名
RSZ_DIR = 'images_resize'
# EXIFデータID
EXIF_MODEL = 272
EXIF_DATETIME = 306



###################################
########## MAIN FUNCTION ##########
###################################
def main():
    ### 画像ファイルパス取得
    files = os.listdir(IMG_DIR)
    # 指定した拡張子(後ろから4文字)以外除外
    files = [f for f in files if f[-4:] in IMG_EXTS]

    ### 画像のリサイズ
    # リサイズ画像出力先ディレクトリの存在確認
    if not os.path.exists(RSZ_DIR):
        os.mkdir(RSZ_DIR)
    rfiles = os.listdir(RSZ_DIR)
    # リサイズ処理
    target = [f for f in files if f not in rfiles] # リサイズ済の除外
    pbar = tqdm(target)
    for file in pbar:
        pbar.set_description("resizing")
        resize(file, IMG_DIR, RSZ_DIR)

    ### EXIF情報を利用
    # モデル, 撮影時刻の取得
    models, datetimes = np.array([]), np.array([])
    for file in files:
        exif = get_exif(IMG_DIR + "/" + file)
        models = np.append(models, exif[EXIF_MODEL])
        datetimes = np.append(datetimes, datetime.strptime(exif[EXIF_DATETIME], '%Y:%m:%d %H:%M:%S'))
    # 撮影時刻によるソート(降順)
    x = np.argsort(datetimes)[::-1]
    models, datetimes, files = models[x], datetimes[x], np.array(files)[x]

    ### HTMLコード生成
    items = ""
    for file, dt, model in zip(files, datetimes, models):
        dt_str = dt.strftime('%Y / %m / %d')
        items += html.HTML_ITEM % (RSZ_DIR, file, RSZ_DIR, file, dt_str)
    html_code = html.HTML % (html.HTML_HEAD + html.HTML_BODY % items)

    ### ファイル作成 & 書き込み
    fd = open('index.html', 'w')
    fd.write(html_code)
    fd.close()



###############################
########## FUNCTIONS ##########
###############################
def resize(file, indir, outdir):
    """ 画像のリサイズ
        (微妙だけど)EXIFデータを返す

        Parameters
        ----------
        * file : 画像ファイル名
        * indir : リサイズ元画像があるディレクトリへのパス
        * outdir : リサイズ後画像の出力先ディレクトリへのパス

        Returns
        -------
        * void
    """
    img = Image.open(indir + "/" + file)
    r = MAX_RESIZE_LEN / max(img.width, img.height)
    img_rsz = img.resize((int(img.width*r), int(img.height*r)), Image.LANCZOS)
    img_rsz.save(outdir + "/" + file)


def get_exif(filepath):
    """ EIXFデータの取得

        Parameteres
        -----------
        * filepath : 画像ファイルパス

        Returns
        -------
        * exif : 画像のEXIFデータ
    """
    return Image.open(filepath)._getexif()


###########################
########### MAIN ##########
###########################
if __name__ == '__main__':
    main()
