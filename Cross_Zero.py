import sys
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QButtonGroup
from PyQt5.QtWidgets import QInputDialog


class MyWidget(QMainWindow):
    def __init__(self):
        self.board = [[0] * 7] * 7
        self.player = 1
        super().__init__()
        self.mode, okBtnPressed = QInputDialog.getItem(
            self,
            "Количество игроков",
            "Выберите режим игры",
            ("Один игрок", "Два игрока"),
            0,
            False
        )
        uic.loadUi('cross_zero.ui', self)
        self.buttons.buttonClicked.connect(self.run)

    def run(self):
        btn = self.sender().text()[-2:]
        self.statusBar().showMessage(btn.text() + ' was pressed')
        print(btn)
        if self.mode == "Один игрок":
            cont = self.play_AI()
            for i in range(7):
                for j in range(7):
                    name_btn = 'pushButton_' + str(i) + str(j)
                    if self.board[i][j] == 1:
                        self.name_btn.setText('X')
                    if self.board[i][j] == 2:
                        self.name_btn.setText('O')
            if not cont[0]:
                rezult = ['Ничья', 'Победа первого игрока!', 'Победа второго игрока!']
                self.end, okBtnPressed = QInputDialog.getItem(
                    self,
                    "Игра окончена!",
                    rezult[cont[1]],
                    ("Ура!", ""),
                    1,
                    False
                )
        else:
            cont = self.play(btn)
            for i in range(7):
                for j in range(7):
                    name_btn = 'pushButton_' + str(i) + str(j)
                    if self.board[i][j] == 1:
                        self.name_btn.setText('X')
                    if self.board[i][j] == 2:
                        self.name_btn.setText('O')
            if not cont[0]:
                rezult = ['Ничья', 'Победа первого игрока!', 'Победа второго игрока!']
                self.end, okBtnPressed = QInputDialog.getItem(
                    self,
                    "Игра окончена!",
                    rezult[cont[1]],
                    ("Ура!", ""),
                    1,
                    False
                )


    def win(self, rez):    #возвращает победителя
        if rez:
            if rez[1] == 1:
                return False, 1
            if rez[1] == 2:
                return False, 2

    def play_AI(self):    #определяет ход AI в зависимости от ситуации на поле
        cnt = 0
        for i in range(7):
            for j in range(7):
                if self.board[i][j] != 0:
                    cnt += 1
        if cnt == 49:
            return False, 0
        if cnt == 1:
            if self.board[3][3] == 0:
                self.board[3][3] = 2
                return True
            else:
                crd = random.choice([(2, 2), (2, 3), (2, 4), (3, 2),
                                     (3, 4), (4, 2), (4, 3), (4, 4)])
                self.board[crd[0]][crd[1]] = 2
                return True
        elif cnt == 3:
            if self.board[3][3] == 1:
                if 1 in self.adjacent((3, 3)):
                    for i in range(2, 5):
                        for j in range(2, 5):
                            if (self.board[i][j] == 0 and
                                        1 in self.adjacent((i, j)) and
                                        2 in self.adjacent((i, j))):
                                self.board[i][j] = 2
                                return True
            for i in range(2, 5):
                for j in range(2, 5):
                    if (self.board[i][j] == 0 and
                                2 in self.adjacent((i, j))):
                        self.board[i][j] = 2
                        return True

        w = self.win(self.is_win())
        if w:
            return False, w[1]
        rez_f = self.are_four()
        if rez_f:
            self.board[rez_f[1][0]][rez_f[1][1]] = 2
            return True
        rez_f = self.are_three()
        if rez_f:
            self.board[rez_f[1][0]][rez_f[1][1]] = 2
            return True
        for i in range(7):
            for j in range(7):
                if self.adjacent((i, j)):
                    if (self.board[i][j] == 0
                        and 1 in self.adjacent((i, j)) and 2 in self.adjacent((i, j))):
                        self.board[i][j] = 2
                        return True
        for i in range(7):
            for j in range(7):
                if self.adjacent((i, j)):
                    if self.board[i][j] == 0 and 2 in self.adjacent((i, j)):
                        self.board[i][j] = 2
                        return True
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 0:
                    self.board[i][j] = 2
                    return True


    def is_win(self):    #проверяет, не ли на поле линии длины 5, то есть не победил ли один из игроков
        win = ([1] * 5, [2] * 5)
        for i in range(7):
            for j in range(7):
                if ((j < 3 and self.board[i][j:j + 5] in win) or
                        (i < 3 and [self.board[i][j],
                                    self.board[i + 1][j],
                                    self.board[i + 2][j],
                                    self.board[i + 3][j],
                                    self.board[i + 4][j]] in win) or
                        (j < 3 and i < 3 and [self.board[i][j],
                                    self.board[i + 1][j + 1],
                                    self.board[i + 2][j + 2],
                                    self.board[i + 3][j + 3],
                                    self.board[i + 4][j + 4]] in win) or
                        (i > 3 and j > 3 [self.board[i][j],
                                          self.board[i + 1][j - 1],
                                          self.board[i + 2][j - 2],
                                          self.board[i + 3][j - 3],
                                          self.board[i + 4][j - 4]] in win)):
                    return True, self.board[i][j]    #возвращает номер игрока
        return False

    def are_three(self):    #проверяет наличие линии длины 3, по обеим сторонам которой пустые клетки
        win = ([1] * 4, [2] * 4)
        for i in range(7):
            for j in range(7):
                if (self.board[i][j] == 0 and
                        (j < 3 and self.board[i][i + 1:j + 4] == win[0] and
                                 self.board[i][j + 4] == 0) or
                        (i < 3 and [self.board[i + 1][j],
                                    self.board[i + 2][j],
                                    self.board[i + 3][j]] == win[0] and
                                 self.board[i + 4][j] == 0) or
                        (j < 3 and i < 3 and [self.board[i + 1][j + 1],
                                              self.board[i + 2][j + 2],
                                              self.board[i + 3][j + 3]]
                            == win[0] and self.board[i + 4][j + 4] == 0) or
                        (i > 3 and j > 3 and [self.board[i + 1][j - 1],
                                              self.board[i + 2][j - 2],
                                              self.board[i + 3][j - 3]]
                            == win[0] and self.board[i + 4][j - 4] == 0)):
                    return True, (i, j)    #возвращает координаты искомой пустой клетки
        for i in range(7):
            for j in range(7):
                if (self.board[i][j] == 0 and
                        (j < 3 and self.board[i][i + 1:j + 4] == win[1] and
                                 self.board[i][j + 4] == 0) or
                        (i < 3 and [self.board[i + 1][j],
                                    self.board[i + 2][j],
                                    self.board[i + 3][j]] == win[1] and
                                 self.board[i + 4][j] == 0) or
                        (j < 3 and i < 3 and [self.board[i + 1][j + 1],
                                              self.board[i + 2][j + 2],
                                              self.board[i + 3][j + 3]]
                            == win[1] and self.board[i + 4][j + 4] == 0) or
                        (i > 3 and j > 3 and [self.board[i + 1][j - 1],
                                              self.board[i + 2][j - 2],
                                              self.board[i + 3][j - 3]]
                            == win[1] and self.board[i + 4][j - 4] == 0)):
                    return True, (i, j)    #возвращает координаты искомой пустой клетки
        return False

    def are_four(self):    #проверяет наличие линии длины 4, с одной стороны от которй пустая клетка
        win = ([1] * 4, [2] * 4)
        for i in range(7):
            for j in range(7):
                if (self.board[i][j] == 0 and
                        (j < 3 and self.board[i][i + 1:j + 5] in win) or
                        (i < 3 and [self.board[i + 1][j],
                                    self.board[i + 2][j],
                                    self.board[i + 3][j],
                                    self.board[i + 4][j]] in win) or
                        (j < 3 and i < 3 and [self.board[i + 1][j + 1],
                                              self.board[i + 2][j + 2],
                                              self.board[i + 3][j + 3],
                                              self.board[i + 4][j + 4]]
                        in win) or
                        (i > 3 and j > 3 and [self.board[i + 1][j - 1],
                                              self.board[i + 2][j - 2],
                                              self.board[i + 3][j - 3],
                                              self.board[i + 4][j - 4]]
                        in win) or
                        (j > 3 and self.board[i][i - 1:j - 5:-1] in win) or
                        (i > 3 and [self.board[i - 1][j],
                                    self.board[i - 2][j],
                                    self.board[i - 3][j],
                                    self.board[i - 4][j]] in win) or
                        (j > 3 and i > 3 and [self.board[i - 1][j - 1],
                                              self.board[i - 1][j - 1],
                                              self.board[i - 2][j - 2],
                                              self.board[i - 3][j - 3],
                                              self.board[i - 4][j - 4]]
                        in win) or
                        (i < 3 and j < 3 and [self.board[i - 1][j + 1],
                                              self.board[i - 2][j + 2],
                                              self.board[i - 3][j + 3],
                                              self.board[i - 4][j + 4]]
                        in win)):
                    return True, (i, j)    #возвращает координаты искомой пустой клетки
        return False

    def adjacent(self, cell):    #получаем список содержимого клеток вокруг данной
        if (cell[0] and cell[1] and cell[0] != 6 and cell[1] != 6):
            return [self.board[cell[0] - 1][cell[1] - 1],
                    self.board[cell[0] - 1][cell[1]],
                    self.board[cell[0] - 1][cell[1] + 1],
                    self.board[cell[0]][cell[1] - 1],
                    self.board[cell[0]][cell[1] + 1],
                    self.board[cell[0] + 1][cell[1] - 1],
                    self.board[cell[0] + 1][cell[1]],
                    self.board[cell[0] +1][cell[1] + 1],]
        else:
            return False

    def play(self, cords): #игра двух людей
        cnt = 0
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 0:
                    cnt += 1
        if cnt == 0:
            return False, 0
        self.board[cords[0]][cords[1]] = self.player
        w = self.win(self.is_win())
        if w:
            return False, w[1]
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
