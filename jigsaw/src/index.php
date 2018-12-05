<?php

$valid_files = array("1.php", "2.php", "3.php", "4.php", "5.php", "6.php", "7.php", "8.php", "9.php", "10.php", "11.php", "12.php", "13.php", "14.php", "15.php", "16.php", "17.php", "18.php", "19.php", "20.php", "21.php", "22.php", "23.php", "24.php", "25.php", "26.php", "27.php", "28.php", "29.php", "30.php", "31.php", "32.php", "33.php", "34.php", "35.php", "36.php", "37.php", "38.php", "39.php", "40.php", "41.php", "42.php", "43.php", "44.php", "45.php", "46.php", "47.php", "48.php", "49.php", "50.php", "51.php", "52.php", "53.php", "54.php", "55.php", "56.php", "57.php", "58.php", "59.php", "60.php", "61.php", "62.php", "63.php", "64.php", "65.php", "66.php", "67.php", "68.php", "69.php", "70.php", "71.php", "72.php", "73.php", "74.php", "75.php", "76.php", "77.php", "78.php", "79.php", "80.php", "81.php", "82.php", "83.php", "84.php", "85.php", "86.php", "87.php", "88.php", "89.php", "90.php", "91.php", "92.php", "93.php", "94.php");

function check_inclusion($filename, $files) {
  return array_search($filename, $files, true);
}

$filenames = array();

for ($i = 1; $i < 8; ++$i) {
  if (!isset($_GET[$i]) ||
      !check_inclusion($_GET[$i], $valid_files) ||
      check_inclusion($_GET[$i], $filenames)) {
    show_source(__FILE__);
    die("<img src=/static/nope.gif>");
  }
  else {
    $filenames[] = $_GET[$i];
  }
}

foreach ($filenames as $file) include('includes/' . $file);

?>
