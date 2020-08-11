import sys,os
sys.path.append('../')

from lookups import PKMString
from structure import PersonalTable,WC8
pmtext = PKMString('zh')
buf = bytearray(open('../resources/bytes/personal_swsh','rb').read())
pt = PersonalTable(buf)

def getString(slist):
    if slist[0] == slist[1]:
        return slist[0]
    else:
        output = ''
        for ii in range(9):
            output += '{{tt|' + slist[ii] + '|' + WC8.LANG[ii] + '}}<br>'
        return output[:-4]

def getribbon(flag):
    if flag[0] == 16:
        if flag[1] == 26:
            return '经典奖章'
        if flag[1] == 28:
            return '活动奖章'
        if flag[1] == 29:
            return '生日奖章'
        if flag[1] == 31:
            return '回忆奖章'
        if flag[1] == 32:
            return '许愿奖章'
    return flag

def getndex(species,forme):
    output = f'{species:03}'
    if forme == 0:
        return output
    if species in PersonalTable.Alolalist and forme == 1:
        return output + 'A'
    if species in PersonalTable.Galarlist:
        return output + 'G'

epath = './Wondercards/'
for file in os.listdir(epath):
    if file[-4:] != '.wc8':
        continue
    buf = bytearray(open(epath + file,'rb').read())
    wc = WC8(buf)
    if not wc.isPokemon():
        continue
    pi = pt.getFormeEntry(wc.species(),wc.forme())

    nicknamelist = []
    otlist = []
    for idx in range(9):
        nicknamelist.append(wc.nickname(idx))
        otlist.append(wc.ownername(idx))

    if wc.isHome():
        print('''{{活动赠送宝可梦\n|gen=8\n|game=HOME''')
    else:
        print('''{{活动赠送宝可梦\n|gen=8\n|game=SWSH''')
    print(f'|ndex={getndex(wc.species(),wc.forme())}')
    print(f'|pokemon={pmtext.species[wc.species()]}')
    if getString(nicknamelist) != '':
        print(f'|nickname={getString(nicknamelist)}')
    if wc.gender() > 2:
        gender = 'both'
    else:
        gender = ['M','F',''][wc.gender()]
    print(f'|gender={gender}')
    print(f'|imagegender=')
    if wc.isShiny():
        print(f'|shiny=s')
    if wc.canGMax():
        print(f'|max=yes')
    print(f'|level={wc.level()}')
    if wc.level() != wc.metLevel():
        print(f'|met={wc.metLevel()}')
    print(f'|type1={pmtext.types[pi.Type1()]}')
    if pi.Type1() != pi.Type2():
        print(f'|type2={pmtext.types[pi.Type2()]}')
    if wc.hasOT():
        print(f'|owner={getString(otlist)}')
        print(f'|ownerid={wc.fullID() % 1000000}')
        print('|ownergender=' + ['M','F'][wc.OTgender()])
    else:
        print('|owner={{主角}}')
        print(f"|ownerid=''主角的ID''")
        print('|ownergender=')
    print(f'|pokeball={pmtext.items[wc.ball()]}')
    if wc.abilityType() < 3:
        print(f'|ability={pmtext.abilities[pi.Abilities()[wc.abilityType()]]}')
    else:
        print(f'|ability={pmtext.abilities[pi.Abilities()[0]]}')
        if pi.Abilities()[1] != pi.Abilities()[0]:
            print(f'|ability2={pmtext.abilities[pi.Abilities()[1]]}')
        if wc.abilityType() == 4 and pi.Abilities()[2] != pi.Abilities()[0]:
            print(f'|abilityh={pmtext.abilities[pi.Abilities()[2]]}')
    if wc.heldItem() != 0:
        print(f'|held={pmtext.items[wc.heldItem()]}')
    for flag in wc.ribbonflags():
        print(f'|ribbonimage={getribbon(flag)}.png')
        print(f'|ribbonname={getribbon(flag)}')
    print(f'|time=')
    if wc.isHome():
        print(f'|inhand= Pokémon HOME（[[命中注定般的相遇]]）')
    else:
        print(f'|inhand= {pmtext.locations[wc.metLocation() - 40001]}（[[命中注定般的相遇]]）')

    if wc.nature() < 25:
        print(f'|nature={pmtext.natures[wc.nature()]}')
    else:
        print(f'|nature=随机')

    if 0xFB < wc.IV_HP() and wc.IV_HP() < 0xFF:
        print(f'|IVRule=保底{wc.IV_HP() - 0xFB}项个体为31')
    def getiv(iv):
        if iv < 32:
            return iv
        else:
            return '?'
    if wc.IV_HP() < 32 or wc.IV_Atk() < 32 or wc.IV_Def() < 32 or wc.IV_SpA() < 32 or wc.IV_SpD() < 32 or wc.IV_Spe() < 32:
        print(f'|IVHP={getiv(wc.IV_HP())}')
        print(f'|IVAtk={getiv(wc.IV_Atk())}')
        print(f'|IVDef={getiv(wc.IV_Def())}')
        print(f'|IVSpA={getiv(wc.IV_SpA())}')
        print(f'|IVSpD={getiv(wc.IV_SpD())}')
        print(f'|IVSp={getiv(wc.IV_Spe())}')

    if wc.EV_HP() + wc.EV_Atk() + wc.EV_Def() + wc.EV_SpA() + wc.EV_SpD() +  wc.EV_Spe() > 0:
        print(f'|EVHP={wc.EV_HP()}')
        print(f'|EVAtk={wc.EV_Atk()}')
        print(f'|EVDef={wc.EV_Def()}')
        print(f'|EVSpA={wc.EV_SpA()}')
        print(f'|EVSpD={wc.EV_SpD()}')
        print(f'|EVSp={wc.EV_Spe()}')

    catlist =['变化','物理','特殊']
    for ii in range(4):
        if wc.move(ii) > 0:
            print(f'|move{ii+1}={pmtext.moves[wc.move(ii)]}|move{ii+1}type={pmtext.movetypes[wc.move(ii)]}|move{ii+1}cat={catlist[pmtext.movecats[wc.move(ii)]]}')
    if wc.isHome():
        print('''|receivegame={{GameIconzh/8|HOME}}\n}}\n''')
    else:
        print('''|receivegame={{GameIconzh/8|SWSH}}\n}}\n''')