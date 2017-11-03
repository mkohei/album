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
# サムネイル用画像サイズ
THUMB_LEN = 200
# 画像保存ディレクトリ名
IMG_DIR = 'images'
# リサイズ画像出力先ディレクトリ名
RSZ_DIR = 'images_resize'
# サムネ用画像出力先ディレクトリ名
THUMB_DIR = 'images_thumb'
# 360viewerページ出力先ディレクトリ名
VIEWER360_DIR = 'viewer360'
# EXIFデータID
EXIF_MODEL = 272
EXIF_ORIENTATION = 274
EXIF_DATETIME = 306



###################################
########## MAIN FUNCTION ##########
###################################
def main():
    ### 画像ファイルパス取得
    files = os.listdir(IMG_DIR)
    # 指定した拡張子(後ろから4文字)以外除外
    files = [f for f in files if f[-4:] in IMG_EXTS]

    ### 画像の読み込みと処理
    ## 出力先ディレクトリの存在確認
    # リサイズ
    if not os.path.exists(RSZ_DIR):
        os.mkdir(RSZ_DIR)
    # サムネイル
    if not os.path.exists(THUMB_DIR):
        os.mkdir(THUMB_DIR)
    # 360viewer
    if not os.path.exists(VIEWER360_DIR):
        os.mkdir(VIEWER360_DIR)
    ## 出力先ディレクトリのファイル取得
    rfiles = os.listdir(RSZ_DIR)
    tfiles = os.listdir(THUMB_DIR)
    vfiles = os.listdir(VIEWER360_DIR)
    ## 画像処理
    models, datetimes = [], []
    pbar = tqdm(files)
    for file in pbar:
        pbar.set_description("image processing")
        # 読込
        img = Image.open(IMG_DIR + "/" + file)
        # resize
        if file not in rfiles: # リサイズ済ならスルー
            resize(img, RSZ_DIR + "/" + file)
        # thumbnail
        if file not in tfiles: # サムネイル用画像作成済ならスルー
            thumbnail(img, THUMB_DIR + "/" + file)
        # EXIF情報の読込(model, datetime)
        exif = get_exif(IMG_DIR + "/" + file)
        models = np.append(models, exif[EXIF_MODEL])
        datetimes = np.append(datetimes, datetime.strptime(exif[EXIF_DATETIME], '%Y:%m:%d %H:%M:%S'))

    # 撮影時刻によるソート(降順)
    x = np.argsort(datetimes)[::-1]
    models, datetimes, files = models[x], datetimes[x], np.array(files)[x]

    ### HTMLコード生成
    blocks, items, dt_prev, cnt = "", "", None, 0
    for file, dt, model in zip(files, datetimes, models):
        dt_str = dt.strftime('%Y / %m / %d')
        img_id = get_id(dt, cnt)
        cnt += 1
        # 日付ブロック分け
        if (dt_prev is not None) and (dt_prev != dt_str):
            blocks += html.HTML_BLOCK % (dt_prev, items)
            items = ""
            cnt = 0
        dt_prev = dt_str
        ## 360viewer?
        eye = "" # 360viewew
        if is_360img(model):
            # 360viewer作成
            if file not in vfiles:
                make_360viewer_page(img_id, "../"+IMG_DIR, VIEWER360_DIR, file)
            # 360viewer link
            eye = html.HTML_360VIEWER % (VIEWER360_DIR, img_id + ".html")
        # list追加
        items += html.HTML_ITEM % (RSZ_DIR, file, THUMB_DIR, file, IMG_DIR, file, img_id, eye)
    blocks += html.HTML_BLOCK % (dt_str, items)
    html_code = html.HTML % (html.HTML_HEAD + html.HTML_BODY % blocks)

    ### ファイル作成 & 書き込み
    fd = open('index.html', 'w')
    fd.write(html_code)
    fd.close()



###############################
########## FUNCTIONS ##########
###############################
# resize
def resize(img, outname, LEN=MAX_RESIZE_LEN, a=0):
    """ 画像のリサイズ

        Parameters
        ----------
        * img : 画像データ(PIL.Image)
        * outname : リサイズ後画像の出力名

        Returns
        -------
        * リサイズ後の画像(PIL.Image)
    """
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
    """ サムネイル用画像の作成(正方形)

        Parameters
        ----------
        * img : 画像データ(PIL.Image)
        * outname : サムネイル用画像の出力名

        Returns
        -------
        * サムネイル用画像(PIL.Image)
    """
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


# get_exif
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


# is 360img
def is_360img(model):
    """ 画像(EXIF)情報から360度画像かどうかを判定
        * modelにTHETAが入っていたら(THETAで取られた画像であれば)...

        Parameters
        ----------
        * model : 撮影機材(モデル)

        Returns
        ------
        * is360img : 360度画像
    """
    return "THETA" in model


# make 360viewer page
def make_360viewer_page(title, indir, outdir, file):
    """ 360viewer pageの作成

        Parameters
        ----------
        * title : page title
        * indir : 表示画像保存先ディレクトリ
        * outdir : page出力先ディレクトリ
        * file : 表示画像名

        Returns
        -------
        * void
    """
    fd = open(outdir + "/" + title + ".html", 'w')
    fd.write(html.HTML_360VIEWER_PAGE % (title, indir, file))
    fd.close()


# id
def get_id(datetime, cnt):
    return datetime.strftime('%Y%m%d') + '%03d' % cnt


###########################
########### MAIN ##########
###########################
if __name__ == '__main__':
    main()
