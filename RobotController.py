import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import time

class RobotController:

    def __init__(self, master):

        self.master = master
        self.master.title("Robot Controller")

        

        # Connexion série
        #self.serial_port = serial.Serial('COM8', 115200)  # Remplacez '/dev/ttyUSB0' par le port série approprié sur votre système
        time.sleep(2)  # Attendez que la connexion série soit établie

        # Frame principale pour centraliser les éléments
        main_frame = ttk.Frame(master)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=500, pady=40)

        # Ajouter une image de fond


        # Création des éléments de l'interface utilisateur
        self.speed_label = ttk.Label(main_frame)
        self.speed_label.grid(row=0, column=0, padx=20, pady=20)

        self.speed_scale = ttk.Scale(main_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=400)
        self.speed_scale.grid(row=0, column=1, padx=10, pady=10)

        self.speed_up_button = tk.Button(main_frame, text="Augmenter la vitesse", command=self.speed_up, width=20, bg='lightgreen', font=("Arial", 10, "bold"))
        self.speed_up_button.grid(row=0, column=2, padx=10, pady=10)

        self.speed_down_button = tk.Button(main_frame, text="Diminuer la vitesse", command=self.speed_down, width=20, bg='lightgreen', font=("Arial", 10, "bold"))
        self.speed_down_button.grid(row=0, column=3, padx=10, pady=10)

       

        # Création d'un sous-frame pour les boutons de contrôle
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=4, pady=20)

        # Positionnement des boutons de contrôle au centre
        button_config = {"width": 10, "height": 2}  # Adjust button size here

        # Define padding and colors for buttons
        button_padding = {"padx": 20, "pady": 10}
        button_colors = {
            "Avancer": {"bg": "lightblue"},
            "Gauche": {"bg": "lightblue"},
            "Arrêter": {"bg": "lightcoral"},
            "Droite": {"bg": "lightblue"},
            "Reculer": {"bg": "lightblue"}
        }

        self.forward_button = tk.Button(control_frame, text="⬆ ", command=self.forward, **button_config, **button_colors["Avancer"],font=("Arial", 15, "bold"))
        self.forward_button.grid(row=0, column=1, **button_padding)

        self.left_button = tk.Button(control_frame, text="⬅ ", command=self.turn_left, **button_config, **button_colors["Gauche"],font=("Arial", 15, "bold"))
        self.left_button.grid(row=1, column=0, **button_padding)

        self.stop_button = tk.Button(control_frame, text="⏹ ", command=self.stop_wheels, **button_config, **button_colors["Arrêter"],font=("Arial", 15, "bold"))
        self.stop_button.grid(row=1, column=1, **button_padding)

        self.right_button = tk.Button(control_frame, text="➡", command=self.turn_right, **button_config, **button_colors["Droite"],font=("Arial", 15, "bold"))
        self.right_button.grid(row=1, column=2, **button_padding)

        self.backward_button = tk.Button(control_frame, text="⬇ ", command=self.backward, **button_config, **button_colors["Reculer"],font=("Arial", 15, "bold"))
        self.backward_button.grid(row=2, column=1, **button_padding)


       

        # Création du graphique
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Vitesse")
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.forward_button.grid(row=0, column=1, padx=30, pady=30)
        self.left_button.grid(row=1, column=0, padx=30, pady=30)
        self.stop_button.grid(row=1, column=1, padx=30, pady=30)
        self.right_button.grid(row=1, column=2, padx=30, pady=30)
        self.backward_button.grid(row=2, column=1, padx=30, pady=30)

        style = ttk.Style()
        style.configure("Custom.TFrame", background="blue")  # Définir le style avec un fond blanc

        main_frame = ttk.Frame(master, style="Custom.TFrame") 

        # Données pour le graphique
        self.time = [0]
        self.speed_data = [0]

    def update_graph(self):
        self.ax.clear()
        self.ax.plot(self.time, self.speed_data, marker='o', linestyle='-')
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Vitesse")
        self.canvas.draw()

    def forward(self):
        speed = self.speed_scale.get()
        if(speed==0):
            return False
        print(f"Avancer à la vitesse {speed}")
        self.time.append(self.time[-1] + 1)
        self.speed_data.append(speed)
        self.update_graph()
        self.send_serial_command(f"Z")  # Envoyer la commande série

    def backward(self):
        speed = self.speed_scale.get()
        if(speed==0):
            return False
        print(f"Reculer à la vitesse {speed}")
        self.time.append(self.time[-1] + 1)
        self.speed_data.append(speed)
        self.update_graph()
        self.send_serial_command(f"S")  # Envoyer la commande série

    def turn_left(self):
        print("Tourner à gauche")
        self.send_serial_command("Q")  # Envoyer la commande série

    def turn_right(self):
        print("Tourner à droite")
        self.send_serial_command("D")  # Envoyer la commande série

    def speed_up(self):
        current_speed = self.speed_scale.get()
        if current_speed < 100:
            self.speed_scale.set(current_speed + 10)
            self.forward()

    def speed_down(self):
        current_speed = self.speed_scale.get()
        if current_speed > 0:
            self.speed_scale.set(current_speed - 10)
            self.backward()

    def stop_wheels(self):
        print("Arrêter les roues")
        self.send_serial_command("A")  # Envoyer la commande série pour arrêter les roues

    def send_serial_command(self, command):
         self.serial_port.write(command.encode())  # Envoyer la commande encodée en bytes

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = RobotController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
