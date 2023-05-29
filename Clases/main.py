import tkinter as tk
from tkinter import font
from tkinter import ttk
from pulp import *


class ventanaconfi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metodo Simplex")
        self.geometry("400x400")
        self.resizable(0, 0)
        self.iconbitmap("Imagenes/icon.ico")
        self.configurar_interfaz()

    def configurar_interfaz(self):
        l1 = tk.Label(self, text="PYSimplex", font=font.Font(family="Arial", size=25))
        l2 = tk.Label(self, text="¿Cuantas variables de decision hay?")
        l3 = tk.Label(self, text="¿Cuantas restricciones hay?")
        t1 = tk.Entry(self)
        t2 = tk.Entry(self)
        b1 = tk.Button(self, text="Continuar")

        def on_keypress(evento):
            if not evento.char.isdigit() and evento.keycode == 127:
                return "break"

        def on_button_click(evento: object):
            if t1.get() != "" and t2.get() != "":
                cv = int(t1.get())
                cr = int(t2.get())
                v.destroy()
                v2 = ventana2(cv, cr)
                v2.mainloop()

        t1.bind('<KeyPress>', on_keypress)
        t2.bind('<KeyPress>', on_keypress)
        b1.bind('<Button-1>', on_button_click)

        l1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        l2.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        l3.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        t1.grid(row=1, column=1, padx=10, pady=10)
        t2.grid(row=2, column=1, padx=10, pady=10)
        b1.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)


class ventana2(tk.Tk):
    def __init__(self, cv, cr):
        super().__init__()
        self.title("Metodo Simplex")
        self.cv = cv
        self.cr = cr
        self.geometry("650x700")
        self.resizable(0, 0)
        self.iconbitmap("Imagenes/icon.ico")
        self.configurar_interfaz()

    def configurar_interfaz(self):

        frame = tk.Frame(self)

        l1 = tk.Label(frame, text="PYSimplex", font=font.Font(family="Arial", size=15))
        l2 = tk.Label(frame, text="¿Cual es el objetivo de la funcion?")
        cb = ttk.Combobox(frame, values=["Maximizar", "Minimizar"], state="readonly")

        l1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        l2.grid(row=1, column=0, padx=10, pady=10)
        cb.grid(row=1, column=1, padx=10, pady=10)
        cb.set("Maximizar")

        frame.pack()

        container1 = tk.Frame(self, height=140)

        # Crear un Canvas dentro del contenedor
        canvas1 = tk.Canvas(container1, height=150)
        if (self.cv <= 4):
            canvas1.config(width=self.cv * 150)
            canvas1.pack(side="left", expand=True)
        else:
            canvas1.pack(side="left", fill="both", expand=True)

        # Agregar Scrollbar al contenedor y vincularlo con el Canvas
        scrollbar1 = ttk.Scrollbar(container1, orient="vertical", command=canvas1.yview)
        scrollbar1.pack(side="right", fill="y")

        frame2 = tk.Frame(canvas1)

        l3 = tk.Label(frame2, text="Funcion :", font=font.Font(family="Arial", size=13))
        l3.grid(row=0, column=0, padx=10, pady=10)

        matrizL = []
        matrizT = []
        ArregloC = []
        restric = []

        container = tk.Frame(self, height=240)

        # Crear un Canvas dentro del contenedor
        canvas = tk.Canvas(container, height=260)
        canvas.pack(side="left", fill="both", expand=True)

        # Agregar Scrollbar al contenedor y vincularlo con el Canvas
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        frame3 = tk.Frame(canvas)

        # combos
        for i in range(self.cr):
            ArregloC.append(ttk.Combobox(frame3, values=["≤", "≥", "="], state="readonly", width=10))
            ArregloC[i].set("≤")

        # restriccion
        for i in range(self.cr):
            restric.append(tk.Entry(frame3, width=8))
        # labels
        for i in range(self.cr + 1):
            labels = []
            if i == 0:
                for j in range(self.cv):
                    if j == self.cv - 1:
                        label = tk.Label(frame2, text="X" + str(j + 1) + "")
                    else:
                        label = tk.Label(frame2, text="X" + str(j + 1) + " +")
                    labels.append(label)
            else:
                for j in range(self.cv):
                    if j == self.cv - 1:
                        label = tk.Label(frame3, text="X" + str(j + 1) + "")
                    else:
                        label = tk.Label(frame3, text="X" + str(j + 1) + " +")
                    labels.append(label)
            matrizL.append(labels)
        # entrys
        for i in range(self.cr + 1):
            entry = []
            if i == 0:
                for j in range(self.cv):
                    en = tk.Entry(frame2, width=7)
                    entry.append(en)
            else:
                for j in range(self.cv):
                    en = tk.Entry(frame3, width=7)
                    entry.append(en)
            matrizT.append(entry)

        aux1 = 1
        for i in range(self.cr + 1):
            aux = 1
            for j in range(self.cv):
                if i == 0:
                    if j == 0:
                        aux = 1
                    elif j % 4 == 0:
                        aux = 0
                        aux1 += 1
                    matrizT[i][j].grid(row=(aux1 - 1) + i, column=aux, padx=10, pady=10)
                    matrizL[i][j].grid(row=(aux1 - 1) + i, column=aux + 1, padx=10, pady=10)
                else:
                    if j % 5 == 0:
                        aux1 += 1
                        aux = 1
                    matrizT[i][j].grid(row=(aux1 - 1) + i, column=aux, padx=10, pady=10)
                    matrizL[i][j].grid(row=(aux1 - 1) + i, column=aux + 1, padx=10, pady=10)
                    if j == self.cv - 1:
                        ArregloC[i - 1].grid(row=(aux1 - 1) + i, column=aux + 2, padx=10, pady=10)
                        restric[i - 1].grid(row=(aux1 - 1) + i, column=aux + 3, padx=10, pady=10)
                aux += 2

        container1.pack(fill="both")
        canvas1.create_window((0, 0), window=frame2, anchor="n")
        frame2.update_idletasks()
        canvas1.configure(scrollregion=canvas1.bbox("all"))

        l4 = tk.Label(self, text="Restricciones", font=font.Font(family="Arial", size=13))
        l4.pack()
        container.pack(fill="both")
        canvas.create_window((0, 0), window=frame3, anchor="n")
        frame3.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        frame4 = tk.Frame(self)

        b = tk.Button(frame4, text="Solucionar :D")
        b.grid(row=0, column=0, padx=10, pady=10)
        b1 = tk.Button(frame, text="Volver")
        b1.grid(row=0, column=1, padx=10, pady=10)

        frame4.pack()

        b2 = tk.Button(self, text="Grafica")
        b2.pack()

        def on_button_click(evento: object):
            prob = None

            if cb.get() == "Maximizar":
                prob = LpProblem("PySimplex", LpMaximize)
            else:
                prob = LpProblem("PySimplex", LpMinimize)

            variables = [LpVariable(f'x{i}', lowBound=0) for i in range(self.cv)]

            prob += lpSum(float(matrizT[0][i].get()) * variables[i] for i in range(self.cv))

            for i in range(self.cr):
                constraint = LpVariable(f'constraint{i}', lowBound=0)
                if ArregloC[i].get() == "≤":
                    prob += lpSum(float(matrizT[i + 1][j].get()) * variables[j] for j in range(self.cv)) <= int(
                        [i].get())
                    prob += constraint == lpSum(float(matrizT[i][j].get()) * variables[j] for j in range(self.cv))
                elif ArregloC[i].get() == "≥":
                    prob += lpSum(float(matrizT[i + 1][j].get()) * variables[j] for j in range(self.cv)) >= int(
                        restric[i].get())
                    prob += constraint == lpSum(float(matrizT[i][j].get()) * variables[j] for j in range(self.cv))

            prob.solve()

            for i in range(self.cv):
                print(value(variables[i]))

            l5 = tk.Label(self, text="La solucion optima es: " + str(prob.objective.value()),
                          font=font.Font(family="Arial", size=20))
            l5.pack()
            for i in range(self.cv):
                laux = tk.Label(self, text="X" + str(i) + " :" + str(variables[i].value()),
                                font=font.Font(family="Arial", size=15))
                laux.pack()

        def clic(evento):
            self.destroy()
            v = ventanaconfi()
            v.mainloop()

        b.bind('<Button-1>', on_button_click)
        b1.bind('<Button-1>', clic)


if __name__ == "__main__":
    v = ventanaconfi()
    v.mainloop()
