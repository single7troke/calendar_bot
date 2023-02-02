from datetime import datetime


def format_time(events):
    for event in events:
        if "date" in event["start"]:
            event["start"] = datetime.strptime(event["start"]["date"], "%Y-%m-%d").date().strftime("%Y-%B-%d")
        else:
            event["start"] = datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S%z").date().strftime(
                "%Y-%B-%d")

    return events


def sort_by_start_time(events):
    events = sorted(events, key=lambda x: datetime.strptime(x["start"], "%Y-%B-%d"))
    return events
