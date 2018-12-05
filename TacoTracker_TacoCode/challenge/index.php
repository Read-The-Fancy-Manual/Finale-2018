<?php require 'db.encoded'; ?>
<!DOCTYPE html>
<html>
<head>
	<title>🌮🌮🌮</title>
	<style type="text/css">
		body {
			font-family: monospace;
			text-align: center;
		}
	</style>
</head>
<body>
	<div>
		<h1>the 🌮 tracker</h1>
		<h3>recipes, pictures and (good) fat</h3>
	</div>
	<div>
		<p>
			<i>The files are freely downloadable<br>for the members of our community, enjoy!</i>
		</p>
		<i>Due to the price rise of jalapenos, inscriptions are <b>closed</b>.</i><br>
		<ul>
			<?php if (empty($_SERVER['PHP_AUTH_USER']) 
				   || $_SERVER['PHP_AUTH_USER'] !== 'tacoslover' 
				   || !isset($_GET['secret_sauce']) 
				   || !isset($_GET['guacamole'])
				   || hash_hmac('gost-crypto', $_GET['secret_sauce'], hash_hmac('gost-crypto', $_GET['guacamole'], getenv("NOT_FOR_YOU"))) !== $_SERVER['PHP_AUTH_PW']) {
				echo "\nACCESS DENIED.";
			} 
			else {
				foreach ($pdo->query("SELECT * FROM torrents") as $row) {
				echo "<li><a href=\"${row['magnet']}\">${row['filename']}</a></li>\n";
			}}?>
		</ul>
	</div>
</body>
</html>
