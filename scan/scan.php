<?php
error_reporting(0);
ini_set('max_execution_time', '0');
header("Content-Type: text/html; charset=UTF-8");
echo "--------------------------------------<br>";
echo "PHP Inside Scan By Nan3r<br>";
echo "Once Only Scan 30 IP，Default End 30<br>";
echo "POST:<br> 1.start=1&end=30<br>2.url=http://xxx.com<br>";
echo "--------------------------------------<br>";

function getip($start=1, $end)
{
	$rs = array();
	$all_ip = exec_get_all_ip();
	$local_ip = gethostbyname($_ENV['COMPUTERNAME']);
	foreach ($all_ip as $k => $ip) {
		if(count($all_ip) > 1 && $ip == $local_ip) 
		{
			unset($all_ip[$k]);
			$local_ip = $all_ip[0];
		}
	}

	for ($i=$start; $i <= $end; $i++) { 
		$rs[] = "http://".substr($local_ip, 0, strrpos($local_ip, '.') + 1).strval($i);
	}
	return $rs;
}

function exec_get_all_ip()
{
	$ip = `ipconfig`;
	$expip = explode(':', $ip);
	$rip = '';
	foreach ($expip as $k => $v) {
			if(preg_match('/IP Address/', $v)){
				$rip .= $expip[$k+1];
		}
	}

	if(preg_match_all("/[0-9]{1,3}(\.[0-9]{1,3}){3}/", $rip, $matchs)){
		foreach ($matchs as $key => $value) {
			foreach ($value as $ipv) {
				if(strlen($ipv) < 7) unset($matchs[$key]);
			}
		}
	}
	return $matchs[0];
}


function get_web_info($url)
{
	$opts = array(  
  		'http'=>array(  
    		'method'=>"GET",  
    		'timeout'=>1,//单位秒 
   		)  
	);
	$result = array(
			'url' => '',
			"web_title" => '',
			'web_server' => '',
			'flag' => 'success'
		);
	$html = file_get_contents($url, false, stream_context_create($opts));
	if(isset($html) && !empty($html)){
		$responseInfo = $http_response_header;
		if(isset($responseInfo) && !empty($responseInfo)){
			if(preg_match("/200/i", $responseInfo[0])){
				$result['url'] = $url;
				$result['web_title'] = get_title($html);
				$result['web_server'] = get_web_server($responseInfo);
			}
		}
	}
	if(!empty($result['url'])){
		echo $result['url'].">>".$result['web_title'].">>".substr($result['web_server'], 7).">>".$result['flag']."<br>";
			@ob_flush();
    @flush();
	} 

}

function get_title($html)
{
	if(preg_match('/<title>(.*?)<\/title>/', str_replace(PHP_EOL, '', $html), $title)) return $title[1];
	else return 'NULL';
}

function get_web_server($responseInfo)
{
	foreach ($responseInfo as $key => $value) {
		if (preg_match('/Server/', $value)) {
			return $value;
		}
	}
}



$start = $_POST['start'];//起始IP
$end = $_POST['end'];//结束IP
$url = $_POST['url'];//获取某个IP的HTML

if(isset($start)){
	if(!isset($end) or intval($end) - intval($start) > 30) die("End-start greater 30");
	$ip = getip($start, $end);
} 
elseif(isset($end)){
	if(!isset($end) or $end > 30) die("End-start greater 30");
	$ip = getip(1, $end);
}elseif(isset($url)){
	if(!preg_match("/http/i", $url)) die("Url Example: http://xxx.com");
	echo file_get_contents($url);
	exit;
}else{
	$ip = getip(1, 30);
}

foreach ($ip as $key => $scan) {
        get_web_info($scan);
}