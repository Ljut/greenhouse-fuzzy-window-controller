import time
from machine import Pin, ADC, PWM
import dht
time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico W!")
time.sleep(1)
print("Molim vas pricekajte.")

pin = Pin(23,Pin.OUT)
pin.value(1)

# definicija pinova
doba_a_dana = ADC(27)
brz_a_vjet = ADC(26)
pada_d_kisa = Pin(18, Pin.IN, Pin.PULL_UP)
dht22 = dht.DHT22(Pin(17))

servo_d_pin = Pin(0)
max_duty = 7864
min_duty = 1802
frequency = 50
servo = PWM(servo_d_pin)
servo.freq (frequency)

racunaj_d_fuzzy = Pin(4, Pin.IN, Pin.PULL_UP)

led = Pin(10, Pin.OUT)
#input_d = Pin(16, Pin.IN, Pin.PULL_UP)
v=True

temp = 0
vlaz = 0
brz_vjet = 0
aqi = 0
vri_dana = 0
da_li_pada_kisa = False

def get_button(button):
    return not button.value()

def get_potmtr(potmtr):
    return potmtr.read_u16()

def get_potmtr_scaled(pot, low, high):
    raw = pot.read_u16()  # Range: 0–65535
    scaled = low + (raw / 65535) * (high - low)
    return scaled

def ispis():
    global temp 
    global vlaz 
    global brz_vjet 
    global aqi 
    global da_li_pada_kisa 
    global vri_dana 
    #global rtc
    print()
    #print("RTC: ",rtc.datetime())
    print("Temperatura:", temp)
    print( "Vlaznost zraka:", vlaz)
    print("Brzina vjetra:",brz_vjet)
    print( "AQ indeks:", aqi)
    print("Doba dana:", vri_dana)


import network
import urequests
import ujson

print("Spajanje na WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")
#wlan.connect('Bbox-0488C286', 'Ua5fxZpMraJLdLF3jE')
while not wlan.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Konektovan!\nProzor je zatvoren.")
servo.duty_u16(min_duty)
time.sleep(.2)
print(wlan.ifconfig())

def post_request_aqi(url, grad):
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = "&"
    """
    r = requests.post(url, json={"grad": grad})
    print(r.json())

def post_request_fuzzy(url, vektor):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    form_data = {
        "TemperaturaZraka":vektor[0],
        "VlaznostZraka":vektor[1],
        "BrzinaVjetra":vektor[2],
        "AQI":vektor[3],
        "DaLiPadaKisa":vektor[4],
        "VrijemeDana":vektor[5]
    }
    # Convert dict to URL-encoded string: key1=value1&key2=value2...
    payload = "&".join(f"{k}={v}" for k, v in form_data.items())

    try:
        print("Salje se zahtjev ka",url)
        response = urequests.post(url, data=payload, headers=headers)
        print(response)
        result = response.text#response.json()
        response.close()
        return result
    except Exception as e:
        print("POST failed:", e)
        return {"error": str(e)}

print("Spreman. Namjestite vrijednosti pa pritisnite crveno dugme.")
print("Ako vam se ne registruje pritisak dugmeta, pritisnite ga ponovno.")

while True:
    dht22.measure() 
    # citaj doba dana
    vri_dana = get_potmtr_scaled(doba_a_dana, 0, 24)

    # citaj brzinu vjetra
    brz_vjet = get_potmtr_scaled(brz_a_vjet, 0, 32.4)

    # citaj da li pada kisa
    if get_button(pada_d_kisa) == 1:
        da_li_pada_kisa = not da_li_pada_kisa
        led.value(da_li_pada_kisa)

    # citaj vlaznost zraka
    vlaz=dht22.humidity()

    # Citaj temperaturu zraka
    temp=dht22.temperature()

    # Računaj fuzzy
    if get_button(racunaj_d_fuzzy) == 1:
        ispis()
        rez_dict=post_request_fuzzy(
            "https://fuzzypico.pythonanywhere.com/paradajz_fuzzy",
            [temp,vlaz,brz_vjet,aqi, int(da_li_pada_kisa),vri_dana]
        )
        print(rez_dict,"\n")
        rez_dict = ujson.loads(rez_dict)
        izbor = max(rez_dict, key=rez_dict.get)
        print("Prozor ce biti ", izbor)
        if izbor == "otvori":
            print("Prozor se otvara")
            servo.duty_u16(max_duty)
            time.sleep(2)
            pass
        elif izbor == "zatvori":
            print("Prozor se zatvara")
            servo.duty_u16(min_duty)
            time.sleep(2)
            pass
        else:
            print("Prozor ostaje kakav je bio")
            pass

    # Citaj AQI
    time.sleep(.1)