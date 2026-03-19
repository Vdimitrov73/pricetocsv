Option Explicit

Dim wsh, fso, csvDir, latestFile
Set wsh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

csvDir     = wsh.ExpandEnvironmentStrings("%USERPROFILE%") & "\Documents\PriceToCSV\"
latestFile = csvDir & "prices_" & Year(Date) & Right("0" & Month(Date), 2) & Right("0" & Day(Date), 2) & ".csv"

If Not fso.FileExists(latestFile) Then
    MsgBox "Today's prices file not found:" & vbCrLf & latestFile
    WScript.Quit
End If

' ── Helper: activate window with retries ─────────────────────
Function ActivateWindow(title, retries)
    Dim i
    For i = 1 To retries
        If wsh.AppActivate(title) Then
            ActivateWindow = True
            WScript.Sleep 300
            Exit Function
        End If
        WScript.Sleep 500
    Next
    MsgBox "Could not activate: " & title & vbCrLf & "Aborting."
    WScript.Quit
End Function

' ── Navigate to Portfolio so Import Prices is available ──────
ActivateWindow "Quicken", 6
wsh.SendKeys "^u"
WScript.Sleep 2000

' ── Step 1: Import security prices ───────────────────────────
ActivateWindow "Quicken", 6
wsh.SendKeys "%f"
WScript.Sleep 400
wsh.SendKeys "i"
WScript.Sleep 400
wsh.SendKeys "i"
WScript.Sleep 800
wsh.SendKeys latestFile
WScript.Sleep 800
ActivateWindow "Import Price Data", 10
wsh.SendKeys "{TAB}{TAB}"
WScript.Sleep 300
wsh.SendKeys " "
WScript.Sleep 500
ActivateWindow "Quicken", 10
wsh.SendKeys "{ENTER}"
WScript.Sleep 800

' ── Step 2: Update currency rates via One Step Update ────────
ActivateWindow "Quicken", 6
WScript.Sleep 400
wsh.SendKeys "^1"            ' Ctrl+1 = One Step Update directly
WScript.Sleep 1500
ActivateWindow "One Step Update", 10
wsh.SendKeys "%u"            ' Alt+U = Update Now button
WScript.Sleep 3000
ActivateWindow "One Step Update Summary", 20
wsh.SendKeys "{ENTER}"       ' Close Summary
WScript.Sleep 300