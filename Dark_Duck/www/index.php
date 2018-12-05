<?php
	session_start();
	if(isset($_SESSION["user"]))
	{
		header('Location: home.php');
		exit();
	}
?>
<html>
<head>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
</head>
<body>
	<div id="content">
		<form action="home.php" method="POST">
			<input type="text" name="username" placeholder="username">
			<input type="password" name="password">
			<input type="submit" name="submit" value="Enregistrer">
		</form>
	</div>
</body>
</html>
