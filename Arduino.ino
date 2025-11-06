#include <Arduino.h>

const uint8_t BUTTON_PINS[7] = {
  D4, // GPIO2 
  D3, // GPIO0  
  D2, // GPIO4
  D1, // GPIO5
  D7, // GPIO13
  D6, // GPIO12
  D5  // GPIO14
};

const char* KEY_LABELS[7] = {
  "F13", "F14", "F15", "F16", "F17", "F18", "F19"
};

struct Button {
  uint8_t pin;
  const char* label;
  bool pressed;                  
  unsigned long lastChangeMs;
};

Button buttons[7];

const unsigned long DEBOUNCE_MS = 30;

void sendEvent(const char* type, const char* key) {
  Serial.print(type);
  Serial.print(' ');
  Serial.println(key);
}

void setup() {
  Serial.begin(115200);
  delay(50);
  Serial.println("# ESP8266 MacroPad ready");

  for (int i = 0; i < 7; i++) {
    buttons[i] = { BUTTON_PINS[i], KEY_LABELS[i], false, 0 };
    pinMode(buttons[i].pin, INPUT_PULLUP);
  }
}

void loop() {
  unsigned long now = millis();

  for (int i = 0; i < 7; i++) {
    bool curr = (digitalRead(buttons[i].pin) == LOW);
    if (curr != buttons[i].pressed && (now - buttons[i].lastChangeMs) > DEBOUNCE_MS) {
      buttons[i].lastChangeMs = now;
      buttons[i].pressed = curr;

      if (curr) {
        sendEvent("DOWN", buttons[i].label);
      } else {
        sendEvent("UP", buttons[i].label);
      }
    }
  }
  delay(2);
}
