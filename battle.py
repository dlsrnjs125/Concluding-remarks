# 전투 시스템

class BattleManager:
    def is_monster_dead(self, monster):
        """
        몬스터의 HP가 0 이하인지 확인하여 사망 여부를 반환합니다.
        """
        return monster.hp <= 0

    def player_attack(self, player, monster):
        """
        플레이어가 몬스터를 공격하고 결과를 출력합니다.
        """
        player.attack(monster)
        if self.is_monster_dead(monster):
            print("몬스터를 처치했습니다!")
        else:
            print(f"몬스터의 남은 HP: {monster.hp}")
