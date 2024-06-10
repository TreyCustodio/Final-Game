from . import vec
import pygame
"""
Screen Constants
"""
RESOLUTION = vec(304,208)
SCALE = 3
UPSCALED = RESOLUTION * SCALE
EPSILON = 0.01




"""
Global boolean values that represent flags.
Used for a variety of special events.
"""
FLAGS = [False for i in range(100)]
for i in range (1, 10):
    FLAGS[i] = True
#FLAGS[62] = True
#1-10 -> Messages that only display once
#1 -> Grand Chapel
#2 ->

#20 - > Shards first pickup

##50-59 -> Respawn/Checkpoints
#50 -> skip intro (post-death)
#51 -> respawn in Grand Chapel

##60 - > flame fields flags


##88-93 -> Blessings
#88 -> Blessings are locked, way is clear
#89 -> No blessings appear
#90 -> Ice chosen
#91 -> Fire chosen
#92 -> Thunder chosen
#93 -> Wind chosen


##94-100 Completion flags
#94 -> Ice complete
#95 -> Fire complete
#96 -> Thunder complete
#97 -> Wind complete





"""
16x16 coordinates of the screen
"""
COORD = [[(i*16, j*16) for j in range(13)] for i in range(18)]







"""
Indicates what C attack and what type of arrow is equipped
"""
EQUIPPED = {

    "C": 1,
    #0 -> fire sword, 1 -> blizzard, 2 -> clap, 3 -> slash
    "Arrow": 1,
    #0 -> regular, 1 -> bombo, 
    "room":0,
    #0 -> regular, 1 -> fire, 2 -> ice, 3- -> thunder, 4-> wind, 5-> super, 6-> hyper
    "area":0,
}



"""
The Player's inventory
"""
INV = {

    ##Health, elements, arrows, currency
    "max_hp": 3,
    "shoot": True,
    "hasBombo": True,
    "fire": True,
    "clap": True,
    "slash": True,
    "cleats": True,
    "maxBombo": 10,
    "bombo": 10,
    "flameShard": 0,
    "frostShard": 0,
    "boltShard": 0,
    "galeShard": 0,
    
    
    ##Maps
    "map0":True,
    "map1":False,
    "map2":False,
    "map3":False,
    "map4":False,

    ##Consumables and key items
    "plant": 1,
    "chanceEmblem": True,
    "syringe":True,
    "potion": 3,
    "smoothie": 3,
    "beer": 8,
    "joint":1,
    "speed":1,
    "wallet": 20,
    "money": 0,
    "keys": 1,

    ##Upgrades
    "flameCost": 50,
    "frostCost": 20,
    "boltCost": 20,
    "galeCost": 20,

}


"""
Text for the intro cutscene

&& -> clear textbox before printing another line
"""
INTRO = {
    -1:"          Majestus.&&\n\
The ruins of an ancient\n\
tribe of religious mages:\n\
      The Naturalites.&&\n\
In paradise, the Naturalites\n\
prayed to their Gods,\n\
the four elemental deities:&&\n\
Firion, of the Flame,&&\n\
Estelle, of the Frost,&&\n\
Kuwabara, of the Bolt,&&\n\
Gladius, of the Gale.&&\n\
The deities granted their\n\
worshippers with power,\n\
and the Naturalites lived\n\
prosperous lives for eons.\n\
Until one day...&&\n\
Vash, the Naturalite King,\n\
waged war on the world.\n\
Using their Gods' blessings\n\
for selfish conquest,\n\
the undefeatable mages\n\
tore apart the outside world,\n\
scorching fields,\n\
freezing oceans,\n\
shocking hearts,\n\
slicing heads.\n\
At the war's climax, the\n\
King, with great audacity,\n\
asked his Gods to grant\n\
him more of their power.\n\
So, the Gods punished his\n\
unquenchable thirst.\n\
They sealed the King and\n\
his people within Majestus,\n\
never to be seen again.&&\n\
As for the Gods...&&\n\
They forsook their role\n\
in the mortal realm,\n\
leaving behind fragments\n\
of their power in Majestus.\n\
Today, some search for\n\
these fragments.\n\
But none who make the\n\
venture have returned...\n",

0:"This is the story of\n\
    Majestus.\n",

1:"Twas the mountainous home\n\
of a tribe of mages:\n\
      The Naturalites.&&\n",

      
2:"In paradise, the Naturalites\n\
prayed to their Gods,\n\
the four elemental deities:&&\n",

3:"Firion, of the Flame,&&\n\
Estelle, of the Frost,&&\n\
Kuwabara, of the Bolt,&&\n\
Gladius, of the Gale.&&\n",

4:"The deities granted their\n\
worshippers with power,\n\
and the Naturalites lived\n\
prosperous lives for eons.\n\
Until one day...&&\n",

5: "Using the blessings of\n\
the Gods for selfish means,\n\
the Naturalite King waged\n\
war on the non-elementals.\n\
And the unconquerable mages\n\
tore apart the outside world,\n\
scorching fields,\n\
freezing oceans,\n\
shocking hearts,\n\
slicing heads.\n",


6: "At the war's climax, the\n\
King, with great audacity,\n\
asked his Gods to grant\n\
him more of their power.\n\
So, the Gods punished his\n\
unquenchable thirst.\n\
They sealed the King and\n\
his people within Majestus,\n\
never to be seen again.&&\n",

7: "As for the Gods...&&\n",

8:"They relinquished their role\n\
in the mortal realm,\n\
leaving behind fragments\n\
of their power in Majestus.\n\
Today, some search for\n\
these fragments.\n\
But none who make the\n\
venture ever return...\n"

}




"""
Item info for the pause screen
"""
INFO = {


"plant":
"A vibrantly green vegetable.\n\
Geemers seem to love it.",

"shoot":
"Old reliable.\n\
Press X to shoot.",

"bombo":
"Bombofauns.\n\
Shoot explosive plants.",

"fire":
"The blessing of fire.\n\
Equip with C.",

"cleats":
"The blessing of ice.\n\
Equip with C.",

"clap":
"The blessing of thunder.\n\
Equip with C.",

"slash":
"The blessing of wind.\n\
Equip with C.",

"chance":
"Chance Emblem\n\
Survive any attack,\n\
if you have more than 1 HP."
}




"""
Icons from icon.png to be used in text display
"""
ICON = {
    "blank": (0,0),
    "plant":(1,0),
    "bombo":(4,0),
    "geemer0":(2,0),
    "geemer1":(3,0)
}






"""
All of the text for npcs!
Follows format:

roomName_class#
"""
SPEECH = {
"flameShard":"You found a flame shard!&&\n\
Use it in the Grand Chapel\n\
to upgrade your flame attack!\n\
Check how many you have\n\
on the pause menu.\n",
"first_bombo":
"You've discovered Bombofauns!&&\n\
Fire these explosive plants\n\
to destroy rocks and enemies.\n\
Equip them on the pause menu\n\
and watch your ammo count!\n",

    "key":
"   Picked up a key.&&",
    "switch_unlocked" : "A switch was unlocked.",
    "door_unlocked" : "A door was unlocked.",
    "room_clear":
"   Room cleared!",
    "intro_geemer":"You thought I was a monster,\n\
didn't you?\n\
Don't worry, man,\n\
I get that a lot.\n\
What's a guy like you\n\
doing in here anyway?\n\
There's only monsters\n\
in here now, dude.\n\
What kind of monsters\n\
you ask?\n\
You know..........&&\n\
The undead........&&\n",

    "intro_geemer1": "I'm a Geemer, man.\n\
I know all kindsa stuff.\n\
My bros are around too.&&\n",

    "intro_geemer2": "My name? Oh, dude...\n\
Geemers don't have names,\n\
man...&&\n",

    "intro_geemer3": "Dude I'm so hungry!\n\
Ya got anything to eat,\n\
mannnnnnnnnn????????????&&\n",

    "intro_sign": "/ Temple of the Naturalites\n\
   These sacred halls host\n\
 unwavering souls, who were\n\
corrupted by power and greed.\n\
  The relics sealed within\n\
    contain the blessings\n\
of the four divine guardians.\n\
      Seek their gifts...",
    
    "intro_plantgeemer":
"Mannnnn, I need energy...\n\
Green energy...\n\
.............................&&\n\
Know what I mean?&&\n",

    "intro_plantgeemer2":
"You're giving me this food?&&\n\
Oh, dude, you're the best!&&\n",


    "intro_plantgeemer3":
"Laaaaaaaaaterrrrr...&&",


    "intro_chest":
"You found a strange plant.&&\n\
Let's see if anyone\n\
around here wants it.\n",

    "intro_entrance":
"   Divine forces prevent\n\
    you from leaving.\n",

    "intro_switches":
"Whattup my guy?&&\n\
If ya had a block to push,\n\
I bet you could keep that\n\
red switch pressed down, man.&&\n\
Yeah the one by my bro.&&\n\
He must be too light to\n\
weigh it down...\n\
He he ha ha...&&\n",

    "intro_switches2":
"Man, I've been pondering...&&\n\
The colors on these switches\n\
define their properties...\n\
Brown switches are normal,\n\
Blue ones are heavy,\n\
Reds pop back up,\n\
Green means they're timed.\n",

    "intro_pushableblocks":
"Do you know about those\n\
pushable blocks?\n\
Dude.&&\n\
They were actually created\n\
by the goddess's ice.\n\
That's why they disappear\n\
when they touch anything\n\
they don't wanna touch.&&\n",

    "intro_roomclear":
"Looks like orange switches\n\
unlock when there's no more\n\
monsters around. Nice.&&\n",

    "intro_combat":
"Have you tried fighting\n\
while on the verge of death?\n\
You should try it sometime.\n\
Fortune favors the brave.\n",

"david":
"There seems to be some\n\
kind of note inside.\n\
\"W h e r e \' s  m y\n\
b i r t h d a y  g i f t ?\"\n\
.....................&&\n\
What?&&\n",


"menu_reminder":
"I'm sure you're quite\n\
versatile with those weapons,\n\
aren't you, baby?&&\n",

"thunder_1":
"Can ya feel the rhythm,\n\
lil guy? Check it!\n\
My name is big G,\n\
Ya can\'t move like me,\n\
can\'t sing like me,\n\
can\'t sting like me,\n\
can\'t swing like me,\n\
don\'t got bling like me...\n\
What? You said Geemers\n\
don\'t have names?\n\
Way to kill the vibe!&&\n",


"thunder_2":
"Soooooooooooo\n\
hungryyyyyyyyyyy...\n\
Foooooooooooood\n\
stolennnnnnnnnn\n\
byyyyyyyyyyyyy\n\
monstersssssssss.\n",

"thunder_fead":
"Yummmmmmmmmmmmm&&\n\
Thankssssssssssss\n\
myyyyyyy guyyyyyy!\n",


"thunder_sign":
"Ya know, game design is\n\
a lot harder than I thought,\n\
but what else would I do?\n\
Write a book?\n\
And who said anything\n\
about a fourth wall?\n",

"plant":
"You found another plant.\n\
Feed it to a hungry Geemer.\n",

"fire":
"Y/NFirion's fire burns\n\
furiously.\n",

"ice":
"Estelle's ice quenches\n\
your sorrows.\n",

"thunder":
"Kuwabara's thunder shocks\n\
your soul.\n",

"wind":
"The winds of Gladius flow\n\
eternally.\n",

"gale_sign":
"The creator of this game\n\
did not finish this room,\n\
but enjoy fighting a bunch\n\
of Davids instead.\n",

"chapel_geemer":
"Praise be to Majestus.&&",

"skipping_text":
"Dude... You can skip\n\
text by pressing SPACE.\n\
It's pretty useful in a\n\
variety of situations.\n\
Like the one you're\n\
in right now.\n\
You see, you think\n\
I'll stop talking\n\
if you listen to me\n\
for long enough,\n\
but I'll never stop\n\
talking, and you'll\n\
never be able to escape\n\
my undying wrath,\n\
as I impose my will\n\
upon your brittle soul,\n\
thrusting your hopes and\n\
dreams into endless oblivion,\n\
never able to return to\n\
your feeble endeavors,\n\
sinking hoplelessly into\n\
a flood of sorrow.\n",


"town_1":
"Welcome to Geemer town,\n\
young traveller.\n",

"shop":
"We've got it all!&&",

"shopkeep":
"If ya see anything you want,\n\
i'll sell it to ya.\n",

"flame_entrance_geemer":
"Ya don't see too many\n\
Geemers around these parts.\n\
Not anymore that is.&&\n\
Everyone used to grow their\n\
bud and farm together...\n\
But the lava knights\n\
keep ruining the land.\n\
What a shame...&&\n",

"flame_entrance_geemer2":
"Oh shit!&&\n\
You're a human!&&\n\
You guys don't eat your\n\
cheeba like we do, right?\n\
Humans have to smoke it!\n\
Ha ha ha ha ha!&&\n",

"flame_dispo":
"If you're lookin to buy,\n\
sorry man but I'm all out.\n\
Haven't been able to grow\n\
in so long, dude...\n\
But if you've got any\n\
green on you...\n\
I can roll you up something\n\
really nice, man!\n",

"flame_roll":
"Y/NLooks like you've got\n\
summa that good good!\n\
Want me to roll for ya?\n",

"bombo_expansion":
"You found some fertilizer\n\
for those pockets of yours!\n\
Maximum Bombofaun carrying\n\
capcity increased by 2!\n",

"boppers":
"Newly discovered invasive\n\
floral species: the Bopper.\n\
These dancing plants always\n\
regrow after being cut down.\n\
Additionally, they produce\n\
Bombofauns in great quantity.\n\
   [Scorching Fields\n\
     Restoration committee]\n",

"post_stomper":
"My brother's remains are\n\
splattered on the grass...\n\
Please help us slay\n\
the rest of those knights!\n",

"null":
"Nothing to see here."


}