<!DOCTYPE html>
<html>

<head>
    <title>title</title>
    <link rel="stylesheet" type="text/css" href="main.css">
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
</head>

<!-- TABLE -->
<table border="1">
<body>

<script>
    function onClick_saveButton() {
        var elements = document.getElementsByTagName("tr");
        console.log(elements);

        for (i=0; i<elements.length; i++) {
            if (elements[i].cells[0].tagName == "TH")) continue;

            
        }
    }
</script>

<div align="center">
    <button class="reset_button" onClick="location.reload();">RESET</button>
    <button class="save_button" onClick="onClick_saveButton();">SAVE</button>
</div>
<hr>

    <?php
        include("lib.php");

        // JSONの読み込み
        $url = "setting.json";
        $json = file_get_contents($url);
        $arr = json_decode($json, true);

        // BUTTON
        // RESET
        // SAVE

        // table headers
        $keys = array(
            'ID'            => 15,
            'Y / m / d'     => 20,
            'H:M'           => 15,
            'S'             => 10,
            'is360v'        => 10,
            'Model'         => 30
        );

        // years
        $year_array = array();

        $year = -1;
        foreach($arr as $data) {
            // Start Year
            if ($year != $data['Y']) {
                // </TABLE>
                if ($year != -1) {
                    print('</tbody>');
                    print('</table>');
                }
                $year_array[] = $data['Y'];

                print('<p align="center">');

                // year title
                print('
                    <button onclick="oc_button'.$data['Y'].'();" id="table_button'.$data['Y'].'"><i class="fa fa-caret-up" aria-hidden="true"></i></button>
                ');
                print($data['Y'].$_br);

                print('</p>');
            
                // <TABLE>
                //print('<table class="album_table table'.$data['Y'].'" border=1 align="center"');
                print('<table class="album_table" id="album_table'.$data['Y'].'" border=1 align="center"');

                // TABLE HEADER
                print('<thead><tr>');
                foreach($keys as $key => $width) {
                    //print('<th width='.$width.'%">'.$key.'</td>');
                    print('<th>'.$key.'</td>');
                }
                print('</tr></thead>');
                print('<tbody id="tbody'.$data['Y'].'">');
            }
            // update year
            $year = $data['Y'];

            // TABLE BODY
            print('<tr>');
            // ID
            print('<td>'.$data['id'].'</td>');
            // Y / m / d
            print('<td>');
            get_ymd_td($data['Y'], $data['m'], $data['d']);
            print('</td>');
            // H:M
            print('<td>');
            get_hm_td($data['H'], $data['M']);
            print('</td>');
            // S
            print('<td>');
            get_s_td($data['S']);
            print('</td>');
            // is360v
            print('<td>');
            get_is360v_td($data['is360v']);
            print('</td>');
            // model
            print('<td class="model">'.$data['model'].'</td>');
            print('</tr>');
        }
        // </TABLE>
        print('</table>');

        // years processing
        br();
        foreach ($year_array as $y) {
            make_oc_button($y);
        }
    ?>

</body>

</html>
