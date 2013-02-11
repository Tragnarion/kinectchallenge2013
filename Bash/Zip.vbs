Set objShell = CreateObject("Shell.Application" ) 
Set Ag=Wscript.Arguments 
set WshShell = WScript.CreateObject("WScript.Shell" ) 

Wscript.Echo "Compressing..."

' Create a new zip file
Set objFSO = CreateObject( "Scripting.FileSystemObject" )
Set objTxt = objFSO.OpenTextFile( Ag(1), 2, True )
objTxt.Write "PK" & Chr(5) & Chr(6) & String( 18, Chr(0) )
objTxt.Close
Set objTxt = Nothing

' Now just put the folder in...
Set DestFldr=objShell.NameSpace(Ag(1)) 
Set SrcFldr=objShell.NameSpace(Ag(0)) 
Set FldrItems=SrcFldr.Items 
DestFldr.CopyHere FldrItems, 16+256

' Sleep a bit, if not the explorer will kill the process :D
Do Until DestFldr.Items.Count = SrcFldr.Items.Count
    WScript.Sleep 200
Loop

Wscript.Echo "Compression done!"