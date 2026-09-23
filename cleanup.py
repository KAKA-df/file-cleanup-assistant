from pathlib import Path
import time

folder_path = Path(input("Folder to scan: "))
if not folder_path.exists():
    print("This Path doesn't exist")
    raise SystemExit
elif not folder_path.is_dir():
    print("This Path is not a directory")
    raise SystemExit
while True:
    try:
        large_file_threshold = float(input("Large file threshold (MiB): "))
        if large_file_threshold <= 0:
            print("Enter a valid number")
            continue
        break
    except ValueError:
        print("Enter a valid number")
limit_bytes = large_file_threshold * 1024 ** 2

while True:
    try:
        limit_days = int(input("Old file threshold (days): "))      
        if limit_days <= 0:
            print("Enter a valid number")
            continue
        break
    except ValueError:
        print("Enter a valid number")

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

flagged_files = []
scanned_count = 0
flagged_count = 0
flagged_bytes = 0

for item in folder_path.rglob("*"):
    if item.is_file():
        try:
            stat_info = item.stat()
        except PermissionError:
            print("Skipped: ", item)
            continue

        byte_count = stat_info.st_size
        size, unit = file_size(byte_count)

        modified_time = stat_info.st_mtime
        age_seconds = time.time() - modified_time
        age_days = age_seconds / (60 * 60 * 24)

        flag = flag_test(byte_count, age_days)
    
        scanned_count += 1

        if flag:
            file_info = (item, byte_count, size, unit, age_days, flag)
            flagged_files.append(file_info)
            flagged_count += 1
            flagged_bytes += byte_count

flagged_files.sort(key=lambda x: x[1], reverse=True)
for item, byte_count, size, unit, age_days, flag in flagged_files:
    print(item, "\nSize: ", round(size, 2), unit, "\nAge: ", round(age_days), "days", "\nFlag: ", flag, "\n")

flagged_size, flagged_unit = file_size(flagged_bytes)
print("----------------------------")
print("Files scanned: ", scanned_count, "\nFiles flagged: ", flagged_count, "\nTotal flagged size: ", round(flagged_size, 2), flagged_unit)