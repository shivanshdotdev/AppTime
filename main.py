import psutil 
import time 
import json  
from pathlib import Path
from pystray import Icon, Menu, MenuItem
from threading import Thread
from html_gui import show_table
from PIL import Image

POLLING_TIME = 5 # in seconds
ALLOWED_TO_RUN = True
APP_DIR = Path.home()/"AppTime"
APP_DIR.mkdir(parents=True, exist_ok=True)
TEMP_LOG_FILE_PATH = APP_DIR/"session_log.json"
PERM_LOG_FILE_PATH = APP_DIR/"usage_log.json"

apps_to_track = [ 'aseprite.exe', 'krita.exe', 'animate.exe', 'blender.exe', 'pencil2d.exe', 'godot_v4.6-stable_win64.exe', 'capcut.exe']
icon_img_file = 'eyes.ico'

time_tracker_dict = {}  

def save_to_temporary_log() -> None:

    with open(TEMP_LOG_FILE_PATH, 'w') as file:
        json.dump(time_tracker_dict, file, indent=4)

def save_to_persistent_log(app:str, duration: float) -> None:

    temp_dict = {}

    try:
        with open(PERM_LOG_FILE_PATH, 'r') as file:
            temp_dict = json.load(file)
    except: 
        pass
    
    temp_dict[app] = duration

    with open(PERM_LOG_FILE_PATH, 'w') as file:
        json.dump(temp_dict, file, indent=4)

        
def calculate_app_run_time(key:int) -> float:
     
     with open(TEMP_LOG_FILE_PATH, 'r') as file:
        start_time_src = json.load(file)
        end_time = time.time()
        running_time = end_time - start_time_src[str(key)]["start_time"]
        return running_time

def start_tracking(app:psutil.Process) -> None:

    time_tracker_dict[app.pid] = {
        "name" : app.name().lower(), 
        "start_time" : app.create_time()
        }   

    save_to_temporary_log()

def stop_tracking(app:str) -> None:

    for app_id, name_time_dict in time_tracker_dict.items():
        if name_time_dict["name"] == app:
            del time_tracker_dict[app_id]
            app_run_time = calculate_app_run_time(app_id)
            print(f"app run time for {app} is {app_run_time}")
            save_to_persistent_log(app, app_run_time)
            break

def main() -> None:
    
    # if file exist, ignore else create the file
    TEMP_LOG_FILE_PATH.touch(exist_ok=True) # empty json at the start
    PERM_LOG_FILE_PATH.touch(exist_ok=True)

    while ALLOWED_TO_RUN:
        
        all_running_apps = [all_apps for all_apps in psutil.process_iter()]
        
        all_apps_in_str: set[str] = set(apps.name().lower() for apps in all_running_apps)
        apps_being_tracked: list[str] = [name_time_dict["name"] for pid, name_time_dict in time_tracker_dict.items()]

        print("Polling..........................")
        print(f"Tracked Apps: {time_tracker_dict}")

              
        for app_under_radar in apps_to_track:

            for app_process in all_running_apps:

                if app_under_radar not in apps_being_tracked: # app not being tracked by us
                    if app_under_radar == app_process.name().lower(): # app that should be tracked if running is running and not being tracked / started
                        start_tracking(app_process)
                        break
                
                else: # app being tracked                       
                    if app_under_radar not in all_apps_in_str: # app which was being tracked has closed
                        stop_tracking(app_under_radar)
                        break

        time.sleep(POLLING_TIME)

def system_tray() -> None:

    def quit_action(icon):
        global ALLOWED_TO_RUN
        ALLOWED_TO_RUN = False
        icon.stop()

    icon_img = Image.open(icon_img_file)
    icon = Icon("AppTime", icon_img, "AppTime", 
                menu=Menu(MenuItem("Quit", quit_action),
                          MenuItem("Show table", show_table))
        )
    icon.run()

Thread(target=system_tray, daemon=True).start()

main()