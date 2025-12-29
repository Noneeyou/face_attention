from datetime import datetime


def now_string():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def hours_between(start_str, end_str):
    start_dt = parse_datetime(start_str)
    end_dt = parse_datetime(end_str)
    delta = end_dt - start_dt
    return round(delta.total_seconds() / 3600, 2)
