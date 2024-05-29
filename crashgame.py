import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import random
import threading
import time
from PIL import ImageTk, Image  # Import PIL module

class CrashGameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Crash Game")
        self.master.geometry("300x300")
        
        self.balance = 1000
        self.multiplier = 1.0
        self.stopped = False
        self.bet_amount = 0
        
        style = ttk.Style()
        style.configure("TFrame", background="#4CAF50")
        style.configure("TLabel", background="#4CAF50", foreground="black", font=("Helvetica", 14))
        style.configure("TButton", background="#4CAF50", foreground="#2E8B57", font=("Helvetica", 12), relief="flat")
        style.map("TButton", background=[("active", "#388e3c")])
        
        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Load and display background image
        self.background_image = Image.open("background_image.jpg")  # Replace "background_image.jpg" with your image file
        self.background_image = self.background_image.resize((300, 300), Image.LANCZOS)  # Resize image to fit window
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.frame, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.balance_label = ttk.Label(self.frame, text=f"Balance: ${self.balance}")
        self.balance_label.pack(pady=10)
        
        self.multiplier_label = ttk.Label(self.frame, text=f"Multiplier: {self.multiplier}")
        self.multiplier_label.pack(pady=5)
        
        self.bet_label = ttk.Label(self.frame, text="Enter Bet Amount:")
        self.bet_label.pack(pady=5)
        
        self.bet_entry = ttk.Entry(self.frame)
        self.bet_entry.pack(pady=5)
        
        self.play_button = ttk.Button(self.frame, text="Play", command=self.start_timer)
        self.play_button.pack(pady=5)
        
        self.cash_out_button = ttk.Button(self.frame, text="Cash Out", command=self.cash_out)
        self.cash_out_button.pack(pady=5)
        
        self.quit_button = ttk.Button(self.frame, text="Quit", command=master.quit)
        self.quit_button.pack(pady=5)
    
    def start_timer(self):
        bet_amount_str = self.bet_entry.get()
        try:
            bet_amount = int(bet_amount_str)
        except ValueError:
            messagebox.showerror("Invalid Bet Amount", "Please enter a valid integer bet amount.")
            return
        
        if bet_amount <= 0:
            messagebox.showerror("Invalid Bet Amount", "Please enter a bet amount greater than zero.")
            return
        
        if bet_amount > self.balance:
            messagebox.showerror("Insufficient Balance", "You do not have enough balance to place this bet.")
            return
        
        self.stopped = False
        self.bet_amount = bet_amount
        self.multiplier = 1.0
        self.update_multiplier_label()
        
        # Start a new thread for the timer
        threading.Thread(target=self.timer_thread, args=(bet_amount,)).start()
    
    def timer_thread(self, bet_amount):
        stop_multiplier_at = random.uniform(1.5, 3.0)  # Random multiplier to stop at
        time_to_stop = random.uniform(5, 10)  # Random time to stop the game
        start_time = time.time()
        
        while time.time() - start_time < time_to_stop and not self.stopped:
            time.sleep(random.uniform(0.5, 2.0))  # Random time interval for multiplier update
            self.multiplier += random.uniform(0.1, 0.5)  # Random increment between 0.1 and 0.5
            self.update_multiplier_label()

        if not self.stopped:
            self.stopped = True
            if self.multiplier >= stop_multiplier_at:
                self.balance -= bet_amount
                messagebox.showinfo("Loss!", f"You didn't cash out in time. You lost ${bet_amount}.")
            
            self.update_balance_label()
        
        
    
    def update_multiplier_label(self):
        self.master.after(100, lambda: self.multiplier_label.config(text=f"Multiplier: {round(self.multiplier, 2)}"))
    
    def update_balance_label(self):
        self.master.after(100, lambda: self.balance_label.config(text=f"Balance: ${self.balance}"))
    
    def cash_out(self):
        if not self.bet_amount:
            messagebox.showerror("No Bet Placed", "Please, place a bet to cash out.")
            return

        if not self.stopped:
            self.stopped = True
            amount_won = int(self.bet_entry.get()) * self.multiplier
            messagebox.showinfo("Cash Out", f"You successfully cashed out. You won ${amount_won}.")
            self.balance += int(self.bet_entry.get()) * self.multiplier
            self.update_balance_label()
            self.bet_amount = 0
    
def main():
    root = tk.Tk()
    app = CrashGameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
