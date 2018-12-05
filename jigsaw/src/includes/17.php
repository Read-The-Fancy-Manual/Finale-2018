<?php
	$ch = curl_init("http://rtfm.re/");
	curl_exec($ch);
	curl_close($ch);
?>
