from http import client
import psutil
import time

def running_status(child_processes):
    print(f"\nChecking child proccesses:\n")
    state = 0
    for process in child_processes:
        check = psutil.pid_exists(process.pid)
        if check == True:
            print(f"|___{process.name} running...")
            state = 1
        else:
            print(f"|\n|_____{process.name} stopped!!! Restarting {process.name}...\n")
            for x in child_processes:
                x.kill()
            state = 0
    return state

