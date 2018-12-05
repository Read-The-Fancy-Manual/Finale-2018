<?php
if(!file_exists("flagi.txt")) {
  die("File not found");
} else {
  $file=fopen("flagi.txt","r");
}
?>