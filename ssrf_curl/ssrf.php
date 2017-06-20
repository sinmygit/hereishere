<?php  
$schema = $_GET['s'];
$ip     = $_GET['i'];
$port   = $_GET['p'];
$query  = $_GET['q'];
if(empty($port)){  
    header("Location: $schema://$ip/$query"); 
} else {
    header("Location: $schema://$ip:$port/$query"); 
}