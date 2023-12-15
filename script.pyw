# imports
from pywnp import WNPRedux
import pypresence
import time
import psutil
from psutil._common import bytes2human
import wmi
import os

computer = wmi.WMI()

# save pid in a file
def save_pid(pid):
    with open("pid.txt", "w") as file:
        file.write(str(pid))
        file.close()
        
# save the pid
save_pid(os.getpid())

# declare a array to used for sharing details between WNP and this script
arr = {"title": "", "artist": "", "platform": "", "cover": "", "title_only": ""}

# initialize pypresence as RPC
RPC = pypresence.Presence(client_id="1184558246514659398")

# Connect to Discord
RPC.connect()

# start logger
def logger(type, message):
    print(f"{type}: {message}")

# start WNP server
WNPRedux.start(
    6867, "1.0.0", logger # 6867==DC in unicode (hope it doesn't conflict with another program running on the same port)
)  


def RPCUpdate(state, details, pltform):
    
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

    
    print(start_of_day_unix)
    
    # declare the variables for the images and text
    large_image = ""
    large_text = ""
    small_image = ""
    small_text = ""

    # set the small image and text to the platform name
    if pltform == "YouTube Music":
        small_image = "ytm"
        small_text = "YouTube Music"
        
    elif pltform == "YouTube":
        small_image = "yt"
        small_text = "YouTube"
        
    else:
        large_image = "base"
        large_text = "My PC"

    # The state and details are set to the name of the GPU and CPU and the RAM usage when no song is playing
    if state == "" and pltform == "Base":
        memory = psutil.virtual_memory()
        state = f"{computer.Win32_VideoController()[0].Name} | RAM: {bytes2human(memory.used)}/{bytes2human(memory.total)}" 
        details = f"{computer.Win32_Processor()[0].Name}" 
        
    # set the large image and text to the cover and title of the song only when the song is playing
    if WNPRedux.is_started and isinstance(WNPRedux.media_info.artist, str) and WNPRedux.media_info.state == "PLAYING":
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


# Get info from the browser extension
def GetInfo():
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

def Start():
    try:
        while True:
            GetInfo()
    except KeyboardInterrupt:
        pass
    finally:
        # RPC.close()
        pass
    
Start()