Option Explicit

Dim ServerName
Dim fso, WriteStuff, OutputText
Dim ws, wmiService, colItemz, item, sPath
Dim CrLf, TabChar

TabChar = Chr(9)
CrLf = Chr(13) & Chr(10)

Set wmiService = GetObject("winmgmts:{authenticationLevel=pktPrivacy}\\.\root\microsoftiisv2")

If WScript.Arguments.Length = 1 Then
   ServerName = WScript.Arguments(0)
Else
   ServerName = "localhost"
End If


Set ws = GetObject( "IIS://" & ServerName & "/W3SVC" )
EnumWebsites ws

Sub EnumWebsites( ws )

    Dim webServer, bindings

    For Each webServer IN ws

        If webServer.Class = "IIsWebServer" Then

            Set colItemz = wmiService.ExecQuery("select * from IIsWebVirtualDirSetting where name = 'W3SVC/" & webServer.Name & "/root'")

            For Each item in colItemz
                sPath = item.Path
            Next

            WScript.Echo _
                "Site ID = " & webServer.Name & CrLf & _
                "Comment = """ & webServer.ServerComment & """ " & CrLf & _
                "State = " & StateTranslation( webServer.ServerState ) & CrLf & _
                "LogDir = " & webServer.LogFileDirectory & CrLf & _
                "Path = " & sPath & _
            ""

            OutputText = OutputText & CrLf & "Site ID = " & webServer.Name & CrLf & _
                "Comment = """ & webServer.ServerComment & """ " & CrLf & _
                "State = " & StateTranslation( webServer.ServerState ) & CrLf & _
                "LogDir = " & webServer.LogFileDirectory & CrLf & _
                "Path = " & sPath & _
                ""

            bindings = EnumBindings(webServer.ServerBindings) & _
            EnumBindings( webServer.SecureBindings )

            If Not bindings = "" THEN
                WScript.Echo "IP Address" & TabChar & _
                "Port" & TabChar & _
                "Host" & CrLf & _
                bindings

                OutputText = OutputText & CrLf & "IP Address" & TabChar & _
                "Port" & TabChar & _
                "Host" & CrLf & _
                bindings
            End If
        End If
    NEXT

    'FileWriter OutputText

End Sub


Sub FileWriter(WriteText)

    Set fso = CreateObject("Scripting.FileSystemObject")
    Set WriteStuff = fso.OpenTextFile("OneOff.txt", 8, True)
    WriteStuff.WriteLine(WriteText)
    WriteStuff.Close

    Set WriteStuff = nothing
    Set fso = nothing

End Sub


Function EnumBindings( objBindingList )

    Dim i, strIP, strPort, strHost
    Dim reBinding, reMatch, reMatches
    Set reBinding = NEW RegExp
    reBinding.Pattern = "([^:]*):([^:]*):(.*)"

    For i = LBOUND( objBindingList ) TO UBOUND( objBindingList )

        Set reMatches = reBinding.Execute( objBindingList( i ) )
        For Each reMatch In reMatches
            strIP = reMatch.SubMatches( 0 )
            strPort = reMatch.SubMatches( 1 )
            strHost = reMatch.SubMatches( 2 )

            If strIP = "" Then strIP = "All Unassigned"
            If strHost = "" Then strHost = "*"
            If LEN( strIP ) < 8 Then strIP = strIP & TabChar

            EnumBindings = EnumBindings & _
            strIP & TabChar & _
            strPort & TabChar & _
            strHost & TabChar & _
            ""
        Next

        EnumBindings = EnumBindings & CrLf
    Next

End Function

Function StateTranslation(StatusID)
    Select Case StatusID
        Case 1
            StateTranslation = "Starting"
        Case 2
            StateTranslation = "Started"
        Case 3
            StateTranslation = "Stopping "
        Case 4
            StateTranslation = "Stopped"
        Case 5
            StateTranslation = "Pausing"
        Case 6
            StateTranslation = "Paused"
        Case 7
            StateTranslation = "Continuing"
        Case ELSE
            StateTranslation = "Unknown state"
    End Select
End Function