import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from mpl_toolkits.mplot3d import Axes3D

# Limites das juntas em graus (conforme especificação)
limites_juntas = [
    (-340, 340),  # J1
    (-235, 235),  # J2
    (-455, 455),  # J3
    (-380, 380),  # J4
    (-360, 360),  # J5
    (-900, 900)   # J6
]

def dh_matrix(theta, d, a, alpha):
    """Matriz de transformação de Denavit-Hartenberg."""
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

def calcular_e_plotar():
    """Calcula as transformações e plota o braço robótico."""
    try:
        thetas = [np.radians(slider.get()) for slider in sliders]

        # Parâmetros DH do robô M-10iD/12
        d = [450, 0, 0, 640, 0, 75]  # Valores em mm
        a = [0, 700, 0, 0, 0, 0]    # Valores em mm
        alpha = [-np.pi/2, 0, -np.pi/2, np.pi/2, -np.pi/2, 0]  # Ângulos em radianos

        T = np.eye(4)
        x_vals, y_vals, z_vals = [0], [0], [0]

        for i in range(num_juntas):
            T = T @ dh_matrix(thetas[i], d[i], a[i], alpha[i])
            x_vals.append(T[0, 3])
            y_vals.append(T[1, 3])
            z_vals.append(T[2, 3])

        ax.cla()
        ax.plot(x_vals, y_vals, z_vals, marker='o', markersize=5, color='blue', label='Pontos do Braço')
       

        ax.set_xlim([-1500, 1500])
        ax.set_ylim([-1500, 1500])
        ax.set_zlim([0, 2000])
        ax.set_title("Braço Robótico 3D")
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.set_zlabel("Z (mm)")
        ax.legend()
        canvas.draw()

    except ValueError as e:
        print(f"Erro: {e}")

def atualizar(event=None):
    """Atualiza a visualização do robô quando o slider é movido."""
    calcular_e_plotar()

# Configuração da interface
root = tk.Tk()
root.title("Simulador de Robô M-10iD/12")

num_juntas = 6
sliders = []

for i in range(num_juntas):
    ttk.Label(root, text=f"Junta {i+1} (Limite: {limites_juntas[i][0]}° a {limites_juntas[i][1]}°):").grid(row=i, column=0)
    slider = tk.Scale(root, from_=limites_juntas[i][0], to=limites_juntas[i][1], orient="horizontal", length=300, command=atualizar)
    slider.grid(row=i, column=1)
    sliders.append(slider)

# Configuração do gráfico
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=num_juntas, column=0, columnspan=2)

# Botão para resetar sliders
ttk.Button(root, text="Resetar", command=lambda: [slider.set(0) for slider in sliders]).grid(row=num_juntas+1, column=0, columnspan=2)

# Inicializa o gráfico
calcular_e_plotar()

root.mainloop()
