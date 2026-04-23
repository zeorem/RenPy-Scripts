# COMBAT.RPY ---------------------------------------------------------------------------------------

# System variables
default turns = []
default max_turns = 12
default allies = []
default enemies = []


init python:

    from copy import deepcopy

    class Skill(object):

        def __init__(self, id=None, name=None, kind=None, element=None, cost=None, 
        damage=10, hits=1, hit_rate=95, targets='enemies', sprites=None, effects=None):
            self.id = id 
            self.name = name 
            self.kind = kind
            self.element = element
            self.cost = cost
            self.hits = hits
            self.damage = damage
            self.hit_rate = hit_rate
            self.targets = targets
            self.sprites = sprites
            self.effects = effects or ['pass']

    class Battler(object):

        def __init__(self, id=None, race=None, name=None, hp=100, mp=10, stg=1, mgc=1, 
        vit=1, spd=1, lck=1, lv=1, xp=0, sprites=None, affinities=None, skills=None, 
        strategy=None):
            self.id = id
            self.race = race 
            self.name = name 
            self.mhp = hp 
            self.hp = self.mhp
            self.mmp = mp 
            self.mp = self.mmp
            self.stg = stg 
            self.mgc = mgc 
            self.vit = vit 
            self.spd = spd 
            self.lck = lck 
            self.lv = lv 
            self.xp = xp 
            self.turn_icon = 'enemy_turn_icon'
            self.sprites = sprites or {'idle':'placeholder_enemy'}
            self.animation = 'idle'
            self.affinities = affinities or []
            self.skills = skills or []
            self.strategy = strategy or []
            self.allegiance = 'enemies'
            self.target = None
        
        def anim(self, animation='idle'):
            return self.sprites[animation]
    
    class Turn(object):

        def __init__(self, battler=None, skill=None):
            self.battler = battler
            self.skill = skill

        def __repr__(self):
            return f"{self.battler.name}'s Turn" if self.battler != None else "Empty Turn"
    
    def initialize_battlers():
        global allies, enemies 

        for a in allies:
            a.allegiance = 'allies'
            a.turn_icon = 'ally_turn_icon'
        for e in enemies:
            e.allegiance = 'enemies'
            e.turn_icon = 'enemy_turn_icon'
        # for b in allies + enemies:
        #     b.spd = sorted([0, b.spd, max_turns])[1]

    def initialize_turns():
        global turns 

        turns = []

        battlers = sorted(allies + enemies, key=lambda x: x.spd, reverse=True)

        # Normal Turn list
        for b in battlers:
            turns.append(Turn(battler=b))
    
    def battle_process():

        initialize_battlers()
        
        initialize_turns()

# ASSETS.RPY
image placeholder_enemy:
    "sprites/battlers/placeholderEnemy01a.png"

image battle_bg:
    fit "scale-up"
    "backgrounds/battleback1.png"

# DECLARATIONS.RPY ---------------------------------------------------------------------------------------

# Skill declarations -------------------------------------------------------------------------------------

default skill_attack = Skill(id='s_1', name=_('Attack'), kind='phys', element='phys', 
cost=0, damage=10, hits=1, hit_rate=95, sprites='attack_sprite', effects=['damage hp'])

# Battler declarations -----------------------------------------------------------------------------------

default battler_dummy = Battler(id='b_0', race='Inactive', name='Dummy')
default battler_player = Battler(id='b_1', race=_('Human'), name='Prota', spd=5)

# Transform declarations

transform turn_counter_in():
    on show:
        align (.5, -.5)
        linear .5 yalign .01
    on hide:
        linear .5 yalign -.5


# Screen declarations -----------------------------------------------------------------------------------

screen turn_display():
    hbox:
        
        at turn_counter_in

        for turn in range(len(turns)):
            frame:
                id f"turn_frame_{turn}"
                background None
                # text f"{turn}"
                add f"gui/battle/{turns[turn].battler.turn_icon}.png"
                

