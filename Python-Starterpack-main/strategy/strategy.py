from abc import abstractmethod
from game.game_state import GameState
from game.item import Item
from util.utility import *
from random import Random
from game.player_state import PlayerState
from game.character_class import CharacterClass

from game.position import Position

class Strategy(object):
    """Before the game starts, pick a class for your bot to start with.

    :returns: A game.CharacterClass Enum.
    """
    def strategy_initialize(self, my_player_index: int) -> None:
        return CharacterClass.KNIGHT

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

        pos = player.position
        speed = player.stat_set.speed
        
        spawnpoint = self.get_spawn(my_player_index)
        center = self.get_close_center(spawnpoint)
        centers = self.centers()

        others = []
        for i in range(len(game_state.player_state_list)):
            if i != my_player_index:
                others.append(game_state.player_state_list[i])

        if player.item == Item.NONE and player.gold >= 8 and pos.x == spawnpoint.x and pos.y == spawnpoint.y:
            return pos

        at_center = False
        for cen in centers:
            if pos.x == cen.x and pos.y == cen.y:
                at_center = True

        if not at_center:
            new_pos = Position()
            if center.x == 4 and center.y == 4:
                new_pos.x = pos.x + 1
                new_pos.y = pos.y + 1
            elif center.x == 4 and center.y == 5:
                new_pos.x = pos.x + 1
                new_pos.y = pos.y - 1
            elif center.x == 5 and center.y == 5:
                new_pos.x = pos.x - 1
                new_pos.y = pos.y - 1
            elif center.x == 5 and center.y == 4:
                new_pos.x = pos.x - 1
                new_pos.y = pos.y + 1

            for p in others:
                if p.stat_set.range >= 2 and self.in_range(new_pos, p.position, p.stat_set.range) and manhattan_distance(new_pos, center) > 1:
                    if player.item == Item.HUNTER_SCOPE:
                        return new_pos
                    return spawnpoint
            
            return new_pos

        safe = []
        for c in centers:
            safe_spot = True
            for p in others:
                if self.in_range(c, p.position, p.stat_set.range):
                    safe_spot = False
            safe.append(safe_spot)
        
        for i in range(len(safe)):
            if safe[i]:
                return centers[i]
        
        damages = []
        for c in centers:
            damage = 0
            for p in others:
                if self.in_range(c, p.position, p.stat_set.range):
                    damage += p.stat_set.damage
            damages.append(damage)
        
        min_dmg = damages.index(min(damages))

        damage = 0
        for p in others:
            if self.in_range(pos, p.position, p.stat_set.range):
                damage += p.stat_set.damage
        if damage == min(damages):
            return pos

        return centers[min_dmg]
            

    def get_spawn(self, my_player_index: int) -> Position:
        spawnpoint = Position()
        if my_player_index == 0:
            spawnpoint.x = 0
            spawnpoint.y = 0
        elif my_player_index == 1:
            spawnpoint.x = 9
            spawnpoint.y = 0
        elif my_player_index == 2:
            spawnpoint.x = 9
            spawnpoint.y = 9
        elif my_player_index == 3:
            spawnpoint.x = 0
            spawnpoint.y = 9
        return spawnpoint
    
    def get_close_center(self, spawnpoint: Position) -> Position:
        center = Position()
        if spawnpoint.x == 0 and spawnpoint.y == 0:
            center.x = 4
            center.y = 4
        elif spawnpoint.x == 9 and spawnpoint.y == 0:
            center.x = 5
            center.y = 4
        elif spawnpoint.x == 0 and spawnpoint.y == 9:
            center.x = 4
            center.y = 5
        elif spawnpoint.x == 9 and spawnpoint.y == 9:
            center.x = 5
            center.y = 5
        return center
    
    def centers(self):
        center1 = Position()
        center1.x = 4
        center1.y = 4

        center2 = Position()
        center2.x = 4
        center2.y = 5

        center3 = Position()
        center3.x = 5
        center3.y = 4

        center4 = Position()
        center4.x = 5
        center4.y = 5

        centers = [center1, center2, center3, center4]
        return centers


    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: Your target's player index.
    """
            
    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        player = game_state.player_state_list[my_player_index]
        others = []
        others_index = []
        for i in range(len(game_state.player_state_list)):
            if i != my_player_index:
                others.append(game_state.player_state_list[i])
                others_index.append(i)

        in_range_players = []
        in_range_index = []

        for i in range(len(others)):
            if self.in_range(player.position, others[i].position, player.stat_set.range):
                in_range_players.append(others[i])
                in_range_index.append(others_index[i])

        for i in range(len(in_range_players)):
            enemy = in_range_players[i]
            if enemy.character_class == CharacterClass.ARCHER:
                return in_range_index[i]

        for i in range(len(in_range_players)):
            if in_range_players[i].health <= player.stat_set.damage:
                return in_range_index[i]

        for i in range(len(in_range_players)):
            enemy = in_range_players[i]
            if enemy.character_class == CharacterClass.WIZARD:
                return in_range_index[i]
        
        for i in range(len(in_range_players)):
            enemy = in_range_players[i]
            if enemy.character_class == CharacterClass.KNIGHT:
                return in_range_index[i]

        return my_player_index

    def in_range(self, pos1: Position, pos2: Position, r: int) -> bool:
        return chebyshev_distance(pos1, pos2) <= r


    """Each turn, pick an item you want to buy. Return Item.None if you don't think you can
    afford anything.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Item object.
    """
    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        player = game_state.player_state_list[my_player_index]
        gold = player.gold
        curr_item = player.item
        if gold >= 8 and curr_item == Item.NONE:
            return Item.HUNTER_SCOPE
        else:
            return Item.NONE

