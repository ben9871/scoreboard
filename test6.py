import tkinter as tk
import time
import random
import csv
import os
from threading import Thread

LEADERBOARD_FILE = "leaderboard.csv"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Team", "Score"])
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader) # skip header row
            return [(row[0], int(row[1])) for row in reader]
    except:
        return []


def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "a") as f:
        writer = csv.writer(f)
        for row in leaderboard:
            writer.writerow(row)

def run_scoreboard(window, team_name, leaderboard_label):
    score = 0
    score_label = tk.Label(window, text="Score: 0", font=("TkDefaultFont", 20), bg="black", fg="white")
    score_label.grid(row=0, column=1, pady=20)
    color_label = tk.Label(window, bg="white", width=80, height=40)
    color_label.grid(row=1, column=1)
    leaderboard = load_leaderboard()

    def update_leaderboard():
        leaderboard.append((team_name.get(), score))
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        save_leaderboard(leaderboard)
        leaderboard_text = "\n".join([f"{i+1}. {team} - {score}" for i, (team, score) in enumerate(leaderboard)])
        leaderboard_label.configure(text=leaderboard_text)
        window.update_idletasks()

    def update_scoreboard(data):
        nonlocal score
        if data == 1:
            score += 1
            if random.random() < 0.3:
                score += 2
                score_label.configure(text=f" TUNNEL!!!!!!   Score:  {score}", fg="purple")
                color_label.configure(bg="purple")
            else:
                score_label.configure(text=f" HIT!!!!!!   Score:   {score}", fg="green")
                color_label.configure(bg="lightgreen")

        elif data == 0:
            score_label.configure(text=f" MISS!!!   Score:   {score}", fg="red")
            color_label.configure(bg="pink")

        window.update_idletasks()
        window.after(500, lambda: score_label.configure(bg="black"))
        window.after(500, lambda: color_label.configure(bg="white"))

    test_data = [random.choice([1, 0]) for _ in range(15)]
    for i, data in enumerate(test_data):
        time.sleep(1)  # simulate delay between incoming data
        update_scoreboard(data)
        if (i + 1) % 15 == 0:
            update_leaderboard()
            window.update_idletasks()

    team_name.set('')
    

   # leaderboard_label.grid(row=0, column=0, rowspan=2, padx=50)
    #leaderboard_label.configure(font=("TkDefaultFont", 18))

    #start_button = tk.Button(window, text="Start", command=lambda: start_game(team_name, window))
   # start_button.grid(row=0, column=2, pady=20)

    team_entry = tk.Entry(window, textvariable=team_name)
    team_entry.grid(row=1, column=2, pady=20)

def start_game(team_name, window):
    if not team_name.get():
        return

    

    #leaderboard_label = tk.Label(window, text="", font=("TkDefaultFont", 18), bg="black", fg="white")
    #leaderboard_label.grid(row=0, column=0, rowspan=2, padx=50)
    #leaderboard_label.configure(font=("TkDefaultFont", 18))

    #leaderboard = load_leaderboard()
    #leaderboard_text = "\n".join([f"{i+1}. {team} - {score}" for i, (team, score) in enumerate(leaderboard)])
    #leaderboard_label.configure(text=leaderboard_text)
    window.update_idletasks()

    run_scoreboard(window, team_name, leaderboard_label)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Scoreboard")
    window.configure(bg="black")

    team_name = tk.StringVar()
    tk.Label(window, text="Enter team name:", font=("TkDefaultFont", 18), bg="black", fg="white").grid(row=1, column=2, pady=20)
    team_entry = tk.Entry(window, textvariable=team_name)
    team_entry.grid(row=1, column=3, pady=20)

    start_button = tk.Button(window, text="Start", command=lambda: start_game(team_name, window))
    start_button.grid(row=1, column=4, pady=20)

    leaderboard_label = tk.Label(window, text="", font=("TkDefaultFont", 18), bg="black", fg="white")
    leaderboard_label.grid(row=0, column=0, rowspan=2, padx=50)
    leaderboard_label.configure(font=("TkDefaultFont", 18))

  #  leaderboard = load_leaderboard()
  #  leaderboard_text = "\n".join([f"{i+1}. {team} - {score}" for i, (team, score) in enumerate(leaderboard)])
  #  leaderboard_label.configure(text=leaderboard_text)
    window.update_idletasks()

    window.mainloop()









