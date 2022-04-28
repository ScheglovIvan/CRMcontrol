from main import ControlOrderStatus
import time


while True:
    try:
        ControlOrderStatus()
    except:
        pass
    
    time_sleep = 350
    print("time slip " + time_sleep + "sec")
    time.sleep(time_sleep)
