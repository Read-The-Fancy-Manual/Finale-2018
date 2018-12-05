<?php

$x = function($s) { return hash("sha256", $s); };
$ap = function($s) { return $x(0); };
$w = function($s) { return $x($ap($s)); };
$gr = "substr";
$s = bin2hex(random_bytes(16));

?>
