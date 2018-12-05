<?php

function presult($s) {

	echo '<div class="result">'.$s.'</div><br /><br />';
}

?>
<html>
	<head>
		<title><?php echo $_TITLE; ?></title>
		<style type="text/css">
			.result {
				padding: 8px;
				color: white;
				border: 1px solid white;
				background-color: black;
				font-family: Lucida Console;
				font-size: 0.8em;
				display: inline-block;
			}

			a { color:  rgb(4, 139, 154); }
		</style>
	</head>
	<body style="background-color: #EEE; color: rgb(95, 95, 95); margin: 0px; padding: 0px; font-family: Tahoma;">
		<table style="width: 100%; background-color: rgb(4, 139, 154); margin: 0px;">
			<tr>
				<td style="padding: 10px;">
					<a href="index.php" style="color: white; font-weight: bold; font-size: 2em; font-variant: small-caps; text-decoration: none"><?php echo $_LONGTITLE; ?></a>
				</td>
			</tr>
		</table>
		<div style="width: 94%; padding: 3%;" >
