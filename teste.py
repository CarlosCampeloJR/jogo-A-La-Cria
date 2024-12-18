import pyxel
import random

# Configurações do jogo
SCREEN_WIDTH = 340
SCREEN_HEIGHT = 180
PLAYER_SIZE = 8
OBJECT_SIZE = 8
NUM_OBJECTS = 3  # Número máximo de objetos na tela

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Jogo de Colisão")
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_speed = 2
        self.objects = []  # Lista de objetos na tela
        self.bg_speed = 1  # Velocidade do fundo (e objetos)
        self.spawn_timer = 0  # Temporizador para criar novos objetos
        self.is_game_over = False
        self.generate_object()  # Gera o primeiro objeto
        pyxel.run(self.update, self.draw)

    def generate_object(self):
        """Gera um novo objeto no lado direito da tela."""
        if len(self.objects) < NUM_OBJECTS:
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT - OBJECT_SIZE)
            self.objects.append([x, y])  # Adiciona o objeto à lista

    def update(self):
        """Atualiza a lógica do jogo, como movimento e colisões."""
        if self.is_game_over:
            return
        
        # Movimento do jogador
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= self.player_speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += self.player_speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= self.player_speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += self.player_speed

        # Aumenta a velocidade do fundo gradualmente
        self.bg_speed += 0.0001

        # Atualiza objetos: movendo-os da direita para a esquerda
        for obj in self.objects:
            obj[0] -= self.bg_speed  # Move o objeto para a esquerda
        
        # Remove objetos que saem da tela
        self.objects = [obj for obj in self.objects if obj[0] > -OBJECT_SIZE]

        # Gera novos objetos se necessário
        if self.spawn_timer <= 0:
            self.generate_object()
            self.spawn_timer = random.randint(30, 90)  # Define o tempo para o próximo spawn (entre 30 e 90 frames)
        else:
            self.spawn_timer -= 1  # Decrementa o timer de spawn

        # Verificar colisão com os objetos
        for obj_x, obj_y in self.objects:
            if self.check_collision(self.player_x, self.player_y, obj_x, obj_y):
                self.is_game_over = True
                break

    def check_collision(self, x1, y1, x2, y2):
        """Verifica colisão entre dois objetos quadrados."""
        return not (x1 + PLAYER_SIZE <= x2 or x1 >= x2 + OBJECT_SIZE or y1 + PLAYER_SIZE <= y2 or y1 >= y2 + OBJECT_SIZE)

    def draw(self):
        """Desenha todos os elementos na tela."""
        pyxel.cls(0)  # Limpa a tela

        if self.is_game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, "GAME OVER!", pyxel.COLOR_RED)
            return
        
        # Desenha o jogador
        pyxel.rect(self.player_x, self.player_y, PLAYER_SIZE, PLAYER_SIZE, pyxel.COLOR_WHITE)

        # Desenha os objetos (eles se movem da direita para a esquerda)
        for obj_x, obj_y in self.objects:
            pyxel.rect(obj_x, obj_y, OBJECT_SIZE, OBJECT_SIZE, pyxel.COLOR_GREEN)

# Inicializa o jogo
Game()
