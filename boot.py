from machine import Pin, ADC
from time import sleep
import dht

dht22 = ADC(Pin(22))

temperatur = ADC(Pin(26))
vlaznost = ADC(Pin(26))
daLiKisaPada = Pin(21, Pin.IN, Pin.PULL_DOWN)

while True:
    
    dht22.measure()
    temp = dht22.temperature()
    hum = dht22.humidity()
    daLiKisaPada.value()
    
    led.value()
    print("Da li kisa pada:",daLiKisaPada.value())
    sleep(2)

temperatura = lista_inputa[0]   #digital 1
vlaznost = lista_inputa[1]      #digital 1
brzinaVjetra = lista_inputa[2]  #2
aqi = lista_inputa[3]           #WIFI
daLiKisaPada = lista_inputa[4]  #digital
vrijemeDana = lista_inputa[5]   #clock