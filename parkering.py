import time
import machine
from picographics import PicoGraphics, DISPLAY_INKY_PACK

# a handy function we can call to clear the screen
# display.set_pen(15) is white and display.set_pen(0) is black
def clear():
    inky.set_pen(15)
    inky.clear()
    inky.update()

def display_address():
    clear()
    inky.set_pen(0)
    inky.text(top_text, 10, 10, 240, 2)
    inky.text(address, 10, 50, 240, 3)
    inky.text(lead_text, 10, 110, 240, 2)
    inky.update()

# Buttons
button_a = machine.Pin(12, machine.Pin.IN, pull=machine.Pin.PULL_UP)
button_b = machine.Pin(13, machine.Pin.IN, pull=machine.Pin.PULL_UP)
button_c = machine.Pin(14, machine.Pin.IN, pull=machine.Pin.PULL_UP)

# Display
inky = PicoGraphics(DISPLAY_INKY_PACK)
WIDTH, HEIGHT = inky.get_bounds()
inky.set_update_speed(3)
inky.set_font("bitmap8")

streets = ["Jul. Bloms Gade","Husumgade","Jagtvej"]
settings = ["gade","tiere","enere","slut"] # street, tens, ones, finish
set_address = False
index = 0
street_index = 0
tens = 0
ones = 4
top_text = "Bilen står ud for:" # The car is in front of
address = streets[street_index]+" "+str(tens+ones)
lead_text = "Tryk på B for at ændre" # Press B to change
display_address()

# Button handling function
def button(pin):
    global last, set_address, index, streets, street_index, tens, ones, address, lead_text, top_text

    address = streets[street_index]+" "+str(tens+ones)
    print("Før: "+address) # Debug text "Before: + address"

    adjust = 0
    changed = False

    time.sleep(0.01)
    if pin.value():
        return

    if pin == button_b and not set_address:
        index = 0
        set_address = True
        top_text = "Vælg gade" # Chose street
        lead_text = "A: op, C: ned, B: næste punkt" # A: up, C: down, B: Next inout
        display_address()
        return

    if set_address:
        if pin == button_b:
            index += 1
            index %= len(settings)
            top_text = "Vælg "+ settings[index] # Chose settings[index]
            changed = True

        if pin == button_a:
            adjust = 1
            changed = True

        if pin == button_c:
            adjust = -1
            changed = True

        if settings[index] == "gade":
            street_index += adjust
            street_index %= len(streets)

        if settings[index] == "tiere":
            tens += adjust*10

        if settings[index] == "enere":
            ones += adjust

        if settings[index] == "slut":
            set_address = False
            changed = True
            top_text = "Bilen står ud for:" # The car is in front of
            address = streets[street_index]+" "+str(tens+ones)
            lead_text = "Tryk på B for at ændre" # Press B to change
            print("Finale: "+address) # Debug text "Final: + address"
#            return

    address = streets[street_index]+" "+str(tens+ones)
    print("Efter: "+address) # Debug text "After: + address"
    display_address()

button_a.irq(trigger=machine.Pin.IRQ_FALLING, handler=button)
button_b.irq(trigger=machine.Pin.IRQ_FALLING, handler=button)
button_c.irq(trigger=machine.Pin.IRQ_FALLING, handler=button)

while True:
    if not set_address:
        address = ""
    time.sleep(0.01)
