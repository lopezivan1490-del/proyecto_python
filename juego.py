import tkinter as tk

def es_par(numero):
    return numero % 2 == 0

def verficar():
    texto = entrada.get()
    if not texto.isdigit():
        resultado.config(text="escribir un munero entero: ")
        return
    n = int(texto)
    if es_par(n):
        resultado.config(texto=str(n) + "es par")
    else:
        resultado.config(texto=str(n) + "es impar")

ventana = tk.Tk()
ventana.title("par o impar")
ventana.geometry("300x180")

tk.Label(ventana, text="escribe un numero")
entrada =tk.Entry(ventana)
entrada.pack()
tk.Button(ventana, text="verificar", command=verficar).pack(pady=8)
resultado =tk.Label(ventana, text="")
ventana.mainloop()