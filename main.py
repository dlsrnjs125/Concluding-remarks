from monster import BlueMushroom
from player import Player
from battle import BattleManager
from game import Game

player = Player("용사", hp=100, attack_power=30)
monster = BlueMushroom()
battle_manager = BattleManager()

game = Game(player, monster, battle_manager)
game.start()