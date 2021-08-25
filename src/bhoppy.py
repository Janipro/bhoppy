# ------------------
# Working as of
# 25.08.2021
# ------------------

import time
import keyboard
import pymem.process
from win32gui import GetWindowText, GetForegroundWindow

if not keyboard:
    print("Keyboard has not been imported!")

if not time:
    print("Time has not been imported!")

if not pymem.process:
    print("Pymem process has not been imported!")

# First we need to load the CS:GO memory offsets. These might change after the game gets updated.
# Special thanks to https://github.com/frk1/hazedumper for these offsets.
dwForceJump = 0x524CFDC
dwLocalPlayer = 0xD8A2DC
dwGlowObjectManager = 0x52EB658
dwEntityList = 0x4DA31EC
m_iGlowIndex = 0xA438
m_fFlags = 0x104
m_bSpotted = 0x93D
m_iTeamNum = 0xF4
m_bDormant = 0xED

game = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(game.process_handle, "client.dll").lpBaseOfDll


def esp():
    player_status = game.read_int(client + dwLocalPlayer)
    glow_pointer = game.read_int(client + dwGlowObjectManager)
    team_id = game.read_int(player_status + m_iTeamNum)

    player_count = game.read_int(client + dwGlowObjectManager + 0x4)
    for i in range(1, player_count):
        current_player = game.read_int(client + dwEntityList + ((i - 1) * 0x10))

        if current_player == 0:
            break

        current_player_glow_status = game.read_int(current_player + m_bDormant)
        current_player_glow_index = game.read_int(current_player + m_iGlowIndex)
        current_player_team_id = game.read_int(current_player + m_iTeamNum)

        if current_player_team_id == 0 or current_player_glow_status == 1:
            continue

        else:
            if team_id != current_player_team_id:
                game.write_int(current_player + m_bSpotted, 1)

            if current_player_team_id == 2:
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x4, 1.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x8, 0.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0xC, 0.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x10, 1.0)
                game.write_int(glow_pointer + (current_player_glow_index * 0x38) + 0x24, 1)
                game.write_int(glow_pointer + (current_player_glow_index * 0x38) + 0x25, 0)

            elif current_player_team_id == 3:
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x4, 0.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x8, 0.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0xC, 1.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x10, 1.0)
                game.write_int(glow_pointer + (current_player_glow_index * 0x38) + 0x24, 1)
                game.write_int(glow_pointer + (current_player_glow_index * 0x38) + 0x25, 0)

            else:
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x4, 0.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x8, 1.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0xC, 0.0)
                game.write_float(glow_pointer + (current_player_glow_index * 0x38) + 0x10, 1.0)
                game.write_int(glow_pointer + (current_player_glow_index * 0x38) + 0x24, 1)
                game.write_int(glow_pointer + (current_player_glow_index * 0x38) + 0x25, 0)


def bhop():
    player_status = game.read_int(client + dwLocalPlayer)
    jump = client + dwForceJump
    on_ground = game.read_int(player_status + m_fFlags)
    if keyboard.is_pressed("space") and on_ground == 257:
        game.write_int(jump, 5)
        time.sleep(0.1)
        game.write_int(jump, 4)


def main():
    while True:
        if keyboard.is_pressed("delete"):
            raise SystemExit

        try:
            name = GetWindowText(GetForegroundWindow())
            in_game = game.read_int(client + dwLocalPlayer)
            if in_game and name == "Counter-Strike: Global Offensive":
                if keyboard.is_pressed('p'):
                    while True:
                        bhop()
                        esp()

                        if keyboard.is_pressed('o'):
                            break

        except:
            pass


main()


