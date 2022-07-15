from http import client
import psutil
import time




def running_status(child_processes):
    print(f"\nChecking proccesses:\n")
    for process in child_processes:
        check = psutil.pid_exists(process.pid)
        if check == True:
            print(f"|___{process.name} running...")
        else:
            print(f"|\n|_____{process.name} stopped!!! Restarting {process.name}...")
            for x in child_processes:
                x.kill()
                print("Signal sent, child stopped.")
            time.sleep(2)
            return False
    time.sleep(5)
    running_status(child_processes)

