import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore


widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": []
}

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Young Programmers!")
window.setFixedWidth(1800)
window.move(50, 0)
window.setStyleSheet("background: #00CCFF;")

grid = QGridLayout()


def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def start_game():
    clear_widgets()
    frame2()

def show_frame1():
    clear_widgets()
    frame1()


def create_buttons(answer, l_margin, r_margin):
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(885)
    button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        "margin_left:" + str(l_margin) +"px;" +
        "margin_right:" + str(r_margin) +"px;" +
        "border-radius: 40px;" +
        "border-family: 'shanty';" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 25px 0;" +
        "margin-top: 20px;}" +
        "*:hover{background: '#FF99FF';}"
    )
    button.clicked.connect(show_frame1)
    return button


def frame1():
    # display logo
    image = QPixmap("logo_top2.png")
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
    button.clicked.connect(start_game)
    widgets['button'].append(button)

    grid.addWidget(widgets['logo'][-1], 0, 0, 1, 2)
    grid.addWidget(widgets['button'][-1], 1, 0, 1, 2)

frame1()


def frame2():
    score = QLabel("80")
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        "font-size: 55px;" +
        "color: 'white';" +
        "padding: 55px 50px ;" +
        "margin: 110px 350px;" +
        "background: '#64A314';" +
        "border: 1px solid '#64A314';" +
        "border-radius: 85px;"
    )

    widgets['score'].append(score)

    question = QLabel("Placeholder text will go here")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 35px;" +
        "color: 'white';" +
        "padding: 15px;"
    )

    widgets['question'].append(question)

    button1 = create_buttons("answer1", 75, 45)
    button2 = create_buttons("answer2", 45, 75)
    button3 = create_buttons("answer3", 75, 45)
    button4 = create_buttons("answer4", 45, 75)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    image = QPixmap("logo_button3.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 1px; margin-bottom: 1px")
    widgets['logo'].append(logo)

    grid.addWidget(widgets['score'][-1], 0, 1)
    grid.addWidget(widgets['question'][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets['logo'][-1], 4, 0, 1, 2)

window.setLayout(grid)

window.show()
sys.exit(app.exec())
