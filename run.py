from threading import Thread

from BackEnd.Game import Game
from FrontEnd.GUI import GUI

if __name__ == '__main__':
    gui = GUI()
    game = Game(gui)
    thread = Thread(target=game.run, args=()).start()
    gui.run()
    thread.join()