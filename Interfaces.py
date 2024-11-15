from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QTextEdit, QMenuBar, QMenu, QStatusBar, QFileDialog, QSplitter)
from PySide6.QtCore import Qt
import sys
from Analizador import lexer
from sintaxis import Parser


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
        
        editarTexto = menuDeArchivos.addAction("Editar Texto")
        editarTexto.setCheckable(True)
        editarTexto.triggered.connect(self.editarTexto)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layoutPrincipal = QGridLayout(central_widget)

        # Splitter principal para dividir en parte superior e inferior
        splitter_principal = QSplitter(Qt.Horizontal)
        
        splitter_inferior = QSplitter(Qt.Horizontal)
        splitter_superior = QSplitter(Qt.Vertical)

        # Campo de texto para analisis
        self.campoDeTexto = QTextEdit()
        self.campoDeTexto.setPlaceholderText("Escriba su código aquí")

        # Campo de analisis Sintactico
        self.campoDeTextoDerecha = QTextEdit()
        self.campoDeTextoDerecha.setReadOnly(True)
        self.campoDeTextoDerecha.setPlaceholderText("Resultado del análisis")

        # Campo de texto para mostrar tokens correctos
        self.campoCorrectos = QTextEdit()
        self.campoCorrectos.setPlaceholderText("Tokens correctos")
        self.campoCorrectos.setReadOnly(True)

        # Campo de texto para mostrar errores
        self.campoErrores = QTextEdit()
        self.campoErrores.setPlaceholderText("Errores")
        self.campoErrores.setReadOnly(True)

        # Barra de estado
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Listo")
        
        layoutPrincipal.addWidget(splitter_principal, 0, 0)
        splitter_principal.addWidget(splitter_superior)
        splitter_superior.addWidget(self.campoDeTexto)
        splitter_superior.addWidget(splitter_inferior)
        splitter_inferior.addWidget(self.campoCorrectos)
        splitter_inferior.addWidget(self.campoErrores)
        splitter_principal.addWidget(self.campoDeTextoDerecha)
        
        self.campoCorrectos.setStyleSheet("background-color: #b5da9e")
        self.campoErrores.setStyleSheet("background-color: #f6989d")        
        
    def editarTexto(self):
        if self.campoDeTexto.isReadOnly():
            self.campoDeTexto.setReadOnly(False)
            self.campoDeTexto.setStyleSheet("QTextEdit[readOnly=\"false\"] { background-color: white; }")
        else:
            self.campoDeTexto.setReadOnly(True)
            self.campoDeTexto.setStyleSheet("QTextEdit[readOnly=\"true\"] { background-color: lightgray; }")
        
                 
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
        tokensOK, tokensERR, tokensLimpios, _ = lexer(texto)
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
        if len(errores) == 0:
            self.analizarSintax(tokensLimpios)
        
    def analizarSintax(self, tokens):
        parser = Parser(tokens)
        try:
            resultado = parser.programa()
            self.campoDeTextoDerecha.setPlainText(str(resultado))
            print(f"EL TEXTO ES{parser.statements}")
        except SyntaxError as e:
            self.campoDeTextoDerecha.setPlainText(str(e))
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())