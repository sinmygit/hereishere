@echo off
echo ######wmic识别安装到系统中的补丁情况######
wmic qfe get description,installedOn


echo ######识别正在运行的服务######
sc query type= service
net start

echo ######识别开机启动的程序，包括路径######
wmic startup list full

echo ######查看系统中网卡的IP地址和MAC地址######
wmic nicconfig get ipaddress,macaddress

echo ######查看系统中开放的共享######
wmic share get name,path
net share

echo ######查看系统中开启的日志######
wmic nteventlog get path,filename,writeable


echo ######查看当前系统是否是VMWARE######
wmic bios list full | find /i "vmware"

echo ######显示系统中的曾经连接过的无线密码######
netsh wlan show profiles 
echo 'name="wifiname" key=clear'

echo ######查看系统中安装的软件以及版本######
wmic product get name,version


pause