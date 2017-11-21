<?php

function is_img($filename) {
    $IMG_EXTS = ['.jpg', '.JPG'];

    $ext = substr($filename, -4);

    foreach ($IMG_EXTS as $e) {
        if($e == $ext) return True;
    }
    return False;
}


# ------------------------------

function pre_dump($obj) {
    echo '<pre>';
    var_dump($obj);
    echo '</pre>';
}
?>