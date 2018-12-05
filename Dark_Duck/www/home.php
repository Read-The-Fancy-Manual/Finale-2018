<?php
	session_start();

	if(isset($_COOKIE["hash"]))
	{
		$hash = array(
			"A755E73616D5F109B344310A0484564847CC0F1F935DC03C575739D2889801B1A103352AA516ABB1A02F4C35AE9E6CAE6F817929C1B148E9B4D63D471C902E67" => "HodorTheHaxor",
			"276C92A21FF75DD64582A71F741BC94A836D681BA088C8DA94933331C446331E69997068B7396B55E080CC3040F99E01BC7B36EC35E3E06221F24C6AEF749CF2" => "MhackBird",
			"7B3AF9A4A9384637F7FA2D216DAE620B7134CB00CDD607B1E25C11B7C77E7FC8B6D3959572C61D03F0142B65EC719D2179A876DEEB6E56CA916F838D470D45FE" => "Th3_L5D",
			"61251196EFC879A8D5CD3C8949E41A8D1E4AFF20E627755CAD83D81243D8C35DBD303801088325E5659D69A4DAEF85029417C8EDB2C1F04F16C7C3FFCCAA4942" => "InfauxSec",
			"FC14914289B746A1A026470CBBFEAD0E70066CB3FE513681D6A07EFBCA0C692C6C7BC04835E2AEFAF726664945ED51A916B7472E4D6F233C93941016E468206D" => "Bidule",
			"0B48DA3A6ACDB9FEE4F8632988B62EFC68ED18C5E0C55666D4A336373D00F2CC5A2002E7B118B335E3AE7A04498AFBCB21CB035BAB48D5C51CEE98F8B606C060" => "Shrewk",
		);

		$cookie = $_COOKIE["hash"];
		$_SESSION["user"] = $hash[$cookie];
	}
	
	if(isset($_SESSION["user"]))
	{
			$user = $_SESSION["user"];
			$ip = array(
    			"HodorTheHaxor" => "56.78.91.121",
    			"MhackBird" => "33.45.89.12",
    			"Th3_L5D" => "127.0.0.1",
    			"InfauxSec" => "90.14.56.78",
    			"Bidule" => "78.66.44.22",
    			"Shrewk" => "90.33.99.44",
			);
			if($ip[$_SESSION["user"]] != $_SERVER["HTTP_X_FORWARDED_FOR"])
			{
				header('Location: index.php');
				exit();
			}
	}
	else
	{
		header('Location: index.php');
		exit();
	}

?>
<html>
<head>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
	<link rel="stylesheet" href="style.css">
</head>
<body>
	<div id="content">
		<h1>Bienvenue <?= $user ?> !</h1><br/>
		<?php 
			$rank = array(
				"HodorTheHaxor" => 0,
				"MhackBird" => 1,
				"Th3_L5D" => 2,
				"InfauxSec" => 0,
				"Bidule" => 1,
				"Shrewk" => 0,
			);
			echo "<u>Liste des fichiers:</u></br>";
			if($rank[$user] >= 2)
			{
				echo "<!-- ?f=<nondufichier> -->";
				$dir = scandir("3CAB376F1B761F06EDE8412329344983293F1A8141841EA57B49C522CA4AE80693D15838C26369DBFFF712BCC1541F102FDAFA18156B70E910010DCAD9D69560");
				foreach($dir as $value)
				{
					if($value != "password.txt")
					{
						echo $value."</br>";
					}
					
				}
				if(isset($_GET["f"]))
				{
					if($_GET["f"] == "hacked.php")
					{
						include("3CAB376F1B761F06EDE8412329344983293F1A8141841EA57B49C522CA4AE80693D15838C26369DBFFF712BCC1541F102FDAFA18156B70E910010DCAD9D69560/hacked.php");
					}
					elseif($_GET["f"] == "password.txt")
					{
						include("3CAB376F1B761F06EDE8412329344983293F1A8141841EA57B49C522CA4AE80693D15838C26369DBFFF712BCC1541F102FDAFA18156B70E910010DCAD9D69560/password.txt");
					}
				}
			}
		?>
	</div>

</body>
</html>
