# 플래이어 클래스

class Player:
    def __init__(self, name, hp=100, attack_power=30):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

    def attack(self, monster):
        damage = self.attack_power - monster.defense
        if damage < 1:
            damage = 1

        monster.hp -= damage
        if monster.hp < 0:
            monster.hp = 0

        print(f"{self.name}이(가) {monster.name}을(를) 공격했습니다!")
        print(f"{monster.name}에게 {damage}의 피해를 입혔습니다.")

    def info(self):
        print(f"--- {self.name} 정보 ---")
        print(f"체력(HP): {self.hp} | 공격력: {self.attack_power}")
