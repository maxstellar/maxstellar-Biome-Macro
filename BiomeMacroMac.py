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
from PIL import Image
import subprocess
import platformdirs

logging.basicConfig(
    filename='crash.log',  # Optional: Specify a file to log to
    level=logging.INFO,  # Set the minimum level for logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Customize the log format
)

logger = logging.getLogger('mylogger')


def popup(message, title):
    applescript = """
    display dialog "{message}" ¬
    with title "{title}" ¬
    with icon caution ¬
    buttons {{"OK"}}
    """.format(message=message, title=title)

    subprocess.call("osascript -e '{}'".format(applescript), shell=True)


def my_handler(types, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))
    popup("Check crash.log for information on this crash.", "Crashed!")
    sys.exit()


# exception handler / logger
sys.excepthook = my_handler

# create UI window
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title("maxstellar's Biome Macro")
root.geometry('505x235')
root.resizable(False, False)
dirname = os.path.dirname(__file__)
tabview = customtkinter.CTkTabview(root, width=505, height=180)
tabview.grid(row=0, column=0, sticky='nsew', columnspan=75)
tabview.add("Webhook")
tabview.add("Macro")
tabview.add("Credits")
tabview._segmented_button.configure(font=customtkinter.CTkFont(family="Segoe UI", size=16))
tabview._segmented_button.grid(sticky="w", padx=15)

# read configuration file
config_name = 'config.ini'
config = configparser.ConfigParser()
if not os.path.exists(config_name):
    logger.info("Config file not found, creating one...")
    print("Config file not found, creating one...")
    config['Webhook'] = {'webhook_url': "", 'private_server': "", 'multi_webhook': "0", 'multi_webhook_urls': ""}
    config['Macro'] = {'aura_detection': "0"}
    with open(config_name, 'w') as configfile:
        config.write(configfile)
config.read(config_name)
webhookURL = customtkinter.StringVar(root, config['Webhook']['webhook_url'])
psURL = customtkinter.StringVar(root, config['Webhook']['private_server'])
multi_webhook = customtkinter.StringVar(root, config['Webhook']['multi_webhook'])
if multi_webhook.get() != "1" and webhookURL.get() == "Multi-Webhook On":
    webhookURL.set("")
webhook_urls_string = customtkinter.StringVar(root, config['Webhook']['multi_webhook_urls'])
webhook_urls = webhook_urls_string.get().split()

# variables
roblox_open = False
log_directory = platformdirs.user_log_dir("Roblox", None)
biome_colors = {"NORMAL": "ffffff", "SAND STORM": "F4C27C", "HELL": "5C1219", "STARFALL": "6784E0", "CORRUPTION": "9042FF", "NULL": "000000", "GLITCHED": "65FF65", "WINDY": "91F7FF", "SNOWY": "C4F5F6", "RAINY": "4385FF", "DREAMSPACE": "ff7dff"}
started = False
stopped = False
destroyed = False
debug_window = False
aura_detection = customtkinter.IntVar(root, int(config['Macro']['aura_detection']))


def stop():
    global stopped
    # write config data
    config.set('Webhook', 'webhook_url', webhookURL.get())
    config.set('Webhook', 'private_server', psURL.get())
    with open(config_name, 'w+') as configfile:
        config.write(configfile)

    # end webhook
    if started and not stopped:
        if multi_webhook.get() != "1":
            if "discord.com" in webhookURL.get() and "https://" in webhookURL.get():
                ending_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                ending_embed = discord_webhook.DiscordEmbed(
                    description="[" + time.strftime('%H:%M:%S') + "]: Macro stopped.")
                ending_embed.set_footer(text="maxstellar's Biome Macro for Mac",
                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                ending_webhook.add_embed(ending_embed)
                ending_webhook.execute()

        else:
            ending_embed = discord_webhook.DiscordEmbed(
                description="[" + time.strftime('%H:%M:%S') + "]: Macro stopped.")
            ending_embed.set_footer(text="maxstellar's Biome Macro for Mac",
                             icon_url="https://maxstellar.github.io/maxstellar.png")
            for url in webhook_urls:
                ending_webhook = discord_webhook.DiscordWebhook(url=url)
                ending_webhook.add_embed(ending_embed)
                ending_webhook.execute()
    else:
        sys.exit()
    stopped = True


if multi_webhook == "1":
    if len(webhook_urls) < 2:
        popup("there's no reason to use multi-webhook... without multiple webhooks??", "bruh are you serious")
    elif len(webhook_urls) > 14:
        if len(webhook_urls) > 49:
            popup("you've gotta be doing this on purpose now... you don't need this many webhooks", "this is ridiculous")
        else:
            popup("bro you do not need this many webhooks", "okay dude wtf")
    stop()


def x_stop():
    global destroyed
    destroyed = True
    stop()


def get_latest_log_file():
    files = os.listdir(log_directory)
    paths = [os.path.join(log_directory, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def is_roblox_running():
    processes = []
    for i in psutil.process_iter():
        try:
            processes.append(i.name())
        except:
            pass
    return "RobloxPlayer" in processes


def check_for_hover_text(file):
    last_event = None
    last_aura = None
    file.seek(0, 2)
    while True:
        if keyboard.ispressed("F1"):
            stop()
        if not stopped:
            root.update()
        else:
            if not destroyed:
                root.destroy()
            sys.exit()
        check = is_roblox_running()
        if check:
            line = file.readline()
            if line:
                print(line)
                if '"command":"SetRichPresence"' in line:
                    try:
                        json_data_start = line.find('{"command":"SetRichPresence"')
                        if json_data_start != -1:
                            json_data = json.loads(line[json_data_start:])
                            event = json_data.get("data", {}).get("largeImage", {}).get("hoverText", "")
                            state = json_data.get("data", {}).get("state", "")
                            aura = state[10:-1]
                            if event and event != last_event:
                                if multi_webhook.get() != "1":
                                    if "discord.com" not in webhookURL.get() or "https://" not in webhookURL.get():
                                        popup("Invalid or missing webhook link.", "Error")
                                        stop()
                                        return
                                    webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                    if event == "NORMAL":
                                        if last_event is not None:
                                            print(time.strftime('%H:%M:%S') + f": Biome Ended - " + last_event)
                                            embed = discord_webhook.DiscordEmbed(
                                                title="[" + time.strftime('%H:%M:%S') + "]",
                                                color=biome_colors[last_event],
                                                description="> ## Biome Ended - " + last_event)
                                            embed.set_thumbnail(url="https://maxstellar.github.io/biome_thumb/" + last_event.replace(" ", "%20") + ".png")
                                            embed.set_footer(text="maxstellar's Biome Macro for Mac", icon_url="https://maxstellar.github.io/maxstellar.png")
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
                                        embed.set_footer(text="maxstellar's Biome Macro for Mac",
                                                         icon_url="https://maxstellar.github.io/maxstellar.png")
                                        webhook.add_embed(embed)
                                        if event == "GLITCHED" or event == "DREAMSPACE":
                                            webhook.set_content("@everyone " + psURL.get())
                                        webhook.execute()
                                else:
                                    if event == "NORMAL":
                                        if last_event is not None:
                                            print(time.strftime('%H:%M:%S') + f": Biome Ended - " + last_event)
                                            for url in webhook_urls:
                                                webhook = discord_webhook.DiscordWebhook(url=url)
                                                embed = discord_webhook.DiscordEmbed(
                                                    title="[" + time.strftime('%H:%M:%S') + "]",
                                                    color=biome_colors[last_event],
                                                    description="> ## Biome Ended - " + last_event)
                                                embed.set_thumbnail(
                                                    url="https://maxstellar.github.io/biome_thumb/" + last_event.replace(" ", "%20") + ".png")
                                                embed.set_footer(text="maxstellar's Biome Macro for Mac",
                                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                        else:
                                            pass
                                    else:
                                        print(time.strftime('%H:%M:%S') + f": Biome Started - {event}")
                                        for url in webhook_urls:
                                            embed = discord_webhook.DiscordEmbed(
                                                title="[" + time.strftime('%H:%M:%S') + "]",
                                                color=biome_colors[event],
                                                description="> ## Biome Started - " + event)
                                            embed.set_thumbnail(
                                                url="https://maxstellar.github.io/biome_thumb/" + event.replace(" ", "%20") + ".png")
                                            embed.set_footer(text="maxstellar's Biome Macro for Mac",
                                                             icon_url="https://maxstellar.github.io/maxstellar.png")
                                            webhook = discord_webhook.DiscordWebhook(url=url)
                                            webhook.add_embed(embed)
                                            if event == "GLITCHED" or event == "DREAMSPACE":
                                                webhook.set_content("@everyone " + psURL.get())
                                            webhook.execute()
                                last_event = event
                            if state and aura != last_aura and aura != "n":
                                if aura_detection.get() == 1 and aura != "None":
                                    if multi_webhook.get() != "1":
                                        if "discord.com" not in webhookURL.get() or "https://" not in webhookURL.get():
                                            popup("Invalid or missing webhook link.", "Error")
                                            stop()
                                            return
                                        webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                        print(time.strftime('%H:%M:%S') + f": Aura Equipped - {aura}")
                                        embed = discord_webhook.DiscordEmbed(
                                            title="[" + time.strftime('%H:%M:%S') + "]",
                                            description="> ## Aura Equipped - " + aura)
                                        embed.set_footer(text="maxstellar's Biome Macro for Mac",
                                                         icon_url="https://maxstellar.github.io/maxstellar.png")
                                        webhook.add_embed(embed)
                                        webhook.execute()
                                    else:
                                        print(time.strftime('%H:%M:%S') + f": Aura Equipped - {aura}")
                                        for url in webhook_urls:
                                            webhook = discord_webhook.DiscordWebhook(url=url)
                                            embed = discord_webhook.DiscordEmbed(
                                                title="[" + time.strftime('%H:%M:%S') + "]",
                                                description="> ## Aura Equipped - " + aura)
                                            embed.set_footer(text="maxstellar's Biome Macro for Mac",
                                                             icon_url="https://maxstellar.github.io/maxstellar.png")
                                            webhook.add_embed(embed)
                                            webhook.execute()
                                last_aura = aura
                    except json.JSONDecodeError:
                        print("Error decoding JSON")
            else:
                time.sleep(0.1)
        else:
            print("Roblox is closed, waiting for Roblox to start...")
            if multi_webhook.get() != "1":
                if "discord.com" not in webhookURL.get() or "https://" not in webhookURL.get():
                    popup("Invalid or missing webhook link.", "Error")
                    stop()
                    return
                close_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                close_embed = discord_webhook.DiscordEmbed(
                    description="[" + time.strftime('%H:%M:%S') + "]: Roblox was closed/crashed.")
                close_embed.set_footer(text="maxstellar's Biome Macro for Mac", icon_url="https://maxstellar.github.io/maxstellar.png")
                close_webhook.add_embed(close_embed)
                close_webhook.execute()
            else:
                for url in webhook_urls:
                    close_webhook = discord_webhook.DiscordWebhook(url=url)
                    close_embed = discord_webhook.DiscordEmbed(
                        description="[" + time.strftime('%H:%M:%S') + "]: Roblox was closed/crashed.")
                    close_embed.set_footer(text="maxstellar's Biome Macro for Mac", icon_url="https://maxstellar.github.io/maxstellar.png")
                    close_webhook.add_embed(close_embed)
                    close_webhook.execute()
            root.title("maxstellar's Biome Macro - Paused")
            while True:
                if not stopped:
                    root.update()
                else:
                    if not destroyed:
                        root.destroy()
                    sys.exit()
                check = is_roblox_running()
                if check:
                    break
                time.sleep(0.1)
            time.sleep(5)
            latest_log = get_latest_log_file()
            if not latest_log:
                logger.info("No log files found.")
                print("No log files found.")
                return
            with open(latest_log, 'r', encoding='utf-8') as file:
                print(f"Using log file: {latest_log}")
                print()
                logger.info(f"Using log file: {latest_log}")
                root.title("maxstellar's Biome Macro - Running")
                check_for_hover_text(file)


def open_url(url):
    webbrowser.open(url, new=2, autoraise=True)


def auradetection_toggle_update():
    if aura_detection.get() == 1:
        popup("This feature is EXPERIMENTAL.\nThere are many limitations with aura detection.\n\nIt detects all auras "
              "that get equipped, so if you equip an aura yourself, it will get detected. Additionally, it will only "
              "detect auras that auto-equip.\n\nIt is also incapable of detecting dupes (for example, "
              "rolling Celestial with Celestial already equipped) or Overture: History, for some weird reason.",
              "Warning")
    config.set('Macro', 'aura_detection', str(aura_detection.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def init():
    global roblox_open, started

    if started:
        return

    webhook_field.configure(state="disabled", text_color="gray")
    ps_field.configure(state="disabled", text_color="gray")

    # write new settings to config
    config.set('Webhook', 'webhook_url', webhookURL.get())
    config.set('Webhook', 'private_server', psURL.get())

    # Writing our configuration file to 'example.ini'
    with open(config_name, 'w+') as configfile:
        config.write(configfile)

    # start webhook
    starting_embed = discord_webhook.DiscordEmbed(
        description="[" + time.strftime('%H:%M:%S') + "]: Macro started!")
    starting_embed.set_footer(text="maxstellar's Biome Macro for Mac", icon_url="https://maxstellar.github.io/maxstellar.png")
    if multi_webhook.get() != "1":
        if "discord.com" not in webhookURL.get() or "https://" not in webhookURL.get():
            popup("Invalid or missing webhook link.", "Error")
            stop()
            return
        starting_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
        starting_webhook.add_embed(starting_embed)
        starting_webhook.execute()
    else:
        for url in webhook_urls:
            starting_webhook = discord_webhook.DiscordWebhook(url=url)
            starting_webhook.add_embed(starting_embed)
            starting_webhook.execute()

    started = True

    # start detection
    if is_roblox_running():
        roblox_open = True
        logger.info("Roblox is open.")
        print("Roblox is open.")
        root.title("maxstellar's Biome Macro - Running")
    else:
        logger.info("Roblox is closed, waiting for Roblox to start...")
        print("Roblox is closed, waiting for Roblox to start...")
        root.title("maxstellar's Biome Macro - Paused")
        while True:
            if not stopped:
                root.update()
            else:
                if not destroyed:
                    root.destroy()
                sys.exit()
            check = is_roblox_running()
            if check:
                break
            time.sleep(0.1)
    time.sleep(5)
    latest_log = get_latest_log_file()
    if not latest_log:
        logger.info(print("No log files found."))
        print("No log files found.")
        return
    with open(latest_log, 'r', encoding='utf-8') as file:
        print(f"Using log file: {latest_log}")
        print()
        logger.info(f"Using log file: {latest_log}")
        root.title("maxstellar's Biome Macro - Running")
        check_for_hover_text(file)


tabview.set("Webhook")

webhook_label = customtkinter.CTkLabel(tabview.tab("Webhook"), text="Webhook URL:", font=customtkinter.CTkFont(family="Segoe UI", size=20))
webhook_label.grid(column=0, row=0, columnspan=2, padx=(10, 0), pady=(5, 0), sticky="w")

webhook_field = customtkinter.CTkEntry(tabview.tab("Webhook"), font=customtkinter.CTkFont(family="Segoe UI", size=20), width=335, textvariable=webhookURL)
webhook_field.grid(row=0, column=1, padx=(144, 0), pady=(10, 0), sticky="w")
if multi_webhook.get() == "1":
    webhook_field.configure(state="disabled", text_color="gray")
    webhookURL.set("Multi-Webhook On")

ps_label = customtkinter.CTkLabel(tabview.tab("Webhook"), text="Private Server URL:", font=customtkinter.CTkFont(family="Segoe UI", size=20))
ps_label.grid(column=0, row=1, padx=(10, 0), pady=(20, 0), columnspan=2, sticky="w")

ps_field = customtkinter.CTkEntry(tabview.tab("Webhook"), font=customtkinter.CTkFont(family="Segoe UI", size=20), width=296, textvariable=psURL)
ps_field.grid(row=1, column=1, padx=(183, 0), pady=(23, 0), sticky="w")

start_button = customtkinter.CTkButton(root, text="Start", font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75, command=init)
start_button.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

stop_button = customtkinter.CTkButton(root, text="Stop", font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75, command=stop)
stop_button.grid(row=1, column=1, padx=(5, 0), pady=(10, 0), sticky="w")

max_pfp = customtkinter.CTkImage(dark_image=Image.open(dirname + "/maxstellar.png"), size=(100, 100))
max_pfp_label = customtkinter.CTkLabel(tabview.tab("Credits"), image=max_pfp, text="")
max_pfp_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

sols_sniper = customtkinter.CTkImage(dark_image=Image.open(dirname + "/sols_sniper.png"), size=(100, 100))
sols_sniper_label = customtkinter.CTkLabel(tabview.tab("Credits"), image=sols_sniper, text="")
sols_sniper_label.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky="w")

credits_frame = customtkinter.CTkFrame(tabview.tab("Credits"))
credits_frame.grid(row=0, column=2, padx=(10, 0), pady=(10, 0), sticky="w")

max_label = customtkinter.CTkLabel(credits_frame, text="maxstellar - Creator", font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"))
max_label.grid(row=0, column=0, padx=(10, 0), sticky="nw")

youtube_link = customtkinter.CTkLabel(credits_frame, text="YouTube", font=("Segoe UI", 14, "underline"), text_color="dodgerblue", cursor="pointinghand")
youtube_link.grid(row=1, column=0, padx=(10, 0), sticky="nw")
youtube_link.bind("<Button-1>", lambda e: open_url("https://youtube.com/@maxstellar_"))

sniper_label = customtkinter.CTkLabel(credits_frame, text="dannw & yeswe - Developers", font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"))
sniper_label.grid(row=2, column=0, padx=(10, 0), sticky="nw")

support_link = customtkinter.CTkLabel(credits_frame, text="Discord", font=("Segoe UI", 14, "underline"), text_color="dodgerblue", cursor="pointinghand")
support_link.grid(row=3, column=0, padx=(10, 0), sticky="nw")
support_link.bind("<Button-1>", lambda e: open_url("https://discord.gg/solsniper"))

detection_toggle = customtkinter.CTkCheckBox(tabview.tab("Macro"), text="Aura Detection [Experimental]", font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=aura_detection, command=auradetection_toggle_update)
detection_toggle.grid(row=0, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w")

root.bind("<Destroy>", lambda event: x_stop())
root.bind("<Button-1>", lambda e: e.widget.focus_set())

root.mainloop()
