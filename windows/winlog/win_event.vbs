
'x.vbs > m.txt ->dump all login machine name.
'x.vbs username > m.txt ->dump username login machine name.
'download m.txt,C:\\temp\\Security.evt.
'get-content m.txt |get-unique -> this can get unique machine name.

strComputer = "."
Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate,(Security)}!\\" _
    & strComputer & "\root\cimv2")
Set colEvents = objWMIService.ExecQuery _
    ("Select * from Win32_NTLogEvent Where Logfile = 'Security'") 

Set args = WScript.Arguments
For each objEvent in colEvents
    if args.Count = 1 then
        if instr(objEvent.Message, WScript.Arguments(0)) > 0 then
            Wscript.Echo "Computer Name: " & objEvent.ComputerName
            'Wscript.Echo "Message: " & objEvent.Message
            'Wscript.Echo "User: " & objEvent.User
        end if
    else 
        Wscript.Echo "Computer Name: " & objEvent.ComputerName
    end if
Next

'dump Security evtx
Set objSWbemServices = GetObject ("winmgmts:{(Security, Backup)}")

Set colEventLogFiles = objSWbemServices.ExecQuery _
    ("Select * From Win32_NTEventLogFile " _
    & "Where LogFileName = 'Security'")
          
For Each objEventLogFile In colEventLogFiles
    objEventLogFile.BackupEventLog ("C:\\temp\\Security.evt")
Next