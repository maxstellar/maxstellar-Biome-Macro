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
import ctypes
import autoit
from win11toast import toast
from PIL import Image

logging.basicConfig(
    filename='crash.log',  # Optional: Specify a file to log to
    level=logging.INFO,  # Set the minimum level for logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Customize the log format
)

logger = logging.getLogger('mylogger')


def my_handler(types, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))
    ctypes.windll.user32.MessageBoxW(0, "Check crash.log for information on this crash.", "Crashed!", 0)
    sys.exit()


# exception handler / logger
sys.excepthook = my_handler

# create UI window
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title("maxstellar's Biome Macro")
root.geometry('505x285')
root.resizable(False, False)
dirname = os.path.dirname(__file__)
root.iconbitmap(dirname + '\\icon.ico')
tabview = customtkinter.CTkTabview(root, width=505, height=230)
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
    config['Macro'] = {'aura_detection': "0", 'aura_notif': "0", 'heavenly_pop': "0", 'heavenly_amt': "0",
                       'oblivion_pop': "0", "oblivion_amt": "0"}
    config['Biomes'] = {'windy': "1", 'snowy': "1", 'rainy': "1", 'sand_storm': "1", 'hell': "1", "starfall": "1",
                        "corruption": "1", "null": "1"}
    with open(config_name, 'w') as conffile:
        config.write(conffile)
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
log_directory = os.path.expandvars(r"%localappdata%\Roblox\logs")
packages_path = os.path.expandvars(r"%localappdata%\Packages")
roblox_folder = None
roblox_log_path = None
roblox_version = None
biome_colors = {"NORMAL": "ffffff", "SAND STORM": "F4C27C",
                "HELL": "5C1219", "STARFALL": "6784E0", "CORRUPTION": "9042FF", "NULL": "000000", "GLITCHED": "65FF65",
                "WINDY": "91F7FF", "SNOWY": "C4F5F6", "RAINY": "4385FF", "DREAMSPACE": "ff7dff"}
started = False
stopped = False
destroyed = False
debug_window = False
aura_detection = customtkinter.IntVar(root, int(config['Macro']['aura_detection']))
aura_notif = customtkinter.IntVar(root, int(config['Macro']['aura_notif']))
heavenly_pop = customtkinter.IntVar(root, int(config['Macro']['heavenly_pop']))
heavenly_amt = customtkinter.StringVar(root, config['Macro']['heavenly_amt'])
oblivion_pop = customtkinter.IntVar(root, int(config['Macro']['oblivion_pop']))
oblivion_amt = customtkinter.StringVar(root, config['Macro']['oblivion_amt'])
screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
tlw_open = False
windy = customtkinter.IntVar(root, int(config['Biomes']['windy']))
snowy = customtkinter.IntVar(root, int(config['Biomes']['snowy']))
rainy = customtkinter.IntVar(root, int(config['Biomes']['rainy']))
sand_storm = customtkinter.IntVar(root, int(config['Biomes']['sand_storm']))
hell = customtkinter.IntVar(root, int(config['Biomes']['hell']))
starfall = customtkinter.IntVar(root, int(config['Biomes']['starfall']))
corruption = customtkinter.IntVar(root, int(config['Biomes']['corruption']))
null = customtkinter.IntVar(root, int(config['Biomes']['null']))
glitched = customtkinter.IntVar(root, 1)
dreamspace = customtkinter.IntVar(root, 1)


def get_biome_color(biome):
    try:
        return biome_colors[biome]
    except:
        return "ff69b4"


def stop():
    global stopped
    # write config data
    config.set('Webhook', 'webhook_url', webhookURL.get())
    config.set('Webhook', 'private_server', psURL.get())
    if not heavenly_amt.get().isnumeric():
        heavenly_amt.set("0")
    config.set('Macro', 'heavenly_amt', heavenly_amt.get())
    if not oblivion_amt.get().isnumeric():
        oblivion_amt.set("0")
    config.set('Macro', 'oblivion_amt', oblivion_amt.get())
    with open(config_name, 'w+') as configfile:
        config.write(configfile)

    # end webhook
    if started and not stopped:
        if multi_webhook.get() != "1":
            if "discord.com" in webhookURL.get() and "https://" in webhookURL.get():
                ending_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                ending_embed = discord_webhook.DiscordEmbed(
                    description="[" + time.strftime('%H:%M:%S') + "]: Macro stopped.")
                ending_embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                        icon_url="https://maxstellar.github.io/maxstellar.png")
                ending_webhook.add_embed(ending_embed)
                ending_webhook.execute()

        else:
            ending_embed = discord_webhook.DiscordEmbed(
                description="[" + time.strftime('%H:%M:%S') + "]: Macro stopped.")
            ending_embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                    icon_url="https://maxstellar.github.io/maxstellar.png")
            for url in webhook_urls:
                ending_webhook = discord_webhook.DiscordWebhook(url=url)
                ending_webhook.add_embed(ending_embed)
                ending_webhook.execute()
    else:
        sys.exit()
    stopped = True


if multi_webhook.get() == "1":
    if len(webhook_urls) < 2:
        ctypes.windll.user32.MessageBoxW(0, "there's no reason to use multi-webhook... without multiple webhooks??",
                                         "bruh are you serious", 0)
        stop()
    elif len(webhook_urls) > 14:
        if len(webhook_urls) > 49:
            ctypes.windll.user32.MessageBoxW(0,
                                             "you've gotta be doing this on purpose now... you don't need this many webhooks",
                                             "this is ridiculous", 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, "bro you do not need this many webhooks", "okay dude wtf", 0)
        stop()


def x_stop():
    global destroyed
    destroyed = True
    stop()


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


def res_conv(x: int, y: int, resolution_from: tuple, resolution_to: tuple) -> tuple:
    assert x < resolution_from[0] and y < resolution_from[1], "Input coordinate is larger than resolution"
    x_ratio = resolution_to[0] / resolution_from[0]  # ratio to multiply x co-ord
    y_ratio = resolution_to[1] / resolution_from[1]  # ratio to multiply y co-ord
    return int(x * x_ratio), int(y * y_ratio)


def click(x, y):
    converted_coords = res_conv(x, y, (2560, 1440), screensize)
    convex, convey = converted_coords
    autoit.mouse_click("left", convex, convey)


def use(item: str, quantity: str):
    time.sleep(1)
    click(56, 715)
    time.sleep(1)
    click(1678, 450)
    time.sleep(1)
    click(1703, 489)
    time.sleep(1)
    autoit.send(item)
    time.sleep(1)
    click(1120, 588)
    time.sleep(1)
    click(792, 768)
    click(792, 768)
    time.sleep(1)
    autoit.send("{BACKSPACE}")
    time.sleep(1)
    autoit.send(quantity)
    time.sleep(1)
    click(914, 765)
    time.sleep(1)
    click(56, 715)


def check_for_hover_text(file):
    global roblox_version
    last_event = None
    last_aura = None
    file.seek(0, 2)
    while True:
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
                                        ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.", "Error",
                                                                         0)
                                        stop()
                                        return
                                    webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                    if event == "SNOWY":
                                        if last_event is not None:
                                            print(time.strftime('%H:%M:%S') + f": Biome Ended - " + last_event)
                                            if globals()[last_event.replace(" ", "_").lower()].get() == 1:
                                                embed = discord_webhook.DiscordEmbed(
                                                    title="[" + time.strftime('%H:%M:%S') + "]",
                                                    color=get_biome_color(last_event),
                                                    description="> ## Biome Ended - " + last_event)
                                                embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                                embed.set_thumbnail(
                                                    url="https://maxstellar.github.io/biome_thumb/" + last_event.replace(
                                                        " ", "%20") + ".png")
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                        else:
                                            pass
                                    else:
                                        print(time.strftime('%H:%M:%S') + f": Biome Started - {event}")
                                        if globals()[event.replace(" ", "_").lower()].get() == 1:
                                            embed = discord_webhook.DiscordEmbed(
                                                title="[" + time.strftime('%H:%M:%S') + "]",
                                                color=get_biome_color(event),
                                                description="> ## Biome Started - " + event)
                                            embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                             icon_url="https://maxstellar.github.io/maxstellar.png")
                                            embed.set_thumbnail(
                                                url="https://maxstellar.github.io/biome_thumb/" + event.replace(" ",
                                                                                                                "%20") + ".png")
                                            webhook.add_embed(embed)
                                        if event == "GLITCHED" or event == "DREAMSPACE":
                                            webhook.set_content("@everyone " + psURL.get())
                                        webhook.execute()
                                        if event == "GLITCHED":
                                            if heavenly_pop.get() == 1:
                                                use("Heavenly Potion II", heavenly_amt.get())
                                                webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                                embed = discord_webhook.DiscordEmbed(
                                                    description="[" + time.strftime(
                                                        '%H:%M:%S') + "]: Automatically popped " + heavenly_amt.get() + " Heavenly Potion IIs!",
                                                    color="ff98dc")
                                                embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                            if oblivion_pop.get() == 1:
                                                use("Oblivion Potion", oblivion_amt.get())
                                                webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                                embed = discord_webhook.DiscordEmbed(
                                                    description="[" + time.strftime(
                                                        '%H:%M:%S') + "]: Automatically popped " + oblivion_amt.get() + " Oblivion Potions!",
                                                    color="8a43d1")
                                                embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                else:
                                    if event == "SNOWY":
                                        if last_event is not None:
                                            print(time.strftime('%H:%M:%S') + f": Biome Ended - " + last_event)
                                            if globals()[last_event.replace(" ", "_").lower()].get() == 1:
                                                for url in webhook_urls:
                                                    webhook = discord_webhook.DiscordWebhook(url=url)
                                                    embed = discord_webhook.DiscordEmbed(
                                                        title="[" + time.strftime('%H:%M:%S') + "]",
                                                        color=get_biome_color(last_event),
                                                        description="> ## Biome Ended - " + last_event)
                                                    embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                                     icon_url="https://maxstellar.github.io/maxstellar.png")
                                                    embed.set_thumbnail(
                                                        url="https://maxstellar.github.io/biome_thumb/" + last_event.replace(
                                                            " ", "%20") + ".png")
                                                    webhook.add_embed(embed)
                                                    webhook.execute()
                                        else:
                                            pass
                                    else:
                                        print(time.strftime('%H:%M:%S') + f": Biome Started - {event}")
                                        if globals()[event.replace(" ", "_").lower()].get() == 1:
                                            for url in webhook_urls:
                                                embed = discord_webhook.DiscordEmbed(
                                                    title="[" + time.strftime('%H:%M:%S') + "]",
                                                    color=get_biome_color(event),
                                                    description="> ## Biome Started - " + event)
                                                embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                                embed.set_thumbnail(
                                                    url="https://maxstellar.github.io/biome_thumb/" + event.replace(" ",
                                                                                                                    "%20") + ".png")
                                                webhook = discord_webhook.DiscordWebhook(url=url)
                                                webhook.add_embed(embed)
                                                if event == "GLITCHED" or event == "DREAMSPACE":
                                                    webhook.set_content("@everyone " + psURL.get())
                                                webhook.execute()
                                        if event == "GLITCHED":
                                            if heavenly_pop.get() == 1:
                                                use("Heavenly Potion II", heavenly_amt.get())
                                                for url in webhook_urls:
                                                    webhook = discord_webhook.DiscordWebhook(url=url)
                                                    embed = discord_webhook.DiscordEmbed(
                                                        description="[" + time.strftime(
                                                            '%H:%M:%S') + "]: Automatically popped " + heavenly_amt.get() + " Heavenly Potion IIs!",
                                                        color="ff98dc")
                                                    embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                                     icon_url="https://maxstellar.github.io/maxstellar.png")
                                                    webhook.add_embed(embed)
                                                    webhook.execute()
                                            if oblivion_pop.get() == 1:
                                                use("Oblivion Potion", oblivion_amt.get())
                                                for url in webhook_urls:
                                                    webhook = discord_webhook.DiscordWebhook(url=url)
                                                    embed = discord_webhook.DiscordEmbed(
                                                        description="[" + time.strftime(
                                                            '%H:%M:%S') + "]: Automatically popped " + oblivion_amt.get() + " Oblivion Potions!",
                                                        color="8a43d1")
                                                    embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                                     icon_url="https://maxstellar.github.io/maxstellar.png")
                                                    webhook.add_embed(embed)
                                                    webhook.execute()
                                last_event = event
                            if state and aura != last_aura and aura != "n":
                                if aura_detection.get() == 1 and aura != "None":
                                    if multi_webhook.get() != "1":
                                        if "discord.com" not in webhookURL.get() or "https://" not in webhookURL.get():
                                            ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.",
                                                                             "Error", 0)
                                            stop()
                                            return
                                        webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                        print(time.strftime('%H:%M:%S') + f": Aura Equipped - {aura}")
                                        embed = discord_webhook.DiscordEmbed(
                                            title="[" + time.strftime('%H:%M:%S') + "]",
                                            description="> ## Aura Equipped - " + aura)
                                        embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                         icon_url="https://maxstellar.github.io/maxstellar.png")
                                        webhook.add_embed(embed)
                                        webhook.execute()
                                        if aura_notif.get() == 1:
                                            toast("You rolled " + aura + "!")
                                    else:
                                        print(time.strftime('%H:%M:%S') + f": Aura Equipped - {aura}")
                                        for url in webhook_urls:
                                            webhook = discord_webhook.DiscordWebhook(url=url)
                                            embed = discord_webhook.DiscordEmbed(
                                                title="[" + time.strftime('%H:%M:%S') + "]",
                                                description="> ## Aura Equipped - " + aura)
                                            embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                                             icon_url="https://maxstellar.github.io/maxstellar.png")
                                            webhook.add_embed(embed)
                                            webhook.execute()
                                        if aura_notif.get() == 1:
                                            toast("You rolled " + aura + "!")
                                last_aura = aura
                    except json.JSONDecodeError:
                        print("Error decoding JSON")
            else:
                time.sleep(0.1)
        else:
            print("Roblox is closed, waiting for Roblox to start...")
            if multi_webhook.get() != "1":
                if "discord.com" not in webhookURL.get() or "https://" not in webhookURL.get():
                    ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.", "Error", 0)
                    stop()
                    return
                close_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                close_embed = discord_webhook.DiscordEmbed(
                    description="[" + time.strftime('%H:%M:%S') + "]: Roblox was closed/crashed.")
                close_embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                       icon_url="https://maxstellar.github.io/maxstellar.png")
                close_webhook.add_embed(close_embed)
                close_webhook.execute()
            else:
                for url in webhook_urls:
                    close_webhook = discord_webhook.DiscordWebhook(url=url)
                    close_embed = discord_webhook.DiscordEmbed(
                        description="[" + time.strftime('%H:%M:%S') + "]: Roblox was closed/crashed.")
                    close_embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                                           icon_url="https://maxstellar.github.io/maxstellar.png")
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
            if roblox_version == "player":
                logger.info("Detected Roblox Player.")
                print("Detected Roblox Player.")
                time.sleep(5)
            else:
                logger.info("Detected Roblox Microsoft Store.")
                print("Detected Roblox Microsoft Store.")
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
        ctypes.windll.user32.MessageBoxW(0,
                                         "This feature is EXPERIMENTAL.\nThere are many limitations with aura detection.\n\nIt detects all auras that get equipped, so if you equip an aura yourself, it will get detected. Additionally, it will only detect auras that auto-equip.\n\nIt is also incapable of detecting dupes (for example, rolling Celestial with Celestial already equipped) or Overture: History, for some weird reason.",
                                         "Warning", 0)
    config.set('Macro', 'aura_detection', str(aura_detection.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def auranotif_toggle_update():
    config.set('Macro', 'aura_notif', str(aura_notif.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def heavenly_toggle_update():
    if heavenly_pop.get() == 1:
        ctypes.windll.user32.MessageBoxW(0,
                                         "This feature is EXPERIMENTAL.\nPlease remember to turn off Auto-Heavenly whenever you tab out of Roblox, or stop AFK-ing.\nAdditionally, by using this feature, you run the risk of the macro glitching out somehow and popping your potions.\n\nUSE AT YOUR OWN RISK!",
                                         "Warning", 0)
    config.set('Macro', 'heavenly_pop', str(heavenly_pop.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def oblivion_toggle_update():
    config.set('Macro', 'oblivion_pop', str(oblivion_pop.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def tlw_toggle_update(toggle):
    config.set('Biomes', toggle, str(globals()[toggle].get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def manage_tlw():
    global tlw_open, dirname
    if not tlw_open:
        # create tlw
        tlw_open = True
        tlw = customtkinter.CTkToplevel()
        tlw.bind("<Destroy>", lambda e: globals().__setitem__('tlw_open', False))
        tlw.title("Configure Biomes")
        tlw_label = customtkinter.CTkLabel(tlw, text="Choose which biomes get sent!", font=customtkinter.CTkFont(family="Segoe UI", size=20))
        tlw_label.grid(row=0, column=0, columnspan=2, pady=10)
        windy_toggle = customtkinter.CTkCheckBox(tlw, text="Windy",
                                                 font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=windy,
                                                 command=lambda: tlw_toggle_update("windy"))
        windy_toggle.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        snowy_toggle = customtkinter.CTkCheckBox(tlw, text="Snowy",
                                                 font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=snowy,
                                                 command=lambda: tlw_toggle_update("snowy"))
        snowy_toggle.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        rainy_toggle = customtkinter.CTkCheckBox(tlw, text="Rainy",
                                                 font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=rainy,
                                                 command=lambda: tlw_toggle_update("rainy"))
        rainy_toggle.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        sand_storm_toggle = customtkinter.CTkCheckBox(tlw, text="Sand Storm",
                                                      font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                      variable=sand_storm,
                                                      command=lambda: tlw_toggle_update("sand_storm"))
        sand_storm_toggle.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        hell_toggle = customtkinter.CTkCheckBox(tlw, text="Hell", font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=hell, command=lambda: tlw_toggle_update("hell"))
        hell_toggle.grid(row=4, column=1, sticky="w", padx=10, pady=10)
        starfall_toggle = customtkinter.CTkCheckBox(tlw, text="Starfall", font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=starfall, command=lambda: tlw_toggle_update("starfall"))
        starfall_toggle.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        corruption_toggle = customtkinter.CTkCheckBox(tlw, text="Corruption", font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=corruption, command=lambda: tlw_toggle_update("corruption"))
        corruption_toggle.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        null_toggle = customtkinter.CTkCheckBox(tlw, text="Null", font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=null, command=lambda: tlw_toggle_update("null"))
        null_toggle.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        tlw.after(0, tlw.focus)
        tlw.after(100, lambda: tlw.resizable(False, False))
        tlw.after(250, lambda: tlw.iconbitmap(dirname + '\\icon.ico'))


def init():
    global roblox_open, started

    if started:
        return

    webhook_field.configure(state="disabled", text_color="gray")
    ps_field.configure(state="disabled", text_color="gray")

    # write new settings to config
    config.set('Webhook', 'webhook_url', webhookURL.get())
    config.set('Webhook', 'private_server', psURL.get())
    config.set('Macro', 'heavenly_amt', heavenly_amt.get())
    config.set('Macro', 'oblivion_amt', oblivion_amt.get())

    # Writing our configuration file to 'example.ini'
    with open(config_name, 'w+') as configfile:
        config.write(configfile)

    # start webhook
    starting_embed = discord_webhook.DiscordEmbed(
        description="[" + time.strftime('%H:%M:%S') + "]: Macro started!")
    starting_embed.set_footer(text="maxstellar's Biome Macro | v1.2",
                              icon_url="https://maxstellar.github.io/maxstellar.png")
    if multi_webhook.get() != "1":
        if "discord.com" not in webhookURL.get() or "https://" not in webhookURL.get():
            ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.", "Error", 0)
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
    if not roblox_open:
        if roblox_version == "player":
            logger.info("Detected Roblox Player.")
            print("Detected Roblox Player.")
            time.sleep(1.5)
        else:
            logger.info("Detected Roblox Microsoft Store.")
            print("Detected Roblox Microsoft Store.")
            time.sleep(3.5)
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

webhook_label = customtkinter.CTkLabel(tabview.tab("Webhook"), text="Webhook URL:",
                                       font=customtkinter.CTkFont(family="Segoe UI", size=20))
webhook_label.grid(column=0, row=0, columnspan=2, padx=(10, 0), pady=(5, 0), sticky="w")

webhook_field = customtkinter.CTkEntry(tabview.tab("Webhook"), font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                       width=335, textvariable=webhookURL)
webhook_field.grid(row=0, column=1, padx=(144, 0), pady=(10, 0), sticky="w")
if multi_webhook.get() == "1":
    webhook_field.configure(state="disabled", text_color="gray")
    webhookURL.set("Multi-Webhook On")

ps_label = customtkinter.CTkLabel(tabview.tab("Webhook"), text="Private Server URL:",
                                  font=customtkinter.CTkFont(family="Segoe UI", size=20))
ps_label.grid(column=0, row=1, padx=(10, 0), pady=(20, 0), columnspan=2, sticky="w")

ps_field = customtkinter.CTkEntry(tabview.tab("Webhook"), font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                  width=300, textvariable=psURL)
ps_field.grid(row=1, column=1, padx=(179, 0), pady=(23, 0), sticky="w")

biome_button = customtkinter.CTkButton(tabview.tab("Webhook"), text="Configure Biomes",
                                       font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
                                       command=manage_tlw)
biome_button.grid(row=2, column=0, padx=(10, 0), columnspan=2, pady=(20, 0), sticky="w")

start_button = customtkinter.CTkButton(root, text="Start",
                                       font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
                                       command=init)
start_button.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

stop_button = customtkinter.CTkButton(root, text="Stop",
                                      font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
                                      command=stop)
stop_button.grid(row=1, column=1, padx=(5, 0), pady=(10, 0), sticky="w")

max_pfp = customtkinter.CTkImage(dark_image=Image.open(dirname + "\\maxstellar.png"), size=(125, 125))
max_pfp_label = customtkinter.CTkLabel(tabview.tab("Credits"), image=max_pfp, text="")
max_pfp_label.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="w")

sols_sniper = customtkinter.CTkImage(dark_image=Image.open(dirname + "\\sols_sniper.png"), size=(125, 125))
sols_sniper_label = customtkinter.CTkLabel(tabview.tab("Credits"), image=sols_sniper, text="")
sols_sniper_label.grid(row=0, column=1, padx=(5, 0), pady=(20, 0), sticky="w")

credits_frame = customtkinter.CTkFrame(tabview.tab("Credits"))
credits_frame.grid(row=0, column=2, padx=(7, 0), pady=(20, 0), sticky="w")

max_label = customtkinter.CTkLabel(credits_frame, text="maxstellar - Creator",
                                   font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"))
max_label.grid(row=0, column=0, padx=(5, 0), sticky="nw")

youtube_link = customtkinter.CTkLabel(credits_frame, text="YouTube", font=("Segoe UI", 14, "underline"),
                                      text_color="dodgerblue", cursor="hand2")
youtube_link.grid(row=1, column=0, padx=(5, 0), sticky="nw")
youtube_link.bind("<Button-1>", lambda e: open_url("https://youtube.com/@maxstellar_"))

sniper_label = customtkinter.CTkLabel(credits_frame, text="dannw & yeswe - Developers",
                                      font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"))
sniper_label.grid(row=2, column=0, padx=(5, 0), sticky="nw")

support_link = customtkinter.CTkLabel(credits_frame, text="Discord", font=("Segoe UI", 14, "underline"),
                                      text_color="dodgerblue", cursor="hand2")
support_link.grid(row=3, column=0, padx=(5, 0), sticky="nw")
support_link.bind("<Button-1>", lambda e: open_url("https://discord.gg/solsniper"))

detection_toggle = customtkinter.CTkCheckBox(tabview.tab("Macro"), text="Aura Detection [Experimental]",
                                             font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                             variable=aura_detection, command=auradetection_toggle_update)
detection_toggle.grid(row=0, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w")

detectnotif_toggle = customtkinter.CTkCheckBox(tabview.tab("Macro"), text="Aura Notifications",
                                               font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                               variable=aura_notif, command=auranotif_toggle_update)
detectnotif_toggle.grid(row=1, column=0, columnspan=2, padx=(10, 0), pady=(12, 0), sticky="w")

heavenly_toggle = customtkinter.CTkCheckBox(tabview.tab("Macro"), text="Auto-Heavenly [Experimental]",
                                            font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                            variable=heavenly_pop, command=heavenly_toggle_update)
heavenly_toggle.grid(row=2, column=0, columnspan=2, padx=(10, 0), pady=(5, 0), sticky="w")

heavenly_field = customtkinter.CTkEntry(tabview.tab("Macro"), font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                        width=50, textvariable=heavenly_amt)
heavenly_field.grid(row=2, column=1, padx=(310, 0), pady=(10, 0), sticky="w")

oblivion_toggle = customtkinter.CTkCheckBox(tabview.tab("Macro"), text="Auto-Oblivion",
                                            font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                            variable=oblivion_pop, command=oblivion_toggle_update)
oblivion_toggle.grid(row=3, column=0, columnspan=2, padx=(10, 0), sticky="w")

oblivion_field = customtkinter.CTkEntry(tabview.tab("Macro"), font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                        width=50, textvariable=oblivion_amt)
oblivion_field.grid(row=3, column=1, padx=(175, 0), pady=(3, 0), sticky="w")

root.bind("<Destroy>", lambda event: x_stop())
root.bind("<Button-1>", lambda e: e.widget.focus_set())

root.mainloop()
