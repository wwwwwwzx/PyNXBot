# Go to root of PyNXBot
import sys
sys.path.append('../')
from nxbot import SWSHBot
import json

DumpPath = 'Event/PersonalDump/'
config = json.load(open("../config.json"))

b = SWSHBot(config["IP"])

print("Dumping bonus_rewards...")
b.readEventBlock_BonusRewards(DumpPath)
print("Dumping dai_encount...")
b.readEventBlock_CrystalEncounter(DumpPath)
print("Dumping drop_rewards...")
b.readEventBlock_DropRewards(DumpPath)
print("Dumping normal_encount...")
b.readEventBlock_RaidEncounter(DumpPath)
print("Dumping normal_encount_rigel1...")
b.readEventBlock_RaidEncounter_IoA(DumpPath)
print("Dumping normal_encount_rigel2...")
b.readEventBlock_RaidEncounter_CT(DumpPath)

print("\nDump completed!\n")

b.close()
