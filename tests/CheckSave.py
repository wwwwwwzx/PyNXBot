# Go to root of PyNXBot
import sys
import json
sys.path.append('../')

from nxbot import SWSHBot

config = json.load(open("../config.json"))
b = SWSHBot(config["IP"])

print(f"TID: {b.TrainerSave.TID()}")
print(f"SID: {b.TrainerSave.SID()}")
print(f"TSV: {b.TrainerSave.TSV()}")
print(f"Language: {b.TrainerSave.getLangName()}")
print(f"Money: {b.TrainerSave.Money()}$")
print(f"Watts: {b.TrainerSave.Watts()}\n")

b.close()
