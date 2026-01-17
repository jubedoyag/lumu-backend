import re
from time import gmtime
from datetime import datetime


def parse_date_to_utc(timestamp):

    match = re.match(r"^\d{1,10}$", str(timestamp))
    if match:
        parsed_time = gmtime(int(timestamp))
        parsed_time = datetime(*tuple(parsed_time)[:6]).isoformat()
        return parsed_time + ".000Z"

    match = re.match(r"^\d{11,}$", str(timestamp))
    if match:
        time_ms = str(timestamp)[-3:]
        timestamp = str(timestamp)[:-3]

        parsed_time = gmtime(int(timestamp))
        parsed_time = datetime(*tuple(parsed_time)[:6]).isoformat()

        return f"{parsed_time}.{time_ms}Z"

    match = re.match(
        r"(\d{4})\D(\d{2})\D(\d{2})(\D(\d{2})\D(\d{2})\D(\d{2})(\D(\d{3}))?)?",
        str(timestamp)
    )
    if not match:
        raise Exception("Invalid timestamp")

    if not match.group(4):
        groups = (1, 2, 3)
        matched_groups = tuple(map(int, match.group(*groups)))
        return datetime(*matched_groups).isoformat(timespec="milliseconds") + "Z"

    if not match.group(8):
        groups = (1, 2, 3, 5, 6, 7)
        matched_groups = tuple(map(int, match.group(*groups)))
        return datetime(*matched_groups).isoformat(timespec="milliseconds") + "Z"

    groups = (1, 2, 3, 5, 6, 7, 9)
    matched_groups = list(map(int, match.group(*groups)))
    matched_groups[-1] *= 1000
    return datetime(*matched_groups).isoformat(timespec="milliseconds") + "Z"


def main():
    TIMESTAMPS = [
        '2021-12-03T16:15:30.235Z',
        '2021-12-03T16:15:30.235',
        '2021-10-28T00:00:00.000',
        '2011-12-03T10:15:30',
        1726668850124,
        '1726668850124',
        1726667942,
        '1726667942',
        969286895000,
        '969286895000',
        '2021-1203 16:15:30',
        3336042095,
        '3336042095',
        3336042095000,
        '3336042095000',
        '2021-12-03 16:15:30',
    ]

    for ts in TIMESTAMPS:
        try:
            print(f"- Timestamp: {ts}\t- Parsed timestamp: {parse_date_to_utc(ts)}")
        except:
            print(f"[{datetime.now().isoformat()}] [WARN] Unexpected format: {ts}")


if __name__ == "__main__":
    main()

