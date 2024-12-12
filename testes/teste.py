import pyxel

class MovingObject:
    def __init__(self, x_positions, y_positions, velocities):
        self.x_positions = x_positions
        self.y_positions = y_positions
        self.velocities = velocities

    def update(self):
        for i in range(len(self.x_positions)):
            self.velocities[i] += 0.001  # Incrementa a velocidade gradualmente
            self.x_positions[i] += self.velocities[i]
            if self.x_positions[i] > pyxel.width:
                self.x_positions[i] = -180  # Reposiciona o objeto para o início da tela

    def draw(self):
        for i in range(len(self.x_positions)):
            x = self.x_positions[i]
            y = self.y_positions[i]
            pyxel.blt(x, y, 1, 0, -1, 200, 31)  # Ajuste a largura da imagem para 180

class Game:
    def __init__(self):
        pyxel.init(340, 180, title="A-La-Cria", fps=60)
        self.moving_object = MovingObject(
            x_positions=[0, 180, 360, 540, 720, 900, 1080],
            y_positions=[150, 150, 150, 150, 150, 150, 150],
            velocities=[1, 1, 1, 1, 1, 1, 1]
        )
        pyxel.run(self.update, self.draw)

    def update(self):
        self.moving_object.update()

    def draw(self):
        pyxel.cls(10)  # Limpa a tela com cor de fundo
        self.moving_object.draw()

# Inicia o jogo
Game()