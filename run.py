from threading import Thread

from BackEnd.Game import Game
from FrontEnd.GUI import GUI


# def run_funcs(funcs):
#     for func, args in funcs:
#         func(*args)
#
#
# def print_hello():
#     print("hello")
#
#
# def print_a_string(string1, string2):
#     print(string1 + " " + string2)
#
#
# run_funcs([(print_hello, []), (print_a_string, ["hello", "world"])])

if __name__ == '__main__':
    gui = GUI()
    game = Game(gui, True)
    thread = Thread(target=game.run, args=())
    thread.start()
    gui.run()
    thread.join()
