for /l %i in (1,1,255) do @ping 10.0.1.%i -w 1 -n 1 | find /i "ttl"
for /l %i in (1,1,255) do @ping -a 10.0.1.%i -w 1 -n 1 | find /i "Pinging"
for /l %i in (1,1,255) do @ping -a 10.0.%i.1 -w 1 -n 1 | find /i "Pinging"

FOR /F "eol=- tokens=1 delims=\ " %a IN ('net view') DO @(echo name: %a, ip: & ping %a -w 1 -n 1 | find /i "ttl" & echo.)