
import tkinter as tk
import time
import random
import sqlite3
from threading import Thread
import pygame
pygame.mixer.init()


class Game:
    def __init__(self, team_name, leaderboard):
        self.team_name = team_name
        self.leaderboard = leaderboard
        self.score = 0
        self.test_data = [random.choice([1, 0]) for _ in range(15)]
        self.hit_sound = pygame.mixer.Sound("hit_sound.wav")
        self.miss_sound = pygame.mixer.Sound("wrong2.wav")
        self.tunnel_sound = pygame.mixer.Sound("mixkit2.wav")
        #pygame.mixer.Sound("start.wav").play()
        startup_sound = pygame.mixer.Sound("start.wav")

        # Play the startup sound effect
        startup_sound.play()
    
    def simulate(self, update_callback, leaderboard_callback):
        for i, data in enumerate(self.test_data):
            time.sleep(1)  # simulate delay between incoming data
            self.update_score(data, update_callback)
            if (i + 1) % 15 == 0:
                self.update_leaderboard(leaderboard_callback)
    
    def update_score(self, data, callback):
        if data == 1:
            self.score += 1
            if random.random() < 0.3:
                self.score += 2
                self.tunnel_sound.play()
                callback(f" TUNNEL!!!!!!   Score:  {self.score}", "purple")
            else:
                self.hit_sound.play()
                callback(f" HIT!!!!!!   Score:   {self.score}", "lightgreen")
        elif data == 0:
            self.miss_sound.play()
            callback(f" MISS!!!   Score:   {self.score}", "pink")

    def update_leaderboard(self, callback):
        self.leaderboard.append((self.team_name.get(), self.score))
        self.leaderboard.sort(key=lambda x: x[1], reverse=True)
        callback(self.leaderboard)


class ScoreboardGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Scoreboard")
        self.master.configure(bg="black")
        
        # Set the window size to full-screen
        self.master.attributes("-fullscreen", True)

        # Set the window size to 768 pixels in height
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_height}x{screen_height}")

        self.team_name = tk.StringVar()
        tk.Label(self.master, text="team name:", font=("OCR A extended", 15), bg="black", fg="white").grid(row=1, column=2, pady=20)
        self.team_entry = tk.Entry(self.master, textvariable=self.team_name)
        self.team_entry.grid(row=1, column=3, pady=20)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_game)
        self.start_button.grid(row=1, column=4, pady=20)

        self.leaderboard_label = tk.Label(self.master, text="", font=("OCR A extended", 36), bg="black", fg="white")
        self.leaderboard_label.grid(row=0, column=0, rowspan=2, padx=50)
        self.leaderboard_label.configure(font=("OCR A extended", 18))
        
        self.score_label = tk.Label(self.master, text="Score: 0", font=("OCR A extended", 36), bg="black", fg="white")
        self.score_label.grid(row=0, column=1, pady=20)
        self.color_label = tk.Label(self.master, bg="white", width=140, height=60)
        self.color_label.grid(row=1, column=1)

    def start_game(self):
        if not self.team_name.get():
            return
        
        self.game = Game(self.team_name, self.load_leaderboard())
        Thread(target=self.game.simulate, args=(self.update_scoreboard, self.update_leaderboard)).start()

    def load_leaderboard(self):
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS leaderboard
                     (team text, score integer)''')
        conn.commit()
        c.execute('SELECT * FROM leaderboard ORDER BY score DESC')
        leaderboard = [((row[0], row[1])) for row in c.fetchall()]
        conn.close()
        return leaderboard
    
    def save_leaderboard(self, leaderboard):
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute('DELETE FROM leaderboard')
        c.executemany('INSERT INTO leaderboard VALUES (?, ?)', leaderboard)
        conn.commit()
        conn.close()

    def update_scoreboard(self, text, color):
        self.score_label.configure(text=text, fg=color)
        self.color_label.configure(bg=color)
        self.master.after(500, lambda: self.score_label.configure(bg="black"))
        self.master.after(500, lambda: self.color_label.configure(bg="white"))

    def update_leaderboard(self, leaderboard):
        leaderboard_text = "\n".join([f"{i+1}. {team} - {score}" for i, (team, score) in enumerate(leaderboard)])
        self.leaderboard_label.configure(text=leaderboard_text)
        self.save_leaderboard(leaderboard)
        
if __name__ == "__main__":
    window = tk.Tk()
    ScoreboardGUI(window)
    window.mainloop()


