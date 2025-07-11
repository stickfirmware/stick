class TicTacToe:
    def __init__(self):
        self.tmap = ["", "", "", "", "", "", "", "", "", "inProgress"]
    def checkWin(self, mapd, char):
        lines = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for line in lines:
            if all(mapd[i] == char for i in line):
                return True
        return False
    
    def checkTie(self, mapd):
        return all(cell != "" for cell in mapd[:9])
        
    def status(self, maptemp, me):
        enemy = "O" if me == "X" else "X"
        
        if maptemp[9] != "inProgress":
            return maptemp
        
        if self.checkWin(maptemp, me):
            maptemp[9] = "Won"
            self.tmap = maptemp
            return maptemp
        if self.checkWin(maptemp, enemy):
            maptemp[9] = "Lost"
            self.tmap = maptemp
            return maptemp

        
        if self.checkTie(maptemp):
            maptemp[9] = "Tied"
            self.tmap = maptemp
            return maptemp
        
        return maptemp
        
    def aiMedium(self, playAs):
        maptemp = self.tmap.copy()
        enemy = "X"
        me = playAs
        
        if maptemp[9] != "inProgress":
            return self.status(maptemp, me)
        
        if me == "X":
            enemy = "O"
        
        for i in range(9):
            if maptemp[i] == "":
                mapold = maptemp.copy()
                maptemp[i] = me
                if self.checkWin(maptemp, me):
                    maptemp[9] = "Won"
                    return self.status(maptemp, me)
                else:
                    maptemp = mapold

        block_pos = self.find_block_position(maptemp, enemy)
        if block_pos != -1:
            maptemp[block_pos] = me
            return self.status(maptemp, me)

        if maptemp[0] == enemy and maptemp[2] == enemy and maptemp[1] == "":
            maptemp[1] = me
            return self.status(maptemp, me)
        if maptemp[0] == enemy and maptemp[6] == enemy and maptemp[3] == "":
            maptemp[3] = me
            return self.status(maptemp, me)
        if maptemp[2] == enemy and maptemp[8] == enemy and maptemp[5] == "":
            maptemp[5] = me
            return self.status(maptemp, me)
        if maptemp[6] == enemy and maptemp[8] == enemy and maptemp[7] == "":
            maptemp[7] = me
            return self.status(maptemp, me)

        if maptemp[4] == "":
            maptemp[4] = me
            return self.status(maptemp, me)

        for pos in [0, 2, 6, 8]:
            if maptemp[pos] == "":
                maptemp[pos] = me
                return self.status(maptemp, me)

        for pos in [1, 3, 5, 7]:
            if maptemp[pos] == "":
                maptemp[pos] = me
                return self.status(maptemp, me)

        return maptemp

    def find_block_position(self, board, enemy):
        lines = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for line in lines:
            values = [board[i] for i in line]
            if values.count(enemy) == 2 and values.count("") == 1:
                return line[values.index("")]
        return -1
        
    def aiEasy(self, playAs):
        maptemp = self.tmap
        enemy = "X"
        me = playAs
        
        if maptemp[9] != "inProgress":
            return self.status(maptemp, me)
        
        if me == "X":
            enemy = "O"
        
        if self.checkWin(maptemp, me) == True:
            maptemp[9] = "Won"
            return maptemp
        elif self.checkWin(maptemp, enemy) == True:
            maptemp[9] = "Lost"
            return maptemp
        elif self.checkTie(maptemp) == True:
            maptemp[9] = "Tied"
            return maptemp
        
        # Check if in winning possition
        for i in range(len(maptemp)):
            mapold = maptemp.copy()
            if maptemp[i] == "":
                maptemp[i] = me
                if self.checkWin(maptemp, me) == True:
                    maptemp[9] = "Won"
                    return self.status(maptemp, me)
                else:
                    maptemp = mapold
        
        # If center is free, take it
        if maptemp[4] == "":
            maptemp[4] = me
            return self.status(maptemp, me)
        
        # Take the corners
        if maptemp[0] == "":
            maptemp[0] = me
            return self.status(maptemp, me)
        elif maptemp[2] == "":
            maptemp[2] = me
            return self.status(maptemp, me)
        elif maptemp[6] == "":
            maptemp[6] = me
            return self.status(maptemp, me)
        elif maptemp[8] == "":
            maptemp[8] = me
            return self.status(maptemp, me)
        # Or the edges
        elif maptemp[1] == "":
            maptemp[1] = me
            return self.status(maptemp, me)
        elif maptemp[3] == "":
            maptemp[3] = me
            return self.status(maptemp, me)
        elif maptemp[5] == "":
            maptemp[5] = me
            return self.status(maptemp, me)
        elif maptemp[7] == "":
            maptemp[7] = me
            return self.status(maptemp, me)

import fonts.def_8x8 as f8x8
import fonts.def_8x16 as f8x16
import fonts.def_16x16 as f16x16
import fonts.def_16x32 as f16x32

button_a = None
button_b = None
button_c = None
tft = None

def set_btf(bta, btb, btc, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

def render(board, selected):
    tft.fill(0)
    cell_size = 30
    start_x = 15
    start_y = 15

    for i in range(1, 3):
        tft.fill_rect(start_x + cell_size * i - 2, start_y, 4, cell_size * 3, 65535)
        tft.fill_rect(start_x, start_y + cell_size * i - 2, cell_size * 3, 4, 65535)

    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            val = board[idx]
            cx = start_x + j * cell_size + 7
            cy = start_y + i * cell_size + 8
            color = 65504 if idx == selected else (2016 if val == "X" else 63488)
            if val != "":
                tft.text(f16x16, val, cx, cy, color)
            elif idx == selected:
                tft.text(f16x16, "_", cx, cy, color)
                
tttLevel = 0
tttChar = ""

def play_ttt(level, char):
    import time
    global tft
    ttt = TicTacToe()
    ttt.tmap = [""] * 9 + ["inProgress"]
    selected = 0
    me = char
    
    render(ttt.tmap, selected)
    
    while True:
        if button_b.value() == 0:
            while button_b.value() == 0:
                time.sleep(0.02)
            selected = (selected + 1) % 9
            render(ttt.tmap, selected)
        
        if button_c.value() == 0:
            while button_c.value() == 0:
                time.sleep(0.02)
            break

        if button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(0.02)
            if ttt.tmap[selected] == "" and ttt.tmap[9] == "inProgress":
                ttt.tmap[selected] = me
                ttt.status(ttt.tmap, me)
                render(ttt.tmap, selected)
                
                if ttt.tmap[9] == "inProgress":
                    if level == "medium":
                        ttt.tmap = ttt.aiMedium("O" if me == "X" else "X")
                    else:
                        ttt.tmap = ttt.aiEasy("O" if me == "X" else "X")
                    ttt.status(ttt.tmap, me)
                    render(ttt.tmap, selected)
                    
        if ttt.tmap[9] != "inProgress":
            ttt.status(ttt.tmap, me)
            if ttt.tmap[9] == "Won":
                msg = "You won!"
            elif ttt.tmap[9] == "Lost":
                msg = "You lose!"
            else:
                msg = "Tie!"
            tft.text(f16x16, msg, 0, 0, 65535)
            time.sleep(2)
            break
            
        time.sleep_ms(20)

def run():
    global tttLevel, tttChar
    import modules.menus as menus
    
    if tft is None:
        print("Please call 'set_btf(bta, btb, btc, ttft)' first")
        return
    
    print("Going into main loop")
    work = True
    while work:
        render_choice = menus.menu("TicTacToe", [("Easy AI", 1), ("Medium AI", 2), ("Close", 13)])
        if render_choice == 1:
            tttLevel = 0
        elif render_choice == 2:
            tttLevel = 1
        else:
            break

        char_choice = menus.menu("TicTacToe", [("Play as X", 1), ("Play as O", 2), ("Close", 13)])
        if char_choice == 1:
            tttChar = "X"
        elif char_choice == 2:
            tttChar = "O"
        else:
            break
        
        play_ttt(tttLevel, tttChar)