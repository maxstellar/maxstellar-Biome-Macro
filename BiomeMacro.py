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
aura_images = {"\u00e2\u02dc\u2026": "https://static.wikia.nocookie.net/sol-rng/images/d/d7/Dreamscape_star1_collection.png/revision/latest", "\u00e2\u02dc\u2026\u00e2\u02dc\u2026": "https://static.wikia.nocookie.net/sol-rng/images/4/4f/Dreamscape_star2.png/revision/latest", "fault": "https://static.wikia.nocookie.net/sol-rng/images/e/e1/Fault_Aura_Collection_GIF.gif/revision/latest", "\u00e2\u02dc\u2026\u00e2\u02dc\u2026\u00e2\u02dc\u2026": "https://static.wikia.nocookie.net/sol-rng/images/a/a3/Screenshot_2025-02-09_145439.png/revision/latest", "undead": "https://static.wikia.nocookie.net/sol-rng/images/e/eb/UndeadAura.gif/revision/latest", "corrosive": "https://static.wikia.nocookie.net/sol-rng/images/9/94/Corrosive.gif/revision/latest", "rage : heated": "https://static.wikia.nocookie.net/sol-rng/images/1/14/RageHeatedAura.gif/revision/latest", "ink : leak": "https://static.wikia.nocookie.net/sol-rng/images/d/da/LeakGif.gif/revision/latest", "powered": "https://static.wikia.nocookie.net/sol-rng/images/9/9a/Powered.gif/revision/latest", "watt": "https://static.wikia.nocookie.net/sol-rng/images/c/ca/WattCollection.gif/revision/latest", "aquatic": "https://static.wikia.nocookie.net/sol-rng/images/a/a9/AquaticAura.gif/revision/latest", "solar": "https://static.wikia.nocookie.net/sol-rng/images/4/41/SolarAuraNight.gif/revision/latest", "lunar": "https://static.wikia.nocookie.net/sol-rng/images/d/d3/Lunar_Collection_E7.gif/revision/latest", "starlight": "https://static.wikia.nocookie.net/sol-rng/images/2/22/StarlightCollection.gif/revision/latest", "starrider": "https://static.wikia.nocookie.net/sol-rng/images/1/1a/StarRiderCollection.gif/revision/latest", " :flushed: : lobotomy": "https://static.wikia.nocookie.net/sol-rng/images/f/f6/FlushedLobotomyAura.gif/revision/latest", "permafrost": "https://static.wikia.nocookie.net/sol-rng/images/b/bd/PermaFrostCollection.gif/revision/latest", "hazard : rays": "https://static.wikia.nocookie.net/sol-rng/images/c/c1/Hazard_Rays.gif/revision/latest", "nautilus": "https://static.wikia.nocookie.net/sol-rng/images/e/e2/NautilusAuraNight.gif/revision/latest", "stormal": "https://static.wikia.nocookie.net/sol-rng/images/6/65/Stormal_Collection_E7.gif/revision/latest", "exotic": "https://static.wikia.nocookie.net/sol-rng/images/7/71/ExoticAura150x150.gif/revision/latest", "exotic : apex": "https://static.wikia.nocookie.net/sol-rng/images/0/09/Exotic_Apex_Collection_E7.gif/revision/latest", "exotic : void": "https://static.wikia.nocookie.net/sol-rng/images/c/c7/ExoticVoidCollection.gif/revision/latest", "diaboli : void": "https://static.wikia.nocookie.net/sol-rng/images/e/ee/Diabolivoidcollection.gif/revision/latest", "undead : devil": "https://static.wikia.nocookie.net/sol-rng/images/7/73/UndeadDevilCollectionEon1.gif/revision/latest", "comet": "https://static.wikia.nocookie.net/sol-rng/images/1/16/Comet_collect.gif/revision/latest", "jade": "https://static.wikia.nocookie.net/sol-rng/images/0/06/JadeInCollection.gif/revision/latest", "spectre": "https://static.wikia.nocookie.net/sol-rng/images/e/ed/SpectreCollection.gif/revision/latest", "jazz": "https://static.wikia.nocookie.net/sol-rng/images/2/2d/JazzCollectionBetter.gif/revision/latest", "aether": "https://static.wikia.nocookie.net/sol-rng/images/9/91/AetherCollection.gif/revision/latest", "bounded": "https://static.wikia.nocookie.net/sol-rng/images/5/52/BoundedAuraNight.gif/revision/latest", "celestial": "https://static.wikia.nocookie.net/sol-rng/images/6/64/Celestial_Rework_Collection.gif/revision/latest", "celestial : divine": "https://static.wikia.nocookie.net/sol-rng/images/c/c4/CelestialDivineCollection.gif/revision/latest", "warlock": "https://static.wikia.nocookie.net/sol-rng/images/9/9c/WarlockCollection.gif/revision/latest", "kyawthuite": "https://static.wikia.nocookie.net/sol-rng/images/6/67/Kyawthuite_Collection2.gif/revision/latest", "kyawthuite : remembrance": "https://static.wikia.nocookie.net/sol-rng/images/d/d4/KyawthuiteRememberance.webp/revision/latest", "arcane": "https://static.wikia.nocookie.net/sol-rng/images/d/d8/ArcaneCollectionN3w.gif/revision/latest", "arcane : legacy": "https://static.wikia.nocookie.net/sol-rng/images/7/72/Arcane_Legacy_Collection_E7.gif/revision/latest", "arcane : dark": "https://static.wikia.nocookie.net/sol-rng/images/1/10/Arcane-dark-collection-era9.gif/revision/latest", "magnetic : reverse polarity": "https://static.wikia.nocookie.net/sol-rng/images/8/8f/Magnetic_Reverse_Polarity_Rework_Collection.gif/revision/latest", "undefined": "https://static.wikia.nocookie.net/sol-rng/images/b/b0/Undefined_Collection1.gif/revision/latest", "rage : brawler": "https://static.wikia.nocookie.net/sol-rng/images/0/0b/BrawlerCollection.gif/revision/latest", "astral": "https://static.wikia.nocookie.net/sol-rng/images/5/57/Astral_Era9.gif/revision/latest", "cosmos": "https://static.wikia.nocookie.net/sol-rng/images/4/4c/CosmosCollection.gif/revision/latest", "gravitational": "https://static.wikia.nocookie.net/sol-rng/images/f/fd/Grav_CollectionE9.gif/revision/latest", "bounded : unbound": "https://static.wikia.nocookie.net/sol-rng/images/6/65/Unbound_E7_Collection2.gif/revision/latest", "virtual": "https://static.wikia.nocookie.net/sol-rng/images/8/88/VirtualReworkCollection.gif/revision/latest", "virtual : fatal error": "https://static.wikia.nocookie.net/sol-rng/images/8/8e/FatalErrorCollection.png/revision/latest", "savior": "https://static.wikia.nocookie.net/sol-rng/images/a/a4/Savior_Collection.gif/revision/latest", "poseidon": "https://static.wikia.nocookie.net/sol-rng/images/d/db/PosEra7.gif/revision/latest", "aquatic : flame": "https://static.wikia.nocookie.net/sol-rng/images/7/7f/Aqua_flame_new_gif.gif/revision/latest", "zeus": "https://static.wikia.nocookie.net/sol-rng/images/4/41/Zeus_GIF.gif/revision/latest", "lunar : full moon": "https://static.wikia.nocookie.net/sol-rng/images/4/40/LunarFMReworkCollection.gif/revision/latest", "solar : solstice": "https://static.wikia.nocookie.net/sol-rng/images/1/1c/SolarSolsticeG.gif/revision/latest", "galaxy": "https://static.wikia.nocookie.net/sol-rng/images/f/f8/Galaxy_Aura.gif/revision/latest", "twilight": "https://static.wikia.nocookie.net/sol-rng/images/b/b4/TwilightInCollection.gif/revision/latest", "twilight : iridescent memory": "https://static.wikia.nocookie.net/sol-rng/images/f/fc/Twilight_-_Iridescent_Memory_Collection.gif/revision/latest", "origin": "https://static.wikia.nocookie.net/sol-rng/images/6/6c/OriginCollectionEon1.gif/revision/latest", "hades": "https://static.wikia.nocookie.net/sol-rng/images/8/85/HadesCollection.gif/revision/latest", "hyper-volt": "https://static.wikia.nocookie.net/sol-rng/images/d/d4/HpVl.gif/revision/latest", "velocity": "https://static.wikia.nocookie.net/sol-rng/images/5/54/Velocitygif.gif/revision/latest", "nihility": "https://static.wikia.nocookie.net/sol-rng/images/c/ca/Nihility_collection.gif/revision/latest", "helios": "https://static.wikia.nocookie.net/sol-rng/images/e/ed/HeliosCollection.gif/revision/latest", "starscourge": "https://static.wikia.nocookie.net/sol-rng/images/9/9d/StarscourgeRevampCollection.gif/revision/latest", "starscourge : radiant": "https://static.wikia.nocookie.net/sol-rng/images/1/16/Starscourge_Radiant_Gif2.gif/revision/latest", "sailor": "https://static.wikia.nocookie.net/sol-rng/images/e/e2/SailorCollectionEra7.gif/revision/latest", "sailor : flying dutchman": "https://static.wikia.nocookie.net/sol-rng/images/5/53/DutchmanCollectionEon1.gif/revision/latest", "stormal : hurricane": "https://static.wikia.nocookie.net/sol-rng/images/d/d9/Hurricane_Collection_Eon_1_reupload.gif/revision/latest", "sirius": "https://static.wikia.nocookie.net/sol-rng/images/c/c2/Siriusincollection.gif/revision/latest", "chromatic": "https://static.wikia.nocookie.net/sol-rng/images/d/d6/Chromatic_GIF.gif/revision/latest", "chromatic : genesis": "https://static.wikia.nocookie.net/sol-rng/images/7/72/Genesis-Collection.gif/revision/latest", "aviator": "https://static.wikia.nocookie.net/sol-rng/images/4/43/Aviator_Collection.gif/revision/latest", "ethereal": "https://static.wikia.nocookie.net/sol-rng/images/b/bc/Etherealpretrans.gif/revision/latest", "overseer": "https://static.wikia.nocookie.net/sol-rng/images/0/0b/Overseer-collection.gif/revision/latest", "runic": "https://static.wikia.nocookie.net/sol-rng/images/e/ed/RunicColl.gif/revision/latest", "matrix": "https://static.wikia.nocookie.net/sol-rng/images/9/97/MatrixCollectionEon1.gif/revision/latest", "matrix : overdrive": "https://static.wikia.nocookie.net/sol-rng/images/e/e4/MatrixOverdriveCollection.gif/revision/latest", "matrix : reality": "https://static.wikia.nocookie.net/sol-rng/images/a/a0/Matrix_but_real.gif/revision/latest", "sentinel": "https://static.wikia.nocookie.net/sol-rng/images/9/96/SentinelCollection.gif/revision/latest", "carriage": "https://static.wikia.nocookie.net/sol-rng/images/7/7d/Collection_Carriage.gif/revision/latest", "overture": "https://static.wikia.nocookie.net/sol-rng/images/e/e8/Overture_Collection.gif/revision/latest", "overture : history": "https://static.wikia.nocookie.net/sol-rng/images/6/61/Overture_History_Eon1_Collection.gif/revision/latest", "symphony": "https://static.wikia.nocookie.net/sol-rng/images/f/f5/Symphony_Collection_with_crown.gif/revision/latest", "impeached": "https://static.wikia.nocookie.net/sol-rng/images/2/2f/Impeached_Collectiongifv2.gif/revision/latest", "archangel": "https://static.wikia.nocookie.net/sol-rng/images/4/4f/ArchangelCollection.gif/revision/latest", "bloodlust": "https://static.wikia.nocookie.net/sol-rng/images/f/f9/BloodlustInCollection.gif/revision/latest", "atlas": "https://static.wikia.nocookie.net/sol-rng/images/0/0b/Atlas_collection.gif/revision/latest", "abyssalhunter": "https://static.wikia.nocookie.net/sol-rng/images/2/25/Abyssal_Hunter_Max_Graphics.gif/revision/latest", "gargantua": "https://static.wikia.nocookie.net/sol-rng/images/5/5a/GargantuaStable.gif/revision/latest", "apostolos": "https://static.wikia.nocookie.net/sol-rng/images/1/17/In-collection_Apostolos.gif/revision/latest", "ruins": "https://static.wikia.nocookie.net/sol-rng/images/7/74/Ruins.collection.gif/revision/latest", "sovereign": "https://static.wikia.nocookie.net/sol-rng/images/0/05/Sovereign_Collection_E8.gif/revision/latest", "ruins : withered": "https://static.wikia.nocookie.net/sol-rng/images/a/a9/Ruins_-_witheredincollection2.png/revision/latest", "aegis": "https://static.wikia.nocookie.net/sol-rng/images/a/ab/AegisCollection.gif/revision/latest", "pixelation": "https://static.wikia.nocookie.net/sol-rng/images/6/61/Pixelation_In-Game.gif/revision/latest", "luminosity": "https://static.wikia.nocookie.net/sol-rng/images/e/ea/Luminosity_Collection.gif/revision/latest", "glitch": "https://static.wikia.nocookie.net/sol-rng/images/a/a1/Era8glitchcollection.gif/revision/latest", "oppression": "https://static.wikia.nocookie.net/sol-rng/images/c/c1/OppressionCollectionEon1.gif/revision/latest", "memory": "https://static.wikia.nocookie.net/sol-rng/images/a/ad/MemoryCollectionEon1.gif/revision/latest", "oblivion": " ://static.wikia.nocookie.net/sol-rng/images/c/c5/Oblivion_colletion_eon1-1.gif/revision/latest", "wonderland": "https://static.wikia.nocookie.net/sol-rng/images/3/39/WonderlandCollection.gif/revision/latest", "santa frost": "https://static.wikia.nocookie.net/sol-rng/images/3/32/FrostCollection.gif/revision/latest", "winter fantasy": "https://static.wikia.nocookie.net/sol-rng/images/8/8e/Winter_Fantasy%28Collection%29.gif/revision/latest", "express": "https://static.wikia.nocookie.net/sol-rng/images/1/10/ExpressCollectionGIf.gif/revision/latest", "abomitable": "https://static.wikia.nocookie.net/sol-rng/images/b/bb/AbomitableIngame.gif/revision/latest", "atlas : yuletide": "https://static.wikia.nocookie.net/sol-rng/images/e/e4/Roblox2025-02-0917-24-01-ezgif.com-optimize.gif/revision/latest", " :flushed : : troll": "https://static.wikia.nocookie.net/sol-rng/images/f/fb/TrollCollection.gif/revision/latest", "origin : onion": "https://static.wikia.nocookie.net/sol-rng/images/c/c3/OnionCollection.gif/revision/latest", "glock : shieldofthesky": "https://static.wikia.nocookie.net/sol-rng/images/5/5f/Glock_of_the_sky_in_Collection_%28better_version%29.png/revision/latest", "anubis": "https://static.wikia.nocookie.net/sol-rng/images/a/a7/AnubisC.gif/revision/latest", "blizzard": "https://static.wikia.nocookie.net/sol-rng/images/0/02/Screenshot_2025-04-19_103324.png/revision/latest", "jazz : orchestra": "https://static.wikia.nocookie.net/sol-rng/images/3/35/Orchestra_jazz.gif/revision/latest", "astral : legendarium": "https://static.wikia.nocookie.net/sol-rng/images/f/fe/Legendcollec.png/revision/latest", "stargazer": "https://static.wikia.nocookie.net/sol-rng/images/9/97/Stargazerincollection.gif/revision/latest", "harnessed": "https://static.wikia.nocookie.net/sol-rng/images/9/94/Harnessed_collec.gif/revision/latest/", "raven": "https://static.wikia.nocookie.net/sol-rng/images/5/5a/RavenCollection.gif/revision/latest", "anima": "https://static.wikia.nocookie.net/sol-rng/images/f/f4/AnimaCollection.gif/revision/latest", "juxtaposition": "https://static.wikia.nocookie.net/sol-rng/images/1/1e/JuxtapColl.gif/revision/latest", "unknown": "https://static.wikia.nocookie.net/sol-rng/images/b/b6/Unknownincollection.gif/revision/latest", "elude": "https://static.wikia.nocookie.net/sol-rng/images/1/11/EludeCollection.gif/revision/latest", "prologue": "https://static.wikia.nocookie.net/sol-rng/images/d/d6/PrologueCollection.gif/revision/latest", "dreamscape": "https://static.wikia.nocookie.net/sol-rng/images/1/1a/DreamscapeInCollection.gif/revision/latest", "manta": "https://static.wikia.nocookie.net/sol-rng/images/3/31/Manta_In-Collection.gif/revision/latest", "aegis : watergun": "https://static.wikia.nocookie.net/sol-rng/images/a/ac/Aegis_Watergun_in_collection.gif/revision/latest"}

# read configuration file
config_name = 'config.ini'
config = configparser.ConfigParser()
if not os.path.exists(config_name):
    logger.info("Config file not found, creating one...")
    print("Config file not found, creating one...")
    config['Webhook'] = {'webhook_url': "", 'private_server': "", "discord_user_id": "", 'multi_webhook': "0",
                         'multi_webhook_urls': ""}
    config['Macro'] = {'aura_detection': "1", 'aura_notif': "0", "aura_ping": "0", "min_rarity_to_ping": "", "last_roblox_version": "", "username_override": ""}
    config['Biomes'] = {'windy': "Message", 'snowy': "Message", 'rainy': "Message", 'sand_storm': "Message",
                        'hell': "Message", "starfall": "Message",
                        "corruption": "Message", "null": "Message", "blazing_sun": "Message", "jester": "Ping"}
    with open(config_name, 'w') as conffile:
        config.write(conffile)
config.read(config_name)
webhookURL = customtkinter.StringVar(root, config['Webhook']['webhook_url'])
psURL = customtkinter.StringVar(root, config['Webhook']['private_server'])
discID = customtkinter.StringVar(root, config['Webhook']['discord_user_id'])
multi_webhook = customtkinter.StringVar(root, config['Webhook']['multi_webhook'])
if multi_webhook.get() != "1" and webhookURL.get() == "Multi-Webhook On":
    webhookURL.set("")
webhook_urls_string = customtkinter.StringVar(root, config['Webhook']['multi_webhook_urls'])
webhook_urls = webhook_urls_string.get().split()
last_roblox_version = config['Macro']['last_roblox_version']
username_override = config['Macro']['username_override']

# variables
roblox_open = False
versions_directory = os.path.expandvars(r"%localappdata%\Roblox\Versions")
log_directory = os.path.expandvars(r"%localappdata%\Roblox\logs")
packages_path = os.path.expandvars(r"%localappdata%\Packages")
roblox_folder = None
roblox_log_path = None
roblox_version = None
biome_colors = {"NORMAL": "ffffff", "SAND STORM": "F4C27C",
                "HELL": "5C1219", "STARFALL": "6784E0", "CORRUPTION": "9042FF", "NULL": "000000", "GLITCHED": "65FF65",
                "WINDY": "91F7FF", "SNOWY": "C4F5F6", "RAINY": "4385FF", "DREAMSPACE": "ff7dff",
                "BLAZING SUN": "FFFF00"}
started = False
stopped = False
paused = False
destroyed = False
debug_window = False
aura_detection = customtkinter.IntVar(root, int(config['Macro']['aura_detection']))
aura_notif = customtkinter.IntVar(root, int(config['Macro']['aura_notif']))
aura_ping = customtkinter.IntVar(root, int(config['Macro']['aura_ping']))
tlw_open = False
windy = customtkinter.StringVar(root, config['Biomes']['windy'])
snowy = customtkinter.StringVar(root, config['Biomes']['snowy'])
rainy = customtkinter.StringVar(root, config['Biomes']['rainy'])
sand_storm = customtkinter.StringVar(root, config['Biomes']['sand_storm'])
hell = customtkinter.StringVar(root, config['Biomes']['hell'])
starfall = customtkinter.StringVar(root, config['Biomes']['starfall'])
corruption = customtkinter.StringVar(root, config['Biomes']['corruption'])
null = customtkinter.StringVar(root, config['Biomes']['null'])
glitched = customtkinter.StringVar(root, "Message")
dreamspace = customtkinter.StringVar(root, "Message")
blazing_sun = customtkinter.StringVar(root, config['Biomes']['blazing_sun'])
jester = customtkinter.StringVar(root, config['Biomes']['jester'])
roblox_username = ""


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
    config.set('Webhook', 'discord_user_id', discID.get())
    if detectping_field.get() == "Minimum Rarity":
        config.set('Macro', 'min_rarity_to_ping', "")
    else:
        config.set('Macro', 'min_rarity_to_ping', detectping_field.get())
    with open(config_name, 'w+') as configfile:
        config.write(configfile)

    # end webhook
    if started and not stopped:
        if multi_webhook.get() != "1":
            if "discord" in webhookURL.get() and "https://" in webhookURL.get():
                ending_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                ending_embed = discord_webhook.DiscordEmbed(
                    description="[" + time.strftime('%H:%M:%S') + "]: Macro stopped.")
                ending_embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                        icon_url="https://maxstellar.github.io/maxstellar.png")
                ending_webhook.add_embed(ending_embed)
                ending_webhook.execute()
        else:
            ending_embed = discord_webhook.DiscordEmbed(
                description="[" + time.strftime('%H:%M:%S') + "]: Macro stopped.")
            ending_embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                    icon_url="https://maxstellar.github.io/maxstellar.png")
            for url in webhook_urls:
                ending_webhook = discord_webhook.DiscordWebhook(url=url)
                ending_webhook.add_embed(ending_embed)
                ending_webhook.execute()
    else:
        sys.exit()
    stopped = True


def pause():
    global paused
    paused = not paused
    if paused:
        root.title("maxstellar's Biome Macro - Paused")
    else:
        root.title("maxstellar's Biome Macro - Running")


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


def apply_fast_flags(version):
    global versions_directory, packages_path, roblox_folder
    if roblox_version == 'player':
        # create ClientSettings folder in RobloxPlayer directory, if not already existing
        clientsettings_directory = os.path.join(versions_directory, version, "ClientSettings")
    elif roblox_version == 'store':
        clientsettings_directory = os.path.join(packages_path, roblox_folder, "LocalState", "ClientSettings")
    else:
        print("Error finding Roblox version while applying fast flags.")
        logger.error("Error finding Roblox version while applying fast flags.")
        stop()
        return
    try:
        os.mkdir(clientsettings_directory)
    except OSError as e:
        logger.error(e)
        print(e)
    # create settings json file, if not already existing
    flags = {"FStringDebugLuaLogLevel": "debug", "FStringDebugLuaLogPattern": "ExpChat/mountClientApp"}
    try:
        with open(clientsettings_directory + "/ClientAppSettings.json", "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {}
    existing_data.update(flags)
    with open(clientsettings_directory + "/ClientAppSettings.json", "w") as f:
        json.dump(existing_data, f, indent=4)
    print("Successfully patched Roblox and added fast flags.")
    logger.info("Successfully patched Roblox and added fast flags at " + clientsettings_directory + "/ClientAppSettings.json")
    restart_approve = ctypes.windll.user32.MessageBoxW(0,
                                     "Roblox has successfully been patched to enable roll and merchant detection.\nRoblox needs to restart for these changes to apply.\nRestart?",
                                     "Restart?", 4)
    if restart_approve == 6:
        if roblox_version == "player":
            for process in (process for process in psutil.process_iter() if process.name() == "RobloxPlayerBeta.exe"):
                process.kill()
            roblox_exe_path = os.path.join(versions_directory, version, "RobloxPlayerBeta.exe")
            os.startfile(roblox_exe_path)
        elif roblox_version == "store":
            for process in (process for process in psutil.process_iter() if process.name() == "Windows10Universal.exe"):
                process.kill()
        print("Successfully closed/restarted Roblox.")
        ctypes.windll.user32.MessageBoxW(0,
                                         "Successfully patched Roblox to enable Aura and Merchant detection.\nRoblox should have automatically quit and reopened, if not, manually close Roblox and reopen it.\nIt's recommended that you also restart the macro to ensure detection works correctly.",
                                         "Warning", 0)
    else:
        ctypes.windll.user32.MessageBoxW(0,
                                         "Roblox will need to restart to enable these new features (roll and merchant detection).\nPlease finish what you are doing and restart Roblox and the macro ASAP.",
                                         "Warning", 0)


def get_latest_log_file():
    if roblox_log_path:
        files = [f for f in os.listdir(roblox_log_path) if f.endswith(".log")]
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(roblox_log_path, f)))
        return os.path.join(roblox_log_path, latest_file)
    return None


def patch_roblox():
    global last_roblox_version
    if not started:
        ctypes.windll.user32.MessageBoxW(0, 'Start the macro by clicking the "Start" button before attempting to patch Roblox.', "Error", 0)
    apply_fast_flags(last_roblox_version)


def is_roblox_running():
    return detect_roblox_version() is not None


def check_for_hover_text(file):
    global roblox_version, roblox_username
    last_event = None
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
            if line and not paused:
                if '"command":"SetRichPresence"' in line:
                    try:
                        json_data_start = line.find('{"command":"SetRichPresence"')
                        if json_data_start != -1:
                            json_data = json.loads(line[json_data_start:])
                            event = json_data.get("data", {}).get("largeImage", {}).get("hoverText", "")
                            if event and event != last_event:
                                if multi_webhook.get() != "1":
                                    if "discord" not in webhookURL.get() or "https://" not in webhookURL.get():
                                        ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.", "Error",
                                                                         0)
                                        stop()
                                        return
                                    webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                    if event == "NORMAL":
                                        if last_event is not None:
                                            print(time.strftime('%H:%M:%S') + f": Biome Ended - " + last_event)
                                            if globals()[last_event.replace(" ", "_").lower()].get() != "Nothing":
                                                embed = discord_webhook.DiscordEmbed(
                                                    title="[" + time.strftime('%H:%M:%S') + "]",
                                                    color=get_biome_color(last_event),
                                                    description="> ## Biome Ended - " + last_event + "\n" + psURL.get())
                                                embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                                embed.set_thumbnail(
                                                    url="https://maxstellar.github.io/biome_thumb/" + last_event.replace(
                                                        " ", "_") + ".png")
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                        else:
                                            pass
                                    else:
                                        print(time.strftime('%H:%M:%S') + f": Biome Started - {event}")
                                        if globals()[event.replace(" ", "_").lower()].get() != "Nothing":
                                            embed = discord_webhook.DiscordEmbed(
                                                title="[" + time.strftime('%H:%M:%S') + "]",
                                                color=get_biome_color(event),
                                                description="> ## Biome Started - " + event + "\n" + psURL.get())
                                            embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                             icon_url="https://maxstellar.github.io/maxstellar.png")
                                            embed.set_thumbnail(
                                                url="https://maxstellar.github.io/biome_thumb/" + event.replace(" ", "_") + ".png")
                                            webhook.add_embed(embed)
                                        if globals()[event.replace(" ", "_").lower()].get() == "Ping":
                                            webhook.set_content(f"<@{discID.get()}>")
                                        if event == "GLITCHED" or event == "DREAMSPACE":
                                            webhook.set_content("@everyone")
                                        webhook.execute()
                                else:
                                    if event == "NORMAL":
                                        if last_event is not None:
                                            print(time.strftime('%H:%M:%S') + f": Biome Ended - " + last_event)
                                            if globals()[last_event.replace(" ", "_").lower()].get() != "Nothing":
                                                for url in webhook_urls:
                                                    webhook = discord_webhook.DiscordWebhook(url=url)
                                                    embed = discord_webhook.DiscordEmbed(
                                                        title="[" + time.strftime('%H:%M:%S') + "]",
                                                        color=get_biome_color(last_event),
                                                        description="> ## Biome Ended - " + last_event + "\n" + psURL.get())
                                                    embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                                     icon_url="https://maxstellar.github.io/maxstellar.png")
                                                    embed.set_thumbnail(
                                                        url="https://maxstellar.github.io/biome_thumb/" + last_event.replace(
                                                            " ", "_") + ".png")
                                                    webhook.add_embed(embed)
                                                    webhook.execute()
                                        else:
                                            pass
                                    else:
                                        print(time.strftime('%H:%M:%S') + f": Biome Started - {event}")
                                        if globals()[event.replace(" ", "_").lower()].get() != "Nothing":
                                            for url in webhook_urls:
                                                embed = discord_webhook.DiscordEmbed(
                                                    title="[" + time.strftime('%H:%M:%S') + "]",
                                                    color=get_biome_color(event),
                                                    description="> ## Biome Started - " + event + "\n" + psURL.get())
                                                embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                                embed.set_thumbnail(
                                                    url="https://maxstellar.github.io/biome_thumb/" + event.replace(" ", "_") + ".png")
                                                webhook = discord_webhook.DiscordWebhook(url=url)
                                                webhook.add_embed(embed)
                                                if globals()[event.replace(" ", "_").lower()].get() == "Ping":
                                                    webhook.set_content(f"<@{discID.get()}>")
                                                if event == "GLITCHED" or event == "DREAMSPACE":
                                                    webhook.set_content("@everyone")
                                                webhook.execute()
                                last_event = event
                    except json.JSONDecodeError:
                        print("Error decoding JSON")
                elif "Incoming MessageReceived Status:" in line:
                    # check if message is specially formatted (aura roll, jester)
                    if "</font>" in line:
                        if aura_detection.get() == 1 and "HAS FOUND" in line:
                            # handle HAS FOUND message
                            userdata, _, auradata = line.partition("HAS FOUND")
                            auradata = auradata[1:-8]
                            aura, _, rarity = auradata.partition(", ")
                            rarity = rarity[15:-1]
                            int_rarity = rarity.replace(',', '')
                            message_color = line[line.find('<font color="#') + len('<font color="#'):line.find('">', line.find('<font color="#'))]
                            # remove [From Biome]
                            int_rarity = int_rarity.split()[0]
                            if int(int_rarity) < 99999 and aura != "Fault" and "\u00e2\u02dc\u2026" not in aura:
                                continue
                            _, _, full_user = userdata.rpartition(">")
                            full_user = full_user[:-1]
                            if "(" in full_user:
                                _, _, rolled_username = full_user.partition("(")
                                rolled_username = rolled_username[1:]
                            else:
                                rolled_username = full_user[1:]
                            if rolled_username == roblox_username.strip():
                                if multi_webhook.get() != "1":
                                    if "discord" not in webhookURL.get() or "https://" not in webhookURL.get():
                                        ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.",
                                                                         "Error", 0)
                                        stop()
                                        return
                                    webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                    print(time.strftime('%H:%M:%S') + f": Aura Rolled - {aura}")
                                    embed = discord_webhook.DiscordEmbed(
                                        title="[" + time.strftime('%H:%M:%S') + "]",
                                        description="> ## You rolled " + aura + "!\n**Chance of 1 in " + rarity + "**",
                                        color=message_color)
                                    embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                     icon_url="https://maxstellar.github.io/maxstellar.png")
                                    embed.set_thumbnail(url=aura_images[aura.lower()])
                                    webhook.add_embed(embed)
                                    if aura_ping.get() == 1 and int(int_rarity) >= int(detectping_field.get()):
                                        webhook.set_content(f"<@{discID.get()}>")
                                    webhook.execute()
                                    if aura_notif.get() == 1:
                                        toast("You rolled " + aura + "!")
                                else:
                                    print(time.strftime('%H:%M:%S') + f": Aura Rolled - {aura}")
                                    for url in webhook_urls:
                                        webhook = discord_webhook.DiscordWebhook(url=url)
                                        embed = discord_webhook.DiscordEmbed(
                                            title="[" + time.strftime('%H:%M:%S') + "]",
                                            description="> ## You rolled " + aura + "!\n**Chance of 1 in " + rarity + "**",
                                            color=message_color)
                                        embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                         icon_url="https://maxstellar.github.io/maxstellar.png")
                                        embed.set_thumbnail(url=aura_images[aura.lower()])
                                        webhook.add_embed(embed)
                                        if aura_ping.get() == 1 and int(int_rarity) >= int(detectping_field.get()):
                                            webhook.set_content(f"<@{discID.get()}>")
                                        webhook.execute()
                                    if aura_notif.get() == 1:
                                        toast("You rolled " + aura + "!")
                        elif aura_detection.get() == 1 and "The Blinding Light has devoured" in line:
                            if roblox_username in line:
                                if multi_webhook.get() != "1":
                                    if "discord" not in webhookURL.get() or "https://" not in webhookURL.get():
                                        ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.",
                                                                         "Error", 0)
                                        stop()
                                        return
                                    webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                    print(time.strftime('%H:%M:%S') + f": Aura Rolled - Luminosity")
                                    embed = discord_webhook.DiscordEmbed(
                                        title="[" + time.strftime('%H:%M:%S') + "]",
                                        description=f"> ## The Blinding Light has devoured {roblox_username}\n**Chance of 1 in 1,200,000,000**",
                                        color="98b7e0")
                                    embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                     icon_url="https://maxstellar.github.io/maxstellar.png")
                                    embed.set_thumbnail(url=aura_images['luminosity'])
                                    webhook.add_embed(embed)
                                    if aura_ping.get() == 1 and 1200000000 >= int(detectping_field.get()):
                                        webhook.set_content(f"<@{discID.get()}>")
                                    webhook.execute()
                                    if aura_notif.get() == 1:
                                        toast("You rolled Luminosity!")
                                else:
                                    print(time.strftime('%H:%M:%S') + f": Aura Rolled - Luminosity")
                                    for url in webhook_urls:
                                        webhook = discord_webhook.DiscordWebhook(url=url)
                                        embed = discord_webhook.DiscordEmbed(
                                            title="[" + time.strftime('%H:%M:%S') + "]",
                                            description=f"> ## The Blinding Light has devoured {roblox_username}\n**Chance of 1 in 1,200,000,000**",
                                            color="98b7e0")
                                        embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                         icon_url="https://maxstellar.github.io/maxstellar.png")
                                        embed.set_thumbnail(url=aura_images['luminosity'])
                                        webhook.add_embed(embed)
                                        if aura_ping.get() == 1 and 1200000000 >= int(detectping_field.get()):
                                            webhook.set_content(f"<@{discID.get()}>")
                                        webhook.execute()
                                    if aura_notif.get() == 1:
                                        toast("You rolled Luminosity!")
                        elif jester.get() != "Nothing" and "[Merchant]: Jester has arrived on the island!!" in line:
                            if multi_webhook.get() != "1":
                                if "discord" not in webhookURL.get() or "https://" not in webhookURL.get():
                                    ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.",
                                                                     "Error", 0)
                                    stop()
                                    return
                                webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                                print(time.strftime('%H:%M:%S') + f": Jester has arrived!")
                                embed = discord_webhook.DiscordEmbed(
                                    title="[" + time.strftime('%H:%M:%S') + "]",
                                    description=f"> ## Jester has arrived!\n<t:{int(time.time())}:R>\n\n{psURL.get()}",
                                    color="a352ff"
                                )
                                embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                 icon_url="https://maxstellar.github.io/maxstellar.png")
                                embed.set_thumbnail(
                                    url="https://static.wikia.nocookie.net/sol-rng/images/d/db/Headshot_of_Jester.png/revision/latest?cb=20240630142936")
                                webhook.add_embed(embed)
                                if jester.get() == "Ping":
                                    webhook.set_content(f"<@{discID.get()}>")
                                webhook.execute()
                            else:
                                print(time.strftime('%H:%M:%S') + f": Jester has arrived!")
                                for url in webhook_urls:
                                    webhook = discord_webhook.DiscordWebhook(url=url)
                                    embed = discord_webhook.DiscordEmbed(
                                        title="[" + time.strftime('%H:%M:%S') + "]",
                                        description=f"> ## Jester has arrived!\n<t:{int(time.time())}:R>\n\n{psURL.get()}",
                                        color="a352ff"
                                    )
                                    embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                                     icon_url="https://maxstellar.github.io/maxstellar.png")
                                    embed.set_thumbnail(
                                        url="https://static.wikia.nocookie.net/sol-rng/images/d/db/Headshot_of_Jester.png/revision/latest?cb=20240630142936")
                                    webhook.add_embed(embed)
                                    if jester.get() == "Ping":
                                        webhook.set_content(f"<@{discID.get()}>")
                                    webhook.execute()
                elif 'Eden has appeared' in line and "<" in line:
                    if multi_webhook.get() != "1":
                        if "discord" not in webhookURL.get() or "https://" not in webhookURL.get():
                            ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.",
                                                             "Error", 0)
                            stop()
                            return
                        webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                        print(time.strftime('%H:%M:%S') + ": Eden has appeared somewhere in The Limbo.")
                        embed = discord_webhook.DiscordEmbed(
                            title="[" + time.strftime('%H:%M:%S') + "]",
                            description="> ## Eden has appeared somewhere in The Limbo.",
                            color="000000"
                        )
                        embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                         icon_url="https://maxstellar.github.io/maxstellar.png")
                        embed.set_thumbnail(
                            url="https://maxstellar.github.io/biome_thumb/eden.png")
                        webhook.add_embed(embed)
                        webhook.set_content(f"<@{discID.get()}>")
                        webhook.execute()
                    else:
                        print(time.strftime('%H:%M:%S') + ": Eden has appeared somewhere in The Limbo.")
                        for url in webhook_urls:
                            webhook = discord_webhook.DiscordWebhook(url=url)
                            embed = discord_webhook.DiscordEmbed(
                                title="[" + time.strftime('%H:%M:%S') + "]",
                                description="> ## Eden has appeared somewhere in The Limbo.",
                                color="000000"
                            )
                            embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                             icon_url="https://maxstellar.github.io/maxstellar.png")
                            embed.set_thumbnail(
                                url="https://maxstellar.github.io/biome_thumb/eden.png")
                            webhook.add_embed(embed)
                            webhook.set_content(f"<@{discID.get()}>")
                            webhook.execute()
            else:
                time.sleep(0.1)
        else:
            print("Roblox is closed, waiting for Roblox to start...")
            if multi_webhook.get() != "1":
                if "discord" not in webhookURL.get() or "https://" not in webhookURL.get():
                    ctypes.windll.user32.MessageBoxW(0, "Invalid or missing webhook link.", "Error", 0)
                    stop()
                    return
                close_webhook = discord_webhook.DiscordWebhook(url=webhookURL.get())
                close_embed = discord_webhook.DiscordEmbed(
                    description="[" + time.strftime('%H:%M:%S') + "]: Roblox was closed/crashed.")
                close_embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                       icon_url="https://maxstellar.github.io/maxstellar.png")
                close_webhook.add_embed(close_embed)
                close_webhook.execute()
            else:
                for url in webhook_urls:
                    close_webhook = discord_webhook.DiscordWebhook(url=url)
                    close_embed = discord_webhook.DiscordEmbed(
                        description="[" + time.strftime('%H:%M:%S') + "]: Roblox was closed/crashed.")
                    close_embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                                           icon_url="https://maxstellar.github.io/maxstellar.png")
                    close_webhook.add_embed(close_embed)
                    close_webhook.execute()
            root.title("maxstellar's Biome Macro - No Roblox Detected")
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
    config.set('Macro', 'aura_detection', str(aura_detection.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def auranotif_toggle_update():
    config.set('Macro', 'aura_notif', str(aura_notif.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def auraping_toggle_update():
    config.set('Macro', 'aura_ping', str(aura_ping.get()))
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_windy(new_val):
    config.set('Biomes', "windy", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_snowy(new_val):
    config.set('Biomes', "snowy", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_rainy(new_val):
    config.set('Biomes', "rainy", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_sand_storm(new_val):
    config.set('Biomes', "sand_storm", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_hell(new_val):
    config.set('Biomes', "hell", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_starfall(new_val):
    config.set('Biomes', "starfall", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_corruption(new_val):
    config.set('Biomes', "corruption", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_null(new_val):
    config.set('Biomes', "null", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_blazing_sun(new_val):
    config.set('Biomes', "blazing_sun", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def set_jester(new_val):
    config.set('Biomes', "jester", new_val)
    with open(config_name, 'w+') as configfile:
        config.write(configfile)


def manage_tlw():
    global tlw_open, dirname
    if not tlw_open:
        # create tlw
        tlw_open = True
        tlw = customtkinter.CTkToplevel()
        tlw.bind("<Destroy>", lambda e: globals().__setitem__('tlw_open', False))
        tlw.title("Configure Pings")
        tlw_label = customtkinter.CTkLabel(tlw, text="Choose what you get notified for!",
                                           font=customtkinter.CTkFont(family="Segoe UI", size=20))
        tlw_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        windy_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                   font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                   variable=windy,
                                                   command=set_windy)
        windy_toggle.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        snowy_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                   font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                   variable=snowy,
                                                   command=set_snowy)
        snowy_toggle.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        rainy_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                   font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                   variable=rainy,
                                                   command=set_rainy)
        rainy_toggle.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        sand_storm_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                        font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                        variable=sand_storm,
                                                        command=set_sand_storm)
        sand_storm_toggle.grid(row=4, column=1, sticky="w", padx=10, pady=10)
        blazing_sun_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                         font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                         variable=blazing_sun,
                                                         command=set_blazing_sun)
        blazing_sun_toggle.grid(row=5, column=1, sticky="w", padx=10, pady=10)
        hell_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                  font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=hell,
                                                  command=set_hell)
        hell_toggle.grid(row=1, column=3, sticky="w", padx=10, pady=10)
        starfall_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                      font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                      variable=starfall, command=set_starfall)
        starfall_toggle.grid(row=2, column=3, sticky="w", padx=10, pady=10)
        corruption_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                        font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                        variable=corruption, command=set_corruption)
        corruption_toggle.grid(row=3, column=3, sticky="w", padx=10, pady=10)
        null_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                  font=customtkinter.CTkFont(family="Segoe UI", size=20), variable=null,
                                                  command=set_null)
        null_toggle.grid(row=4, column=3, sticky="w", padx=10, pady=10)
        jester_toggle = customtkinter.CTkOptionMenu(tlw, values=["Message", "Ping", "Nothing"],
                                                    font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                                    variable=jester,
                                                    command=set_jester)
        jester_toggle.grid(row=5, column=3, sticky="w", padx=10, pady=10)
        windy_label = customtkinter.CTkLabel(tlw, text="Windy",
                                             font=customtkinter.CTkFont(family="Segoe UI", size=20))
        windy_label.grid(column=0, row=1, padx=(10, 0), pady=10, sticky="w")
        snowy_label = customtkinter.CTkLabel(tlw, text="Snowy",
                                             font=customtkinter.CTkFont(family="Segoe UI", size=20))
        snowy_label.grid(column=0, row=2, padx=(10, 0), pady=10, sticky="w")
        rainy_label = customtkinter.CTkLabel(tlw, text="Rainy",
                                             font=customtkinter.CTkFont(family="Segoe UI", size=20))
        rainy_label.grid(column=0, row=3, padx=(10, 0), pady=10, sticky="w")
        sand_storm_label = customtkinter.CTkLabel(tlw, text="Sand Storm",
                                                  font=customtkinter.CTkFont(family="Segoe UI", size=20))
        sand_storm_label.grid(column=0, row=4, padx=(10, 0), pady=10, sticky="w")
        blazing_sun_label = customtkinter.CTkLabel(tlw, text="Blazing Sun",
                                                   font=customtkinter.CTkFont(family="Segoe UI", size=20))
        blazing_sun_label.grid(column=0, row=5, padx=(10, 0), pady=10, sticky="w")
        hell_label = customtkinter.CTkLabel(tlw, text="Hell",
                                            font=customtkinter.CTkFont(family="Segoe UI", size=20))
        hell_label.grid(column=2, row=1, padx=(10, 0), pady=10, sticky="w")
        starfall_label = customtkinter.CTkLabel(tlw, text="Starfall",
                                                font=customtkinter.CTkFont(family="Segoe UI", size=20))
        starfall_label.grid(column=2, row=2, padx=(10, 0), pady=10, sticky="w")
        corruption_label = customtkinter.CTkLabel(tlw, text="Corruption",
                                                  font=customtkinter.CTkFont(family="Segoe UI", size=20))
        corruption_label.grid(column=2, row=3, padx=(10, 0), pady=10, sticky="w")
        null_label = customtkinter.CTkLabel(tlw, text="Null",
                                            font=customtkinter.CTkFont(family="Segoe UI", size=20))
        null_label.grid(column=2, row=4, padx=(10, 0), pady=10, sticky="w")
        jester_label = customtkinter.CTkLabel(tlw, text="Jester",
                                              font=customtkinter.CTkFont(family="Segoe UI", size=20))
        jester_label.grid(column=2, row=5, padx=(10, 0), pady=10, sticky="w")
        tlw.after(0, tlw.focus)
        tlw.after(100, lambda: tlw.resizable(False, False))
        tlw.after(250, lambda: tlw.iconbitmap(dirname + '\\icon.ico'))


def init():
    global roblox_open, started, paused, roblox_username, last_roblox_version

    if paused:
        paused = False
        root.title("maxstellar's Biome Macro - Running")

    if started:
        return

    webhook_field.configure(state="disabled", text_color="gray")
    ps_field.configure(state="disabled", text_color="gray")
    discid_field.configure(state="disabled", text_color="gray")
    if "," in detectping_field.get():
        new_dp_val = detectping_field.get().replace(",", "")
        detectping_field.delete(0, len(detectping_field.get()) + 1)
        detectping_field.insert(0, new_dp_val)
    if not detectping_field.get().isnumeric():
        detectping_field.delete(0, len(detectping_field.get()) + 1)
    detectping_field.configure(state="disabled", text_color="gray")
    # write new settings to config
    config.set('Webhook', 'webhook_url', webhookURL.get())
    config.set('Webhook', 'private_server', psURL.get())
    config.set('Webhook', 'discord_user_id', discID.get())
    if detectping_field.get() == "Minimum Rarity":
        config.set('Macro', 'min_rarity_to_ping', "")
    else:
        config.set('Macro', 'min_rarity_to_ping', detectping_field.get())

    # Writing configuration file to 'config.ini'
    with open(config_name, 'w+') as configfile:
        config.write(configfile)

    # start webhook
    starting_embed = discord_webhook.DiscordEmbed(
        description="[" + time.strftime('%H:%M:%S') + "]: Macro started!")
    starting_embed.set_footer(text="maxstellar's Biome Macro | v2.0.2",
                              icon_url="https://maxstellar.github.io/maxstellar.png")
    if multi_webhook.get() != "1":
        if "discord" not in webhookURL.get() or "https://" not in webhookURL.get():
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

    if not discID.get().isnumeric():
        ctypes.windll.user32.MessageBoxW(0,
                                         "Discord User ID should only be a number.\nIf it is something else, such as @everyone, or your username, that is not your Discord User ID.",
                                         "Error", 0)
        stop()
        return

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
        root.title("maxstellar's Biome Macro - No Roblox Detected")
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
        # checking for username
        found_update_version = False
        found_username = False
        for line in file:
            if "[FLog::UpdateController] version response:" in line:
                found_update_version = True
                try:
                    json_data_start = line.find('{"version')
                    if json_data_start != -1:
                        json_data = json.loads(line[json_data_start:])
                        update_version = json_data.get("clientVersionUpload", "")
                        logger.info("Update version found: " + update_version)
                        print("Update version found: " + update_version)
                except:
                    print("Encountered error while parsing JSON to find Roblox update version.")
                    logger.error("Encountered error while parsing JSON to find Roblox update version.")
                    stop()
                if update_version == last_roblox_version and update_version != "":
                    pass
                else:
                    last_roblox_version = update_version
                    # write new version to config
                    config.set('Macro', 'last_roblox_version', last_roblox_version)
                    with open(config_name, 'w+') as configfile:
                        config.write(configfile)
                    apply_fast_flags(update_version)
            elif "Local character loaded:" in line and "Incoming MessageReceived Status:" not in line:
                try:
                    _, _, roblox_username = line.partition("Local character loaded: ")
                    roblox_username = roblox_username.strip()
                    logger.info("Username found: " + roblox_username)
                    print("Username found: " + roblox_username)
                    break
                except:
                    print("Encountered error finding username.")
                    logger.error("Encountered error finding username.")
                    stop()
        if roblox_username == "" and username_override == "":
            ctypes.windll.user32.MessageBoxW(0,
                                             'The macro failed to find your Roblox username (possibly due to Microsoft Store Roblox).\nPlease manually input your Roblox username (NOT YOUR DISPLAY NAME. For example, @KrystaiTwo) in the "username_override" field\nin the "config.ini" file in the macro directory in order to reenable roll detection. Jester and Eden detection will not be affected',
                                             "Warning", 0)
        elif roblox_username == "" and username_override != "":
            roblox_username = username_override
        if not found_update_version and roblox_version == "store":
            apply_fast_flags(None)
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

discid_label = customtkinter.CTkLabel(tabview.tab("Webhook"), text="Discord User ID:",
                                      font=customtkinter.CTkFont(family="Segoe UI", size=20))
discid_label.grid(column=0, row=2, padx=(10, 0), pady=(20, 0), columnspan=2, sticky="w")

discid_field = customtkinter.CTkEntry(tabview.tab("Webhook"), font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                      width=324, textvariable=discID)
discid_field.grid(row=2, column=1, padx=(155, 0), pady=(23, 0), sticky="w")

biome_button = customtkinter.CTkButton(tabview.tab("Macro"), text="Configure Pings",
                                       font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
                                       command=manage_tlw)
biome_button.grid(row=3, column=0, padx=(10, 0), columnspan=2, pady=(12, 0), sticky="w")

# patch_button = customtkinter.CTkButton(tabview.tab("Macro"), text="Patch Roblox",
#                                       font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
#                                       command=patch_roblox)
# patch_button.grid(row=3, column=1, padx=(10, 0), columnspan=2, pady=(12, 0), sticky="w")

start_button = customtkinter.CTkButton(root, text="Start",
                                       font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
                                       command=init)
start_button.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

pause_button = customtkinter.CTkButton(root, text="Pause",
                                       font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
                                       command=pause)
pause_button.grid(row=1, column=1, padx=(5, 0), pady=(10, 0), sticky="w")

stop_button = customtkinter.CTkButton(root, text="Stop",
                                      font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), width=75,
                                      command=stop)
stop_button.grid(row=1, column=2, padx=(5, 0), pady=(10, 0), sticky="w")

max_pfp = customtkinter.CTkImage(dark_image=Image.open(dirname + "\\maxstellar.png"), size=(70, 70))
max_pfp_label = customtkinter.CTkLabel(tabview.tab("Credits"), image=max_pfp, text="")
max_pfp_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

sols_sniper = customtkinter.CTkImage(dark_image=Image.open(dirname + "\\sols_sniper.png"), size=(70, 70))
sols_sniper_label = customtkinter.CTkLabel(tabview.tab("Credits"), image=sols_sniper, text="")
sols_sniper_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

credits_frame = customtkinter.CTkFrame(tabview.tab("Credits"))
credits_frame.grid(row=0, column=1, padx=(7, 0), pady=(10, 0), sticky="w")

credits_frame_2 = customtkinter.CTkFrame(tabview.tab("Credits"))
credits_frame_2.grid(row=1, column=1, padx=(7, 0), pady=(10, 0), sticky="w")

max_label = customtkinter.CTkLabel(credits_frame, text="maxstellar - Creator",
                                   font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"))
max_label.grid(row=0, column=0, padx=(5, 0), sticky="nw")

youtube_link = customtkinter.CTkLabel(credits_frame, text="YouTube", font=("Segoe UI", 14, "underline"),
                                      text_color="dodgerblue", cursor="hand2")
youtube_link.grid(row=1, column=0, padx=(5, 0), sticky="nw")
youtube_link.bind("<Button-1>", lambda e: open_url("https://youtube.com/@maxstellar_"))

sniper_label = customtkinter.CTkLabel(credits_frame_2, text="dannw & yeswe - Developers",
                                      font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"))
sniper_label.grid(row=2, column=0, padx=(5, 0), pady=(5, 0), sticky="nw")

support_link = customtkinter.CTkLabel(credits_frame_2, text="Discord", font=("Segoe UI", 14, "underline"),
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

detectping_toggle = customtkinter.CTkCheckBox(tabview.tab("Macro"), text="Aura Pings",
                                              font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                              variable=aura_ping, command=auraping_toggle_update)
detectping_toggle.grid(row=2, column=0, columnspan=2, padx=(10, 0), pady=(12, 0), sticky="w")
detectping_field = customtkinter.CTkEntry(tabview.tab("Macro"), font=customtkinter.CTkFont(family="Segoe UI", size=20),
                                          width=155, textvariable=None, placeholder_text="Minimum Rarity")
detectping_field.grid(row=2, column=1, padx=(130, 0), pady=(10, 0), sticky="w")

min_rarity_to_ping = config['Macro']['min_rarity_to_ping']
if min_rarity_to_ping != "":
    detectping_field.insert(0, min_rarity_to_ping)

root.bind("<Destroy>", lambda event: x_stop())
root.bind("<Button-1>", lambda e: e.widget.focus_set())

root.mainloop()
