from machine import Pin, ADC
import time

pin = Pin(23,Pin.OUT)
pin.value(1)

#temp_a_pin = ADC(27)
vlaz_a_pin = ADC(Pin(26))
#button = Pin(20, Pin.IN, Pin.PULL_UP)
brz_d_vjet = Pin(18, Pin.IN, Pin.PULL_UP)
aqi_d_wifi = Pin(19, Pin.IN, Pin.PULL_UP)
vri_d_dana = Pin(20, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)
input_d = Pin(16, Pin.IN, Pin.PULL_UP)
v=True

temp = 0
vlaz = 0
brz_vjet = False
aqi = False
vri_dana = False

def get_button(button):
    return not button.value()

def get_potmtr(potmtr):
    return potmtr.read_u16()

def button_press_function():
    led.value(1)

def button_released_function():
    led.value(0)

while False:
    if get_button() == 1:
        button_press_function()
    else:
        button_released_function()

while True:
    if get_button(brz_d_vjet) == 1:
        brz_vjet = not brz_vjet
    if get_button(aqi_d_wifi) == 1:
        aqi = not aqi
    if get_button(vri_d_dana) == 1:
        vri_dana = not vri_dana
    if get_button(input_d) == 1:
        vlaz = int(input("Unesite vlaznost zraka:"))
        temp = int(input("Unesite temperaturu zraka:"))

    #vlaz = get_potmtr(vlaz_a_pin)
    #time.sleep(.2)
    #volt = round((3.3/65535)*vlaz,2)
    #percent = int(vlaz/65535*100)
    led.value(v)
    #print(v)
    print("Temperatura:", temp, "Vlaznost zraka:", vlaz,
              "Brzina vjetra:",brz_vjet, "AQ indeks:", aqi,
              "Noc:", vri_dana)
    time.sleep(.1)
