import win32gui
import win32api

def change_language(id: int):
    window_handle = win32gui.GetForegroundWindow()
    win32api.PostMessage(window_handle, 0x0050, 0, id)

def change_to_main():
    change_language(0x4090409)

def change_to_second():
    change_language(0x00000419)
