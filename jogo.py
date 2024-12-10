                   #codigo Principal do Jogo#
import pyxel

def update():
    pass

def draw():
    pyxel.cls(0)
    pyxel.text(25, 45, 'Feito por :\nCarlos Eduardo Xavier Campelo Junior\nNicolas Gauterio Xavier', 7)#pyxel.frame_count % 16)
    
pyxel.init(180, 120, title='Hello')
pyxel.run(update, draw)