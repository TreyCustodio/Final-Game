from . import vec

RESOLUTION = vec(304,208)
SCALE = 3
UPSCALED = RESOLUTION * SCALE
EPSILON = 0.01

#Universal flags for special conditions
FLAGS = [False for i in range(100)]

COORD = [[(i*16, j*16) for j in range(13)] for i in range(15)]

"""
The invenetory!
"""
INV = {
    "max_hp": 5,
    "plant": 0,
    "shoot": True,
    "fire": True,
    "clap": True,
    "cleats": True
    
}

"""
Item info for the pause screen
"""
INFO = {
"plant":
"A mysterious plant.\n\
Geemers seem to dig it."
}

"""
All icons from icon.png
"""
ICON = {
    "blank": (0,0),
    "plant":(1,0)
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

    "intro_geemer1": "I'm a Geemer, man.\n\
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
...................\n\
Know what I mean?",

    "intro_plantgeemer2":
"You're giving me this food?\n\
Oh, dude, you're the best!",


    "intro_plantgeemer3":
"Laaaaaaaaaterrrrr...",


    "intro_chest":
"You acquired a strange plant.\n\
Maybe someone wants it.",

    "intro_entrance":
"    No turning back now.",

    "intro_switches":
"Whattup my dude?\n\
If ya had a block to push,\n\
I bet you could keep that\n\
red switch pressed down, man.\n\
Yeah the one by my bro.\n\
He must be too light to\n\
weigh it down...\n\
He he ha ha...",

    "intro_switches2":
"Man, I've been pondering...\n\
The colors on these switches\n\
define their properties...\n\
Brown switches are normal,\n\
Blue ones are heavy,\n\
Reds pop back up,\n\
Green means they're timed.",

    "intro_pushableblocks":
"You know those blue blocks?\n\
The ones you can push?\n\
Dude.\n\
They're actually creatures\n\
made out of icy magic.\n\
They move away if they touch\n\
anything they don't want to.",

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
Try it out, but be careful!"


}