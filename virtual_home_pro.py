import tkinter as tk
import speech_recognition as sr
import pyttsx3
import threading
import time
import csv
from datetime import datetime

class SmartHomePro:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Energy Command Center - SIDDUSPACE")
        self.root.geometry("1200x900")
        self.root.configure(bg="#050505")
        self.main_breaker = False
        self.active_phase = "R" 
        self.total_units = 0.0
        self.current_load_w = 0
        self.wattage = {
            "fan": 75, "tube light": 40, "color light": 20, "tv": 150,
            "ac": 1500, "light": 30, "night lamp": 10,
            "refrigerator": 250, "mixer grinder": 500, "heater": 2000
        }

        self.rooms = {
            "hall": {"box": (40, 40, 400, 260), "devices": {
                "fan 1": {"pos": (100, 120), "type": "fan", "state": False},
                "fan 2": {"pos": (180, 120), "type": "fan", "state": False},
                "tube light": {"pos": (260, 120), "type": "tube light", "state": False},
                "color light": {"pos": (340, 120), "type": "color light", "state": False},
                "tv": {"pos": (220, 200), "type": "tv", "state": False}}},
            "bedroom 1": {"box": (420, 40, 680, 260), "devices": {
                "ac": {"pos": (480, 120), "type": "ac", "state": False},
                "fan": {"pos": (550, 120), "type": "fan", "state": False},
                "light": {"pos": (620, 120), "type": "light", "state": False}}},
            "kitchen": {"box": (40, 280, 280, 500), "devices": {
                "refrigerator": {"pos": (100, 380), "type": "refrigerator", "state": True},
                "light": {"pos": (220, 380), "type": "light", "state": False},
                "mixer grinder": {"pos": (160, 450), "type": "mixer grinder", "state": False}}}
        }

        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.setup_ui()
        threading.Thread(target=self.energy_loop, daemon=True).start()

    def setup_ui(self):
        self.ctrl_panel = tk.Frame(self.root, bg="#111", width=250, highlightthickness=1, highlightbackground="#333")
        self.ctrl_panel.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(self.ctrl_panel, text="MASTER CONTROL", fg="#00ffcc", bg="#111", font=("Arial", 12, "bold")).pack(pady=20)
        tk.Label(self.ctrl_panel, text="PHASE SELECTOR", fg="white", bg="#111", font=("Arial", 9)).pack()
        phase_frame = tk.Frame(self.ctrl_panel, bg="#111")
        phase_frame.pack(pady=10)
        self.phase_btns = {}
        for p in ["R", "Y", "B"]:
            btn = tk.Button(phase_frame, text=p, width=4, bg="#222", fg="white", command=lambda x=p: self.set_phase(x))
            btn.pack(side="left", padx=2)
            self.phase_btns[p] = btn
        self.set_phase("R")
        self.breaker_btn = tk.Button(self.ctrl_panel, text="MAIN BREAKER: OFF", bg="#442222", fg="white", 
                                     height=2, width=20, command=self.toggle_breaker)
        self.breaker_btn.pack(pady=30)
        self.main_display = tk.Frame(self.root, bg="#050505")
        self.main_display.pack(side="right", expand=True, fill="both")
        self.meter_frame = tk.Frame(self.main_display, bg="#0a0a0a", height=150, highlightthickness=1, highlightbackground="#00ffcc")
        self.meter_frame.pack(fill="x", padx=20, pady=10)
        
        self.lbl_load = tk.Label(self.meter_frame, text="0 W", font=("Consolas", 30, "bold"), bg="#0a0a0a", fg="#ff3333")
        self.lbl_load.place(x=50, y=40)
        tk.Label(self.meter_frame, text="CURRENT LOAD", bg="#0a0a0a", fg="#666").place(x=50, y=10)

        self.lbl_units = tk.Label(self.meter_frame, text="0.000 kWh", font=("Consolas", 20), bg="#0a0a0a", fg="#00ffcc")
        self.lbl_units.place(x=350, y=45)
        tk.Label(self.meter_frame, text="CONSUMPTION", bg="#0a0a0a", fg="#666").place(x=350, y=10)

        self.lbl_bill = tk.Label(self.meter_frame, text="₹ 0.00", font=("Consolas", 20), bg="#0a0a0a", fg="#ffcc00")
        self.lbl_bill.place(x=650, y=45)
        tk.Label(self.meter_frame, text="TOTAL CHARGES", bg="#0a0a0a", fg="#666").place(x=650, y=10)
        self.canvas = tk.Canvas(self.main_display, width=800, height=550, bg="#0f0f0f", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.draw_floor_plan()
        self.v_btn = tk.Button(self.main_display, text="🎤 START VOICE COMMAND", font=("Arial", 12, "bold"),
                               bg="#00ffcc", fg="#000", height=2, command=self.start_voice_thread)
        self.v_btn.pack(pady=10)

    def set_phase(self, phase):
        self.active_phase = phase
        for p, btn in self.phase_btns.items():
            color = {"R": "#ff3333", "Y": "#ffcc00", "B": "#3333ff"}[p]
            btn.config(bg=color if p == phase else "#222", fg="white" if p == phase else "#666")

    def toggle_breaker(self):
        self.main_breaker = not self.main_breaker
        color = "#00ff00" if self.main_breaker else "#442222"
        text = "MAIN BREAKER: ON" if self.main_breaker else "MAIN BREAKER: OFF"
        self.breaker_btn.config(bg=color, text=text)
        self.draw_floor_plan() 

    def draw_floor_plan(self):
        self.canvas.delete("all")
        for room_name, info in self.rooms.items():
            x1, y1, x2, y2 = info["box"]
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="#333", width=2)
            self.canvas.create_text(x1+20, y1+15, text=room_name.upper(), fill="#555", font=("Arial", 8, "bold"))
            
            for dev_name, dev_info in info["devices"].items():
                ix, iy = dev_info["pos"]
                is_glowing = self.main_breaker and dev_info["state"]
                color = "#00ffcc" if is_glowing else "#1a1a1a"
                glow_size = 15 if is_glowing else 12
                self.canvas.create_oval(ix-glow_size, iy-glow_size, ix+glow_size, iy+glow_size, fill=color, outline="#444")
                self.canvas.create_text(ix, iy+25, text=dev_name.upper(), fill="#888", font=("Arial", 7))

    def energy_loop(self):
        while True:
            load = 0
            if self.main_breaker:
                for room in self.rooms.values():
                    for dev_info in room["devices"].values():
                        if dev_info["state"]:
                            load += self.wattage[dev_info["type"]]
            
            self.current_load_w = load
            self.total_units += (load / 1000) / 3600 
            bill = self.total_units * 2 if self.total_units <= 100 else (200 + (self.total_units-100)*5)

            self.lbl_load.config(text=f"{load} W")
            self.lbl_units.config(text=f"{self.total_units:.4f} kWh")
            self.lbl_bill.config(text=f"₹ {bill:.2f}")
            time.sleep(1)

    def process_command(self, text):
        text = text.lower()
        if not self.main_breaker and "breaker" not in text:
            self.engine.say("Main breaker is off. Please turn on power first.")
            self.engine.runAndWait()
            return

        action = "on" in text or "start" in text
        for room_name, info in self.rooms.items():
            if room_name in text:
                for dev_name, dev_info in info["devices"].items():
                    if dev_name in text or dev_info["type"] in text:
                        dev_info["state"] = action
                        self.draw_floor_plan()
                        self.engine.say(f"{room_name} {dev_name} turned {'on' if action else 'off'}")
                        self.engine.runAndWait()
                        return

    def start_voice_thread(self):
        self.v_btn.config(text="LISTENING...", bg="#ff3333")
        threading.Thread(target=self.listen).start()

    def listen(self):
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                cmd = self.recognizer.recognize_google(audio)
                self.root.after(0, lambda: self.process_command(cmd))
            except: pass
        self.v_btn.config(text="🎤 START VOICE COMMAND", bg="#00ffcc")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomePro(root)
    root.mainloop()