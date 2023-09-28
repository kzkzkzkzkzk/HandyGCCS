#!/usr/bin/env python3
# This file is part of Handheld Game Console Controller System (HandyGCCS)
# Copyright 2022-2023 Derek J. Clark <derekjohn.clark@gmail.com>

import sys
from evdev import InputDevice, InputEvent, UInput, ecodes as e, list_devices, ff

from .. import constants as cons

handycon = None

def init_handheld(handheld_controller):
    global handycon
    handycon = handheld_controller
    handycon.BUTTON_DELAY = 0.2
    handycon.CAPTURE_CONTROLLER = True
    handycon.CAPTURE_KEYBOARD = True
    handycon.CAPTURE_POWER = True
    handycon.GAMEPAD_ADDRESS = 'usb-0000:0a:00.3-2/input0'
    handycon.GAMEPAD_NAME = 'Microsoft X-Box 360 pad'
    handycon.KEYBOARD_ADDRESS = 'usb-0000:0a:00.3-3/input0'
    handycon.KEYBOARD_NAME = 'Asus Keyboard'
    handycon.KEYBOARD_2_ADDRESS = 'usb-0000:0a:00.3-3/input2'
    handycon.KEYBOARD_2_NAME = 'Asus Keyboard'


# Captures keyboard events and translates them to virtual device events.
async def process_event(seed_event, active_keys):
    global handycon

    # Button map shortcuts for easy reference.
    button5 = handycon.button_map["button5"]  # Default MOD

    ## Loop variables
    button_on = seed_event.value
    this_button = None

    # Handle missed keys. 
    if active_keys == [] and handycon.event_queue != []:
        this_button = handycon.event_queue[0]

    # BUTTON 5 (Default: Mode) Control Center Short Press.
    if active_keys == [186] and button_on == 1 and button5 not in handycon.event_queue:
        handycon.event_queue.append(button5)
    elif active_keys == [] and seed_event.code in [186] and button_on == 0 and button5 in handycon.event_queue:
        this_button = button5

    # Create list of events to fire.
    # Handle new button presses.
    if this_button and not handycon.last_button:
        handycon.event_queue.remove(this_button)
        handycon.last_button = this_button
        await handycon.emit_now(seed_event, this_button, 1)

    # Clean up old button presses.
    elif handycon.last_button and not this_button:
        await handycon.emit_now(seed_event, handycon.last_button, 0)
        handycon.last_button = None
