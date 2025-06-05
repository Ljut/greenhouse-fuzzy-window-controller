import network
import time
import urequests # handles making and servicing network requests

print("Connecting to WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")
#wlan.connect('Bbox-0488C286', 'Ua5fxZpMraJLdLF3jE')
while not wlan.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")
print(wlan.ifconfig())


"""# Example 1. Make a GET request for google.com and print HTML
# Print the html content from google.com
print("1. Querying google.com:")
r = urequests.get("http://www.google.com")
print(r.content)
r.close()"""
"""
# Example 2. urequests can also handle basic json support! Let's get the current time from a server
print("\n\n2. Querying the current GMT+0 time:")
r = urequests.get("http://date.jsontest.com") # Server that returns the current GMT+0 time.
print(r.json())
a = r.json()
print(a['milliseconds_since_epoch'])
#t= float(int(a['milliseconds_since_epoch']))
print(time.time())
print(time.localtime(time.time()))"""


def get_time():
    response = urequests.get("http://worldtimeapi.org/api/timezone/Europe/Paris")
    data = response.json()
    print(data)
    timestamp = data["unixtime"]
    return timestamp

current_time = get_time() 
print(current_time )
formatted_time = time.localtime(current_time)
#Print the time to the console or perform any other actions with it:
 
print(formatted_time)