import os
import time
import json
import webbrowser
import psutil
import discord_webhook
import configparser
import customtkinter
import logging
import sys

logging.basicConfig(
    filename='crash.log',  # Optional: Specify a file to log to
    level=logging.WARNING,  # Set the minimum level for logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Customize the log format
)

logger = logging.getLogger('mylogger')


def my_handler(types, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))
    print("Check crash.log for info on this crash.")
    time.sleep(10)
    sys.exit()


# exception handler / logger
sys.excepthook = my_handler

# create UI window
root = customtkinter.CTk()
root.title("maxstellar's Biome Macro")
root.geometry('550x225')
root.resizable(False, False)
dirname = os.path.dirname(__file__)
root.iconbitmap(dirname + '\\icon.ico')

# read configuration file
config_name = 'config.ini'
config = configparser.ConfigParser()
if not os.path.exists(config_name):
    print("Config file not found, creating one...")
    config['Webhook'] = {'webhook_url': "", 'private_server': ""}
    with open(config_name, 'w') as configfile:
        config.write(configfile)
config.read(config_name)
webhookURL = customtkinter.StringVar(root, config['Webhook']['webhook_url'])
psURL = customtkinter.StringVar(root, config['Webhook']['private_server'])

# constants
roblox_open = False
log_directory = os.path.expandvars(r"%localappdata%\Roblox\logs")
packages_path = os.path.expandvars(r"%localappdata%\Packages")
roblox_folder = None
roblox_log_path = None
roblox_version = None
biome_colors = {"NORMAL": "ffffff", "PUMPKIN MOON": "d55f09", "GRAVEYARD": "454545", "SAND STORM": "F4C27C", "HELL": "5C1219", "STARFALL": "6784E0", "CORRUPTION": "9042FF", "NULL": "000000", "GLITCHED": "65FF65", "WINDY": "91F7FF", "SNOWY": "C4F5F6", "RAINY": "4385FF"}


def detect_roblox_version():
    global roblox_log_path, roblox_version, roblox_folder
    for proc in psutil.process_iter(['name']):
        if 'RobloxPlayerBeta.exe' in proc.info['name']:
            if roblox_version != 'player':
                roblox_version = 'player'
                roblox_log_path = log_directory
            return 'player'
        elif 'Windows10Universal.exe' in proc.info['name']:
            if roblox_version != 'store':
                roblox_version = 'store'
                for folder in os.listdir(packages_path):
                    if folder.startswith("ROBLOXCORPORATION.ROBLOX"):
                        roblox_folder = folder
                        roblox_log_path = os.path.join(packages_path, roblox_folder, "LocalState", "logs")
            return 'store'
    return None


def get_latest_log_file():
    if roblox_log_path:
        files = [f for f in os.listdir(roblox_log_path) if f.endswith(".log")]
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(roblox_log_path, f)))
        return os.path.join(roblox_log_path, latest_file)
    return None


def is_roblox_running():
    return detect_roblox_version() is not None


def check_for_hover_text(file, roblox_open):
    global roblox_version
    last_event = None
    file.seek(0, 2)
    while True:
        check = is_roblox_running()
        if check:
            line = file.readline()
            if line:
                if '"command":"SetRichPresence"' in line:
                    try:
                        json_data_start = line.find('{"command":"SetRichPresence"')
                        if json_data_start != -1:
                            json_data = json.loads(line[json_data_start:])
                            event = json_data.get("data", {}).get("largeImage", {}).get("hoverText", "")
                            if event and event != last_event:
                                webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                if event == "NORMAL":
                                    if last_event is not None:
                                        print(time.strftime('%H:%M:%S') + f": Biome Ended - " + last_event)
                                        embed = discord_webhook.DiscordEmbed(
                                            title="[" + time.strftime('%H:%M:%S') + "]",
                                            color=biome_colors[last_event],
                                            description="> ## Biome Ended - " + last_event)
                                        embed.set_thumbnail(url="https://maxstellar.github.io/biome_thumb/" + last_event.replace(" ", "%20") + ".png")
                                        webhook.add_embed(embed)
                                        webhook.execute()
                                    else:
                                        pass
                                else:
                                    print(time.strftime('%H:%M:%S') + f": Biome Started - {event}")
                                    embed = discord_webhook.DiscordEmbed(
                                        title="[" + time.strftime('%H:%M:%S') + "]",
                                        color=biome_colors[event],
                                        description="> ## Biome Started - " + event)
                                    embed.set_thumbnail(url="https://maxstellar.github.io/biome_thumb/" + event.replace(" ", "%20") + ".png")
                                    webhook.add_embed(embed)
                                    if event == "GLITCHED":
                                        webhook.set_content("@everyone " + psURL.get())
                                    webhook.execute()
                                last_event = event
                    except json.JSONDecodeError:
                        print("Error decoding JSON")
            else:
                time.sleep(0.1)
        else:
            print("Roblox is closed, waiting for Roblox to start...")
            close_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
            close_embed = discord_webhook.DiscordEmbed(
                description="[" + time.strftime('%H:%M:%S') + "]: Roblox was closed/crashed.")
            close_webhook.add_embed(close_embed)
            close_webhook.execute()
            while True:
                check = is_roblox_running()
                if check:
                    break
                time.sleep(0.05)
            if roblox_version == "player":
                print("Detected Roblox Player.")
                time.sleep(5)
            else:
                print("Detected Roblox Microsoft Store.")
                time.sleep(5)
            latest_log = get_latest_log_file()
            if not latest_log:
                print("No log files found.")
                return
            with open(latest_log, 'r', encoding='utf-8') as file:
                print(f"Using log file: {latest_log}")
                print()
                check_for_hover_text(file, False)


def open_url(url):
    webbrowser.open(url, new=2, autoraise=True)


def init():
    global roblox_open
    # write new settings to config
    config.set('Webhook', 'webhook_url', webhookURL.get())
    config.set('Webhook', 'private_server', psURL.get())

    # Writing our configuration file to 'example.ini'
    with open(config_name, 'w+') as configfile:
        config.write(configfile)

    root.destroy()

    # start webhook
    starting_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
    starting_embed = discord_webhook.DiscordEmbed(
        description="[" + time.strftime('%H:%M:%S') + "]: Macro started!")
    starting_webhook.add_embed(starting_embed)
    starting_webhook.execute()

    # start detection
    if is_roblox_running():
        roblox_open = True
        print("Roblox is open.")
    else:
        print("Roblox is closed, waiting for Roblox to start...")
        while True:
            check = is_roblox_running()
            if check:
                break
            time.sleep(0.1)
    if not roblox_open:
        if roblox_version == "player":
            print("Detected Roblox Player.")
            time.sleep(1.5)
        else:
            print("Detected Roblox Microsoft Store.")
            time.sleep(3.5)
    latest_log = get_latest_log_file()
    if not latest_log:
        print("No log files found.")
        return
    with open(latest_log, 'r', encoding='utf-8') as file:
        print(f"Using log file: {latest_log}")
        print()
        check_for_hover_text(file, roblox_open)


print("Welcome to maxstellar's Biome Macro!")
print()
print("Subscribe to my YouTube channel: https://youtube.com/@maxstellar_")
print("If there are any issues with the macro, join our Discord server: https://discord.gg/solsniper")
print()
print("ALL CREDITS GO TO maxstellar, dannw, and yeswe")
print("--------------------------------------------")

webhook_label = customtkinter.CTkLabel(root, text="Webhook URL:", font=customtkinter.CTkFont(size=20))
webhook_label.grid(column=0, row=0, columnspan=4, padx=(10, 40), pady=(20, 0), sticky="w")

webhook_field = customtkinter.CTkEntry(root, font=customtkinter.CTkFont(size=20), width=300, textvariable=webhookURL)
webhook_field.grid(row=0, column=1, padx=(33, 0), pady=(20, 0), sticky="w")

ps_label = customtkinter.CTkLabel(root, text="Private Server URL:", font=customtkinter.CTkFont(size=20))
ps_label.grid(column=0, row=1, columnspan=4, padx=(10, 40), pady=(20, 0), sticky="w")

ps_field = customtkinter.CTkEntry(root, font=customtkinter.CTkFont(size=20), width=300, textvariable=psURL)
ps_field.grid(row=1, column=1, padx=(78, 0), pady=(20, 0), sticky="w")

start_button = customtkinter.CTkButton(root, text="Start", font=customtkinter.CTkFont(size=20, weight="bold"), width=75, command=init)
start_button.grid(row=2, column=0, padx=(10, 0), pady=(20, 0), sticky="w")

donate_button = customtkinter.CTkButton(root, text="YouTube", font=customtkinter.CTkFont(size=20, weight="bold"), width=75, command=lambda: open_url("https://youtube.com/@maxstellar_"))
donate_button.grid(row=3, column=0, padx=(10, 0), pady=(20, 0), sticky="w")

support_button = customtkinter.CTkButton(root, text="Join Discord for help", font=customtkinter.CTkFont(size=20, weight="bold"), width=75, command=lambda: open_url("https://discord.gg/solsniper"))
support_button.grid(row=3, column=1, padx=(10, 0), pady=(20, 0), sticky="w")

root.mainloop()
