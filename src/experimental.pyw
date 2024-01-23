import discordsdk as dsdk
import time

application_id = 1184558246514659398
app = dsdk.Discord(application_id, dsdk.CreateFlags.default)
activity_manager = app.get_activity_manager()

activity = dsdk.Activity()
activity.state = "Testing Game SDK"
activity.details = "Testing Game SDK"
activity.timestamps.start = 0

activity_manager.update_activity(activity, lambda result: print("Activity updated."))

timer = 0

while 1:
    time.sleep(1/10)
    app.run_callbacks()

    timer += 1
    if timer == 600:  # clear activity after 60 seconds
        activity_manager.clear_activity(lambda result: debug_callback("clear_activity", result))