import datetime


def get_current_time():
    current_time = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    return current_time