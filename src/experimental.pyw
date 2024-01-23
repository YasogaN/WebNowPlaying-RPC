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
