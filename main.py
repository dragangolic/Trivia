import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore


widgets = {
    "logo": [],
    "button": []
}

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Fenix Programmers!")
window.setFixedWidth(1800)
window.move(50, 50)
window.setStyleSheet("background: #00CCFF;")

grid = QGridLayout()

def frame1():
    # display logo
    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 10px;")
    widgets['logo'].append(logo)

    # button widget
    button =QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet("*{border: 4px solid '#990000';" +
                         "border-radius: 45px;" +
                         "font-size: 75px;" +
                         "color: 'white';" +
                         "padding: 25px 0;" +
                         "margin: 70px 170px;}" +
                         "*:hover{background: '#FF99FF';}"
                         )
    widgets['button'].append(button)

    grid.addWidget(widgets['logo'][-1], 0, 0)
    grid.addWidget(widgets['button'][-1], 1, 0)

frame1()

window.setLayout(grid)

window.show()
sys.exit(app.exec())
