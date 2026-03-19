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

' ── Navigate to Investing → Portfolio (makes Import Prices available) ─
wsh.AppActivate "Quicken"
WScript.Sleep 500
wsh.SendKeys "^u"            ' Ctrl+U = Investing → Portfolio
WScript.Sleep 2000

' ── Step 1: Import security prices ───────────────────────────
wsh.SendKeys "%f"            ' File menu
WScript.Sleep 400
wsh.SendKeys "i"             ' Import submenu
WScript.Sleep 400
wsh.SendKeys "i"             ' Import Security Prices
WScript.Sleep 1200
wsh.SendKeys latestFile
WScript.Sleep 1000
wsh.AppActivate "Import Price Data"
WScript.Sleep 400
wsh.SendKeys "{TAB}{TAB}"    ' Skip past Date field to OK button
WScript.Sleep 300
wsh.SendKeys " "             ' Click OK
WScript.Sleep 3000           ' Wait for import
wsh.AppActivate "Quicken"
WScript.Sleep 300
wsh.SendKeys "{ENTER}"       ' Dismiss "Successfully Imported X prices"
WScript.Sleep 1000

' ── Step 2: Update currency rates ────────────────────────────
wsh.AppActivate "Quicken"
WScript.Sleep 500
wsh.SendKeys "^q"            ' Open Currency List
WScript.Sleep 1500
wsh.AppActivate "Currency List"
WScript.Sleep 600
wsh.SendKeys "%u"            ' Update Rates → opens One Step Update
WScript.Sleep 1500
wsh.AppActivate "One Step Update"
WScript.Sleep 500
wsh.SendKeys "%u"            ' Click Update Now!
WScript.Sleep 9000           ' Wait for download
wsh.AppActivate "One Step Update Summary"
WScript.Sleep 1000
wsh.SendKeys "{ENTER}"       ' Close Summary
WScript.Sleep 800
wsh.AppActivate "Currency List"
WScript.Sleep 400
wsh.SendKeys "{ESC}"         ' Close Currency List
WScript.Sleep 500

