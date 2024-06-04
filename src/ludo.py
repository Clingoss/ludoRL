import pygame
import random
import time
from src.board import Board
from src.color import Color
from src.player import Player
from src.RNDbot import RNDbot
from src.RL import RL
import numpy as np

class Ludo:

    number_of_players = 4
    is_playing = True
    players = []
    current_player_id = 0
    current_action = 0
    stars = [6,12,19,25,32,38,45,51]
    pity = 1

    def __init__(self,red,blue,yellow,green):
        pygame.init()

        self.winner = 0

        self.players = [Player(Color.COLORS[x]) for x in range(0, self.number_of_players)]
        self.board = Board(self.players)
        self.RED = red
        self.BLUE = blue
        self.YELLOW = yellow
        self.GREEN = green

        self.play()

    def play(self):
        while self.in_game():

            self.board.current_player(self.current_player())
            self.board.update()

            # for event in pygame.event.get():
            #     if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
            #         self.next_action()
            #     elif event.type == pygame.QUIT:
            #         self.is_playing = False
            
            #time.sleep(1)

            if self.next_action():
                break

    def next_action(self):
        if self.current_action == 0:
            self.roll()
            return 0
        elif self.current_action == 1:
            return 1
        else:
            self.next_player()
            return 0
        
    def rndAction(self, dice,playercount,playerName):
        actions = []
        if dice==6:
            actions.append(playerName.action(1))
        else:
            actions.append(0)
        if playercount > 0:
            actions.append(playerName.action(playercount))
        else : 
            actions.append(playercount)
        return actions
    
    def rlAction(self, dice, playercount, rlType, playerName, offset):
        actions = []
        if playercount < 0:
            actions.append(0)
            actions.append(0)
        elif playercount==0 and dice!=6:
            actions.append(0)
            actions.append(0)
        else :
            playerPos = np.zeros(4,dtype=np.int8)
            enemyPos = np.zeros(58)
            for active in range(playercount+1):
                playerPos[active]=self.current_player().active_piece(active).position
            for player in self.players:
                if player != self.current_player():
                    for pieces in range(player.pieces_out()):
                        pos = self.board.get_cell(player.color, player.active_piece(pieces).position)
                        try:
                            enemyPos[int(pos)]+=1
                        except:
                            1
            
            if rlType == 'Q':
                player = playerName.runQ(playerPos,offset,enemyPos,dice)
            elif rlType == 'sQ':
                player = playerName.runSpecial(playerPos,offset,enemyPos,dice)
            else:
                player = playerName.runSARSA(playerPos,offset,enemyPos,dice)
            
            if player > playercount:
                actions.append(1)
                actions.append(0)
            else:
                actions.append(0)
                actions.append(player)
            
        return actions

    
    def playerAction(self,dice,playercount):
        if self.current_player().color == "RED":
            return self.rlAction(dice,playercount,'Q',self.RED,0)
        elif self.current_player().color == "BLUE":
            return self.rlAction(dice,playercount,'sQ',self.BLUE,39)
        elif self.current_player().color == "YELLOW":
            return self.rndAction(dice,playercount,self.YELLOW)
        else :
            return self.rlAction(dice,playercount,'SARSA',self.GREEN,13)

    def roll(self):
        roll = random.randint(1,6)
        num = 0

        actions = self.playerAction(roll,self.current_player().pieces_out()-1)

        if roll == 6 and self.current_player().pieces_out()==0:
            self.current_player().takeout()
            self.pity = 4
        elif roll == 6 and actions[0] and self.current_player().pieces_in() != 0:
            self.current_player().takeout()
            num = self.current_player().pieces_out()-1
            self.pity = 4
        elif self.current_player().pieces_out():
            num = actions[1]
            self.current_player().move(roll,num)
            self.pity = 4
        else :
            self.pity += 1

        if self.current_player().active_piece(num):
            cell = self.current_player().active_piece(num).position
            for i in range(len(self.stars)-1):
                if cell == self.stars[i]:
                    self.current_player().move(self.stars[i+1]-self.stars[i],num)

        # Knock pieces off the board if we landed on them
        self.knock_off(num)

        self.board.roll = roll

        if self.current_player().has_won():
            self.winner = self.current_player().color
            self.current_action = 1
        else:
            self.current_action = 2

    def in_game(self):
        return self.is_playing

    def current_player(self):
        return self.players[self.current_player_id]

    def next_player(self):
        # Roll again if you get a 6
        if self.board.roll != 6 and self.pity%4==0:
            self.current_player_id += 1
            self.pity = 1
            if self.current_player_id == self.number_of_players:
                self.current_player_id = 0


        self.board.roll = 0
        self.current_action = 0

    def knock_off(self,num):
        # Get cell we are on
        if self.current_player().active_piece(num):
            cell = self.board.get_cell(self.current_player().color, self.current_player().active_piece(num).position)
            
            for player in self.players:
                if player != self.current_player():
                    for pieces in range(player.pieces_out()):
                        if player.active_piece(pieces):
                            players_cell = self.board.get_cell(player.color, player.active_piece(pieces).position)

                            if cell.track_id == players_cell.track_id:
                                if cell.track_id == "1" or cell.track_id == "14" or cell.track_id == "27" or cell.track_id == "40":
                                    if cell.track_id == "1" and self.current_player().color=="RED":
                                        player.active_piece(pieces).return_to_start()

                                    elif cell.track_id == "40" and self.current_player().color=="BLUE":
                                        player.active_piece(pieces).return_to_start()

                                    elif cell.track_id == "27" and self.current_player().color=="YELLOW":
                                        player.active_piece(pieces).return_to_start()

                                    elif cell.track_id == "14" and self.current_player().color=="GREEN":
                                        player.active_piece(pieces).return_to_start()

                                    else:
                                        self.current_player().active_piece(num).return_to_start()
                                        return 

                                elif cell.track_id == "48" or cell.track_id == "35" or cell.track_id == "22" or cell.track_id == "9":
                                    self.current_player().active_piece(num).return_to_start()
                                    return 

                                else:
                                    try:
                                        if players_cell.track_id == self.board.get_cell(player.color, player.active_piece(pieces+1).position).track_id:
                                            self.current_player().active_piece(num).return_to_start()
                                            return 
                                        try:
                                            if players_cell.track_id == self.board.get_cell(player.color, player.active_piece(pieces+2).position).track_id:
                                                self.current_player().active_piece(num).return_to_start()
                                                return 
                                            try:
                                                if players_cell.track_id == self.board.get_cell(player.color, player.active_piece(pieces+3).position).track_id:
                                                    self.current_player().active_piece(num).return_to_start()
                                                    return 
                                            except:
                                                player.active_piece(pieces).return_to_start()
                                        except:
                                            player.active_piece(pieces).return_to_start()
                                    except:
                                        player.active_piece(pieces).return_to_start()
