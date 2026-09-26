from pathlib import Path
from send2trash import send2trash
import time
import hashlib

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

def file_hash(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as file:
        while True:
            data = file.read(1024 * 1024)
            if not data:
                break

            hasher.update(data)
    return hasher.hexdigest()

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
size_groups = {}
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

        if byte_count in size_groups:
            size_groups[byte_count].append(item)
        else:
            size_groups[byte_count] = [item]            
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

for byte_count, files in size_groups.items():
    if len(files) >= 2:
        hash_groups = {}
        for each_file in files:
            try:
                hash_code = file_hash(each_file)
            except (PermissionError, FileNotFoundError):
                print("Skipped hashing: ", each_file)
                continue

            if hash_code in hash_groups:
                hash_groups[hash_code].append(each_file)
            else:
                hash_groups[hash_code] = [each_file]
        for hash_code, duplicate_files in hash_groups.items():
            if len(duplicate_files) >= 2:
                print("\nThese are duplicate files: ")
                for duplicate_file in duplicate_files:
                    print(duplicate_file)
                size, unit = file_size(byte_count)
                print("Size: ", size, unit, "\n")

flagged_files.sort(key=lambda x: x[1], reverse=True)
for number, (item, byte_count, size, unit, age_days, flag) in enumerate(flagged_files, start=1):
    print(f"[{number}]", 
          item, 
          "\nSize: ", round(size, 2), unit, 
          "\nAge: ", round(age_days), "days", 
          "\nFlag: ", flag,
          "\n")

flagged_size, flagged_unit = file_size(flagged_bytes)
print("----------------------------")
print("Files scanned: ", scanned_count, "\nFiles flagged: ", flagged_count, "\nTotal flagged size: ", round(flagged_size, 2), flagged_unit)

if not flagged_files:
    print("No files need cleanup")
    raise SystemExit  

while True:
    try:
        selection = int(input("Choose a file number: "))
        if selection < 1 or selection > len(flagged_files):
            print("Enter a valid file number")
            continue
        break
    except ValueError:
        print("Enter a valid file number") 
selected_file = flagged_files[selection - 1]
print("Selected file: ", selected_file[0])
while True:
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == 'y':
        print("Confirmed: ", selected_file[0])
        send2trash(selected_file[0])
        break
    elif confirm == 'n':
        print("Cancelled")
        break
    else:
        print("Enter y or n: ")