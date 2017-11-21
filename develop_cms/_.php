<!DOCTYPE html>
<html>

<head>
    <title>title</title>
</head>

<body>
    <?php
        include("lib.php");
        $newline = '<br>';
        $DIR = "images";

        if ($dir = opendir($DIR)) {
            while ($file = readdir($dir)) {
                if (is_img($file)) {
                    echo $file.$newline;

                    //$exif = exif_read_data($DIR."/".$file, 0, true);
                    $exif = exif_read_data($DIR."/".$file, 'IFDO');
                    pre_dump($exif);
                }
            }
        }
    ?>
</body>

</html>
