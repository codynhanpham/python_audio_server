# Generate bat files in bat_files/{host}_{port}/ directory

# Ask user for the host IP address, use the PORT in .env file
# Create a directory with name as host_port in bat_files/ directory (also create bat_files/ directory if it doesn't exist)

# Each bat file correlates to each file name in audio/ directory
# curl -X GET http://{host}:{port}/play/{file_name}

import os
from dotenv import load_dotenv
load_dotenv()

HOST = input("Enter host IP address: ")
if not HOST:
    HOST = "localhost"
PORT = os.getenv("PORT") or 5055

if not os.path.exists(f"bat_files/{HOST}_{PORT}"):
    os.makedirs(f"bat_files/{HOST}_{PORT}")

count = 0
for file in os.listdir("audio"):
    # if not end in .wav or .mp3, skip
    if not file.endswith(".wav") and not file.endswith(".mp3"):
        continue
    
    file_name = file.split(".")[0]
    with open(f"bat_files/{HOST}_{PORT}/{file_name}.bat", "w") as bat_file:
        bat_file.write(f"curl -X GET http://{HOST}:{PORT}/play/{file_name}")
    print(f"Created bat file for {file_name}")
    count += 1
    
print()
print(f"Created {count} bat files in bat_files/{HOST}_{PORT}/ directory")

# Generate another bat named start_new_log.bat that calls /startnewlog route
with open(f"bat_files/{HOST}_{PORT}/start_new_log.bat", "w") as bat_file:
    bat_file.write(f"curl -X GET http://{HOST}:{PORT}/startnewlog")

print()
print(f"Created start_new_log.bat file in bat_files/{HOST}_{PORT}/ directory")

# Press Enter to exit
input("Press Enter to exit...")