# ------------------
# Working as of
# 07.11.2020
# ------------------

import time
import keyboard
import pymem.process
from win32gui import GetWindowText, GetForegroundWindow

if not keyboard:
    print("Keyboard has not been imported!")

if not time:
    print("Time has not been imported!")

if not pymem:
    print("Pymem has not been imported!")

if not GetWindowText or GetForegroundWindow:
    print("Win32gui has not been imported correctly!")

# First we need to load the CS:GO memory offsets. These might change after an update.
dwForceJump = 0x51FBFA8
dwLocalPlayer = 0xD3DD14
m_fFlags = 0x104

game = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(game.process_handle, "client.dll").lpBaseOfDll

while True:
    if keyboard.is_pressed("delete"):
        raise SystemExit

    try:
        name = GetWindowText(GetForegroundWindow())
        if game.read_int(client + dwLocalPlayer) and name == "Counter-Strike: Global Offensive":
            player_status = game.read_int(client + dwLocalPlayer)
            jump = client + dwForceJump
            on_ground = game.read_int(player_status + m_fFlags)
            if keyboard.is_pressed('space') and on_ground == 257:
                game.write_int(jump, 5)
                time.sleep(0.15)
                game.write_int(jump, 4)
    except:
        pass



