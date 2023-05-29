import sys
import re
from builtins import print

from PyQt5 import uic
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QTableWidgetItem, QMessageBox
from pulp import LpMaximize, LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, LpBinary

class interfaz(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("simplex.ui", self)
        self.fondo.setStyleSheet("background-color: darkgray;")
        self.setFixedSize(self.size())
        app_icon = QIcon("Imagenes/icon.ico")
        self.setWindowIcon(app_icon)
        self.setWindowTitle("Py Solver")
        self.fun = []
        self.val = []

        self.prob = 0
        self.flag = False
        self.crear()
        self.Tres.itemSelectionChanged.connect(self.actualizar_boton)
        self.vaciar.clicked.connect(self.eliminar_fila)
        self.cv.valueChanged.connect(self.actualizar_campos)
        self.cb.activated.connect(self.actualizar_componente)
        self.ag.clicked.connect(self.agregar_elemento)
        self.gen.clicked.connect(self.resolver)

    def actualizar_campos(self, num):
        if (num == 2):
            self.TGra.setVisible(True)
        else:
            self.TGra.setVisible(False)
        self.crear()

    def crear(self):
        self.fun = []
        self.val = []
        while self.lay.count():
            item = self.lay.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.Ffun.setLayout(self.lay)

        label = QLabel("Funcion :")
        font = QFont("Segoe Print", 11, QFont.Bold)
        label.setFont(font)
        c = 1
        f = 0
        j = self.cv.value()
        for i in range(j):
            if i != j - 1:
                self.fun.append(QLabel("X" + str(i + 1) + " +"))
            else:
                self.fun.append(QLabel("X" + str(i + 1)))
            self.val.append(QLineEdit())
            self.val[i].setFont(font)
            self.fun[i].setFont(font)
            if i == 0:
                self.lay.addWidget(label, 0, 0, 1, 2)
                c = 2
            if (i + 1) % 3 == 0:
                f += 2
                c = 0
            self.lay.addWidget(self.val[i], f, c)
            self.lay.addWidget(self.fun[i], f, c + 1)
            c += 2

    def actualizar_componente(self, index):
        if index >= 2:
            self.valor.setEnabled(False)
            regex = QRegExp("[,x0-9]+", Qt.CaseInsensitive)
            validator = QRegExpValidator(regex)
            self.restri.setValidator(validator)
            self.flag = True
        else:
            self.valor.setEnabled(True)
            regex = QRegExp("[-+x0-9]+", Qt.CaseInsensitive)
            validator = QRegExpValidator(regex)
            self.restri.setValidator(validator)

    def agregar_elemento(self):
        num_filas = self.Tres.rowCount()
        item1 = QTableWidgetItem(self.restri.text() + "")
        item2 = QTableWidgetItem(self.cb.currentText())
        item3 = QTableWidgetItem(self.valor.text())

        if (self.cb.currentText() == ">=" or self.cb.currentText() == "<=") and (
                self.restri.text() != "" and self.valor.text() != "" and "x" in self.restri.text()):
            self.Tres.insertRow(num_filas)
            self.Tres.setItem(num_filas, 0, item1)
            self.Tres.setItem(num_filas, 1, item2)
            self.Tres.setItem(num_filas, 2, item3)
            self.restri.setText("")
            self.valor.setText("")
        elif (
                self.cb.currentText() == "Int" or self.cb.currentText() == "Binario") and self.restri.text() != "" and "x" in self.restri.text():
            self.Tres.insertRow(num_filas)
            self.Tres.setItem(num_filas, 0, item1)
            self.Tres.setItem(num_filas, 1, item2)
            self.Tres.setItem(num_filas, 2, item3)
            self.restri.setText("")
            self.valor.setText("")
            print("a")
        else:
            alerta = QMessageBox()
            alerta.setIcon(QMessageBox.Warning)
            alerta.setWindowTitle("Advertencia")
            alerta.setText("Revisa la restriccion por favor")
            alerta.setStandardButtons(QMessageBox.Ok)
            alerta.exec_()

    def actualizar_boton(self):
        filas_seleccionadas = len(self.Tres.selectedRanges()) > 0
        self.vaciar.setEnabled(filas_seleccionadas)

    def eliminar_fila(self):
        filas_seleccionadas = self.Tres.selectionModel().selectedRows()

        respuesta = QMessageBox.question(self, "Confirmar eliminación",
                                         "¿Estás seguro de eliminar la(s) fila(s) seleccionada(s)?",
                                         QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            for index in reversed(filas_seleccionadas):
                fila = index.row()
                self.Tres.removeRow(fila)

    def resolver(self):
        self.Tsol.setRowCount(0)
        if self.max.isChecked():
            prob = LpProblem("Ejemplo", LpMaximize)
        else:
            prob = LpProblem("Ejemplo", LpMinimize)

        variables = [LpVariable(f'x{i}', lowBound=0) for i in range(self.cv.value())]

        prob += lpSum(float(self.val[i].text() + "0") * variables[i] for i in range(self.cv.value()))

        valorrestr = [LpVariable(f'x{i}', lowBound=0) for i in range(self.Tres.rowCount())]

        coeficientes=0
        varaux=0
        for i in range(self.Tres.rowCount()):
            aux = self.Tres.item(i, 1).text()
            if aux == "Int" or aux == "Binario":
                varaux = (self.Tres.item(i, 0).text()).split(",")
                for j in range(len(varaux)):
                    if (aux == "Int"):
                        variables[int(varaux[j][1]) - 1].cat = LpInteger
                    else:
                        variables[int(varaux[j][1]) - 1].cat = LpBinary
                        variables[int(varaux[j][1]) - 1].upBound = 1

            else:
                match = re.findall(r'(-?\d+)(x\d+)', str(self.Tres.item(i, 0).text()))
                coeficientes = [int(item[0]) for item in match]  # Extraer los coeficientes
                varaux = [int(item[1][1:]) for item in match]  # Extraer las variables
                constraint = LpVariable(f'constraint{i}', lowBound=0)
                print(coeficientes)
                print(varaux)
                print(self.Tres.item(i, 2).text())
                if (aux == "<="):
                    valorrestr[i] = lpSum(
                        float(coeficientes[j]) * variables[int(varaux[j]) - 1] for j in range(len(varaux)))
                    prob += valorrestr[i] <= float(self.Tres.item(i, 2).text())
                else:
                    prob += lpSum(
                        float(coeficientes[j]) * variables[int(varaux[j]) - 1] for j in range(len(varaux))) >= float(
                        self.Tres.item(i, 2).text())

                prob += constraint == lpSum(
                    float(coeficientes[j]) * variables[int(varaux[j]) - 1] for j in range(len(varaux)))

        prob.solve()

        self.SolL.setText("La Solucion Optima es: " + str(prob.objective.value() / 10))
        saux = ""
        for i in range(self.cv.value()):
            saux += " x" + str(i) + " :" + str(variables[i].value())

        for i in range(self.Tres.rowCount()):
            match = re.findall(r'(-?\d+)(x\d+)', str(self.Tres.item(i, 0).text()))
            coeficientes = [int(item[0]) for item in match]  # Extraer los coeficientes
            varaux = [int(item[1][1:]) for item in match]  # Extraer las variables
            item1 = QTableWidgetItem(
                str(lpSum(float(coeficientes[j]) * variables[int(varaux[j]) - 1].value() for j in range(len(varaux)))))
            item2 = QTableWidgetItem(self.Tres.item(i, 1).text())
            item3 = QTableWidgetItem(self.Tres.item(i, 2).text())
            self.Tsol.insertRow(i)
            self.Tsol.setItem(i, 0, item1)
            self.Tsol.setItem(i, 1, item2)
            self.Tsol.setItem(i, 2, item3)

        self.varS.setText(saux)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = interfaz()
    GUI.show()
    sys.exit(app.exec_())
