import streamlit as st
import contextlib
import io
from player import Player
from monster import BlueMushroom
from battle import BattleManager

# Streamlit 페이지 설정
st.set_page_config(page_title="RETRO 8-BIT MONSTER SLAYER", page_icon="🎮", layout="centered")

# 레트로 폰트 및 스타일 로드 (동네 오락실 게임기 감성)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Share+Tech+Mono&display=swap');
@import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2107@1.1/NeoDunggeunmo.woff');

body {
    background-color: #0F0F13;
    color: #F0F0F0;
}
.arcade-title {
    font-family: 'NeoDunggeunmo', monospace;
    font-size: 32px;
    color: #FFD700;
    text-align: center;
    text-shadow: 3px 3px #FF0055, -2px -2px #00E5FF;
    padding: 20px 0 5px 0;
    margin-bottom: 5px;
    letter-spacing: 2px;
}
.arcade-subtitle {
    font-family: 'NeoDunggeunmo', monospace;
    font-size: 16px;
    color: #00E5FF;
    text-align: center;
    margin-bottom: 25px;
    letter-spacing: 2px;
}
.cabinet-blue {
    background-color: #161622;
    border: 4px solid #00E5FF;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 0 15px #00E5FF;
    margin-bottom: 20px;
}
.cabinet-red {
    background-color: #161622;
    border: 4px solid #FF0055;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 0 15px #FF0055;
    margin-bottom: 20px;
}
.stats-font {
    font-family: 'Share Tech Mono', monospace;
    font-size: 17px;
    color: #E0E0FF;
    line-height: 1.6;
    text-align: left;
    background-color: #0B0B0F;
    padding: 10px;
    border-radius: 6px;
    margin-top: 10px;
}
.lvl-badge {
    font-family: 'Press Start 2P', monospace;
    font-size: 11px;
    background-color: #FFD700;
    color: #000000;
    padding: 5px 10px;
    border-radius: 5px;
    display: inline-block;
    margin-bottom: 12px;
    box-shadow: 0 0 5px #FFD700;
}
.log-box {
    background-color: #050508;
    border: 2px solid #333344;
    border-radius: 8px;
    padding: 15px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 15px;
    color: #00FF66;
    height: 200px;
    overflow-y: auto;
    box-shadow: inset 0 0 10px #000000;
}
.vs-divider {
    font-family: 'Press Start 2P', monospace;
    font-size: 24px;
    color: #FF0055;
    text-align: center;
    padding-top: 110px;
    text-shadow: 2px 2px #000;
    animation: blinker 1.5s linear infinite;
}
@keyframes blinker {
    50% { opacity: 0.3; }
}
</style>
""", unsafe_allow_html=True)

# 타이틀 표시
st.markdown('<div class="arcade-title">몬스타 몹 잡기</div>', unsafe_allow_html=True)
st.markdown('<div class="arcade-subtitle">동전 넣기 _</div>', unsafe_allow_html=True)

# 세션 상태 초기화 (레벨 및 경험치 시스템 도입)
if "player_level" not in st.session_state:
    st.session_state.player_level = 1
if "player_exp" not in st.session_state:
    st.session_state.player_exp = 0
if "monster_level" not in st.session_state:
    st.session_state.monster_level = 1

if "player" not in st.session_state:
    st.session_state.player = Player("용사", hp=100, attack_power=30)
if "monster" not in st.session_state:
    st.session_state.monster = BlueMushroom()
    # 몬스터 레벨에 따른 스펙 스케일링
    st.session_state.monster.hp = 50 + (st.session_state.monster_level - 1) * 15
    st.session_state.monster.attack_power = 5 + (st.session_state.monster_level - 1) * 3
    st.session_state.monster.defense = 2 + (st.session_state.monster_level - 1) * 1
if "battle_manager" not in st.session_state:
    st.session_state.battle_manager = BattleManager()
if "log" not in st.session_state:
    st.session_state.log = ["GAME STARTED! READY? FIGHT!"]

player = st.session_state.player
monster = st.session_state.monster
battle_manager = st.session_state.battle_manager

# 레이아웃 구성
col1, col_vs, col2 = st.columns([4, 1, 4])

with col1:
    st.markdown('<div class="cabinet-blue">', unsafe_allow_html=True)
    st.markdown(f'<div class="lvl-badge">LV.{st.session_state.player_level}</div>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:#00E5FF; margin:0 0 10px 0;">👤 {player.name}</h3>', unsafe_allow_html=True)
    
    # 용사 픽셀 이미지 렌더링
    st.image("warrior.png", use_container_width=True)
    
    # 네온 체력바 (HP Gauge)
    hp_pct = max(0, min(100, int(player.hp)))
    st.markdown(f"""
    <div style="background-color:#222; border-radius:5px; height:16px; width:100%; margin-bottom:5px; border: 1px solid #00E5FF;">
        <div style="background-color:#00FF66; height:14px; width:{hp_pct}%; border-radius:4px; box-shadow: 0 0 10px #00FF66; transition: width 0.3s ease;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stats-font">
        ❤️ HP: <b>{player.hp} / 100</b><br>
        ⚔️ ATTACK: <b>{player.attack_power}</b><br>
        ⚡ EXP: <b>{st.session_state.player_exp} / 100</b>
    </div>
    """, unsafe_allow_html=True)
    
    # 경험치 게이지 (EXP Bar)
    exp_pct = max(0, min(100, st.session_state.player_exp))
    st.markdown(f"""
    <div style="background-color:#111; border-radius:3px; height:6px; width:100%; margin-top:6px; border: 1px solid #444;">
        <div style="background-color:#FFD700; height:4px; width:{exp_pct}%; border-radius:2px; box-shadow: 0 0 5px #FFD700;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_vs:
    st.markdown('<div class="vs-divider">VS</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="cabinet-red">', unsafe_allow_html=True)
    st.markdown(f'<div class="lvl-badge" style="background-color:#FF0055; color:#ffffff; box-shadow: 0 0 5px #FF0055;">LV.{st.session_state.monster_level}</div>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:#FF0055; margin:0 0 10px 0;">👾 {monster.name}</h3>', unsafe_allow_html=True)
    
    # 몬스터 픽셀 이모지 네온 박스 렌더링
    st.markdown("""
    <div style="font-size: 110px; height: 160px; display: flex; align-items: center; justify-content: center; filter: drop-shadow(0 0 12px #FF0055); margin-bottom: 20px; user-select: none;">
        🍄
    </div>
    """, unsafe_allow_html=True)
    
    # 네온 체력바 (HP Gauge)
    max_monster_hp = 50 + (st.session_state.monster_level - 1) * 15
    m_hp_pct = max(0, min(100, int((monster.hp / max_monster_hp) * 100)))
    st.markdown(f"""
    <div style="background-color:#222; border-radius:5px; height:16px; width:100%; margin-bottom:5px; border: 1px solid #FF0055;">
        <div style="background-color:#FF0055; height:14px; width:{m_hp_pct}%; border-radius:4px; box-shadow: 0 0 10px #FF0055; transition: width 0.3s ease;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stats-font">
        ❤️ HP: <b>{monster.hp} / {max_monster_hp}</b><br>
        ⚔️ ATTACK: <b>{monster.attack_power}</b><br>
        🛡️ DEFENSE: <b>{monster.defense}</b>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# 게임 작동 흐름 제어
if player.hp <= 0:
    st.error("💀 GAME OVER... 용사가 전투 불능 상태에 빠졌습니다!")
    if st.button("🎮 INSERT COIN (이어하기/처음부터)", use_container_width=True):
        st.session_state.player_level = 1
        st.session_state.player_exp = 0
        st.session_state.monster_level = 1
        st.session_state.player = Player("용사", hp=100, attack_power=30)
        st.session_state.monster = BlueMushroom()
        st.session_state.log = ["CREDIT INSERTED. READY... GO!"]
        st.rerun()

elif monster.hp <= 0:
    st.balloons()
    st.success(f"🎉 STAGE CLEAR! {monster.name}을(를) 완벽히 소탕했습니다!")
    
    # 보상 경험치 계산 (몬스터 레벨에 비례)
    exp_reward = 40 + st.session_state.monster_level * 10
    
    if st.button("➡️ 획득한 전리품 정산 및 다음 Stage", use_container_width=True):
        st.session_state.player_exp += exp_reward
        st.session_state.log.append(f"🏆 {monster.name} 소탕 완료! EXP +{exp_reward} 획득")
        
        # 플레이어 레벨업 계산
        if st.session_state.player_exp >= 100:
            st.session_state.player_level += 1
            st.session_state.player_exp %= 100
            player.attack_power += 10
            player.hp = 100  # 레벨업 특전으로 HP 풀 회복
            st.session_state.log.append(f"⭐️⭐️ LEVEL UP! 플레이어 레벨이 {st.session_state.player_level}(으)로 상승했습니다! (공격력 +10, HP 최대 회복) ⭐️⭐️")
            
        # 다음 단계 몬스터 세팅 (점진적 난이도 스케일링)
        st.session_state.monster_level += 1
        st.session_state.monster = BlueMushroom()
        st.session_state.monster.hp = 50 + (st.session_state.monster_level - 1) * 15
        st.session_state.monster.attack_power = 5 + (st.session_state.monster_level - 1) * 3
        st.session_state.monster.defense = 2 + (st.session_state.monster_level - 1) * 1
        
        st.session_state.log.append(f"👾 [Stage {st.session_state.monster_level}] Lv.{st.session_state.monster_level} 파랑버섯이 출현했습니다!")
        st.rerun()

else:
    # 아케이드 느낌의 공격 버튼
    if st.button("⚔️ ATTACK (공격하기)", use_container_width=True):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            # 1. 플레이어 공격 (BattleManager 로직)
            battle_manager.player_attack(player, monster)
            
            # 2. 몬스터가 살아있다면 반격 처리
            if not battle_manager.is_monster_dead(monster):
                player.hp -= monster.attack_power
                if player.hp < 0:
                    player.hp = 0
                print(f"💥 {monster.name}이(가) 반격하여 {player.name}에게 {monster.attack_power}의 피해를 입혔습니다!")
                if player.hp <= 0:
                    print(f"💀 {player.name}이(가) 쓰러졌습니다...")

        # 캡처한 텍스트 로그에 반영
        console_output = f.getvalue().strip()
        if console_output:
            for line in console_output.split('\n'):
                if line.strip():
                    st.session_state.log.append(line.strip())
        st.rerun()

# 레트로 아케이드 터미널 로그박스
st.markdown('### 📜 SYSTEM LOG')
log_entries = "<br>".join([f"> {entry}" for entry in reversed(st.session_state.log)])
st.markdown(f'<div class="log-box">{log_entries}</div>', unsafe_allow_html=True)
