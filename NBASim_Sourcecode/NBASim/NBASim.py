import pygame
import math
import operator
import random
from enum import Enum
from pygame.locals import *
Radius = 30
width = 1280
height = 768
SCREENRECT = Rect(0, 0, width, height)

#
Display_text = "Press 's' to launch Stats Board. Press 'p' to progress the game."

# Speed
SPEED = 30
ball_speed = 45
# Court Side
LEFT = 'Left'
RIGHT = 'Right'

# Ratio Settings
GENERAL_SHOOTING_RATIO = 0.35
GENERAL_XFACTOR = 0.3
GENERAL_TRIPLE_RATIO = 0.25
GENERAL_LAYUP_DUNK_RATIO = 0.45
GENERAL_REBOUND_RATIO = 0.7
GENERAL_STEAL_RATIO = 0.3
GENERAL_BLOCK_RATIO = 0.4

Shooting_Base_PG = 0.1
Shooting_Base_SG = 0.12
Shooting_Base_SF = 0.1
Shooting_Base_PF = 0.09
Shooting_Base_C = 0.08

LD_BASE_PG = 0.15
LD_BASE_SG = 0.2
LD_BASE_SF = 0.25
LD_BASE_PF = 0.3
LD_BASE_C = 0.35

RB_BASE_PG = 0.22
RB_BASE_SG = 0.25
RB_BASE_SF = 0.3
RB_BASE_PF = 0.35
RB_BASE_C = 0.45

# match CASE
CASE_PASS = 100
CASE_JUMPSHOT = 1
CASE_LAYUP_DUNK = 2
CASE_TRIPLE = 3
CASE_STEAL = 4
CASE_BLOCK = 5

# Other
OFF_REBOUND = 0.8

# Court Position
LEFT_BASKET_POS = (82, int(SCREENRECT.height / 2))
RIGHT_BASKET_POS = (1199, int(SCREENRECT.height / 2))

LEFT_POS_5 = (150, 292)
LEFT_POS_4 = (150, 476)
LEFT_POS_3 = (308, 188)
LEFT_POS_2 = (308, 580)
LEFT_POS_1 = (388, 384)

LEFT_OFFPOS_1 = (448, 384)
LEFT_OFFPOS_2 = (348, 610)
LEFT_OFFPOS_3 = (348, 158)
LEFT_OFFPOS_4 = (190, 496)
LEFT_OFFPOS_5 = (190, 272)

RIGHT_POS_5 = (1130, 292)
RIGHT_POS_4 = (1130, 476)
RIGHT_POS_3 = (972, 188)
RIGHT_POS_2 = (972, 580)
RIGHT_POS_1 = (892, 384)

RIGHT_OFFPOS_5 = (1090, 272)
RIGHT_OFFPOS_4 = (1090, 496)
RIGHT_OFFPOS_3 = (932, 158)
RIGHT_OFFPOS_2 = (932, 610)
RIGHT_OFFPOS_1 = (842, 384)

Spots_for_Team_left_DEF = [LEFT_POS_1, LEFT_POS_2, LEFT_POS_3, LEFT_POS_4, LEFT_POS_5]
Spots_for_Team_left_OFF = [RIGHT_OFFPOS_1, RIGHT_OFFPOS_2, RIGHT_OFFPOS_3, RIGHT_OFFPOS_4, RIGHT_OFFPOS_5]

Spots_for_Team_right_DEF = [RIGHT_POS_1, RIGHT_POS_2, RIGHT_POS_3, RIGHT_POS_4, RIGHT_POS_5]
Spots_for_Team_right_OFF = [LEFT_OFFPOS_1, LEFT_OFFPOS_2, LEFT_OFFPOS_3, LEFT_OFFPOS_4, LEFT_OFFPOS_5]



# Color
black = Color('black')
red = Color('red')
blue = Color('blue')
yello = Color('Green Yellow')


def GetMovingDirection(current, target, speed):
    x = target[0] - current[0]
    y = target[1] - current[1]
    dist = math.hypot(x, y)
    if dist != 0:
        x, y = x/dist, y/dist
    else:
        x, y = 0, 0

    return (x * speed, y * speed)

# Enum class to store baller position
class Position(Enum):
    PointGuard = 1
    ShootingGuard = 2
    SmallForward = 3
    PowerForward = 4
    Center = 5

def load_image(file):

    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface


def load_sound(file):

    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return sound

def getRandom(min, max):
    return random.uniform(min, max)

def Calculator(rating, ratio):
    return (rating/100) * ratio



pygame.init()
screen = pygame.display.set_mode(SCREENRECT.size)
font = pygame.font.SysFont(None, 25)
name = pygame.font.SysFont(None, 20)
main_t = pygame.font.SysFont(None, 100)

ball = load_image("ball.png")
swish_sound = load_sound("Swish.wav")
rim_sound = load_sound("rim.wav")

def text_object(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, row):
    textSurf, textRect = text_object(msg, black, font)
    textRect.center = (SCREENRECT.width/2, SCREENRECT.height/15 * row)
    screen.blit(textSurf, textRect)

def print_player_name(msg, x, y):
    textSurf, textRect = text_object(msg, yello, name)
    textRect.center = (x, y)
    screen.blit(textSurf, textRect)

def print_main_text(msg, row):
    textSurf, textRect = text_object(msg, black, main_t)
    textRect.center = (SCREENRECT.width/2, SCREENRECT.height/7 * row)
    screen.blit(textSurf, textRect)


def stats_board(match):

    stats = True

    while stats:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stats = False
                if event.key == pygame.K_b:
                    stats = False
                if event.key == pygame.K_p:
                    match.matchGenerator()


        screen.fill(Color('white'))

        stat = match.build_stats()
        for i in range(len(stat)):
            message_to_screen(stat[i], i+1)


        pygame.display.update()
    runSim()

class Baller:

    pts = reb = ast = stl = blk = threeptShot = twoptShot = threeptHit = twoptHit = 0

    xFactor = possession = 0



    def __init__(self, name, position, jumpshot, triple, layup, reb_rating, stl_rating, blk_rating):
        self.name = name
        self.position = position
        self.jumpshot = jumpshot
        self.triple = triple
        self.layup = layup
        self.reb_rating = reb_rating
        self.stl_rating = stl_rating
        self.blk_rating = blk_rating
        self.court_pos = (0, 0)
        self.target = (0, 0)


    def draw_player(self, color, pos):
        pygame.draw.circle(screen, color, pos, Radius, 0)
        print_player_name(self.name, pos[0], pos[1])
        self.court_pos = pos

    def countPts(self):
        return self.twoptHit * 2 + self.threeptHit * 3

    def resetBaller(self):
        xFactor = possession = pts = reb = ast = stl = blk = threeptShot = twoptShot = threeptHit = twoptHit = 0

    def initXFactor(self):
        return getRandom(0, GENERAL_XFACTOR)

    def get_2_FGP(self):
        if self.twoptShot == 0:
            return 'N/A'

        else:
            return "{:.0%}".format(self.twoptHit/self.twoptShot)

    def get_3_FGP(self):
        if self.threeptShot == 0:
            return 'N/A'
        else:
            return "{:.0%}".format(self.threeptHit/self.threeptShot)


    def passball(self, target):
        self.possession = 0
        target.possesstion = 1
        log = self.name + ' pass to ' + target.name
        print(log)

    # Calculate the shooting percentage for each shot
    def shootingCalc(self):
        ratio = 0
        if self.position.value == 1:
            ratio = Shooting_Base_PG
        elif self.position.value == 2:
            ratio = Shooting_Base_SG
        elif self.position.value == 3:
            ratio = Shooting_Base_SF
        elif self.position.value == 4:
            ratio = Shooting_Base_PF
        elif self.position.value == 5:
            ratio = Shooting_Base_C
        return ratio + self.initXFactor() + Calculator(self.jumpshot, GENERAL_SHOOTING_RATIO)

    # Calculate the 3pt shooting percentage for each shot
    def tripleCalc(self):
        ratio = 0
        if self.position.value == 1:
            ratio = Shooting_Base_PG
        elif self.position.value == 2:
            ratio = Shooting_Base_SG
        elif self.position.value == 3:
            ratio = Shooting_Base_SF
        elif self.position.value == 4:
            ratio = Shooting_Base_PF
        elif self.position.value == 5:
            ratio = Shooting_Base_C
        return ratio + self.initXFactor() + Calculator(self.triple, GENERAL_TRIPLE_RATIO)

    # Calculate the 3pt shooting percentage for each shot
    def LDCalc(self):
        ratio = 0
        if self.position.value == 1:
            ratio = LD_BASE_PG
        elif self.position.value == 2:
            ratio = LD_BASE_SG
        elif self.position.value == 3:
            ratio = LD_BASE_SF
        elif self.position.value == 4:
            ratio = LD_BASE_PF
        elif self.position.value == 5:
            ratio = LD_BASE_C
        return ratio + self.initXFactor() + Calculator(self.layup, GENERAL_LAYUP_DUNK_RATIO)

    # Calculate the ratio related to Rebounding
    def RebCalc(self):
        ratio = 0
        if self.position.value == 1:
            ratio = RB_BASE_PG
        elif self.position.value == 2:
            ratio = RB_BASE_SG
        elif self.position.value == 3:
            ratio = RB_BASE_SF
        elif self.position.value == 4:
            ratio = RB_BASE_PF
        elif self.position.value == 5:
            ratio = RB_BASE_C
        return ratio + self.initXFactor() + Calculator(self.reb_rating, GENERAL_REBOUND_RATIO)

    # Calculate the ratio related to steal
    def StlCalc(self):

        return self.initXFactor() + Calculator(self.stl_rating, GENERAL_STEAL_RATIO)

    def BlkCalc(self):
        return self.initXFactor() + Calculator(self.blk_rating, GENERAL_BLOCK_RATIO)

    def jumpShot(self):
        self.possession = 0
        return self.shootingCalc()

    def tripleShot(self):
        self.possession = 0
        return self.tripleCalc()

    def layupNDunk(self):
        self.possession = 0
        return self.LDCalc()

    def rebound(self):
        return self.RebCalc()

    def steal(self):
        return self.StlCalc()

    def block(self):
        return self.BlkCalc()

    def made2Shot(self):
        self.pts += 2
        self.twoptShot += 1
        self.twoptHit += 1

    def made3Shot(self):
        self.pts += 3
        self.threeptHit += 1
        self.threeptShot += 1
    def miss2Shot(self):
        self.twoptShot += 1

    def miss3Shot(self):
        self.threeptShot += 1

    def madeReb(self):
        self.possession = 1
        self.reb += 1

    def madeAst(self):
        self.ast += 1

    def madeStl(self):
        self.possession = 1
        self.stl += 1

    def madeBlk(self):
        self.possession = 1
        self.blk += 1


class Team:
    players = []
    totalPts = totalReb = totalAst = totalStl = totalBlk = 0
    prevPoss = 0
    gameStart = False
    shotMaker = 0
    # The player who gets the highest rebound ratio currently
    rebound_winner = 0
    # off_pos = [(0, 0)] * 5
    # def_pos = [(0, 0)] * 5
    current_pos = [(0, 0)] * 5
    target_pos = [(0, 0)] * 5
    side = ''

    # Having trouble with list and dictionary values
    # Hardcoding position value:
    def_pos1 = (0, 0)
    def_pos2 = (0, 0)
    def_pos3 = (0, 0)
    def_pos4 = (0, 0)
    def_pos5 = (0, 0)

    off_pos1 = (0, 0)
    off_pos2 = (0, 0)
    off_pos3 = (0, 0)
    off_pos4 = (0, 0)
    off_pos5 = (0, 0)

    def __init__(self, name, color, side):
        self.name = name
        self.color = color
        self.side = side


    def set_side(self):

        if self.side == LEFT:

            # self.off_pos = Spots_for_Team_left_OFF
            # self.def_pos = Spots_for_Team_left_DEF
            self.def_pos1 = LEFT_POS_1
            self.def_pos2 = LEFT_POS_2
            self.def_pos3 = LEFT_POS_3
            self.def_pos4 = LEFT_POS_4
            self.def_pos5 = LEFT_POS_5

            self.off_pos1 = RIGHT_OFFPOS_1
            self.off_pos2 = RIGHT_OFFPOS_2
            self.off_pos3 = RIGHT_OFFPOS_3
            self.off_pos4 = RIGHT_OFFPOS_4
            self.off_pos5 = RIGHT_OFFPOS_5

        elif self.side == RIGHT:

            # self.off_pos = Spots_for_Team_right_OFF
            # self.def_pos = Spots_for_Team_right_DEF
            self.def_pos1 = RIGHT_POS_1
            self.def_pos2 = RIGHT_POS_2
            self.def_pos3 = RIGHT_POS_3
            self.def_pos4 = RIGHT_POS_4
            self.def_pos5 = RIGHT_POS_5

            self.off_pos1 = LEFT_OFFPOS_1
            self.off_pos2 = LEFT_OFFPOS_2
            self.off_pos3 = LEFT_OFFPOS_3
            self.off_pos4 = LEFT_OFFPOS_4
            self.off_pos5 = LEFT_OFFPOS_5

        self.current_pos = [self.def_pos1, self.def_pos2, self.def_pos3, self.def_pos4, self.def_pos5]


        # for i in range(len(self.def_pos)):
        #     self.current_pos.append(self.def_pos[i])
        #     print(self.current_pos[i])


    def setRoster(self, playerList):
        self.players = playerList


    def countTotalPts(self):
        if len(self.players) > 0:
            for player in self.players:
                self.totalPts += player.pts

    def countTotalRebs(self):
        if len(self.players) > 0:
            for player in self.players:
                self.totalReb += player.reb

    def countTotalAst(self):
        if len(self.players) > 0:
            for player in self.players:
                self.totalAst += player.ast

    def countTotalStl(self):
        if len(self.players) > 0:
            for player in self.players:
                self.totalStl += player.stl

    def countTotalBlk(self):
        if len(self.players) > 0:
            for player in self.players:
                self.totalBlk += player.blk

    def resetTeam(self):
        totalPts = totalReb = totalAst = totalStl = totalBlk = 0
        prevPoss = 0

    def draw_players(self):
        if len(self.players) == len(self.current_pos):

            for i in range(len(self.players)):
                self.players[i].draw_player(self.color, self.current_pos[i])

    def draw_ball(self, ball_pos):

        screen.blit(ball, ball_pos)


    def update_current_pos(self):
        # delta_d = GetMovingDirection(RIGHT_POS_5, LEFT_BASKET_POS, 10)
        # RIGHT_POS_5 = (int(RIGHT_POS_5[0] + delta_d[0]), int(RIGHT_POS_5[1] + delta_d[1]))

        if len(self.players) == len(self.current_pos):

            if self.checkPossession() == 0: # Deffense Pos
                self.target_pos = [self.def_pos1, self.def_pos2, self.def_pos3, self.def_pos4, self.def_pos5]

            elif self.checkPossession() is not 0: # Offense Pos

                self.target_pos = [self.off_pos1, self.off_pos2, self.off_pos3, self.off_pos4, self.off_pos5]

            for i in range(len(self.players)):
                if math.hypot(self.target_pos[i][0] - self.current_pos[i][0], self.target_pos[i][1] - self.current_pos[i][1]) <= 40:
                    self.current_pos[i] = self.target_pos[i]
                else:
                    delta_d = GetMovingDirection(self.current_pos[i], self.target_pos[i], SPEED)
                    self.current_pos[i] = (int(self.current_pos[i][0] + delta_d[0]), int(self.current_pos[i][1] + delta_d[1]))

        self.draw_players()

    # Find the corresponding player by the given position
    def findPlayer(self, pos):
        target = ''
        for player in self.players:
            if player.position == pos:
                target = player
        return target

    def setPossesion(self, pos):
        for player in self.players:
            if player.position == pos:
                player.possession = 1
                print(player.name + ' gains possession!')

    # Check whether this team has possession
    # Return the player who has the possession right now
    def checkPossession(self):
        result = 0
        for player in self.players:
            if player.possession == 1:
                result = player.position

        return result

    def lostPossession(self):
        for player in self.players:
            player.possession = 0
        self.prevPoss = 0

    # Handle passing case
    def passing(self, target):
        current = self.checkPossession()
        if current != target:
            self.prevPoss = current
            for player in self.players:
                if player.position == target:
                    self.findPlayer(current).passball(player)
                    self.findPlayer(target).possession = 1
                    return CASE_PASS
        else:
            return CASE_PASS * -1



    # Handle jumpshot case
    def jumpShot(self):

        current = self.findPlayer(self.checkPossession())
        ratio = current.jumpShot()
        checker = getRandom(0, 1)
        self.shotMaker = current

        if ratio <= checker:
            current.made2Shot()
            self.totalPts += 2
            return CASE_JUMPSHOT
        else:
            current.miss2Shot()
            return CASE_JUMPSHOT * -1

    # Handle 3pt shot case
    def tripleShot(self):

        current = self.findPlayer(self.checkPossession())
        ratio = current.tripleShot()
        checker = getRandom(0, 1)
        self.shotMaker = current

        if ratio <= checker:
            current.made3Shot()
            self.totalPts += 3
            return CASE_TRIPLE
        else:
            current.miss3Shot()
            return CASE_TRIPLE * -1

    # Handle layup/dunk case
    def layupNDunk(self):
        current = self.findPlayer(self.checkPossession())
        ratio = current.layupNDunk()
        checker = getRandom(0, 1)
        self.shotMaker = current

        if ratio <= checker:
            current.made2Shot()
            self.totalPts += 2
            return CASE_LAYUP_DUNK
        else:
            current.miss2Shot()
            return CASE_LAYUP_DUNK * -1
    # Handle stealing case
    def steal(self):

        steal_attempts = []
        for player in self.players:
            steal_attempts.append(player.steal())

        index, value = max(enumerate(steal_attempts), key=operator.itemgetter(1))

        for player in self.players:
            if player.position.value == index + 1:
                player.madeStl()
        return CASE_STEAL

    # Handle Blocking case
    def block(self):

        block_attempts = []
        for player in self.players:
            block_attempts.append(player.block())

        index, value = max(enumerate(block_attempts), key=operator.itemgetter(1))

        for player in self.players:
            if player.position.value == index + 1:
                player.madeBlk()

        return CASE_BLOCK

    # Handle Rebound case
    def rebound(self):
        rebound_attempts = []
        for player in self.players:
            temp = player.rebound()
            rebound_attempts.append(temp)
            # print("rebound ratio: " + str(temp))
        index, value = max(enumerate(rebound_attempts), key=operator.itemgetter(1))

        # print("index is: " + str(index))
        for player in self.players:
            if player.position.value == index + 1:
                self.rebound_winner = player
                # print("winner is: " + player.name)
        # print("Winner ratio is: " + str(value))
        return value


    # Update team behavior
    def update_behavior(self):

        behavior_checker = getRandom(0, 10)

        print("behavior checker for Team" + self.name + " is: " + str(behavior_checker))
        result = 0
        if self.gameStart:
            if self.checkPossession() != 0:
                # Pass behavior
                if behavior_checker <= 5:
                    target = self.players[random.randint(0, len(self.players) - 1)].position
                    result = self.passing(target)
                elif behavior_checker > 5:
                    current = self.checkPossession()
                    if current == Position.PointGuard:
                        case_random = getRandom(0, 10)
                        if case_random <= 5:
                            result = self.jumpShot()
                        elif case_random > 5 and case_random <= 8:
                            result = self.layupNDunk()
                        elif case_random > 8:
                            result = self.tripleShot()
                    elif current == Position.ShootingGuard:
                        case_random = getRandom(0, 10)
                        if case_random <= 4:
                            result = self.jumpShot()
                        elif case_random > 4 and case_random <= 7:
                            result = self.layupNDunk()
                        elif case_random > 7:
                            result = self.tripleShot()
                    elif current == Position.SmallForward:
                        case_random = getRandom(0, 10)
                        if case_random <= 4:
                            result = self.jumpShot()
                        elif case_random > 4 and case_random <= 8:
                            result = self.layupNDunk()
                        elif case_random > 8:
                            result = self.tripleShot()
                    elif current == Position.PowerForward:
                        case_random = getRandom(0, 10)
                        if case_random <= 4:
                            result = self.jumpShot()
                        elif case_random > 4 and case_random <= 8.5:
                            result = self.layupNDunk()
                        elif case_random > 8.5:
                            result = self.tripleShot()
                    elif current == Position.Center:
                        case_random = getRandom(0, 10)
                        if case_random <= 3:
                            result = self.jumpShot()
                        elif case_random > 3 and case_random <= 8.5:
                            result = self.layupNDunk()
                        elif case_random > 8.5:
                            result = self.tripleShot()
                    else:
                        print("Team " + self.name + " has no update in this turn.")

            elif self.checkPossession() == 0:
                if behavior_checker <= 1:
                    result = self.steal()
                elif behavior_checker > 1 and behavior_checker <= 2:
                    result = self.block()
                else:
                    print("Team " + self.name +  " has no update in this turn.")
        return result


class Match:

    t1score = t2score = possession = 0
    statement = []
    ball_pos = (0, 0)


    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.shot_made = False
        self.shot_miss = False

    def jumpball(self):

        print(self.team1.current_pos)
        print(self.team2.current_pos)

        self.team1.set_side()
        self.team2.set_side()
        self.ball_pos = (SCREENRECT.width/2, SCREENRECT.height/2)
        print(self.team1.current_pos)
        print(self.team2.current_pos)



        self.team1.gameStart = True
        self.team2.gameStart = True

        jump = random.randint(1, 2)
        if jump == 1:
            self.possession = 1
            print("Jump Ball! " + self.team1.name + " Wins!")
            self.team1.setPossesion(Position.PointGuard)

        else:
            self.possession = 2
            print("Jump Ball! " + self.team2.name + " Wins!")
            self.team2.setPossesion(Position.PointGuard)


    def reboundBattle(self, t1, t2):
        if t1 > t2:
            self.team1.rebound_winner.madeReb()
            self.team2.prevPoss = 0
            self.possession = 1
            print(self.team1.rebound_winner.name + ' Rebound. (' + str(self.team1.rebound_winner.reb) + ' rebounds)')
        elif t1 < t2:
            self.team2.rebound_winner.madeReb()
            self.team1.prevPoss = 0
            self.possession = 2
            print(self.team2.rebound_winner.name + ' Rebound. (' + str(self.team2.rebound_winner.reb) + ' rebounds)')
        elif t1 == t2:
            recast = random.randint(1, 2)
            if recast == 1:
                self.team1.rebound_winner.madeReb()
                self.team2.prevPoss = 0
                self.possession = 1
                print(self.team1.rebound_winner.name + ' Rebound. (' + str(self.team1.rebound_winner.reb) + ' rebounds)')
            else:
                self.team2.rebound_winner.madeReb()
                self.team1.prevPoss = 0
                self.possession = 2
                print(self.team2.rebound_winner.name + ' Rebound. (' + str(self.team2.rebound_winner.reb) + ' rebounds)')

    def draw_ball(self):

        if self.possession == 1:
            # self.team1.draw_ball(self.ball_pos)
            current_possession = self.team1.findPlayer(self.team1.checkPossession())

        else:
            self.team2.draw_ball(self.ball_pos)

    def update_ball(self):

        if not(self.shot_made or self.shot_miss):
            if self.possession == 1 :
                current_possession = self.team1.findPlayer(self.team1.checkPossession())
            elif self.possession == 2:
                current_possession = self.team2.findPlayer(self.team2.checkPossession())


            target_ball_pos = current_possession.court_pos


        else:
            if self.possession == 1:
                target_ball_pos = (LEFT_BASKET_POS[0] - 20, LEFT_BASKET_POS[1] - 20)

            else:
                target_ball_pos = (RIGHT_BASKET_POS[0] - 20, RIGHT_BASKET_POS[1] - 20)

            if self.shot_made:
                case = 1
            elif self.shot_miss:
                case = 0

        delta_d = GetMovingDirection(self.ball_pos, target_ball_pos, ball_speed)


        if math.hypot(self.ball_pos[0] - target_ball_pos[0],
                      self.ball_pos[1] - target_ball_pos[1]) <= 30:
            self.ball_pos = target_ball_pos

        else:
            self.ball_pos = (int(self.ball_pos[0] + delta_d[0]), int(self.ball_pos[1] + delta_d[1]))

        if self.ball_pos == (LEFT_BASKET_POS[0] - 20, LEFT_BASKET_POS[1] - 20) or self.ball_pos == (RIGHT_BASKET_POS[0] - 20, RIGHT_BASKET_POS[1] - 20):
            self.shot_made = False
            self.shot_miss = False
            self.play_basket_sound(case)

        screen.blit(ball, self.ball_pos)

    def print_main_Text(self):
        print_main_text(str(self.team1.totalPts) + ' : ' + str(self.team2.totalPts), 1)
        message_to_screen(Display_text, 13)


    def play_basket_sound(self, case):
        if case == 1:
            swish_sound.play()
        else:
            rim_sound.play()

    def matchGenerator(self):

        t1 = self.team1.update_behavior()
        t2 = self.team2.update_behavior()

        if t1 == CASE_STEAL:

            self.team2.lostPossession()
            self.possession = 1
            print('Ball Stolen by ' + self.team1.findPlayer(self.team1.checkPossession()).name + '. ')
        elif t1 == CASE_BLOCK:
            self.team2.lostPossession()
            self.possession = 1
            print('Shot Blocked by ' + self.team1.findPlayer(self.team1.checkPossession()).name + '. ')
        elif t2 == CASE_STEAL:
            self.team1.lostPossession()
            self.possession = 2
            print('Ball Stolen by ' + self.team2.findPlayer(self.team2.checkPossession()).name + '. ')
        elif t2 == CASE_BLOCK:
            self.team1.lostPossession()
            self.possession = 2
            print('Shot Blocked by ' + self.team2.findPlayer(self.team2.checkPossession()).name + '. ')

        elif t1 == 1 or t1 == 2 or t1 == 3: # Shot made
            self.team2.setPossesion(Position.PointGuard)
            if self.team1.prevPoss != 0:
                self.team1.findPlayer(self.team1.prevPoss).madeAst()
            self.team1.prevPoss = 0
            self.possession = 2
            if t1 == 1:
                text = self.team1.shotMaker.name + ' Jump Shot Made. (' + str(self.team1.shotMaker.pts) + ' pts)'
                print(text)
                Display_text = text

            elif t1 ==2:
                print(self.team1.shotMaker.name + ' Layup/Dunk Made. (' + str(self.team1.shotMaker.pts) + ' pts)')
            elif t1 == 3:
                print(self.team1.shotMaker.name + ' 3pt Shot Made. (' + str(self.team1.shotMaker.pts) + ' pts)')
            self.shot_made = True

        elif t2 == 1 or t2 == 2 or t2 ==3:
            self.team1.setPossesion(Position.PointGuard)
            if self.team2.prevPoss != 0:
                self.team2.findPlayer(self.team2.prevPoss).madeAst()
            self.team2.prevPoss = 0
            self.possession = 1
            if t2 == 1:
                print(self.team2.shotMaker.name + ' Jump Shot Made. (' + str(self.team2.shotMaker.pts) + ' pts)')
            elif t2 == 2:
                print(self.team2.shotMaker.name + ' Layup/Dunk Made. (' + str(self.team2.shotMaker.pts) + ' pts)')
            elif t2 == 3:
                print(self.team2.shotMaker.name + ' 3pt Shot Made. (' + str(self.team2.shotMaker.pts) + ' pts)')
            self.shot_made = True

        elif t1 == -1 or t1 == -2 or t1 == -3:
            if t1 == -1:
                print(self.team1.shotMaker.name + ' Jump Shot Miss. (' + str(self.team1.shotMaker.pts) + ' pts)')
            elif t1 ==-2:
                print(self.team1.shotMaker.name + ' Layup/Dunk Miss. (' + str(self.team1.shotMaker.pts) + ' pts)')
            elif t1 == -3:
                print(self.team1.shotMaker.name + ' 3pt Shot Miss. (' + str(self.team1.shotMaker.pts) + ' pts)')
            self.reboundBattle(self.team1.rebound() * OFF_REBOUND, self.team2.rebound())
            self.shot_miss = True

        elif t2 == -1 or t2 == -2 or t2 == -3:
            self.reboundBattle(self.team1.rebound(), self.team2.rebound() * OFF_REBOUND)
            if t2 == -1:
                print(self.team2.shotMaker.name + ' Jump Shot Miss. (' + str(self.team2.shotMaker.pts) + ' pts)')
            elif t2 == -2:
                print(self.team2.shotMaker.name + ' Layup/Dunk Miss. (' + str(self.team2.shotMaker.pts) + ' pts)')
            elif t2 == -3:
                print(self.team2.shotMaker.name + ' 3pt Shot Miss. (' + str(self.team2.shotMaker.pts) + ' pts)')
            self.shot_miss = True
        elif t1 == 100 or t1 == 100:
            pass
        elif t2 == 100 or t2 == -100:
            pass

        print ('------------------------- Match Team ' + self.team1.name + ' vs Team ' + self.team2.name + ': ' + str(self.team1.totalPts) + ' : ' + str(self.team2.totalPts) + ' ------------------------------')


    def build_stats(self):
        t1pg = self.team1.findPlayer(Position.PointGuard)
        t1sg = self.team1.findPlayer(Position.ShootingGuard)
        t1sf = self.team1.findPlayer(Position.SmallForward)
        t1pf = self.team1.findPlayer(Position.PowerForward)
        t1c = self.team1.findPlayer(Position.Center)

        t2pg = self.team2.findPlayer(Position.PointGuard)
        t2sg = self.team2.findPlayer(Position.ShootingGuard)
        t2sf = self.team2.findPlayer(Position.SmallForward)
        t2pf = self.team2.findPlayer(Position.PowerForward)
        t2c = self.team2.findPlayer(Position.Center)

        stats =[]
        row1 = 'Stats Board: Team ' + self.team1.name + ' VS Tean' + self.team2.name
        row2 = '    Player   |  PTS  |  AST  |  REB  |  STL  |  BLK  |  3pt FGP  |  2pt FGP  |'
        row3 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t1pg.name, t1pg.pts, t1pg.ast, t1pg.reb, t1pg.stl, t1pg.blk, t1pg.get_3_FGP() + ' '+ str(t1pg.threeptHit) + '/' + str(t1pg.threeptShot), t1pg.get_2_FGP() + ' '+ str(t1pg.twoptHit) + '/' + str(t1pg.twoptShot))
        row4 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t1sg.name, t1sg.pts, t1sg.ast, t1sg.reb, t1sg.stl, t1sg.blk, t1sg.get_3_FGP() + ' '+ str(t1sg.threeptHit) + '/' + str(t1sg.threeptShot), t1sg.get_2_FGP() + ' '+ str(t1sg.twoptHit) + '/' + str(t1sg.twoptShot))
        row5 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t1sf.name, t1sf.pts, t1sf.ast, t1sf.reb, t1sf.stl, t1sf.blk, t1sf.get_3_FGP() + ' '+ str(t1sf.threeptHit) + '/' + str(t1sf.threeptShot), t1sf.get_2_FGP() + ' '+ str(t1sf.twoptHit) + '/' + str(t1sf.twoptShot))
        row6 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t1pf.name, t1pf.pts, t1pf.ast, t1pf.reb, t1pf.stl, t1pf.blk, t1pf.get_3_FGP() + ' '+ str(t1pf.threeptHit) + '/' + str(t1pf.threeptShot), t1pf.get_2_FGP() + ' '+ str(t1pf.twoptHit) + '/' + str(t1pf.twoptShot))
        row7 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t1c.name, t1c.pts, t1c.ast, t1c.reb, t1c.stl, t1c.blk, t1c.get_3_FGP() + ' ' + str(t1c.threeptHit) + '/' + str(t1c.threeptShot), t1c.get_2_FGP() + ' '+ str(t1c.twoptHit) + '/' + str(t1c.twoptShot))
        row8 = ''

        row9 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t2pg.name, t2pg.pts, t2pg.ast, t2pg.reb, t2pg.stl, t2pg.blk, t2pg.get_3_FGP() + ' ' + str(t2pg.threeptHit) + '/' + str(t2pg.threeptShot), t2pg.get_2_FGP() + ' '+ str(t2pg.twoptHit) + '/' + str(t2pg.twoptShot))
        row10 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t2sg.name, t2sg.pts, t2sg.ast, t2sg.reb, t2sg.stl, t2sg.blk, t2sg.get_3_FGP() + ' ' + str(t2sg.threeptHit) + '/' + str(t2sg.threeptShot), t2sg.get_2_FGP() + ' '+ str(t2sg.twoptHit) + '/' + str(t2sg.twoptShot))
        row11 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t2sf.name, t2sf.pts, t2sf.ast, t2sf.reb, t2sf.stl, t2sf.blk, t2sf.get_3_FGP() + ' ' + str(t2sf.threeptHit) + '/' + str(t2sf.threeptShot), t2sf.get_2_FGP() + ' '+ str(t2sf.twoptHit) + '/' + str(t2sf.twoptShot))
        row12 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t2pf.name, t2pf.pts, t2pf.ast, t2pf.reb, t2pf.stl, t2pf.blk, t2pf.get_3_FGP() + ' ' + str(t2pf.threeptHit) + '/' + str(t2pf.threeptShot), t2pf.get_2_FGP() + ' '+ str(t2pf.twoptHit) + '/' + str(t2pf.twoptShot))
        row13 = '%s |   %d   |   %d   |   %d   |   %d   |   %d   | %s | %s |' % (
            t2c.name, t2c.pts, t2c.ast, t2c.reb, t2c.stl, t2c.blk, t2c.get_3_FGP() + ' ' + str(t2c.threeptHit) + '/' + str(t2c.threeptShot), t2c.get_2_FGP() + ' '+ str(t2c.twoptHit) + '/' + str(t2c.twoptShot))

        row14 = "Press 'b' to back to court. Press 'p' to progress the game."
        stats = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12, row13, row14]
        return stats

    def draw_match(self):
        self.team1.update_current_pos()
        self.team2.update_current_pos()

# name, position, jumpshot, triple, layup, reb_rating, stl_rating, blk_rating
SCurry = Baller('Stephen Curry', Position.PointGuard, 90, 98, 90, 50, 80, 40)
JHarden = Baller('James Harden', Position.ShootingGuard, 85, 85, 88, 60, 75, 55)
KDurant = Baller('Kevin Durant', Position.SmallForward, 95, 95, 90, 80, 65, 67)
TDuncan = Baller('Tim Duncan', Position.PowerForward, 85, 50, 98, 90, 70, 85)
DHoward = Baller('Dwight Howard', Position.Center, 50, 35, 96, 95, 70, 90)

CPaul = Baller('Chris Paul', Position.PointGuard, 85, 80, 80, 50, 90, 45)
KBryant = Baller('Kobe Bryant', Position.ShootingGuard, 88, 82, 93, 65, 70, 60)
LBJ = Baller('LeBron James', Position.SmallForward, 75, 65, 90, 78, 75, 82)
ADavis = Baller("Anthony Davis", Position.PowerForward, 78, 65, 95, 90, 70, 95)
YMing = Baller("Ming Yao", Position.Center, 85, 40, 100, 85, 60, 80)

god = Team("Fire", red, LEFT)
dog = Team("Ice", blue, RIGHT)
god.setRoster([SCurry, JHarden, KDurant, TDuncan, DHoward])
dog.setRoster([CPaul, KBryant, LBJ, ADavis, YMing])

match = Match(god, dog)
match.jumpball()


def runSim():

    # Loading Background
    bgd = load_image('court.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgd.get_width()):
        background.blit(bgd, (x, 0))





    # Frame settings
    clock = pygame.time.Clock()
    court = True
    while court:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    court = False
                if event.key == pygame.K_p:
                    match.matchGenerator()
                if event.key == pygame.K_s:
                    stats_board(match)
        screen.blit(background, (0, 0))
        pygame.display.flip()

        match.draw_match()
        match.update_ball()
        match.print_main_Text()
        pygame.display.update()


        clock.tick(10)

    pygame.quit()


runSim()



