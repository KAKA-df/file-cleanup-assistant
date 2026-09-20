from pathlib import Path
import time

a_copy = Path("D:/") / "Acopy"
limit_bytes = 100 * 1024
limit_days = 90

def file_size(byte_count):
    if byte_count < 1024:
        return byte_count, "bytes"
    elif byte_count < 1024 ** 2:
        return byte_count / 1024, "KiB"
    elif byte_count < 1024 ** 3:
        return byte_count / 1024 ** 2, "MiB"
    else:
        return byte_count / 1024 ** 3, "GiB"

def flag_test(byte_count, days):
    if byte_count > limit_bytes and days > limit_days:
        return "LARGE, OLD"
    elif byte_count > limit_bytes:
        return "LARGE"
    elif days > limit_days:
        return "OLD"

scanned_count = 0
flagged_count = 0
flagged_bytes = 0

for item in a_copy.rglob("*"):
    if item.is_file():
        byte_count = item.stat().st_size
        size, unit = file_size(byte_count)

        modified_time = item.stat().st_mtime
        age_seconds = time.time() - modified_time
        age_days = age_seconds / (60 * 60 * 24)

        flag = flag_test(byte_count, age_days)

        scanned_count += 1

        if flag:
            print(item, round(size, 2), unit, round(age_days), "days old", "\nFlag:", flag)
            flagged_count += 1
            flagged_bytes += byte_count

flagged_size, flagged_unit = file_size(flagged_bytes)
print("\n ----------------------------")
print("Files scanned: ", scanned_count, "\nFiles flagged: ", flagged_count, "\nTotal flagged size: ", round(flagged_size, 2), flagged_unit)