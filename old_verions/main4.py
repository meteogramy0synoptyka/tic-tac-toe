import unittest
import abc

# TODO: spróbuj użyć pep8

# MODEL GRY (dobrze mieć testy, a kod przystosowany)
"""
starting information about the game
- point1
- point2

.. note::
    There are many other Info fields but they may be redundant:
        * param, parameter, arg, argument, key, keyword: Description of a
          parameter.
        * type: Type of a parameter.
        * raises, raise, except, exception: That (and when) a specific
          exception is raised.
        * var, ivar, cvar: Description of a variable.
        * returns, return: Description of the return value.
        * rtype: Return type.
"""
PLAYER1 = "X"
PLAYER2 = "O"
EMPTY = "-"
SIZE = 4

# begin language section

# TODO obsługiwać w przyszłości możliwość obsługi innych formatów danych tekstów np csv z 2 kolumnami. Każdy kolejny język byłby inną kolmną

LANGUAGE = 'eng'
LANGUAGES = ['pl', 'eng']
SHOW_HISTORY = [["historia gry"], ["history game"]]


# 1. utrudniają testowanie
# 2. współbieżność

def set_language(language):
    global LANGUAGE
    LANGUAGE = language

def print_language(message):
    print()
    
    
TRANSLATIONS = {
    'PL': {
        'start': 'Witaj graczu, wybierz pole'
    },
    'ENG': {
        'start': '...'
    }
}

class Translator:
    
    def __init__(self, curr_language, translations):
        self.curr_language = curr_language
        self.translations = translations
    
    def get_translation(self, code):
        lang_translations = self.translations.get(self.curr_language)
        return lang_translations.get(code)
    
    
# message = trans.get_translation('start')
# end language section


def message(ID_communique, language='pl', **args):
    print()


def create_board(size):
    """
    This creates a board
    :param size: number of fiels in one side
    :return:
    """
    result = []
    for _ in range(size):
        row = [EMPTY] * size  # <-- OK
        result.append(row)
    return result


def set_board_value(plansza, położenie, player):
    x = położenie[0]
    y = położenie[1]
    plansza[x][y] = player


def has_free_field(board):
    for row in board:
        if EMPTY in row:
            return True
    return False


def is_end(board):
    for row in board:
        if any([row[i] != EMPTY for i in row]):
            return False
    return True


def is_free_position(board, position):
    row, col = position
    return board[row][col] == EMPTY


def has_line(board, symbol):
    def hor(n):
        return all([board[n][it] == symbol for it in range(SIZE)])

    def ver(n):
        return all([board[it][n] == symbol for it in range(SIZE)])

    def cross1():
        return all([board[it][it] == symbol for it in range(SIZE)])

    def cross2():
        return all([board[it][SIZE - 1 - it] == symbol for it in range(SIZE)])

    horizontals = any([hor(it) for it in range(SIZE)])
    verticals = any([ver(it) for it in range(SIZE)])
    return any([horizontals, verticals, cross1(), cross2()])


def make_position(human_number, size):
    index = human_number - 1
    return [index // size, index % size]


def make_human_position(position, size):
    row, col = position
    return row * size + col + 1


def make_human_positions(positions, size):
    human_positions = []
    for pos in positions:
        human_positions.append(make_human_position(pos, size))
    return human_positions


def make_queue():
    return [PLAYER1, PLAYER2]


def update_queue(queue):
    first, second = queue
    queue[0] = second
    queue[1] = first


def make_game(user):
    return {
        'board': create_board(SIZE),
        'queue': make_queue(),
        'running': True,
        'user': user,
        'history': []
    }


def get_player(game):
    return game['queue'][0]


# Wyświetlanie


def wyswietl_old(plansza):
    for linia in plansza:
        for pole in linia:
            print(pole, ", ", end='')
        print("|")
    print()


def wyswietl(plansza):
    for linia in plansza:
        for pole in linia:
            print(pole, "", end='')
        print()
    print()


def display_hist(game):
    print_language(SHOW_HISTORY)
    print(str(game['history']))


# Interakcja

# Użytkownicy (źródła danych)

class BaseUser(abc.ABC):

    @abc.abstractmethod
    def get_position(self, message, board):
        pass

ANSWER_YES = "y"
ANSWER_NO = "n"


class RealUser(BaseUser):  # <---------------------------

    def __init__(self, translator):
        self.translator = translator
        
    def get_position(self, message, board):
        USER_MIN_VALUE = 1
        USER_MAX_VALUE = SIZE ** 2

        while True:
            human_number = self._get_valid_number_from_range(
                message, 
                from_value=USER_MIN_VALUE, 
                to_value=USER_MAX_VALUE
            )

            position = make_position(human_number, size=len(board)) 
            if is_free_position(board, position):
                return position
            print(trans.get_translation('no-free')
            # print(['To jest pole jest już zajęte'],
                  # ["This field is just reserved"])

    def _is_answer(self, s):
        return s in [ANSWER_YES, ANSWER_NO]


    def _ask_for_history(self):
        while True:
            print(["czy chcesz odtworzyć grę ?? [y/n]"],
                  ["do you want restore a game ?? [y/n]"])
            line = input()  #
            answer = line.lower().strip()
            if is_answer(answer):
                return answer == ANSWER_YES


    def _get_valid_number_from_range(self, message, from_value, to_value):
        while True:
            number = get_valid_number(message)
            if from_value <= number <= to_value:  # <-- is_valid_number(x)
                return number
            else:
                print(['Wymagana liczba od {} do {}'.format(from_value, to_value)], [
                       'Required number from {} to {}'.format(from_value, to_value)])

    def _get_valid_number(self, message):
        while True:
            try:
                return int(input(message))
            except ValueError:
                print(['podaj jeszcze raz'], ['write the next time'])

    
    
    # def make_game(self, user):
    #     return make_game(user)


class DevUser(BaseUser):

    def __init__(self, seq):
        self.seq = seq
        self.index = 0 if seq else -1

    def get_position(self, message, board):
        if self.index < len(self.seq):
            value = self.seq[self.index]
            self.index += 1
            return make_position(int(value), size=len(board))
        raise Exception('Illegal state')


#     def make_game(self, user):
#         return make_game(user)

# wprowadzenie do super: https://rhettinger.wordpress.com/2011/05/26/super-considered-super/

# Dziedziczenie (relacja JEST) vs Kompozycja (relacja MA)
class HistoryUserVersion1(DevUser):

    def __init__(self, history):
        human_positions = make_human_positions(history)
        super().__init__(human_positions)  # woła DevUser.__init__

    def get_position(self, message, board):
        # 1. DevUser.get_position(message, board)
        position = super().get_position(message, board)

        # 2. czekanie na kliknięcie (ze strony użytkownika)
        input()

        # 3. zwrcamy wartość jaką wcześniej otrzymaliśmy z get_position
        return position


# Java Efektywne Programowanie: Kompozycja > *Dziedziczenie*

# KOMPOZYCJA
class HistoryUser(BaseUser):

    def __init__(self, history, size):
        # przekształcamy listę list w listę pozycji jakie osoba wpisuje
        seq = make_human_positions(history, size)
        self._dev_user = DevUser(seq)  #

    def get_position(self, message, board):
        # 1. DevUser.get_position(message, board)
        position = self._dev_user.get_position(message, board)

        # 2. czekanie na kliknięcie (ze strony użytkownika)
        input()

        # 3. zwrcamy wartość jaką wcześniej otrzymaliśmy z get_position
        return position


# class HistUser(BaseUser):

#     def __init__(self, seq):
#         self.seq = seq
#         self.index = 0 if seq else -1

#     def get_position(self, message, board):
#         if self.index < len(self.seq):
#             value = self.seq[self.index]
#             self.index += 1
#             while True:
#                 if input()==' ':
#                     print("Pole {} zostalo zajete".format(int(value)))
#                     return make_position(int(value), size=len(board))
#         raise Exception('Illegal state')

# !!!
# def make_game(self, user):
#     return {
#         'board': rozpocznij(SIZE),
#         'queue': make_queue(),
#         'running': True,
#         'user': user,
#         'history': self.seq
#     }


# Warto dodać pole size do game, aby była możliwość odpalania różnych gier w ramach tego samego procesu.

# LOGIKA przepyw gry (charakterystyczny dla konsoli), rdzen

def update_game(game, console):
    wyswietl(game['board'])

    # print(trans.get_translation('make-move'), get_player(game))
    print('Ruch wykonuje', get_player(game))  # <---
    position = game['user'].get_position('Podaj pozycję ', game['board'])
    set_board_value(game['board'], position, get_player(game))

    game['history'].append(position)
    game['running'] = not is_end(game)

    if not game['running']:
        wyswietl(game['board'])
        print("KONIEC GRY!! Wygrał gracz ", get_player(game))

    update_queue(game['queue'])


def run_game(game):
    while game['running']:
        update_game(game, None)


# CO jest lepsze?
# 1) lista list z indeksami
# 2) lista human_position

def run_history(finished_game):
    user = HistoryUser(finished_game['history'], SIZE)  # <-- BRAWO!
    game = make_game(user)
    run_game(game)


def make_ttt_program():
    user = DevUser(['2', '6', '3', '7', '4', '9', '1'])
    return {
        'user': user,
        'trans': Translator('pl', TRANSLATIONS),
        'game': make_game(user)
    }
    

def run_program(program):
    run_game(program['game'])
    
    
def main():
    # user = DevUser(['2', '6', '3', '7', '4', '9', '1'])
    # # user = RealUser()
    # game = make_game(user)
    
    program = make_ttt_program()
    run_program(program)
    
    # run_game(game)

    # display_hist(game)  # Pokazywanie na potrzeby developerskie
    # answer = ask_for_history()

    # if answer:
        # run_history(game)

    # for _ in range(5):
    # print(user.get_position())


# tests.py


class ModelGame(unittest.TestCase):
    def test_create_board_size_0(self):
        self.assertEquals([[]], create_board(0), 'when size={}'.format(0))

    def test_create_board_size_1(self):
        self.assertEquals([[EMPTY]], create_board(1), 'when size={}'.format(1))

    def test_create_board_size_2(self):
        self.assertEquals([[EMPTY, EMPTY], [EMPTY, EMPTY]],
                          create_board(2), 'when size={}'.format(2))

    def test_create_board_size_3(self):
        self.assertEquals([3*[EMPTY], 3*[EMPTY], 3*[EMPTY]],
                          create_board(3), 'when size={}'.format(3))

    def test_has_free_field(self, size):
        self.assertNotEquals()


class HumanPositionTests(unittest.TestCase):

    def test_when_size_equals_1(self):
        self._run_mini_tests(size=1)

    def test_when_size_equals_2(self):
        self._run_mini_tests(size=2)

    def test_when_size_equals_3(self):
        self._run_mini_tests(size=3)

    def _run_mini_tests(self, size):
        last_number = size * size
        for number in range(1, last_number + 1):
            pos = make_position(number, size)
            human_pos = make_human_position(pos, size)
            self.assertEquals(number, human_pos, 'when size={}'.format(size))


# class BoardOperationsTests(board, position):
# empty_board = [[] for row in range()]
# def test_has_free_field(self):
# self.


# unittest.main()
main()

######################################################################
# NOTATKI

# Bibliotka: requests
# requests.get('')


# KOD, KTÓRY URUCHAMIA GRĘ

# pycharm - skroty
# Ctrl+Shift+MINUS
# Ctrl+Shift+PLUS

# TODO:
# napisz testy do najważniejszych fragmentów kodu

# TODO:
# obsługa języka polskiego / angielskiego, język ustala użytkownik na początku procesu

# TODO:
# użytkownik określa wielkość planszy na której gra

# TODO:
# tryb 1: do N gier  [X, X, X, O, O] -> X*3 > O*2
# tryb 2: do N gier przewagi dla 3 byłoby tak: [X, O, X, X, O, X, X] -> X*5, O*2 i jest 3 różnicy
# tryb 3: do N gier pod rząd, dla 3 byłoby tak: [X, O, X, X, O, X, X, X] -> ostatnie N meczy ma znaczenie

# 2h 15min

