# Go to root of PyNXBot
import sys
sys.path.append('../')
from nxbot import SWSHBot
import json

DumpPath = 'Event/PersonalDump/'
config = json.load(open("../config.json"))

b = SWSHBot(config["IP"])

b.readEventBlock_RaidEncounter(DumpPath)
b.readEventBlock_RaidEncounter_IoA(DumpPath)
b.readEventBlock_RaidEncounter_CT(DumpPath)
b.readEventBlock_DropRewards(DumpPath)
b.readEventBlock_BonusRewards(DumpPath)
b.readEventBlock_CrystalEncounter(DumpPath)

b.close()
