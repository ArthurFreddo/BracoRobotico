import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.patches import Circle

def dh_matrix(theta, d=1, a=1, alpha=0):
    """Matriz de transformação de Denavit-Hartenberg."""
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

def calcular_e_plotar():
    """Calcula as transformações e plota o braço robótico."""
    try:
        thetas = [np.radians(float(entry.get())) for entry in entries_theta if entry.get() != '']
        if len(thetas) != num_juntas:
            raise ValueError("Preencha todos os campos.")

        T = np.eye(4)  # Matriz identidade inicial
        x_vals, y_vals = [0], [0]

        for theta in thetas:
            T = T @ dh_matrix(theta)
            x_vals.append(T[0, 3])
            y_vals.append(T[1, 3])

        ax.cla()
        ax.plot(x_vals, y_vals, marker='o', markersize=5, color='blue', label='Pontos do Braço')
        ax.quiver(x_vals[:-1], y_vals[:-1], np.diff(x_vals), np.diff(y_vals), angles='xy', scale_units='xy', scale=1, color='red', label='Eixos')
        
        # Adiciona a garra no ponto final
        garra = Circle((x_vals[-1], y_vals[-1]), 0.1, color='black', label='Garra')
        ax.add_patch(garra)

        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_title("Braço Robótico 2D")
        ax.legend()
        canvas.draw()

        # Exibe as matrizes de transformação
        text_results.delete(1.0, tk.END)
        for i, theta in enumerate(thetas):
            T = dh_matrix(theta) if i == 0 else T @ dh_matrix(theta)
            text_results.insert(tk.END, f"Transformação {i+1}:\n{T}\n\n")
        
        # Adiciona mensagens explicativas
        mostrar_mensagens()

    except ValueError as e:
        messagebox.showerror("Erro de Entrada", str(e))

def mostrar_mensagens():
    """Mostra mensagens explicativas na interface."""
    # Adiciona uma mensagem explicativa sobre o gráfico
    messagebox.showinfo("Gráfico do Braço Robótico", 
        "Esse gráfico mostra a oq seria a config do braço robótico.\n"
        "Pontos azuis representam as juntas e a linha vermelha mostra os eixos.")
    
    # Adiciona uma mensagem sobre as matrizes de transformação
    messagebox.showinfo("Matrizes de Transformação", 
        "As matrizes de transformação exibidas abaixo representam\n"
        "as posições e rotações de cada junta em relação à anterior.")

# Configuração da interface
root = tk.Tk()
root.title("Denavit-Hartenberg - Braço Robótico")

num_juntas = 3
entries_theta = [ttk.Entry(root) for _ in range(num_juntas)]

for i, entry in enumerate(entries_theta):
    ttk.Label(root, text=f"θ (graus) para o Eixo {i+1}:").grid(row=i, column=0)
    entry.grid(row=i, column=1)

ttk.Button(root, text="Calcular e Plotar", command=calcular_e_plotar).grid(row=num_juntas, column=0, columnspan=2)

# Configuração do gráfico
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=num_juntas+1, column=0, columnspan=2)

# Exibição das matrizes
text_results = tk.Text(root, height=10, width=50)
text_results.grid(row=num_juntas+2, column=0, columnspan=2)

root.mainloop()
