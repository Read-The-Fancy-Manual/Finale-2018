<?php

function getFib($n) {
    return round(pow((sqrt(5)+1)/2, $n) / sqrt(5));
};

$i = 0;

while($i<1000) {
    echo getFib($i).'</br>';
    ++$i;
}

?>
