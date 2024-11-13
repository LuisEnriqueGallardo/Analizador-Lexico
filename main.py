from PySide6.QtWidgets import QApplication
from Interfaces import VentanaPrincipal
from Analizador import lexer
    

    
if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec_()