from time import sleep
import _thread
from machine import Pin, PWM

run_program = True

temperatura = lista_inputa[0]   #digital 1
vlaznost = lista_inputa[1]      #digital 1
brzinaVjetra = lista_inputa[2]  #2
aqi = lista_inputa[3]           #WIFI
daLiKisaPada = lista_inputa[4]  #digital
vrijemeDana = lista_inputa[5]   #clock


def core0_thread():
    global run_program
    counter = 0
    while run_program:
        print("button")
        #print("Main:", counter)
        #counter += 2
        sleep(1)

def core1_thread():
    global run_program
    counter = 1
    while run_program:
        #print("Backend:", counter)
        #counter += 2
        sleep(2)
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

