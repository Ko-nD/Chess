class Movement:
    @staticmethod
    def do_step(figure, x1, y1, x2, y2, board):
        figure.do_movement(x2, y2)
        board.board[y1][x1] = '.'
        board.board[y2][x2] = figure

    
    @staticmethod
    def back_step(figure, x1, y1, x2, y2, board, last_kill):
        figure.do_movement(x1, y1)
        board.board[y2][x2] = last_kill
        board.board[y1][x1] = figure


    @staticmethod
    def check_step(figure, x1, y1, x2, y2, board):
        if isinstance(figure, Bishop) or isinstance(figure, Rook) or isinstance(figure, Queen):
            x_min, x_max, y_min, y_max = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
            if abs(x1 - x2) == abs(y1 - y2) and  not isinstance(figure, Rook):
                if (x1 - x2) * (y1 - y2) > 0: # проверка на направление диагонального хода
                    return not True in [board.is_figure(x_min + i,y_min + i) for i in range(1, abs(x1 - x2))]
                else:
                    return not True in [board.is_figure(x_max - i, y_min + i) for i in range(1, abs(x1 - x2))]
            elif x1 == x2 and not isinstance(figure, Bishop):
                return not True in [board.is_figure(x1, i) for i in range(y_min + 1, y_max)]
            elif y1 == y2 and  not isinstance(figure, Bishop):
                return not True in [board.is_figure(i, y1) for i in range(x_min + 1, x_max)]
                

        if isinstance(figure, Pawn):
            if board.is_figure(x2, y2, 1 - figure.color):
                return abs(y1 - y2) == 1 and abs(x1 - x2) == 1
            if figure.color:
                return (y1 == 1 and  (y2 - y1) == 2 or (y2 - y1) == 1) and x1 == x2
            else:
                return (y1 == 6  and  (y1 - y2) == 2 or (y1 - y2) == 1) and x1 == x2

        
        if isinstance(figure, Knight):
            return abs(x1 - x2) == 1 and abs(y1 - y2) == 2 or abs(x1 - x2) == 2 and abs(y1 - y2) == 1

        
        if isinstance(figure, King):
            if not board.shax(figure, board.board[y2][x2]):
                if abs(x1 - x2) == 2 and y1 == y2 and not figure.step:
                    if  x2 == 2: 
                        x1_rook = 0
                        x2_rook = 3
                    else:
                        x1_rook = 7
                        x2_rook = 5
                    rook = board.board[y1][x1_rook]
                    if isinstance(rook, Rook) and Movement.check_step(rook, x1_rook, y1, 4, y1, board):
                        Movement.do_step(rook, x1_rook, y1, x2_rook, y1, board) # y1 = y2 = rook.y
                        return True
                else:
                    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 #обычная проверка


        return False


    @staticmethod
    def get_figure(now_color, board):
        x1, y1 = input('Выберите фигуру: ')
        x1 = ord(x1) - ord('A') # переводим букву в значение соответствующего столбца
        y1 = 8 - int(y1) # т.к. в шахматах номирование строк снизу вверх

        if (board.board[y1][x1] == '.') or (board.board[y1][x1].color != now_color):
            print('Вы выбрали пустое поле или же фигуру не своего цвета')
            return Movement.get_figure(now_color, board)

        return (board.board[y1][x1])


    @staticmethod
    def get_step(figure, board):
        x2, y2 = input('Сделайте ход: ')
        x2 = ord(x2) - ord('A') 
        y2 = 8 - int(y2)
        x1, y1 = figure.x, figure.y

        if (not Movement.check_step(figure, x1, y1, x2, y2, board)) or board.is_figure(x2, y2, figure.color):
            print('Ход невозможен, сходите по-другому!')
            return Movement.get_step(figure, board)

        return (x2, y2)


class Figure:
    chess_type = 'Default'


    def __init__(self, color, x, y, board):
        self.color = color # white = 0, black = 1
        self.x = x
        self.y = y
        self.board = board


    def __str__(self):
        pictures = {'P' : "♙", 'R' : "♖", 'N' : "♘", 'B' : "♗", 'K' : "♔", 'Q' : "♕", \
             'p': "♟", 'r' : "♜", 'n' : "♞", 'b' : "♝", 'k' : "♚", 'q' : "♛" }
        return pictures[self.chess_type if self.color else self.chess_type.lower()]

    
    def do_movement(self, x, y):
        self.x = x
        self.y = y

                            
class Pawn(Figure):
    chess_type = 'P'


class Bishop(Figure):
    chess_type = 'B'


class Rook(Figure):
    chess_type = 'R'

            
class Queen(Figure):
    chess_type = 'Q'


class King(Figure):
    chess_type = 'K'
    step = False


class Knight(Figure):
    chess_type = 'N'


class Board:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(1, i, 1, self)
            self.board[6][i] = Pawn(0, i, 6, self)
            if i == 0 or i == 7:
                self.board[0][i] = Rook(1, i, 0, self)
                self.board[7][i] = Rook(0, i, 7, self)
            if i == 1 or i == 6:
                self.board[0][i] = Knight(1, i, 0, self)
                self.board[7][i] = Knight(0, i, 7, self)
            if i == 2 or i == 5:
                self.board[0][i] = Bishop(1, i, 0, self)
                self.board[7][i] = Bishop(0, i, 7, self)
        self.board[0][3] = Queen(1, 3, 0, self)
        self.board[7][3] = Queen(0, 3, 7, self)
        self.board[0][4] = King(1, 4, 0, self)
        self.board[7][4] = King(0, 4, 7, self)
        
        self.figures = [[], []] 
        for i in range(8):
            for j in range(8):
                item = self.board[i][j] 
                if item != '.':
                    self.figures[item.color].append(item)


    def show(self):
        str_board = [[str(self.board[i][j]) for j in range(8)] for i in range(8)]
        print('   A B C D E F G H ')
        for i in range(8):
            print(f'{8 - i}  {" ".join(str_board[i])}  {8 - i}')
        print('   A B C D E F G H \n')


    def is_figure(self, x, y, color=None):
        if self.board[y][x] != '.':
            if color != None and self.board[y][x].color == color:
                return True
            elif color != None:
                return False
            return True 
        return False
        
    
    def kill_figure(self, figure):
        del self.figures[figure.color][self.figures[figure.color].index(figure)]

    
    def add_figure(self, figure):
        self.figures[figure.color].append(figure)
            

    def shax(self, king, last_kill=None):
        for figure in self.figures[1 - king.color]:
            if not isinstance(figure, King) and figure != last_kill \
                and Movement.check_step(figure, figure.x, figure.y, king.x, king.y, self):
                return True
        return False
        

    def mate(self, king):
        if not Board.shax(self, king): return False # если нет шаха то нет и мата
        for figure in self.figures[king.color]:
            for i in range(8):
                for j in range(8):
                    if Movement.check_step(figure, figure.x, figure.y, j, i, self) \
                        and not self.is_figure(j, i, king.color):
                        last_kill = self.board[i][j]
                        step = [figure, figure.x, figure.y, j, i, self] # параметры хода
                        Movement.do_step(*step)
                        if not Board.shax(self, king, last_kill): 
                            Movement.back_step(*step, last_kill)
                            return False
                        Movement.back_step(*step, last_kill)
        return True

class Game:
    def __init__(self):
        self.board = Board()


    def start(self):
        step_counter = 0 #белые ходят первые
        self.board.show()
        kings = [self.board.board[7][4], self.board.board[0][4]]
        
        while True:
            now_color = step_counter % 2 # текущий цвет ходящих
            if self.board.mate(kings[now_color]):
                print(f"{'Чёрные' if now_color else 'Белые'} проиграли")
                break

            figure = Movement.get_figure(now_color, self.board) # получение фигуры для хода
            x1, y1 = figure.x, figure.y # для возврата хода
            x2, y2 = Movement.get_step(figure, self.board) # получение координат хода 

            if isinstance(figure, Pawn) and (y2 == 0 or y2 == 7): # пешка в королеву
                self.board.kill_figure(figure)
                figure = Queen(figure.color, x1, y1, self.board)
                self.board.add_figure(figure)

            last_kill = self.board.board[y2][x2]
            step = [figure, x1, y1, x2, y2, self.board] # параметры хода
            Movement.do_step(*step) # совершение хода

            if self.board.shax(kings[now_color], last_kill): # проверка на шах 
                print('Ход невозможен, у вас шах! Переходите')
                Movement.back_step(*step, last_kill) # откат хода 
                continue
            
            if last_kill != '.': # удаляем фигуру из списка
                self.board.kill_figure(last_kill)
            print('Ход выполнен\n')

            if isinstance(figure, King): #проверка нехождения короля для рокировки
                figure.step = True
            
            self.board.show()
            step_counter += 1 


g1 = Game() # создание игры 
g1.start() # Запуск игры














