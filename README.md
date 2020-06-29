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
* CFW
* Internet Connection
* [sys-botbase](https://github.com/olliz0r/sys-botbase) 1.5
* [ldn_mitm](https://github.com/spacemeowx2/ldn_mitm)
* [Luxray](https://github.com/3096/luxray) (only for some bots)

## Usage
Use [CaptureSight](https://github.com/zaksabeast/CaptureSight/)/CheckDen script to check your Den id

Raid Finder:
1) Install the latest release of [Python](https://www.python.org/downloads/)
2) Connect your Switch to Interet
3) Start sys-botbase and ldn_mitm
4) Go to System Settings, check your Switch IP and write it inside config.json file
5) Start the game and set game text speed to normal
6) Save in front of an empty Den and leave the game opened. You must have at least one Wishing Piece in your bag
7) Modify research filters inside the script according to what is written below
8) Run the script

* r.ShinyType == 'None'/'Star'/'Square' (!= 'None' for both Square/Star shiny type)
* Util.STRINGS.natures[r.Nature] == 'Nature' (i.e. Util.STRINGS.natures[r.Nature] == 'Timid')
* r.Ability == 1/2/'H'
* r.IVs == spread_name (spread_name = [x,x,x,x,x,x])

Stars Finder:
1) Install the latest release of [Python](https://www.python.org/downloads/)
2) Connect your Switch to Interet
2) Start sys-botbase, ldn_mitm and luxray (the yellow cursor of luxray has to be over "+3" button)
3) Go to System Settings, check your Switch IP and write it inside config.json file
4) Start the game, save in front of an Den whose beam has been generated through a Wishing Piece and leave the game opened
5) Run the script

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
