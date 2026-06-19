import random
import time

import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(
    page_title="Turbo Racer",
    page_icon="🏎️"
)


WIDTH = 400
HEIGHT = 700


# ---------- LOAD IMAGES ----------
player_img = Image.open(
    "assets/player.png"
).convert("RGBA")

enemy_img = Image.open(
    "assets/enemy.png"
).convert("RGBA")

coin_img = Image.open(
    "assets/coin.png"
).convert("RGBA")

player_img = player_img.resize((60,100))
enemy_img = enemy_img.resize((60,100))
coin_img = coin_img.resize((40,40))


# ---------- STATE ----------

if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.car = 180
    st.session_state.enemies = []
    st.session_state.coins = []
    st.session_state.money = 0
    st.session_state.score = 0
    st.session_state.speed = 8
    st.session_state.nitro = 0



def start():
    st.session_state.running = True



def reset():
    st.session_state.running = False
    st.session_state.enemies = []
    st.session_state.coins = []
    st.session_state.money = 0
    st.session_state.score = 0
    st.session_state.speed = 8
    st.session_state.nitro = 0
    st.session_state.car = 180



def left():
    if st.session_state.car > 100:
        st.session_state.car -= 30


def right():
    if st.session_state.car < 250:
        st.session_state.car += 30



def use_nitro():
    if st.session_state.nitro > 0:
        st.session_state.nitro -= 1
        st.session_state.speed += 10

def pause():
    st.session_state.paused = not st.session_state.paused

# ---------- MENU ----------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("⬅️"):
        left()

with col2:
    if st.button("🚀 Nitro"):
        use_nitro()

with col3:
    if st.button("➡️"):
        right()

with col4:
    if st.button("🏁 START"):
        start()

with col5:
    if st.button("⏸️ PAUSE"):
        pause()
# ---------- SHOP ----------

st.sidebar.title("🛒 Shop")

if st.sidebar.button("⚡ Upgrade speed (10💰)"):
    if st.session_state.money >= 10:
        st.session_state.money -= 10
        st.session_state.speed += 2


if st.sidebar.button("🚀 Nitro +1 (5💰)"):
    if st.session_state.money >= 5:
        st.session_state.money -= 5
        st.session_state.nitro += 1


st.sidebar.write(
    "💰",
    st.session_state.money
)

st.sidebar.write(
    "🚀",
    st.session_state.nitro
)



# ---------- DRAW ----------

def draw():

    img = Image.new(
        "RGBA",
        (WIDTH,HEIGHT),
        "green"
    )

    draw = ImageDraw.Draw(img)


    # silnice + zatáčky
    draw.rounded_rectangle(
        (70,0,330,HEIGHT),
        40,
        fill="black"
    )


    # čáry
    for y in range(0,HEIGHT,80):
        draw.rectangle(
            (195,y,205,y+40),
            fill="white"
        )


    # hráč

    img.alpha_composite(
        player_img,
        (
            st.session_state.car,
            550
        )
    )

    # nepřátelé

    for e in st.session_state.enemies:
        img.alpha_composite(
            enemy_img,
            (
                e["x"],
                e["y"]
            )
        )

    # mince

    for c in st.session_state.coins:
        img.alpha_composite(
            coin_img,
            (
                c["x"],
                c["y"]
            )
        )

    return img



# ---------- GAME LOOP ----------


if st.session_state.running and not st.session_state.paused:

    if random.randint(1, 20) == 1:

        lanes = [100, 170, 240]

        # najdi volné pruhy
        possible = []

        for lane in lanes:

            blocked = False

            for e in st.session_state.enemies:
                if (
                        e["x"] == lane
                        and e["y"] < 220
                ):
                    blocked = True

            if not blocked:
                possible.append(lane)

        # vždy necháme aspoň jeden průjezdný pruh
        if len(possible) > 1:
            lane = random.choice(possible)

            st.session_state.enemies.append(
                {
                    "x": lane,
                    "y": -120
                }
            )

    if random.randint(1, 25) == 1:

        lanes = [110, 180, 250]
        possible = []

        for lane in lanes:

            safe = True

            # kontrola nepřátel
            for e in st.session_state.enemies:
                if (
                        e["x"] == lane
                        and abs(e["y"] + 50) < 180
                ):
                    safe = False

            # kontrola dalších mincí
            for c in st.session_state.coins:
                if (
                        abs(e["x"] - lane) < 70
                        and abs(e["y"]) < 220
                ):
                    safe = False

            if safe:
                possible.append(lane)

        if possible:
            lane = random.choice(possible)

            st.session_state.coins.append(
                {
                    "x": lane,
                    "y": -50
                }
            )


    for e in st.session_state.enemies:
        e["y"] += st.session_state.speed



    for c in st.session_state.coins:
        c["y"] += st.session_state.speed

    for c in st.session_state.coins[:]:

        for e in st.session_state.enemies:

            if (
                    c["x"] == e["x"]
                    and abs(c["y"] - e["y"]) < 80
            ):
                st.session_state.coins.remove(c)
                break
    # sběr mincí

    PLAYER_X = st.session_state.car
    PLAYER_Y = 550

    for c in st.session_state.coins[:]:

        if (
                abs(c["x"] - PLAYER_X) < 50
                and abs(c["y"] - PLAYER_Y) < 60
        ):
            st.session_state.money += 1
            st.session_state.coins.remove(c)



    # crash

    PLAYER_X = st.session_state.car
    PLAYER_Y = 550

    for e in st.session_state.enemies:

        if (
                abs(e["x"] - PLAYER_X) < 45
                and abs(e["y"] - PLAYER_Y) < 70
        ):
            st.error("💥 CRASH!")
            st.session_state.running = False



    st.session_state.score += 1



    st.image(
        draw(),
        width=400
    )


    st.metric(
        "🏆 Skóre",
        st.session_state.score
    )


    time.sleep(0.05)
    st.rerun()



else:

    st.image(draw(),width=400)

    st.info(
        "Klikni START a začni závod!"
    )