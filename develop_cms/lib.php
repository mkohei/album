<?php

$_br = '<br>';
$DIR = "images";

# ------------------------------

function pre_dump($obj) {
    echo '<pre>';
    var_dump($obj);
    echo '</pre>';
}

function br() {
    echo nl2br("\n");
}

# -------------------------------

function make_oc_button($y) {
    print('<script>');
    print('cnt'.$y.'=0;');
    print('function oc_button'.$y.'() {');
        print('console.log("Hello!");');
        print('if (cnt'.$y.'%2==0) {');
            print('val = "none";');
            print('str = '."'".'<i class="fa fa-caret-down" aria-hidden="true"></i>'."';");
        print('} else {');
            //print('val = "table-row-group";');
            print('val = "table";');
            print('str = '."'".'<i class="fa fa-caret-up" aria-hidden="true"></i>'."';");
        print('}');
        //print('document.getElementById("table'.$y.'").style.display=val;');
        print('document.getElementById("album_table'.$y.'").style.display=val;');
        print('document.getElementById("table_button'.$y.'").innerHTML=str;');
        print('cnt'.$y.'++;');
    print('}');
    print('</script>');
}


function get_is360v_td($val) {
    if ($val == 1) $v = ' checked="checked"';
    else $v = '';
    printf('<input type="checkbox"'.$v.'>');
}


function get_ymd_td($y, $m, $d) {
    print(
        sprintf('<input type="date" value="%4d-%02d-%02d">', $y, $m, $d)
    );
}


function get_hm_td($h, $m) {
    print(sprintf(
        '<input type="time" value="%02d:%02d">',
    $h, $m));
}


function get_s_td($s) {
    print("<select>");
    foreach(range(0, 59) as $i) {
        printf('<option value="%d"', $i+1);
        if ($s==$i) print(' selected');
        printf('>%d</option>', $i);
    }
    print("</select>");
}


$a = '<tbody id="tbody2017">
<tr>
    <td></td>
    <td>20170000</td>
    <td>
        <input type="date" value="2017-01-12">
    </td>
    <td>
        <input type="time" value="20:20">
    </td>
    <td>
        <select name="second">
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
        </select>
    </td>
    <td>1</td>
    <td>RICHO THETA S</td>
</tr>
</tbody>';
?>