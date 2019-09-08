import pyHook
import pythoncom
import win32gui
import win32process
import os
from threading import Thread
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import time

class Shared:
    screenshot_directory = "screenshots"
    last_screenshot = ""
    x_dimension = 37
    y_dimension = 37

class ExecuteScreenshot(Thread):
    def __init__(self, screenshot_name, event_position):
        self.screenshot_name = screenshot_name
        self.event_position = event_position
        Thread.__init__(self)

    def run(self):
        os.system("nircmd.exe savescreenshot "+self.screenshot_name)
        source_img = Image.open(self.screenshot_name).convert("RGBA")
        draw = ImageDraw.Draw(source_img)
        draw.rectangle([self.event_position[0], self.event_position[1], self.event_position[0]+Shared.x_dimension, self.event_position[1]+Shared.y_dimension], fill="red")
        source_img.save(self.screenshot_name)

def mouseup(event):
    event_position = event.Position
    screenshot_name = os.path.join(Shared.screenshot_directory, "Screenshot_"+str(int(time.time()*1000))+".png")
    Shared.last_screenshot = screenshot_name
    t = ExecuteScreenshot(screenshot_name, event_position)
    t.start()
    
    return True

def get_log_path():
    username = ""
    try:
        username = str(os.getenv('username'))
    except:
        pass
    computername = ""
    try:
        computername = str(os.environ['COMPUTERNAME'])
    except:
        pass
    return "clicks_"+username+"_"+computername+".csv"

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
    username = ""
    try:
        username = str(os.getenv('username'))
    except:
        pass
    computername = ""
    try:
        computername = str(os.environ['COMPUTERNAME'])
    except:
        pass
    current_timestamp = str(time.time())
    F = open(get_log_path(), "a")
    F.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (pid, window_id, window_name, window_position, window_dimension, event_position, event_position_rel, username, computername, current_timestamp, Shared.last_screenshot))
    F.close()
    
    return True

if not os.path.exists(Shared.screenshot_directory):
    os.mkdir(Shared.screenshot_directory)
log_path = get_log_path()
if not os.path.exists(log_path):
    F = open(log_path,"w")
    F.write("pid;window_id;window_name;window_position;window_dimension;event_position;event_position_rel;username;computername;current_timestamp;last_screenshot\n")
    F.close()
hm = pyHook.HookManager()
hm.SubscribeMouseAllButtonsUp(mouseup)
hm.SubscribeMouseAllButtonsDown(onclick)
hm.HookMouse()
pythoncom.PumpMessages()
hm.UnhookMouse()