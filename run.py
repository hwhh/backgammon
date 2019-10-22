import threading
from threading import Thread

from BackEnd.Game import Game
from BackEnd.Player import Player
from FrontEnd.GUI import GUI

if __name__ == '__main__':
    e = threading.Event()
    gui = GUI()

    # When the gui receives an event ping the correct player which
    # will call the game function with the action and its own colour

    player1 = Player('w')
    player2 = Player('b')
    game = Game(gui, player1, player2)
    gui.set_players([player1, player2])

    # Currently te players are running in the main thread which could cause issues later on

    thread = Thread(target=game.run, args=())
    thread.start()
    gui.run()
    thread.join()
