# -*- coding: utf-8 -*-

###############################
########## CONSTANTS ##########
###############################
"""
* HTML % (HTML_HEAD + HTML_BODY)
* HTML_BODY % HTML_BLOCK(s)
* HTML_BLOCK % (date, HTML_ITEM(s))
* HTML_ITEM % (dir[resize], img, dir[thumbnail], img, dir[origin], img, download_name, HTML_360VIEWER or blank)
* HTML_360VIEWER % (dir[360view], file.html)

* HTML_360VIEWER_PAGE % (title, dir[origin], file)
"""

###############################
########## VARIABLES ##########
###############################
date_list = []
items_list = []

###############################
########## FUNCTIONS ##########
###############################
def clear():
    """ 状態初期化 """
    date_list.clear()
    items_list.clear()

def set_title(newtitle):
    title = newtitle

def add_block(date):
    """ ブロックの追加 """
    date_list.append(date)
    items_list.append("")

def add_item(thumb_dir, view_dir, download_dir, view360_dir, file, img_id):
    """ アイテムの追加 """
    a = ""
    if view360_dir is not None:
        a = HTML_360VIEWER % (view360_dir, file)
    items_list[-1] += HTML_ITEM % (view_dir, file, thumb_dir, file, download_dir, file, img_id, a)

def get(title=""):
    """ カスタムしたHTMLコードの取得 """
    blocks = ""
    for date, items in zip(date_list, items_list):
        blocks += HTML_BLOCK % (date, items)
    return HTML % (HTML_HEAD + HTML_BODY % blocks)


###############################
########## CONSTANTS ##########
###############################
HTML = """
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="no-js">
<!--<![endif]-->

%s

</html>
"""

HTML_HEAD = """
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>KRLAB ALBUM</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Free HTML5 Template by FREEHTML5.CO" />
    <meta name="keywords" content="free html5, free template, free bootstrap, html5, css3, mobile first, responsive" />
    <meta name="author" content="FREEHTML5.CO" />

    <!-- 
    //////////////////////////////////////////////////////

    FREE HTML5 TEMPLATE 
    DESIGNED & DEVELOPED by FREEHTML5.CO

    Website:         http://freehtml5.co/
    Email:           info@freehtml5.co
    Twitter:         http://twitter.com/fh5co
    Facebook:        https://www.facebook.com/fh5co

    //////////////////////////////////////////////////////
     -->

    <!-- Facebook and Twitter integration -->
    <meta property="og:title" content="" />
    <meta property="og:image" content="" />
    <meta property="og:url" content="" />
    <meta property="og:site_name" content="" />
    <meta property="og:description" content="" />
    <meta name="twitter:title" content="" />
    <meta name="twitter:image" content="" />
    <meta name="twitter:url" content="" />
    <meta name="twitter:card" content="" />

    <!-- Place favicon.ico and apple-touch-icon.png in the root directory -->
    <link rel="shortcut icon" href="favicon.ico">

    <!-- Google Webfonts -->
    <link href='http://fonts.googleapis.com/css?family=Roboto:400,300,100,500' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet' type='text/css'>

    <!-- Animate.css -->
    <link rel="stylesheet" href="css/animate.css">
    <!-- Icomoon Icon Fonts-->
    <link rel="stylesheet" href="css/icomoon.css">
    <!-- Magnific Popup -->
    <link rel="stylesheet" href="css/magnific-popup.css">
    <!-- Salvattore -->
    <link rel="stylesheet" href="css/salvattore.css">
    <!-- Theme Style -->
    <link rel="stylesheet" href="css/style.css">
    <!-- Modernizr JS -->
    <script src="js/modernizr-2.6.2.min.js"></script>
    <!-- FOR IE9 below -->
    <!--[if lt IE 9]>
    <script src="js/respond.min.js"></script>
    <![endif]-->

</head>
"""

HTML_BODY = """
<body>

    <div id="fh5co-offcanvass">
        <a href="#" class="fh5co-offcanvass-close js-fh5co-offcanvass-close">Menu <i class="icon-cross"></i> </a>
        <h1 class="fh5co-logo"><a class="navbar-brand" href="index.html">KRLAB</a></h1>
        <ul>
            <li><a href="http://krlab.info.kochi-tech.ac.jp/">Home</a></li>
            <li class="active"><a href="index.html">Album</a></li>
            <li><a href="https://www.kochi-tech.ac.jp/">KUT</a></li>
            <li><a href="http://www.info.kochi-tech.ac.jp/">KUT Information</a></li>
            <li><a href="http://krlab.info.kochi-tech.ac.jp/~kurihara/">Toru Kurihara</a></li>
        </ul>
        <h3 class="fh5co-lead">Connect with us</h3>
        <p class="fh5co-social-icons">
            <a href="#"><i class="icon-twitter"></i></a>
            <a href="#"><i class="icon-facebook"></i></a>
            <a href="#"><i class="icon-instagram"></i></a>
            <a href="#"><i class="icon-dribbble"></i></a>
            <a href="#"><i class="icon-youtube"></i></a>
        </p>
    </div>
    <header id="fh5co-header" role="banner">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <a href="#" class="fh5co-menu-btn js-fh5co-menu-btn">Menu <i class="icon-menu"></i></a>
                    <a class="navbar-brand" href="index.html">KRLAB*ALBUM %s</a>
                </div>
            </div>
        </div>
    </header>
    <!-- END .header -->

    <div id="fh5co-main">
        %s
    </div>

    <footer id="fh5co-footer">

        <div class="container">
            <div class="row row-padded">
                <div class="col-md-12 text-center">
                    <p class="fh5co-social-icons">
                        <a href="#"><i class="icon-twitter"></i></a>
                        <a href="#"><i class="icon-facebook"></i></a>
                        <a href="#"><i class="icon-instagram"></i></a>
                        <a href="#"><i class="icon-dribbble"></i></a>
                        <a href="#"><i class="icon-youtube"></i></a>
                    </p>
                    <p><small>&copy; Hydrogen Free HTML5 Template. All Rights Reserved. <br>Designed by: <a href="http://freehtml5.co/" target="_blank">FREEHTML5.co</a> | Images by: <a href="http://pexels.com" target="_blank">Pexels</a> </small></p>
                </div>
            </div>
        </div>
    </footer>


    <!-- jQuery -->
    <script src="js/jquery.min.js"></script>
    <!-- jQuery Easing -->
    <script src="js/jquery.easing.1.3.js"></script>
    <!-- Bootstrap -->
    <script src="js/bootstrap.min.js"></script>
    <!-- Waypoints -->
    <script src="js/jquery.waypoints.min.js"></script>
    <!-- Magnific Popup -->
    <script src="js/jquery.magnific-popup.min.js"></script>
    <!-- Salvattore -->
    <script src="js/salvattore.min.js"></script>
    <!-- Main JS -->
    <script src="js/main.js"></script>




</body>
"""

HTML_BLOCK = """
        <br>
        <div align="center">%s</div>
        <div class="container">

            <div class="row">

                <div id="fh5co-board" data-columns>

                %s

                </div>
            </div>
        </div>
"""


HTML_ITEM = """
                    <div class="item">
                        <div class="animate-box">
                            <a href="%s/%s" class="image-popup fh5co-board-img"><img src="%s/%s" alt="krlab album"></a>
                            <div class="fh5co-desc">%s</div>
                        </div>
                    </div>
"""

HTML_ITEM = """
                    <div class="item">
                        <div class="animate-box">
                            <a href="%s/%s" class="image-popup fh5co-board-img"><img src="%s/%s" alt="krlab album"></a>
                            <span>
                                <a href="%s/%s" class="icon-download " download="%s"></a>
                                %s
                            </span>
                        </div>
                    </div>
"""


HTML_360VIEWER = """
                                <a href="%s/%s" class="icon-eye "></a>
"""

HTML_360VIEWER_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>%s</title>
<meta name="description" content="panorama view">
<script src="https://aframe.io/releases/0.4.0/aframe.min.js"></script>
</head>
<body>
<a-scene>
<a-sky src="%s/%s" rotation="0 0 0"></a-sky>
</a-scene>
</body>
</html>
"""
