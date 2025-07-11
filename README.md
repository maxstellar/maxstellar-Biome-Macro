<div align="center" style="text-align: center;">
<h1><img src="icon.ico" height="30px">  maxstellar's Biome Macro</h1>
<p> A small macro that detects biomes in the Roblox game Sol's RNG.<br>This macro started as a small project to detect biomes even when I was using my PC for other things.</p>

![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/maxstellar/maxstellar-Biome-Macro/total)
![GitHub Release](https://img.shields.io/github/v/release/maxstellar/maxstellar-Biome-Macro)
![GitHub License](https://img.shields.io/github/license/maxstellar/maxstellar-Biome-Macro)
</div>

## Features
- Biome detection without OCR
- Aura detection without OCR
- Notifications on Aura roll
- Roll detection without cutscene or equip needed (coming soon!)
- Jester and Eden detection (coming soon!)
- Configurable Discord notifications for biomes and Jester (coming soon!)

## Installation
Download the [latest release](https://github.com/maxstellar/maxstellar-Biome-Macro/releases/latest) as a .zip file and extract into an empty folder. Run the .exe file and configure to your liking.<br><br>
Alternatively, if you already have Python installed, download the Python file along with the required libraries and images, and run it from command line or with your preferred method.

## Common Issues
### Macro doesn't detect biomes
- Close ALL instances of Roblox and the macro, and then opening Roblox, and then opening the macro.
- Make sure your PC time is not offset (early or late)

### Macro detects biomes but can't detect rolls or Jester
Here are a list of things to try, in order:
1. Restart Roblox
2. Delete last_roblox_version value from config.ini file in the macro folder, restart the macro and then run it and let it patch Roblox, and then restart Roblox.
3. Redownload the macro and save it to a different location entirely.

### Macro won't launch (shows error message)
- Make sure the zip file downloaded was extracted fully (into a folder)
- Make sure you are running the macro from the extracted folder (and not from the Home page of File Explorer)
- Delete and reinstall macro

Enjoy!
