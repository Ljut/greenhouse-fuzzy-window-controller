from time import sleep
import _thread
from machine import Pin, ADC

run_program = True
"""
temperatura = lista_inputa[0]   #digital 1
vlaznost = lista_inputa[1]      #digital 1
brzinaVjetra = lista_inputa[2]  #2
aqi = lista_inputa[3]           #WIFI
daLiKisaPada = lista_inputa[4]  #digital
vrijemeDana = lista_inputa[5]   #clock
"""
"""
temp_a_pin = ADC(Pin(27))
vlaz_a_pin = ADC(Pin(26))
brz_d_vjet = Pin(18, Pin.IN, Pin.PULL_DOWN)
aqi_d_wifi = Pin(19, Pin.IN, Pin.PULL_DOWN)
vri_d_dana = Pin(20, Pin.IN, Pin.PULL_DOWN)

temp = 0
vlaz = 0
brz_vjet = False
aqi = False
vri_dana = False

def core0_thread():
    global run_program
    global temp
    global vlaz
    global brz_vjet
    global aqi
    global vri_dana
    counter = 0
    while run_program:
        temp = temp_a_pin.read_u16()
        vlaz = vlaz_a_pin.read_u16()
        print("Temperatura:", temp, "Vlaznost zraka:", vlaz,
              "Brzina vjetra:",brz_vjet, "AQ indeks:", aqi,
              "Noc:", vri_dana)
        #print("button")
        #print("Main:", counter)
        #counter += 2
        sleep(1)

def core1_thread():
    global run_program
    global temp
    global vlaz
    global brz_vjet
    global aqi
    global vri_dana
    counter = 1
    while run_program:
        sleep(1)
        
        #brz_vjet = brz_d_vjet.value()
        #aqi = aqi_d_wifi.value()
        #vri_dana = vri_d_dana.value()
    print("Backend thread exiting.")

# Start second thread
_thread.start_new_thread(core1_thread, ())

try:
    core0_thread()
except BaseException as e:
    print("Caught exception:", type(e).__name__, "-", e)
    run_program = False
    sleep(2)  # Give time for core1 to exit
    print("End.")
"""
"""
pot = ADC(Pin(26))

while True:
    pot_v = pot.read_u16()
    print(pot_v)
    sleep(.1)
"""
led = Pin(20, Pin.OUT)
button = Pin(21, Pin.IN, Pin.PULL_DOWN)

while True:
  led.value(button.value())
  sleep(0.1)
  print(button.value())
