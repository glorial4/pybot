from abc import abstractmethod
from game.game_state import GameState
from game.item import Item
import game.character_class
from util.utility import *
from random import Random

from game.position import Position

class Strategy(object):
    """Before the game starts, pick a class for your bot to start with.

    :returns: A game.CharacterClass Enum.
    """
    def strategy_initialize(self, my_player_index: int) -> None:
        return game.character_class.CharacterClass.KNIGHT

    """Each turn, decide if you should use the item you're holding. Do not try to use the
    legendary Item.None!

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: If you want to use your item
    """
    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False

    """Each turn, pick a position on the board that you want to move towards. Be careful not to
    fall out of the board!

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Position object.
    """
    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        player = game_state.player_state_list[my_player_index]
        posx = player.position.x
        posy = player.position.y
        if in_bounds(player.position):
            otherplayers = []
            for i in game_state.player_state_list:
                if i != my_player_index:
                    otherplayers.append(i)
            around = []
            pos_around = Position()
            speed = player.stat_set.speed
            for i in range(-1*speed, speed+1):
                for j in range(-1*speed, speed+1):
                    pos_around.x = posx + i
                    pos_around.y = posy + j
                    if in_bounds(pos_around):
                        around.append(pos_around)
            dis_center = []
            center = Position()
            center.x = 4
            center.y = 4
            if center.x == player.position.x and center.y == player.position.y:
                return player.position
            for i in range(len(around)):
                dis_center.append(chebyshev_distance(center, around[i]))
            min_dis = min(dis_center)
            min_index = 0
            for i in range(len(dis_center)):
                if min_dis == dis_center[i]:
                    min_index = i
            return around[i]
        return player.position

    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: Your target's player index.
    """
    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        return Random().randint(0, 3)

    """Each turn, pick an item you want to buy. Return Item.None if you don't think you can
    afford anything.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Item object.
    """
    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        return Item.NONE

