from dsdk import Discord as dsdk
from dsdk.enum import ActivityType, CreateFlags
from dsdk.model import Activity
import time

app = dsdk(1184558246514659398,CreateFlags.NoRequireDiscord)
activityManager = app.GetActivityManager

activity = Activity()
activity.State = "Testing Game SDK"
activity.Details = "Testing Game SDK"
activity.Assets.LargeImage = "ytm"
activity.Assets.LargeText = "Testing Game SDK"
activity.Assets.SmallImage = "ytm"
activity.Assets.SmallText = "Testing Game SDK"
activity.Type = ActivityType.Listening

activityManager.UpdateActivity(activity, lambda result: debugCallback("UpdateActivity", result))

timer = 0

while 1:
    time.sleep(1/10)
    app.RunCallbacks()
    
    timer += 1
    if timer == 600: # clear activity after 60 seconds
        activityManager.ClearActivity(lambda result: debugCallback("ClearActivity", result))