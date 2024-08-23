# サスティンペダルをエンターキーにするプログラム

import mido
from pynput.keyboard import Controller, Key

keyboard = Controller()

# MIDIポートをオープン
try:
    input_port = mido.open_input()
except IOError:
    print("MIDIデバイスが見つかりません。")
    exit()

print("MIDI入力を待機中...")

# ペダル入力（CC 64のメッセージ）を監視
for msg in input_port:
    if msg.type == 'control_change' and msg.control == 64:
        if msg.value > 0:  # 押されたら
            print("おされた〜")
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
