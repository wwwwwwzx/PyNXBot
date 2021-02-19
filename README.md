# PyNXBot
 Python Lib for Pokemon Sword and Shield, including many bots!

 ![toxricity](https://i.imgur.com/iMho3F7.png) 

## Warning
 I won't be liable if your Switch get damaged or banned. Use at your own risk.

 ## Features
 * Check Dens info
 * Check Wilds info
 * Check Party Pokémon info
 * Check Box Pokémon info (incoming...)
 * Check Trainer info (incoming...)

 ## Bots
* RaidFinder - useful to softreset Den Seed (Event Raids, Rare Beam Raids, perfect IVs, Shininess at low frames, etc.)
* StarsFinder - useful to softreset Den Species + Stars
* BerryPicker - useful to farm berries/apricorns from trees
* ASpammer - useful to spam A button during boring dialogues, can be used also to farm Items in Cram-o-Matic machine
* LegendaryFinder - useful to softreset Legendary (incoming...)

## Requirements
* [Python](https://www.python.org/downloads/)
	* Install z3-solver and pyserial via [pip](https://pip.pypa.io/en/stable/) if `ImportError` happens.
	   `pip install z3-solver` 
	   `pip install pyserial`
* CFW
* Internet Connection
* [sys-botbase](https://github.com/olliz0r/sys-botbase) 1.5
* [ldn_mitm](https://github.com/spacemeowx2/ldn_mitm)
* [Luxray](https://github.com/3096/luxray) (only for some bots)

## Usage
Use [CaptureSight](https://github.com/zaksabeast/CaptureSight/)/CheckDen script to check your Den id

Raid Finder:
1) Connect your Switch to Internet
2) Start sys-botbase and ldn_mitm
3) Go to System Settings, check your Switch IP and write it inside the "config.json" file
4) Start the game and set game text speed to normal
5) Save in front of an empty Den and leave the game opened. You must have at least one Wishing Piece in your bag
6) Modify research filters inside the script according to what is written below
7) Run the script

* Util.STRINGS.natures[r.Nature] == 'Nature' (i.e. Util.STRINGS.natures[r.Nature] == 'Timid')
* r.Ability == 1/2/'H'
* r.ShinyType == 'None'/'Star'/'Square' (!= 'None' for both Square/Star shiny type)
* r.IVs == spread_name (spread_name = [x,x,x,x,x,x])
* Util.GenderSymbol[r.Gender] == '♂'/'♀'/'-'

Stars Finder:
1) Connect your Switch to Internet
2) Start sys-botbase, ldn_mitm and luxray (the yellow cursor of luxray has to be over "+3" button)
3) Go to System Settings, check your Switch IP and write it inside "config.json" file
4) Start the game, save in front of an Den whose beam has been generated through a Wishing Piece and leave the game opened
5) Run the script

Stationary Finder:
1) Connect your Switch to Interet
2) Start sys-botbase and ldn_mitm
3) Go to System Settings, check your Switch IP and write it inside the "config.json" file
4) Save in front of a stationary and leave the game opened
5) Modify research filters inside the script according to what is written below
6) Run the script

* pk8.getAbilityString() == 1/2/'H'
* Util.STRINGS.natures[pk8.nature()] == 'Nature'
* pk8.shinyString() == 'None'/'Star'/'Square' (!= 'None' for both star/square)
* pk8.IVs == spread_name (spread_name = [x,x,x,x,x,x])
* Util.GenderSymbol[pk8.gender()] == '♂'/'♀'/'-'

### GUI in Python: NXController

This is a port from C++, please check more details from [my prior project](https://github.com/wwwwwwzx/NXController).
1) Install the PyQt5 module via [pip](https://pip.pypa.io/en/stable/):
`pip install pyqt5`
2) Connect your Switch to Internet or Arduino
3) Go to System Settings, check your Switch IP
4) Run the script. The Qt Gui will pop up.

You may change the button setting by editing the json file according to [this website](https://doc.qt.io/qt-5/qt.html#Key-enum). Please note that only decimal numbers are allowed in json.

## Features for fun
Use the binaries and structures from your browsers (iOS, Android): [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/wwwwwwzx/PyNXBot/master?urlpath=lab/tree/test.ipynb). You may have to expose your switch to the internet.

## Always Remember!
Sometimes button inputs of your joycons won't work. This because the fake controller isn't detached from your Switch. 
So, everytime you want to stop the bot, always press CTRL+C and follow the instructions. The bot will detach the fake controller and buttons will work correctly. 

## Credits:
* olliz0r for his great [sys-botbase](https://github.com/olliz0r/sys-botbase) which let open sockets on the Nintendo Switch
* spacemeowx2 for his livesafer [sys-module](https://github.com/spacemeowx2/ldn_mitm). It avoids Switch to disconnect from wifi once game is opened
* 3096 for his great day advancer Switch tool [Luxray](https://github.com/3096/ipswitch/)
* Admiral-Fish for his great app [RaidFinder](https://github.com/Admiral-Fish/RaidFinder) always up to date
* zaksabeast for his great SwSh Switch tool [CaptureSight](https://github.com/zaksabeast/CaptureSight/) (many addresses/checks are taken from there)
* Leanny for his great plugin [PKHeX_Raid_Plugin](https://github.com/Leanny/PKHeX_Raid_Plugin/tree/master/PKHeX_Raid_Plugin) (many addresses/checks are taken from there)
* Kurt for his great app [SysBot.NET](https://github.com/kwsch/SysBot.NET) (many addresses/checks are taken from there)
* [Real96](https://github.com/Real96) for working on the various bots