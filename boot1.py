from time import sleep
import _thread

run_program = True

def core0_thread():
    global run_program
    counter = 0
    while run_program:
        print("Main:", counter)
        counter += 2
        sleep(1)

def core1_thread():
    global run_program
    counter = 1
    while run_program:
        print("Backend:", counter)
        counter += 2
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

