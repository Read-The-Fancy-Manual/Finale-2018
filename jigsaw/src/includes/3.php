<?php

$x = function($s) { return $h($s); };
$h = "substr";
$ap = function($s) { $x($h); }
$w = function($s) { return $x($ap($s)); }
$gs = "array";
$as = "7468655f67346d65";
?>
