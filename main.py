# pip install pynput
import time, random, threading, sys
from pynput import keyboard
from pynput.keyboard import Key

# ---- tune these ----
SPEEDS         = [30, 45, 60, 80, 110, 150, 220, 350, 600, 1000, 10000]  # WPM levels
level          = 2          # start level (60 WPM)
PAUSES_MAX_WPM = 150        # above this: no random stops, max speed
HESITATE_PROB  = 0.02
HESITATE_SEC   = (0.8, 3)
THINK_PROB     = 0.15
THINK_SEC      = (2, 7)
# --------------------

kb = keyboard.Controller()
stop, paused, running = threading.Event(), threading.Event(), threading.Event()
MAC = sys.platform == "darwin"
TEXT = open("input.txt", encoding="utf-8").read().expandtabs(4)

def human():
    return SPEEDS[level] <= PAUSES_MAX_WPM

def nap(sec):
    """Precise sleep; holds while paused, exits on stop."""
    end = time.time() + sec
    while not stop.is_set():
        if paused.is_set():
            time.sleep(0.05); continue
        left = end - time.time()
        if left <= 0: break
        time.sleep(min(0.05, left))

def combo(*keys):
    for k in keys: kb.press(k)
    for k in reversed(keys): kb.release(k)
    time.sleep(0.03 if human() else 0.008)

def clear_after_cursor():
    combo(Key.esc)
    if MAC: combo(Key.cmd, Key.shift, Key.down)
    else:   combo(Key.ctrl, Key.shift, Key.end)
    combo(Key.delete)

def new_line():
    clear_after_cursor()
    combo(Key.enter)
    if MAC: combo(Key.cmd, Key.shift, Key.left)
    else:   combo(Key.shift, Key.home)

def type_human(text):
    stop.clear(); paused.clear()
    for i, line in enumerate(text.split("\n")):
        if stop.is_set(): break
        if i: new_line()
        if human() and random.random() < THINK_PROB:
            nap(random.uniform(*THINK_SEC))
        for ch in line:
            if stop.is_set(): break
            kb.type(ch)
            base = 12 / (SPEEDS[level] * random.uniform(0.85, 1.15))
            d = random.gauss(base, base * 0.3)
            if human():
                if ch in " .,:;(":
                    d += random.uniform(0.05, 0.3)
                if random.random() < HESITATE_PROB:
                    d += random.uniform(*HESITATE_SEC)
            nap(max(0.001, d))
        if human():
            nap(random.uniform(0.1, 0.5))
    if not stop.is_set():
        clear_after_cursor()
    running.clear()

def set_level(step):
    global level
    level = max(0, min(len(SPEEDS) - 1, level + step))
    print(f"Speed: {SPEEDS[level]} WPM")

def on_press(key):
    if key == Key.f8 and not running.is_set():
        running.set()
        threading.Thread(target=type_human, args=(TEXT,), daemon=True).start()
    elif key == Key.f9:
        if paused.is_set(): paused.clear()
        else: paused.set()
    elif key == Key.f10:
        stop.set()
    elif key == Key.f6:
        set_level(-1)
    elif key == Key.f7:
        set_level(+1)
    elif key == Key.esc:
        sys.exit()

print("F8 start | F9 pause/resume | F10 stop | F6 slower | F7 faster")
print(f"Speed: {SPEEDS[level]} WPM")
with keyboard.Listener(on_press=on_press) as l:
    l.join()