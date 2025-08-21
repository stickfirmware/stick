import random
import time

from modules.printer import log
import modules.io_manager as io_man
import modules.powersaving as ps
import modules.popup as popup
import modules.menus as menus
import modules.os_constants as osc

import fonts.def_8x8 as f8x8

tiles = 8 # Tiles, ex. if 8 will make it 8x8
tile_max = 128 # Max pixels, ex. 128x128
bombs_max = 7

# States
# 0 = not seen
# 1 = seen
# 2 = flags

# Gen map
def generate():
    log("Starting generator")
    
    # Map
    tiles_map = [] # Numbered tiles
    
    # Temp generator values
    bomb_positions_temp = []
    bombs = []
    
    # Push proper bomb array
    log("Push arrays")
    for y in range(tiles):
        y_bombs = []
        y_zeroes = []
        for x in range(tiles):
            y_bombs.append(False)
            y_zeroes.append(0)
        bombs.append(y_bombs)
        tiles_map.append(y_zeroes)
    
    # Generate bombs
    log("Generating bombs")
    for i in range(bombs_max):
        rand = 0
        while rand == 0 or rand in bomb_positions_temp:
            rand = random.randint(1, (tiles*tiles) - 1)
        bomb_positions_temp.append(rand)
        
    # Set bombs
    log("Set bombs")
    for bomb in bomb_positions_temp:
        b = bomb
        y = b // tiles
        x = b % tiles
        bombs[y][x] = True
    
    # Calculate tile nums
    log("Calculate tile numbers")
    dirs = [(-1,-1),(-1,0),(-1,1),
            (0,-1),        (0,1),
            (1,-1),(1,0),(1,1)]
    
    for y in range(tiles):
        for x in range(tiles):
            if bombs[y][x]:
                tiles_map[y][x] = -1 # Bomb
            else:
                count = 0
                for dy, dx in dirs:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < tiles and 0 <= nx < tiles:
                        if bombs[ny][nx]:
                            count += 1
                tiles_map[y][x] = count
                
    del bombs
    
    log("Numbers map:")
    for row in tiles_map:
        log(row)
    
        
    del bomb_positions_temp
    
    return tiles_map

# Draw one tile
def draw_tile(tft, x, y, tiles_map, state, tile_size):
    px = x * tile_size
    py = y * tile_size

    if state == 0:  # hidden
        tft.fill_rect(px, py, tile_size, tile_size, 50776)
    elif state == 2:  # flag
        tft.fill_rect(px, py, tile_size, tile_size, 65504)
    else:
        if tiles_map[y][x] == -1:
            tft.fill_rect(px, py, tile_size, tile_size, 63488)
        else:
            tft.fill_rect(px, py, tile_size, tile_size, 0)
            # Draw only not 0no wl
            if str(tiles_map[y][x]) != "0":
                num = str(tiles_map[y][x])
                x_text = px + (tile_size - 6) // 2
                y_text = py + (tile_size - 8) // 2
                tft.text(f8x8, num, x_text, y_text, 2019)
    
# Render full map
def render_grid_full(tft, tiles_map, states, sel_x=0, sel_y=0):
    ps.boost_allowing_state(True) # Powersaving boosts
    tile_size = tile_max // tiles

    for y in range(tiles):
        for x in range(tiles):
            draw_tile(tft, x, y, tiles_map, states[y][x], tile_size)

    # highlight selection
    px = sel_x * tile_size
    py = sel_y * tile_size
    tft.rect(px, py, tile_size, tile_size, 63648)

    ps.boost_allowing_state(False) # Disable boosting
    ps.loop() # Back to main freq

# Render only changed tiles
def render_grid_partial(tft, tiles_map, states, states_prev, sel_x, sel_y, last_sel_x, last_sel_y):
    ps.boost_allowing_state(True) # Powersaving boosts
    tile_size = tile_max // tiles

    # updzate only changed tiles
    for y in range(tiles):
        for x in range(tiles):
            if states[y][x] != states_prev[y][x]:
                draw_tile(tft, x, y, tiles_map, states[y][x], tile_size)

    # delete old highlight
    draw_tile(tft, last_sel_x, last_sel_y, tiles_map, states[last_sel_y][last_sel_x], tile_size)

    # highlight selection
    px = sel_x * tile_size
    py = sel_y * tile_size
    tft.rect(px, py, tile_size, tile_size, 63648)

    ps.boost_allowing_state(False) # Disable boosting
    ps.loop() # Back to main freq

    
# Dig
def reveal_tile(x, y, tiles_map, states):
    if states[y][x] == 1:
        return

    stack = [(x, y)]
    dirs = [(-1,-1),(-1,0),(-1,1),
            (0,-1),        (0,1),
            (1,-1),(1,0),(1,1)]

    while stack:
        cx, cy = stack.pop()
        if states[cy][cx] == 1:
            continue
        states[cy][cx] = 1  # reveal

        if tiles_map[cy][cx] == 0:
            # if zero, reveal surrounding tiles
            for dx, dy in dirs:
                nx, ny = cx+dx, cy+dy
                if 0 <= nx < tiles and 0 <= ny < tiles:
                    if states[ny][nx] == 0:  # not revealed
                        stack.append((nx, ny))

# count placed flags
def count_flags(states):
    return sum(row.count(2) for row in states)

# Check if bombs flagged ok
def check_win(tiles_map, states):
    for y in range(tiles):
        for x in range(tiles):
            if tiles_map[y][x] == -1 and states[y][x] != 2:
                return False
            if tiles_map[y][x] != -1 and states[y][x] == 2:
                return False
    return True

# Format time for popups
def format_ticks_ms(ticks):
    seconds_total = ticks // 1000
    s = seconds_total % 60
    minutes_total = seconds_total // 60
    m = minutes_total % 60
    return f"{m:02}:{s:02}"

# Win cb, popup
def win_callback(tick):
    elapsed = time.ticks_diff(time.ticks_ms(), tick)
    text = format_ticks_ms(elapsed)
    popup.show(f"Time: {text}\nMap: {tiles}x{tiles}\nBombs: {bombs_max}", "You win!", 60)
    return True

# Callback for losing, popup
def lose_callback(tick):
    elapsed = time.ticks_diff(time.ticks_ms(), tick)
    text = format_ticks_ms(elapsed)
    popup.show(f"Time: {text}\nMap: {tiles}x{tiles}\nBombs: {bombs_max}", "You lose!", 60)
    return True

def draw_bomb_cell(tft, x, y, tile_size, detonated=False, bg_color=None):
    px = x * tile_size
    py = y * tile_size

    # Random color
    if detonated:
        bg = 63488  # red
    else:
        bg = bg_color if bg_color is not None else random.choice([2019, 63488, 65504, 64512, 2016])

    tft.fill_rect(px, py, tile_size, tile_size, bg)

    char_w, char_h = 6, 8
    x_text = px + (tile_size - char_w) // 2
    y_text = py + (tile_size - char_h) // 2
    tft.text(f8x8, "*", x_text, y_text, 0, bg)  # *
    tft.rect(px, py, tile_size, tile_size, 0)


def mark_wrong_flag(tft, x, y, tile_size, bg_color=0):
    px = x * tile_size
    py = y * tile_size
    tft.fill_rect(px, py, tile_size, tile_size, bg_color)
    
    char_w, char_h = 6, 8
    x_text = px + (tile_size - char_w) // 2
    y_text = py + (tile_size - char_h) // 2
    tft.text(f8x8, "X", x_text, y_text, 63488, bg_color)  # X
    tft.rect(px, py, tile_size, tile_size, 0)



# Animated bomb reveal
def animate_reveal_bombs(tft, tiles_map, states, boom_x, boom_y, delay_ms=15):
    ps.boost_allowing_state(True)
    tile_size = tile_max // tiles

    # Build distance map
    order = []
    for y in range(tiles):
        for x in range(tiles):
            d = abs(x - boom_x) + abs(y - boom_y)
            d += random.randint(0, 1)
            order.append((d, x, y))
    order.sort(key=lambda e: e[0])

    # Detonate central bomb with flash
    for flash in range(2):
        draw_bomb_cell(tft, boom_x, boom_y, tile_size, detonated=True,
                    bg_color=63488 if flash % 2 == 0 else 64512)
        time.sleep_ms(40)

    last_d = -1
    for d, x, y in order:
        if d != last_d:
            time.sleep_ms(delay_ms)
            last_d = d

        is_bomb = (tiles_map[y][x] == -1)
        is_flag = (states[y][x] == 2)

        if is_bomb:
            if x == boom_x and y == boom_y:
                continue
            # small flash before settling on bomb color
            for flash in range(2):
                color = random.choice([2019, 63488, 65504, 64512, 2016])
                draw_bomb_cell(tft, x, y, tile_size, detonated=False, bg_color=color)
                time.sleep_ms(10)
        else:
            if is_flag:
                mark_wrong_flag(tft, x, y, tile_size, bg_color=0)

    ps.boost_allowing_state(False)
    ps.loop()
    
# Main game loop
def game():
    tft = io_man.get('tft')
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    
    # Current and previous selection coordinates
    selection_x, selection_y = 0, 0
    last_sel_x, last_sel_y = 0, 0
    
    # Tile states: 0 = hidden, 1 = revealed, 2 = flag
    states = [[0]*tiles for _ in range(tiles)]
    states_prev = [row[:] for row in states]
    
    # Latest time
    start_time = time.ticks_ms()
    last_time_text = ""
    
    # Generate the game map
    tiles_map = generate()
    
    upd = True
    upd_full = True
    while True:
        if upd:
            if upd_full:
                tft.fill(0)
                render_grid_full(tft, tiles_map, states, selection_x, selection_y)
                upd_full = False
                if osc.ENABLE_DEBUG_PRINTS:
                    tft.text(f8x8, "Debugging enabled, can cheat", 0, 127, 63488)
            else:
                render_grid_partial(
                    tft, tiles_map, states, states_prev,
                    selection_x, selection_y, last_sel_x, last_sel_y
                )
            
            states_prev = [row[:] for row in states]
            last_sel_x, last_sel_y = selection_x, selection_y
            
            upd = False
            
            tft.fill_rect(tile_max, 0, 40, tile_max, 0)  # clear sidebar
            flags_count = count_flags(states)
            tft.text(f8x8, f"Flags:\n{flags_count}/{bombs_max}", tile_max+2, 2, 2019)
            
            if check_win(tiles_map, states):
                time.sleep(2)
                win_callback(start_time)
                break
            
        # Update time
        elapsed = time.ticks_diff(time.ticks_ms(), start_time)
        text = format_ticks_ms(elapsed)
        if last_time_text != text:
            last_time_text = text
            tft.text(f8x8, "Time: " + text, tile_max+2, 10, 2019)
        
        # Button A – tile action
        if button_a.value() == 0:
            res = menus.menu("Tile", [("Dig", 1), ("Flag", 2), ("Cancel", None), ("Exit", 3)],)
            if res == 1:  # Dig
                reveal_tile(selection_x, selection_y, tiles_map, states)
                if tiles_map[selection_y][selection_x] == -1:
                    tft.fill(0)
                    render_grid_full(tft, tiles_map, states, selection_x, selection_y)
                    animate_reveal_bombs(
                        tft, tiles_map, states,
                        selection_x, selection_y,
                        delay_ms=60
                    )
                    time.sleep(0.4)
                    lose_callback(start_time)
                    break
            elif res == 2:  # Flag
                if states[selection_y][selection_x] == 0 or states[selection_y][selection_x] == 2:
                    current_flags = count_flags(states)
                    if current_flags >= bombs_max and states[selection_y][selection_x] != 2:
                        log("Cannot place more flags")
                        popup.show("Cannot place more flags", "Error", 13)
                    else:
                        states[selection_y][selection_x] = 0 if states[selection_y][selection_x] == 2 else 2
            elif res == 3:  # Exit
                return
            upd = True
            upd_full = True
            while button_a.value() == 0:
                time.sleep(0.05)

        # Button B – move X direction
        if button_b.value() == 0:
            selection_x = (selection_x + 1) % tiles
            while button_b.value() == 0:
                time.sleep(0.05)
            upd = True

        # Button C – move Y direction
        if button_c.value() == 0:
            selection_y = (selection_y + 1) % tiles
            while button_c.value() == 0:
                time.sleep(0.05)
            upd = True

        time.sleep(0.02)

def run():
    global tiles
    global bombs_max
    
    while True:
        # Main menu
        menu = menus.menu(
            "Minesweeper",
            [("Start", 1), ("Controls", 2), ("Exit", None)],
        )
        if menu == 1:
            mode = menus.menu("Select game mode", [("Begginer: 8x8", 0), ("Easy: 10x10", 1), ("Medium: 12x12", 2), ("Hard: 16x16", 3), ("Custom", 99), ("Close", None)])
            if mode != None:
                if mode == 99:
                    import modules.numpad as kb
                    tiles = kb.numpad("Enter map size max. 16")
                    if tiles < 1 or tiles > 16:
                        popup.show("Map size must be between 1 and 16", "Error", 15)
                        continue
                    bombs_max = kb.numpad("Enter bombs")
                    if bombs_max < 1 or bombs_max > (tiles*tiles//2):
                        popup.show("Bombs must be between 1 and half of total tiles", "Error", 15)
                        continue
                else:
                    mode_tiles = [8, 10, 12, 16]
                    tiles = mode_tiles[mode]
                    
                    # Calculate bombs, 16%
                    bombs_max = max(1, (tiles * tiles * 16) // 100)
                
                game()
        elif menu == 2:
            popup.show(
                "Use A to dig/flag tiles.\n"
                "Use B to move right.\n"
                "Use C to move down.\n",
                "Controls",
                60
            )
        else:
            break