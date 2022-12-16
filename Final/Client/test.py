from pynput import keyboard

def on_activate(hotkey):
    print('Global hotkey activated!')

def on_release(hotkey):
    print('Global hotkey release!')


hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<alt>+h'))

with keyboard.Listener(
        on_press=on_activate(hotkey.press),
        on_release=on_release(hotkey.release)) as l:
    l.join()