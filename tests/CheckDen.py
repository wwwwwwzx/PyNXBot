# Settings
IP = '192.168.1.7'

# Desired IVs
V6 = [31,31,31,31,31,31]
S0 = [31,31,31,31,31,00]
A0 = [31,00,31,31,31,31]
useFilters = True
MaxResults = 1000
doResearch = True

# Go to root of PyNXBot
import sys
sys.path.append('../')

from lookups import Util
from nxbot import RaidBot
from rng import XOROSHIRO,Raid
from structure import Den

b = RaidBot(IP)
seed = None
print(b.TrainerSave.TID())
print(b.TrainerSave.SID())
for ii in range(RaidBot.DENCOUNT):
        if ii > 99:
                den = Den(b.readDen(ii + 11))
        else:
                den = Den(b.readDen(ii))
        if den.isActive():
                spawn = den.getSpawn(denID = ii, isSword = b.isPlayingSword)
                currShinylock = 0
                if ii > 99:
                        info = f"[IoA] denID {ii-99}"
                else:
                        info = f"denID {ii+1}"
                info += f":0x{den.seed():X}\t{den.stars()}★\tSpecies: {Util.STRINGS.species[spawn.Species()]}\t"
                if spawn.IsGigantamax():
                        info += "G-Max\t"
                if den.isEvent():
                        info += "Event\t"
                        currShinylock = spawn.ShinyFlag()
                if den.isWishingPiece():
                        info += f"Next Shiny Frame: {Raid.getNextShinyFrame(den.seed())}\t"
                        seed = den.seed()
                        info = "!!!\t" + info
                        piecedSpawn = spawn
                        piecedShinylock = currShinylock
                print(info)
                r = Raid(seed = den.seed(), TID = b.TrainerSave.TID(), SID = b.TrainerSave.SID(), flawlessiv = spawn.FlawlessIVs(), shinylock = currShinylock, ability = spawn.Ability(), gender = spawn.Gender(), species = spawn.Species(), altform = spawn.AltForm())
                r.print()
                print()

# Choose RNGable den to calculate frames
if seed is not None and doResearch:
        print('Wishing Piece Den Prediction:')
        i = 0
        while i < MaxResults:
                r = Raid(seed, TID = b.TrainerSave.TID(), SID = b.TrainerSave.SID(), flawlessiv = piecedSpawn.FlawlessIVs(), shinylock = piecedShinylock, ability = piecedSpawn.Ability(), gender = piecedSpawn.Gender(), species = piecedSpawn.Species(), altform = piecedSpawn.AltForm())
                seed = XOROSHIRO(seed).next()
                if useFilters:
                        if (r.ShinyType != 'None' or r.IVs == V6 or r.IVs == S0 or r.IVs == A0) and Util.STRINGS.natures[r.Nature] == 'Careful':
                                print(f"Frame:{i}")
                                r.print()
                else:
                        print(f"Frame:{i}")
                        r.print()
                i += 1
