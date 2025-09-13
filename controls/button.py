from gpiozero import Button
from config import BUTTON_PIN

button = Button(BUTTON_PIN)

listening_state = {"state": False}

def start_listening():
    listening_state["state"] = True
    print("Button pressed: Start listening")

def stop_listening():
    listening_state["state"] = False
    print("Button released: Stop listening")

button.when_pressed = start_listening
button.when_released = stop_listening