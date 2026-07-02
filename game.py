# 게임 화면 및 게임 루프

class Game:
    def __init__(self, player, monster, battle_manager):
        self.player = player
        self.monster = monster
        self.battle_manager = battle_manager

    def show_menu(self):
        print("\n=== 메뉴 ===")
        print("1. 공격하기")
        print("2. 플레이어 정보 보기")
        print("3. 몬스터 정보 보기")
        print("4. 종료")
        print("============")

    def start(self):
        print("게임을 시작합니다!")
        while True:
            self.show_menu()
            choice = input("원하는 메뉴의 번호를 입력하세요: ").strip()

            if choice == "1":
                self.battle_manager.player_attack(self.player, self.monster)
                if self.monster.hp <= 0:
                    print(f"\n축하합니다! {self.monster.name}을(를) 물리쳤습니다!")
                    print("게임을 종료합니다.")
                    break
            elif choice == "2":
                self.player.info()
            elif choice == "3":
                self.monster.info()
            elif choice == "4":
                print("게임을 종료합니다. 이용해 주셔서 감사합니다.")
                break
            else:
                print("잘못된 입력입니다. 1~4 사이의 번호를 입력해 주세요.")