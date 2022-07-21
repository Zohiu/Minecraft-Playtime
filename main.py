# Minecraft playtime viewer
import os
import getpass
import platform
import gzip
import codecs
import datetime

if platform.system() == "Linux":
    mc_folder = f"/home/{getpass.getuser()}/.minecraft/logs"
elif platform.system() == "Windows":
    mc_folder = f"C: \\Users\\{getpass.getuser()}\\AppData\\Roaming\\.minecraft\\logs"
else:
    mc_folder = input("Where is your Minecraft folder located? : ") + "\\logs"


total = 0
fails = 0
total_time = datetime.timedelta()

def getTime(line1, lastline):
    global fails, total_time
    try:
        timestart = line1.split("[")[1].split("]")[0].split(" ")[-1].split(".")[0]
        timeend = lastline.split("[")[1].split("]")[0].split(" ")[-1].split(".")[0]
        datetimestart = datetime.datetime.strptime(timestart, '%H:%M:%S')
        datetimeend = datetime.datetime.strptime(timeend, '%H:%M:%S')
        total_time += datetimeend - datetimestart
        print(f"Total: {total_time}")
    except ValueError:
        fails += 1


for file in os.listdir(mc_folder):
    total += 1
    print(f"amount: {total} fails: {fails} file: {file}")
    if file.endswith(".log"):
        with codecs.open(os.path.join(mc_folder, file), encoding="ISO 8859-15") as f:
            try:
                lines = f.readlines()
                getTime(lines[0], lines[-1])
            except IndexError:
                fails += 1

    elif file.endswith(".log.gz"):
        with gzip.open(os.path.join(mc_folder, file), "rb") as f:
            try:
                try:
                    lines = f.readlines()
                    getTime(lines[0].decode("ISO 8859-15"), lines[-1].decode("ISO 8859-15"))
                except IndexError:
                    fails += 1
            except gzip.BadGzipFile:
                input("The log file " + mc_folder + f"/{file} is corrupt. Press Enter to delete it.")
                os.remove(mc_folder + f"/{file}")
                fails += 1

print("\nYour total playtime in Minecraft is:")
print(total_time)
print(f"(Checked {total} total logs, failed on {fails} of those.)")