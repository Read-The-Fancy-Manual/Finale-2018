<?php
function xor_this($string) {
    $key = ('ITSTHEKEY!!!!!!!');
    $text = $string;

    $outText = '';

    for($i=0; $i<strlen($text); )
    {
        for($j=0; ($j<strlen($key) && $i<strlen($text)); $j++,$i++)
        {
            $outText .= $text{$i} ^ $key{$j};
        }
    }
    return $outText;
}

echo xor_this(hex2bin("3A3D34272D223D3E6D1412161918131134"));

?>
