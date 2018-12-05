<?php

$_TITLE = 'MD Auth';
$_LONGTITLE = 'MD Auth';

require 'header.php';

if(isset($_GET['source'])) {

	highlight_file(__FILE__);
	die();
}

?>
<br />
<a href="?source">Show source</a>
<br /><br />
<!-- The challenge begins here -->
<?php

$con = new SQLite3('mdauth.db');

require 'config.php'; # 7-digit APP_SALT, MAX_ERRORS and check_errors()
if(isset($_POST['login'], $_POST['password'])) {

    $errors = isset($_COOKIE['signed_errors']) ? check_errors($_COOKIE['signed_errors']) : 0;

    if($errors >= MAX_ERRORS) {
        presult('You have been banned for reaching '.MAX_ERRORS.' errors');

    } else {

        $login = $con->escapeString($_POST['login']);
		$hash = md5($con->escapeString(APP_SALT.$_POST['password']), true);

        $query = $con->query("SELECT login FROM users WHERE hash='{$hash}' and login='{$login}'");
		if(!$query) $row=FALSE;
        else $row = $query->fetchArray();

		if($row !== FALSE&& $query->fetchArray() === FALSE) {
            presult("Welcome back {$row['login']}!");

        } else {

            presult('Wrong username/password combination!');
            setcookie('signed_errors', md5(APP_SALT.((string) ($errors+1))), time()+86400);
        }
    }
}

?>
<form action="" method="post">
    <input name="login" placeholder="Login" />
    &nbsp;
    <input name="password" placeholder="Password" type="password" />
    &nbsp;
    <input value="Log in!" type="submit" />
</form>
<?php

require 'footer.php';

?>
