import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore
from urllib.request import urlopen
import json
import pandas as pd
import random

# Initialize GUI application
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Young Programmers!")
window.setFixedWidth(1800)
window.move(50, 0)
window.setStyleSheet("background: #00CCFF;")

grid = QGridLayout()

# Open api link to database
with urlopen("https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple") as webpage:
    # read JSON file & extract data
    data = json.loads(webpage.read().decode())
    df = pd.DataFrame(data["results"])


# load 1 instance of questions & answers at a time from the database
def preload_data(idx):
    # idx parm: selected randomly time and again at function call
    question = df["question"][idx]
    correct = df["correct_answer"][idx]
    wrong = df["incorrect_answers"][idx]

    # fixing characters with bad formatting
    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
    ]

    # replace bad characters in strings
    for tup in formatting:
        question = question.replace(tup[0], tup[1])
        correct = correct.replace(tup[0], tup[1])
    # replace bad characters in lists
    for tup in formatting:
        wrong = [char.replace(tup[0], tup[1]) for char in wrong]

    # store local values globally
    parameters["question"].append(question)
    parameters["correct"].append(correct)

    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])

    # print correct answer to the terminal (for testing)
    print(parameters["correct"][-1])


# dictionary to store local pre-load parameters on a global level
parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [],
    "index": []
}

widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": []
}


def clear_widgets():
    for widget in widgets:
        if widgets[widget]:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def clear_parameters():
    # clear the global dictionary of parameters
    for parm in parameters:
        if parameters[parm]:
            for i in range(0, len(parameters[parm])):
                parameters[parm].pop()
    # populate with initial index & score values
    parameters["index"].append(random.randint(0, 49))
    parameters["score"].append(0)


def start_game():
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    # display the game frame
    frame2()


def create_buttons(answer, l_margin, r_margin):
    # create identical buttons with custom left and right margins
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(885)
    button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        "margin_left:" + str(l_margin) + "px;" +
        "margin_right:" + str(r_margin) + "px;" +
        "border-radius: 40px;" +
        "border-family: 'shanty';" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 25px 0;" +
        "margin-top: 20px;}" +
        "*:hover{background: '#FF99FF';}"
    )
    button.clicked.connect(lambda x: is_correct(button))
    return button


def is_correct(btn):
    # a function to evaluate weather user answer is correct
    if btn.text() == parameters["correct"][-1]:
        # CORRECT ANSWER
        # update score (+10 points)
        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)

        # select a new random index and replace the old one
        parameters["index"].pop()
        parameters["index"].append(random.randint(0, 49))
        # preload data for new index value
        preload_data(parameters["index"][-1])

        # update the text of all widgets with new data
        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["question"][0].setText(parameters["question"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])

        if parameters["score"][-1] == 100:
            # WON THE GAME
            clear_widgets()
            frame3()
    else:
        # WRONG ANSWER - LOST GAME
        clear_widgets()
        frame4()


def frame1():
    clear_widgets()
    # display logo
    image = QPixmap("logo_top.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 10px;")
    widgets['logo'].append(logo)

    # button widget
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet("*{border: 4px solid '#990000';" +
                         "border-radius: 45px;" +
                         "font-size: 75px;" +
                         "color: 'white';" +
                         "padding: 25px 0;" +
                         "margin: 70px 170px;}" +
                         "*:hover{background: '#FF99FF';}"
                         )
    # button callback
    button.clicked.connect(start_game)
    widgets['button'].append(button)

    # place global widgets on the grid
    grid.addWidget(widgets['logo'][-1], 0, 0, 1, 2)
    grid.addWidget(widgets['button'][-1], 1, 0, 1, 2)


frame1()


def frame2():
    # Score widget
    score = QLabel("00")
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

    widgets["score"].append(score)

    # Question widget
    preload_data(parameters["index"][-1])

    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 35px;" +
        "color: 'white';" +
        "padding: 15px;"
    )

    widgets["question"].append(question)

    # Answer button widgets
    button1 = create_buttons(parameters["answer1"][-1], 75, 45)
    button2 = create_buttons(parameters["answer2"][-1], 45, 75)
    button3 = create_buttons(parameters["answer3"][-1], 75, 45)
    button4 = create_buttons(parameters["answer4"][-1], 45, 75)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    # Logo widget
    image = QPixmap("logo_bottom.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 1px; margin-bottom: 1px")
    widgets['logo'].append(logo)

    # Place widget on the grid
    grid.addWidget(widgets['score'][-1], 0, 1)
    grid.addWidget(widgets['question'][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets['logo'][-1], 4, 0, 1, 2)


def frame3():
    # Congratulation widget
    message = QLabel("Congrats! Your score is:\n ")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet("font-family: 'Shanti';" +
                          "font-size: 25px;" +
                          "color: 'white';" +
                          "margin: 100px 0px;"
                          )

    widgets["message"].append(message)

    # Score widget
    score = QLabel("100")
    score.setStyleSheet("font-size: 100px;" +
                        "color: #8FC740;" +
                        "margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    # Go back widget
    message2 = QLabel("Go back to work!")
    meassage2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet("font-family: 'Shanti';" +
                           "font-size: 30;" +
                           "color: 'white'" +
                           "margin-top: 0px;" +
                           "margin-bottom: 75px;")
    widgets["message2"].append(message2)

    # Button widget
    button = QPushButton('Try again')
    button.setStyleSheet(
        "*background: '#BC006C';" +
        "padding: 25px 0px;" +
        "border: 1px solid '#BC006C';" +
        "color: 'white';" +
        "font - family: 'Arial';" +
        "font-size: 25px;" +
        "border-radius: 40px;" +
        "margin: 10px 300px;" +
        "*:hover{background: '#ff1b9e';}"
    )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    widgets["button"].append(button)

    # Logo widget
    image = QPixmap("logo_bottom.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 1px; margin-bottom: 1px")
    widgets["logo"].append(logo)

    # Place widget on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 1, 2)


def frame4():
    # sorry widget
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
    )
    widgets["message"].append(message)

    # score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    # button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#BC006C';
            color: 'white';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#ff1b9e';
        }'''
    )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    # logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    # place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)


window.setLayout(grid)

window.show()
sys.exit(app.exec())
