import serial
from pynput.keyboard import Key, Controller, KeyCode
import time
import sys

# ----------------- KONFIGURATION -----------------
COM_PORT = 'COM3' 
BAUD_RATE = 115200

KEY_MAPPING = {
    "F13": [Key.ctrl_l, 'a'],
    "F14": [Key.alt_l, 's'],  
    "F15": [Key.media_play_pause], 
    "F16": "Ich bin weg, auf wiedersehen",           
    "F17": [Key.shift_l, 'q'],  
    "F18": [Key.alt_l, Key.f4],  
    "F19": [Key.ctrl_l, Key.shift_l, 'e'], 
}


keyboard = Controller()
active_keys = {} 

def simulate_keypress(action, event_type):
    # TEXT
    if isinstance(action, str):
        if event_type == "DOWN":
            print(f"[DOWN] Tippe Text: '{action}'")
            keyboard.type(action)
        return
        
    # MAKRO
    elif isinstance(action, list):
        keys_to_process = action
        
        if event_type == "UP":
            keys_to_process = list(reversed(action))

        print(f"[{event_type}] Gedrückte Tasten: {keys_to_process}")
        
        for key in keys_to_process:
            pynput_key = key
            if isinstance(key, str) and key.upper().startswith('F') and len(key) > 1:
                try:
                    pynput_key = getattr(Key, key.lower())
                except AttributeError:
                    continue 

            if event_type == "DOWN":
                keyboard.press(pynput_key)
            elif event_type == "UP":
                keyboard.release(pynput_key)


def run_listener():
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
        print(f"--- Serieller Port {COM_PORT} geöffnet bei {BAUD_RATE} Baud. ---")
        print("Warte auf Makro-Befehle...")
    except serial.SerialException as e:
        print(f"FEHLER: Serieller Port konnte nicht geöffnet werden: {e}")
        sys.exit(1)
        
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
  
                if line.startswith("DOWN ") or line.startswith("UP "):
                    parts = line.split()
                    event_type = parts[0]
                    key_label = parts[1]

                    if key_label in KEY_MAPPING:
                        target_keys = KEY_MAPPING[key_label]
                        simulate_keypress(target_keys, event_type)
                    else:
                        print(f"WARNUNG: Unbekanntes Key-Label: {key_label}")
            
        except serial.SerialException:
            print("Serieller Port getrennt. Versuche Neuverbindung in 5 Sekunden...")
            ser.close()
            time.sleep(5)
            try:
                ser.open()
            except serial.SerialException:
                pass 
            
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            time.sleep(0.1)

        time.sleep(0.1)

if __name__ == "__main__":
    run_listener()