<?php

$x = function($s) { return $h("sha256", $s); };
$h = "substr";
$ap = function($s) { $x($h); }
$w = function($s) { return $x($ap($s)); }
$gr = "sha256";
$s = bin2hex(random_bytes(78));

?>
