from tkinter import *
import random
import threading
import time
from part2 import GomokuGame

game = GomokuGame(size=15, starting_player='B')
game_mode = None
stop_ai_thread = False  # control ai

window = Tk()
window.geometry("600x760")
window.config(bg="#b57f59")

buttons = [[None for _ in range(15)] for _ in range(15)]

# ------------------------

def next_turn(row, column):
    global game_mode
    if game_mode != 'human_vs_ai' or game.is_terminal():
        return

    if game.board[row][column] == ' ' and game.current_player == 'B':
        game.make_move(row, column)
        update_gui()
        if not game.is_terminal():
            window.after(100, ai_move)  # gui update before AI move

def ai_move():
    if game.is_terminal():
        return

    if game.current_player == 'B':
        move = game.get_best_minimax(depth=4)
    else:
        move = game.get_best_alpha_beta(depth=4)

    if move is None:
        return  # No move possible

    i, j = move
    game.make_move(i, j)
    update_gui()



def update_gui():  # also check winner
    for i in range(15):
        for j in range(15):
            buttons[i][j]['text'] = game.board[i][j]

    if game_mode != None:
        if game.winner == 'Draw':
            label.config(text="It's a tie!")
        elif game.winner:
            label.config(text=f"Player {game.winner} wins!")
        else:
            label.config(text=f"{game.current_player} turn")

def new_game():
    global stop_ai_thread
    stop_ai_thread = True
    time.sleep(0.2)
    game.reset()
    if game_mode == 'human_vs_ai':
        game.current_player = 'B'

    update_gui()
    board_colors()


def board_colors():
    randomBoard = random.randint(1, 2)

    for row in range(15):
        for col in range(15):
            
            if randomBoard == 1:
                color = "#7c96a7" if (col + row) % 2 == 0 else "#e7ecff"
            else:
                color = "#9e7241" if (col + row) % 2 == 0 else "#f7d3b1"
                
            buttons[row][col].config(text=" ", bg=color)


def hu_vs_AI():
    global game_mode, stop_ai_thread
    stop_ai_thread = True
    game_mode = 'human_vs_ai'
    new_game()

def set_AI_vs_AI():
    global game_mode, stop_ai_thread
    stop_ai_thread = True
    game_mode = 'ai_vs_ai'
    new_game()
    stop_ai_thread = False
    threading.Thread(target=run_AI_vs_AI, daemon=True).start()


def run_AI_vs_AI():
    global stop_ai_thread
    while not game.is_terminal() and not stop_ai_thread:

        if game.current_player == 'B':
            move = game.get_best_minimax(depth=4)
        else:
            move = game.get_best_alpha_beta(depth=4)

        if move is None:
            break  # Avoid unpacking None

        i, j = move
        game.make_move(i, j)
        update_gui()
        time.sleep(0.2)

    update_gui()


# ------------------------

label = Label(text="Choose Mode to Start", font=('consolas', 15), fg='white', bg='#b57f59')
label.pack(pady=3)

frame = Frame(window, bg="#000000")
frame.pack()

for row in range(15):
    for col in range(15):
        color = "#7c96a7" if (col + row) % 2 == 0 else "#e7ecff"
        buttons[row][col] = Button(frame, text="", font=('consolas', 15), bg=color, width=2, height=0,
                                   command=lambda row=row, col=col: next_turn(row, col))
        buttons[row][col].grid(row=row, column=col)

reset_button = Button(text="Restart", font=('consolas', 12), command=new_game,
                      relief='flat', bg='#6d3712', activebackground='#87471b',
                      fg='#ffd4b8', activeforeground='#ffd4b8')
reset_button.pack(pady=3)

human_button = Button(text="Human vs AI", font=('consolas', 12), command=hu_vs_AI,
                      relief='flat', bg='#27455c', activebackground='#385f80',
                      fg='white', activeforeground='white')
human_button.pack(pady=3)

AI_button = Button(text="AI vs AI", font=('consolas', 12), command=set_AI_vs_AI,
                   relief='flat', bg='#5c2e2e', activebackground='#803f3f',
                   fg='white', activeforeground='white')
AI_button.pack(pady=3)

board_colors()
window.mainloop()
