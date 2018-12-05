<?php
	$za = new ZipArchive();

	$za->open('sigsegv_pass.zip');
	print_r($za);
	var_dump($za);
	$za->close();
?>