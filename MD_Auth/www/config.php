<?php

define('APP_SALT', '8620371');
define('MAX_ERRORS', 5);

function check_errors($cookie) {

    for($i=0; $i<5; $i++) {

        if(md5(APP_SALT.((string)($i))) == $cookie)
            return $i;
    }

    return 5;
}
