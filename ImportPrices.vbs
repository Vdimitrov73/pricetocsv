Option Explicit

Dim wsh, fso, csvDir, latestFile
Set wsh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

csvDir     = wsh.ExpandEnvironmentStrings("%USERPROFILE%") & "\Documents\PriceToCSV\"
latestFile = csvDir & "prices_" & Year(Date) & Right("0" & Month(Date), 2) & Right("0" & Day(Date), 2) & ".csv"

If Not fso.FileExists(latestFile) Then
	MsgBox "Today's prices file not found:" & vbCrLf & latestFile, vbExclamation + vbSystemModal, "Quicken Update"
	WScript.Quit
End If

' ── Helper: activate window with retries ─────────────────────
Function ActivateWindow(title, retries)
	Dim i
	For i = 1 To retries
		If wsh.AppActivate(title) Then
			WScript.Sleep 300
			ActivateWindow = True
			Exit Function
		End If
		WScript.Sleep 500
	Next
	MsgBox "Could not activate: " & title & vbCrLf & "Aborting.", vbCritical + vbSystemModal, "Quicken Update"
	WScript.Quit
End Function

' ── Helper: SendKeys with built-in delay ─────────────────────
Sub Send(keys, delay)
	wsh.SendKeys keys
	WScript.Sleep delay
End Sub

' ── Navigate to Portfolio so Import Prices is available ──────
ActivateWindow "Quicken", 8
Send "{ESC}{ESC}{ESC}", 400       ' Clear any open menus or half-typed entries
Send "^u", 2000              ' Ctrl+U = Investing -> Portfolio

' ── Step 1: Import security prices ───────────────────────────
ActivateWindow "Quicken", 8
Send "%f", 400               ' File menu
Send "i", 400                ' Import submenu
Send "i", 800                ' Import Security Prices
Send latestFile, 800
ActivateWindow "Import Price", 12
Send "{TAB}{TAB}", 300
Send " ", 500
ActivateWindow "Quicken", 10
Send "{ENTER}", 800

' ── Step 2: Update currency rates via One Step Update ────────
ActivateWindow "Quicken", 8
Send "^1", 1500              ' Ctrl+1 = One Step Update
ActivateWindow "One Step Update", 12
Send "%u", 3000              ' Alt+U = Update Now
ActivateWindow "Summary", 25
Send "{ENTER}", 300          ' Close Summary

MsgBox "Done: prices and currency rates updated.", vbInformation + vbSystemModal, "Quicken Update"