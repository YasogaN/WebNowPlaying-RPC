# imports
from pywnp import WNPRedux
import pypresence
import time
import psutil
from psutil._common import bytes2human
import wmi
import os
import traceback
import subprocess

computer = wmi.WMI()

# stop other scripts from running
def stop_other_scripts():
    if os.path.isfile("src/pid.txt"):
        with open("src/pid.txt", "r") as file:
            pid = file.read()
            file.close()
        os.system("taskkill /PID " + str(pid) + " /F")
        os.remove("src/pid.txt")
    else:
        pass

stop_other_scripts()

# save pid in a file
def save_pid(pid):
    with open("src/pid.txt", "w") as file:
        file.write(str(pid))
        file.close()

# save the pid
save_pid(os.getpid())

# get the start time of the script
startTime = time.time()

# declare a array to used for sharing details between WNP and this script
arr = {"title": "", "artist": "", "platform": "", "cover": "", "title_only": ""}

# initialize pypresence as RPC
RPC = pypresence.Presence(client_id="1184558246514659398")

# Connect to Discord
RPC.connect()

# delete previous log
try:
    os.remove("src/log.txt")
except:
    pass

# start logger
def logger(time, type, message):
    print(f"[{time}] - {type}: {message}")
    log = open("src/log.txt", "a")
    log.write(f"[{time}] - {type}: {message}\n")
    log.close()

# start WNP server
WNPRedux.start(
    6867, "1.0.0", logger # 6867==DC in unicode (hope it doesn't conflict with another program running on the same port)
)  


def RPCUpdate(state, details, pltform):
    try:
        # get the start of the day in unix time
        current_date = time.localtime()
        start_of_day = time.struct_time(
            (
                current_date.tm_year,
                current_date.tm_mon,
                    current_date.tm_mday,
                0,
                0,
                0,
                current_date.tm_wday,
                current_date.tm_yday,
                current_date.tm_isdst,
            )
        )
        start_of_day_unix = time.mktime(start_of_day)
        
        # declare the variables for the images and text
        large_image = ""
        large_text = ""
        small_image = ""
        small_text = ""
        
        # set the small image and text to the platform name
        if pltform == "Apple Music":
            small_image = "apm"
            small_text = "Apple Music"
        
        elif pltform == "Bandcamp":
            small_image = "bc"
            small_text = "Bandcamp"
        
        elif pltform == "Deezer":
            small_image = "dz"
            small_text = "Deezer"
        
        elif pltform == "Invidious":
            small_image = "inv"
            small_text = "Invidious"
        
        elif pltform == "Jellyfin":
            small_image = "jf"
            small_text = "Jellyfin"
        
        elif pltform == "Kick":
            small_image = "kk"
            small_text = "Kick"
        
        elif pltform == "Navidrome":
            small_image = "nvd"
            small_text = "Navidrome"
        
        elif pltform == "Netflix":
            small_image = "ntf"
            small_text = "Netflix"
        
        elif pltform == "Pandora":
            small_image = "pnd"
            small_text = "Pandora"
        
        elif pltform == "Plex":
            small_image = "plx"
            small_text = "Plex"
        
        elif pltform == "Radio Addict":
            small_image = "rda"
            small_text = "Radio Addict"
        
        elif pltform == "Spotify":
            small_image = "spt"
            small_text = "Spotify"
        
        elif pltform == "SoundCloud":
            small_image = "sdc"
            small_text = "SoundCloud"
        
        elif pltform == "Tidal":
            small_image = "td"
            small_text = "Tidal"
        
        elif pltform == "Twitch":
            small_image = "twh"
            small_text = "Twitch"
        
        elif pltform == "VK":
            small_image = "vk"
            small_text = "VK"
        
        elif pltform == "Yandex Music":
            small_image = "yd"
            small_text = "Yandex Music"
        
        elif pltform == "YouTube":
            small_image = "yt"
            small_text = "YouTube"
        
        elif pltform == "YouTube Embeds":
            small_image = "yt"
            small_text = "YouTube"
        
        elif pltform == "YouTube Music":
            small_image = "ytm"
            small_text = "YouTube Music"
            
        elif pltform == "Windows Media Session":
            large_image = "wms"
            large_text = "Windows Media Session"
            state = "Windows Media Session"
        else:
            large_image = "base"
            large_text = "My PC"
        
        # The state and details are set to the name of the GPU and CPU and the RAM usage when no song is playing
        if state == "" and pltform == "Base":
            memory = psutil.virtual_memory()
            state = f"{computer.Win32_VideoController()[0].Name} | RAM: {bytes2human(memory.used)}/{bytes2human(memory.total)}" 
            details = f"{computer.Win32_Processor()[0].Name}" 
        
        # set the large image and text to the cover and title of the song only when the song is playing
        if WNPRedux.is_started and isinstance(WNPRedux.media_info.artist, str) and WNPRedux.media_info.state == "PLAYING" and pltform != "Windows Media Session":
            large_image = arr["cover"]
            large_text = arr["title_only"]
        else:
            large_image = large_image
            large_text = large_text
        
        # idk why i had to this but it was giving me errors if i didnt
        if not large_image:
            large_image = "default_image"
        if not large_text:
            large_text = "default_image"
        if not small_image:
            small_image = "default_image"
        if not small_text:
            small_text = "default_image"
        
        # Update RPC
        RPC.update(
            state=state,
            details=details,
            small_image=small_image,
            small_text=small_text,
            large_image=large_image,
            large_text=large_text,
            start=start_of_day_unix 
        )
        
        logger(time.strftime("%H:%M:%S", time.localtime()), "INFO", f"Updating RPC with {state}, {details}, {pltform}")
    except Exception as e:
        logger(time.strftime("%H:%M:%S", time.localtime()), "ERROR", f"Error updating RPC: {str(e)}")
        traceback.print_exc()

# Get info from the browser extension
def GetInfo():
    try:
        time.sleep(0.25)
        
        # Check if user has started playing media
        if (
        WNPRedux.is_started
        and isinstance(WNPRedux.media_info.artist, str)
        and WNPRedux.media_info.state == "PLAYING"
        ):
            # get info via WNP
            arr["artist"] = WNPRedux.media_info.artist
            arr["title"] = f"{WNPRedux.media_info.title} {WNPRedux.media_info.position}/{WNPRedux.media_info.duration}"
            arr["title_only"] = f"{WNPRedux.media_info.title}"
            arr["platform"] = WNPRedux.media_info.player_name
            arr["cover"] = WNPRedux.media_info.cover_url
            RPCUpdate(arr["artist"], arr["title"], arr["platform"])
        else:
            # if the user is not playing media load the My PC view
            RPCUpdate("", "", "Base")
    except Exception as e:
        logger(time.strftime("%H:%M:%S", time.localtime()), "ERROR", f"Error getting info: {str(e)}")
        traceback.print_exc()

# Get uptime of process
def GetUptime():
    return time.time() - startTime

# restart the script
def Restart():
    if GetUptime() > 3600:
        subprocess.Popen(["pythonw", "src/script.pyw"], creationflags=subprocess.CREATE_NO_WINDOW, shell=False)
        os._exit(0)
    else:
        pass

# start the script
def Start():
    try:
        while True:
            GetInfo()
            Restart()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger(time.strftime("%H:%M:%S", time.localtime()), "ERROR", f"Error in main loop: {str(e)}")
        traceback.print_exc()
        Restart()
    finally:
        # RPC.close()
        pass


Start()