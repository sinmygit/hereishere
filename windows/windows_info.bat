@echo off
echo ######wmicʶ��װ��ϵͳ�еĲ������######
wmic qfe get description,installedOn


echo ######ʶ���������еķ���######
sc query type= service
net start

echo ######ʶ�𿪻������ĳ��򣬰���·��######
wmic startup list full

echo ######�鿴ϵͳ��������IP��ַ��MAC��ַ######
wmic nicconfig get ipaddress,macaddress

echo ######�鿴ϵͳ�п��ŵĹ���######
wmic share get name,path
net share

echo ######�鿴ϵͳ�п�������־######
wmic nteventlog get path,filename,writeable


echo ######�鿴��ǰϵͳ�Ƿ���VMWARE######
wmic bios list full | find /i "vmware"

echo ######��ʾϵͳ�е��������ӹ�����������######
netsh wlan show profiles 
echo 'name="wifiname" key=clear'

echo ######�鿴ϵͳ�а�װ������Լ��汾######
wmic product get name,version