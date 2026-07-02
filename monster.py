# 몬스터 클래스

class Mob:
    def __init__(self, name, hp, attack_power, defense):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense

    def attack(self):
        print(f"[{self.name}] 공격했습니다.")

    def info(self):
        print(f"이름: {self.name} | HP: {self.hp} | 공격력: {self.attack_power} | 방어력: {self.defense}")


class Mushroom(Mob):
    def run(self):
        print(f"[{self.name}] 달리기!")

    def jump(self):
        print(f"[{self.name}] 점프!")


class BlueMushroom(Mushroom):
    def __init__(self, name="파랑버섯", hp=50, attack_power=5, defense=2):
        super().__init__(name, hp, attack_power, defense)
        self.color = "파랑"

    def blue_spore(self):
        print(f"[{self.name}] 파란 포자 날리기!")