import pyHook
import pythoncom
import win32gui
import win32process
import os

def onclick(event):
    window_name = str(event.WindowName)
    window = event.Window
    window_id = str(window)
    window_position_dim = win32gui.GetWindowRect(event.Window)
    window_position = (window_position_dim[0], window_position_dim[1])
    window_dimension = str((window_position_dim[2], window_position_dim[3]))
    _, pid = win32process.GetWindowThreadProcessId(window)
    pid = str(pid)
    event_position = event.Position
    event_position_rel = str((event_position[0] - window_position[0], event_position[1] - window_position[1]))
    
    window_position = str(window_position)
    event_position = str(event_position)
    
    F = open("clicks.csv", "a")
    F.write("%s,%s,%s,%s,%s,%s,%s\n" % (pid, window_id, window_name, window_position, window_dimension, event_position, event_position_rel))
    F.close()
    
    return True

if not os.path.exists("clicks.csv"):
    F = open("clicks.csv","w")
    F.write("pid,window_id,window_name,window_position,window_dimension,event_position,event_position_rel\n")
    F.close()
hm = pyHook.HookManager()
hm.SubscribeMouseAllButtonsDown(onclick)
hm.HookMouse()
pythoncom.PumpMessages()
hm.UnhookMouse()