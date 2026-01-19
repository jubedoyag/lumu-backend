import re
from time import gmtime
from datetime import datetime


def is_ipv4_valid(ip_address):
    match = re.match(r"(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})", ip_address)

    if any(int(octet) > 255 for octet in match.groups()):
        return False

    return bool(match)


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
        raise Exception("Invalid timestamp format")

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

