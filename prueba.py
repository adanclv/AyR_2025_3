import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Árbol de caminos")
        self.resize(1000, 600)
        self.show()

        # Definir el árbol como lista de niveles
        # Cada nivel es una lista de nodos (solo para posicionamiento)
        self.niveles = [
            [0],        # Nivel 0: nodo central
            [0, 1],     # Nivel 1: dos nodos
            [0],
            [0, 1, 2, 3, 4],  # Nivel 3: cinco nodos
            [0],
            [0, 1],     # Nivel 5: dos nodos
            [0],         # Nivel 6: nodo central
            [0, 1],  # Nivel 5: dos nodos
            [0],  # Nivel 6: nodo central
            [0, 1],  # Nivel 5: dos nodos
            [0],  # Nivel 6: nodo central
            [0, 1],  # Nivel 5: dos nodos
            [0],  # Nivel 6: nodo central
        ]

        # Conexiones: lista de tuplas (nivel_actual, indice_nodo_actual, nivel_siguiente, indice_nodo_siguiente)
        self.conexiones = [
            (0,0,1,0),(0,0,1,1),
            (1,0,2,0),(1,1,2,0),
            (2,0,3,0),(2,0,3,1), (2,0,3,2), (2,0,3,3), (2,0,3,4),
            (3,0, 4, 0), (3, 1, 4, 0), (3, 2, 4, 0), (3, 3, 4, 0), (3, 4, 4, 0),
            (4,0,5,0), (4,0,5,1),
            (5,0,6,0), (5,1,6,0)
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont('Arial', 12))

        # Calcular posiciones de nodos
        self.posiciones = []
        ancho = self.width()
        alto_total = self.height()
        niveles_totales = len(self.niveles)
        for nivel_index, nivel in enumerate(self.niveles):
            x = 20 + nivel_index * (ancho // (niveles_totales+1))
            n_nodos = len(nivel)
            fila = []
            for i, _ in enumerate(nivel):
                y = (i+1) * (alto_total // (n_nodos+1))
                fila.append((x, y))
            self.posiciones.append(fila)

        # Dibujar conexiones
        painter.setPen(QColor(150, 0, 0))
        for con in self.conexiones:
            n1, i1, n2, i2 = con
            x1, y1 = self.posiciones[n1][i1]
            x2, y2 = self.posiciones[n2][i2]
            painter.drawLine(x1, y1, x2, y2)

        # Dibujar nodos
        for nivel in self.posiciones:
            for x, y in nivel:
                painter.setBrush(QColor(100,200,250))
                painter.drawEllipse(x-20, y-20, 40, 40)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec_())
