from . import vec

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
#88 -> Blessings are locked, way is clear
#89 -> No blessings appear
#90 -> Ice chosen
#91 -> Fire chosen
#92 -> Thunder chosen
#93 -> Wind chosen


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

    "C": None,
    "Arrow": 0
    #0 -> regular, 1 -> fire, 2 -> ice, 3- -> thunder, 4-> wind, 5-> super, 6-> hyper

}



"""
The Player's inventory
"""
INV = {
    "max_hp": 5,
    "plant": 0,
    "shoot": True,
    "fire": True,
    "clap": True,
    "slash": True,
    "cleats": True 
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


0:"          Majestus.&&\n\
The ruins of an ancient\n\
tribe of religious mages:\n\
      The Naturalites.&&\n",
      
1:"In paradise, the Naturalites\n\
prayed to their Gods,\n\
the four elemental deities:&&\n",

2:"Firion, of the Flame,&&\n\
Estelle, of the Frost,&&\n\
Kuwabara, of the Bolt,&&\n\
Gladius, of the Gale.&&\n",

3:"The deities granted their\n\
worshippers with power,\n\
and the Naturalites lived\n\
prosperous lives for eons.\n\
Until one day...&&\n",

4:"Vash, the Naturalite King,\n\
waged war on the world.\n\
Using their Gods' blessings\n\
for selfish conquest,\n\
the undefeatable mages\n\
tore apart the outside world,\n\
scorching fields,\n\
freezing oceans,\n\
shocking hearts,\n\
slicing heads.\n",

5: "At the war's climax, the\n\
King, with great audacity,\n\
asked his Gods to grant\n\
him more of their power.\n\
So, the Gods punished his\n\
unquenchable thirst.\n\
They sealed the King and\n\
his people within Majestus,\n\
never to be seen again.&&\n\
As for the Gods...&&\n",

6:"They relinquished their role\n\
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
Beemers seem to love it.",

"shoot":
"Old reliable.\n\
Press X to shoot.",

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
Equip with C."
}




"""
Icons from icon.png to be used in text display
"""
ICON = {
    "blank": (0,0),
    "plant":(1,0),
    "geemer":(2,0)
}






"""
All of the text for npcs!
Follows format:

roomName_class#
"""
SPEECH = {
    
    "key":
"   Picked up a key.",
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
in here now, dude.",

    "intro_geemer1": "I'm a Beemer, man.\n\
I know all kindsa stuff.\n\
My bros are around too.",

    "intro_geemer2": "My name? Oh, dude...\n\
Geemers don't have names,\n\
man...",

    "intro_geemer3": "Dude I'm so hungry!\n\
Ya got anything to eat,\n\
mannnnnnnnnn????????????",

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
"You acquired a strange plant.\n\
Maybe someone wants it.",

    "intro_entrance":
"   A divine force prevents\n\
    you from leaving.\n",

    "intro_switches":
"Whattup my dude?&&\n\
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
"You know those blue blocks?\n\
The ones you can push?\n\
Dude.&&\n\
They're actually creatures\n\
made out of Estelle's ice.\n\
They move away if they touch\n\
anything they don't want to.\n",

    "intro_roomclear":
"Looks like orange switches\n\
unlock when there's no more\n\
monsters around. Nice.",

    "intro_combat":
"If you're full of vigor,\n\
your arrows will fly faster.\n\
If you're close to death,\n\
your instincts will kick in.\n\
You'll deal much more damage.\n\
Try it out, but be careful!",

"fire":
"You have chosen\n\
the blessing of fire.\n\
Damage enemies with\n\
a fiery spell!\n\
Select your new C attack\n\
on the pause menu.",

"ice":
"You have chosen\n\
the blessing of ice.\n\
Hold Z to sprint and\n\
tackle enemies.",

"thunder":
"You have chosen\n\
the blessing of thunder.\n\
Deal massive damage to\n\
surrounding enemies!\n\
Select your new C attack\n\
on the pause menu.",

"wind":
"You have chosen\n\
the blessing of wind.\n\
Charge up and fire\n\
a powerful ranged attack!\n\
Select your new C attack\n\
on the pause menu.",





"null":
"Nothing to see here."


}