import wx
import os
import sys

def get_path():
    wildcard = "*.*"
    lastFile = None
    
    filename, _= os.path.split(os.path.abspath(__file__))
    filename += os.sep+"lastfile.txt"
    
    print("Filename: ", filename)
    
    if(os.path.isfile(filename)):
        f = open("lastfile.txt")
        lastFile = f.readline()
        f.close()
    
    print("Last File: ", lastFile)
    
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_CHANGE_DIR
    dialog = wx.FileDialog(None, 'Select Video', wildcard=wildcard, style=style)
    if(lastFile != None):
        dialog.SetPath(lastFile)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        f = open(filename, "w")
        f.write(path)
        f.close()
    else:
        path = None
    dialog.Destroy()
    return path
