from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QMenuBar, QMenu, QStatusBar, QFileDialog, QSplitter)
from PySide6.QtCore import Qt
import sys
from Analizador import lexer

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración principal de la ventana
        self.setWindowTitle("Analizador Léxico")
        self.resize(800, 600)
        
        # Menú para Importar y Exportar
        barraDeMenu = QMenuBar()
        menuDeArchivos = QMenu("Archivo", self)
        
        importar = menuDeArchivos.addAction("Importar")
        importar.triggered.connect(self.importarArchivo)
        
        exportar = menuDeArchivos.addAction("Exportar")
        exportar.triggered.connect(self.exportarArchivo)
        
        analizar = barraDeMenu.addAction("Analizar")
        analizar.triggered.connect(self.analizar)
        
        limpiarCampo = barraDeMenu.addAction("Limpiar Campo")
        limpiarCampo.triggered.connect(self.limpiarCampo)
        
        barraDeMenu.addMenu(menuDeArchivos)
        self.setMenuBar(barraDeMenu)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layoutPrincipal = QVBoxLayout(central_widget)

        # Splitter principal para dividir en parte superior e inferior
        splitter_principal = QSplitter(Qt.Vertical)
        layoutPrincipal.addWidget(splitter_principal)

        # Campo de texto grande superior
        self.campoDeTexto = QTextEdit()
        splitter_principal.addWidget(self.campoDeTexto)

        # Splitter secundario para dividir la parte inferior en dos
        splitter_inferior = QSplitter(Qt.Horizontal)
        splitter_principal.addWidget(splitter_inferior)

        # Campo de texto para mostrar tokens correctos
        self.campoCorrectos = QTextEdit()
        self.campoCorrectos.setReadOnly(True)
        splitter_inferior.addWidget(self.campoCorrectos)

        # Campo de texto para mostrar errores
        self.campoErrores = QTextEdit()
        self.campoErrores.setReadOnly(True)
        splitter_inferior.addWidget(self.campoErrores)

        # Barra de estado
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Listo")
        
    def limpiarCampo(self):
        self.campoDeTexto.clear()
        self.campoDeTexto.setReadOnly(False)
        self.campoCorrectos.clear()
        self.campoErrores.clear()
        self.statusBar().showMessage("Listo")
        
    def importarArchivo(self):
        open_file = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivos de texto (*.txt)")
        if open_file[0]:
            with open(open_file[0], "r") as file:
                self.campoDeTexto.setPlainText(file.read())
                self.campoDeTexto.setReadOnly(True)
                
    def exportarArchivo(self):
        save_file = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Archivos de texto (*.txt)")
        if save_file[0]:
            with open(save_file[0], "w") as file:
                file.write(self.campoDeTexto.toPlainText())
                
    def analizar(self):
        texto = self.campoDeTexto.toPlainText()
        tokensOK, tokensERR = lexer(texto)
        correctos = []
        errores = []
        
        for token in tokensOK:
            correctos.append(token)
        for token in tokensERR:
            errores.append(token)
        if len(errores) == 0:
            self.statusBar().showMessage("Análisis completado sin errores")
        else:
            self.statusBar().showMessage("Análisis completado con errores")
                
        self.campoCorrectos.setPlainText("\n".join([str(token) for token in correctos]))
        self.campoErrores.setPlainText("\n".join([str(token) for token in errores]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())