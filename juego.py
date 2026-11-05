import tkinter as tk
import random
import unicodedata

# Palabras secretas y sus pistas (categorías)
PALABRAS = [
    ("PERRO", "Animal"), ("GATOS", "Animal"), ("TIGRE", "Animal"),
    ("CEBRA", "Animal"), ("PIZZA", "Comida"), ("MANGO", "Comida"),
    ("ARROZ", "Comida"), ("PASTA", "Comida"), ("ROBOT", "Tecnologia"), ("MOUSE", "Tecnologia"),
    ("PIXEL", "Tecnologia"), ("VIDEO", "Tecnologia"),("TENIS", "Deporte"), ("RUGBY", "Deporte"),
    ("BOXEO", "Deporte"), ("ESQUI", "Deporte"), ("ARBOL", "Naturaleza"), ("SELVA", "Naturaleza"),("PASTO", "Naturaleza"),
    ("ROSAS","Naturaleza"),("PLAYA", "Lugar"), ("CAMPO", "Lugar"), ("TORRE", "Lugar"), ("CALLE", "Lugar"),
    ("CHINA", "Pais"), ("JAPON","Pais"),("CHILE", "Pais"), ("INDIA", "Pais")
]

FONDO = "#101827"
PANEL = "#1d2a3d"
TEXTO = "#ffffff"
VERDE = "#467e36"
AMARILLO = "#e6f701"
GRIS = "#526074"


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn").upper().strip()


class Wordleen:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("ADIVINA LA PALABRA")
        ventana.geometry("470x650")
        ventana.resizable(False, False)
        ventana.configure(bg=FONDO)

        tk.Label(ventana, text="ADIVINA LA PALABRA", font=("Arial", 30, "bold"),
                 bg=FONDO, fg=VERDE).pack(pady=(20, 5))
        tk.Label(ventana, text="¡Adivina la palabra secreta!",
                 font=("Arial", 12), bg=FONDO, fg=TEXTO).pack(pady=3)

        self.pista = tk.Label(ventana, text="", font=("Arial", 13, "bold"),
                              bg=FONDO, fg=AMARILLO)
        self.pista.pack(pady=12)

        self.tablero = tk.Frame(ventana, bg=FONDO)
        self.tablero.pack(pady=8)
        self.celdas = []
        for fila in range(6):
            fila_celdas = []
            for columna in range(5):
                celda = tk.Label(self.tablero, text="", width=3, height=1,
                                 font=("Arial", 19, "bold"), bg=PANEL, fg=TEXTO,
                                 relief="solid", bd=1)
                celda.grid(row=fila, column=columna, padx=4, pady=4, ipadx=4, ipady=7)
                fila_celdas.append(celda)
            self.celdas.append(fila_celdas)

        marco = tk.Frame(ventana, bg=FONDO)
        marco.pack(pady=15)
        self.entrada = tk.Entry(marco, font=("Arial", 15), width=12, justify="center",
                                bg=PANEL, fg=TEXTO, insertbackground=TEXTO)
        self.entrada.pack(side="left", padx=5, ipady=7)
        self.entrada.bind("<Return>", lambda evento: self.comprobar())

        self.boton_probar = tk.Button(marco, text="Probar", command=self.comprobar,
                                      font=("Arial", 11, "bold"), bg=VERDE, fg="white",
                                      relief="flat", cursor="hand2", padx=12, pady=8)
        self.boton_probar.pack(side="left", padx=5)

        self.mensaje = tk.Label(ventana, text="Escribe una palabra de 5 letras.",
                                font=("Arial", 10), bg=FONDO, fg=TEXTO, wraplength=420)
        self.mensaje.pack(pady=5)
        tk.Label(ventana, text="Verde: correcta | Amarillo: otra posición | Gris: no está",
                 font=("Arial", 9), bg=FONDO, fg="#b8c4d6", wraplength=420).pack(pady=8)

        tk.Button(ventana, text="Nueva partida", command=self.nueva_partida,
                  font=("Arial", 11, "bold"), bg=PANEL, fg=TEXTO, relief="flat",
                  cursor="hand2", padx=14, pady=8).pack(pady=10)
        self.nueva_partida()

    def nueva_partida(self):
        self.palabra, categoria = random.choice(PALABRAS)
        self.intentos = 0
        self.terminado = False
        self.pista.config(text=f"Pista: categoría {categoria}")
        self.mensaje.config(text="Escribe una palabra de 5 letras.", fg=TEXTO)
        self.entrada.config(state="normal")
        self.boton_probar.config(state="normal")
        self.entrada.delete(0, tk.END)
        for fila in self.celdas:
            for celda in fila:
                celda.config(text="", bg=PANEL, fg=TEXTO)
        self.entrada.focus_set()

    def comprobar(self):
        if self.terminado:
            return
        intento = normalizar(self.entrada.get())
        if len(intento) != 5 or not intento.isalpha():
            self.mensaje.config(text="Escribe una palabra de exactamente 5 letras.",
                                fg="#ffb4a9")
            return

        fila = self.intentos
        for i, letra in enumerate(intento):
            self.celdas[fila][i].config(text=letra)

        estados = ["gris"] * 5
        disponibles = list(self.palabra)
        for i, letra in enumerate(intento):
            if letra == self.palabra[i]:
                estados[i] = "verde"
                disponibles[i] = None
        for i, letra in enumerate(intento):
            if estados[i] == "verde":
                continue
            if letra in disponibles:
                estados[i] = "amarillo"
                disponibles[disponibles.index(letra)] = None

        for i, estado in enumerate(estados):
            color = VERDE if estado == "verde" else AMARILLO if estado == "amarillo" else GRIS
            self.celdas[fila][i].config(bg=color, fg="white")

        self.intentos += 1
        self.entrada.delete(0, tk.END)
        if intento == self.palabra:
            self.finalizar(f"¡Ganaste! Adivinaste en {self.intentos} intento(s).", VERDE)
        elif self.intentos == 6:
            self.finalizar(f"Se acabaron los intentos. La palabra era {self.palabra}.",
                           "#ffb4a9")
        else:
            self.mensaje.config(text=f"No es esa. Te quedan {6 - self.intentos} intentos.",
                                fg=TEXTO)

    def finalizar(self, texto, color):
        self.terminado = True
        self.mensaje.config(text=texto, fg=color)
        self.entrada.config(state="disabled")
        self.boton_probar.config(state="disabled")


if __name__ == "__main__":
    ventana = tk.Tk()
    juego = Wordleen(ventana)
    ventana.mainloop()
