import pyxel
import random

# Estados do jogo
tela = 1  # 1: Créditos, 2: Título, 3: Menu Principal, 4: Gameplay, 5: Game Over
contador = 0
opcao_selecionada = 0
opcoes_menu = ["Iniciar Jogo", "Sair"]

# Variáveis do jogo
personagem_x = 0
personagem_y = 134
velocidade_y = 0
pulando = False

chao_x = [0, 170, 340]
chao_y = 150
chao_vx = 1  # Velocidade inicial ajustada

obstaculos = []
obstaculos_vx = 3
multiplicador_velocidade = 5  # Multiplicador da velocidade dos obstáculos
is_game_over = False


# Reiniciar todas as variáveis do jogo
def reiniciar_jogo_tela():
    global personagem_x, personagem_y, velocidade_y, pulando, chao_x, chao_vx, obstaculos, obstaculos_vx, multiplicador_velocidade, is_game_over
    personagem_x = 0
    personagem_y = 134
    velocidade_y = 0
    pulando = False
    chao_x = [0, 170, 340]
    chao_vx = 1
    obstaculos = []
    obstaculos_vx = 3
    multiplicador_velocidade = 5
    is_game_over = False


# Atualizar o chão
def atualizar_chao_tela():
    global chao_x, chao_vx
    for i in range(len(chao_x)):
        chao_x[i] -= chao_vx * multiplicador_velocidade
        if chao_x[i] + 170 < 0:
            chao_x[i] = max(chao_x) + 170


# Atualizar o personagem
def atualizar_personagem_tela():
    global personagem_y, velocidade_y, pulando, is_game_over
    if pulando:
        personagem_y += velocidade_y
        velocidade_y += 0.5  # Gravidade
        if personagem_y >= 134:  # Limita ao chão
            personagem_y = 134
            velocidade_y = 0
            pulando = False

    # Atualizar obstáculos
    for obstaculo in obstaculos:
        obstaculo[0] -= obstaculos_vx * multiplicador_velocidade
        if obstaculo[0] + 17 < 0:
            obstaculos.remove(obstaculo)

        # Detectar colisão
        if (
            personagem_x < obstaculo[0] + 17
            and personagem_x + 17 > obstaculo[0]
            and personagem_y < obstaculo[1] + 17
            and personagem_y + 17 > obstaculo[1]
        ):
            is_game_over = True


# Gerar novos obstáculos
def gerar_obstaculo_tela():
    if len(obstaculos) < 5:
        x = pyxel.width
        y = 134
        obstaculos.append([x, y])


# Função de atualização
def update():
    global tela, contador, opcao_selecionada, is_game_over, multiplicador_velocidade

    if tela == 1:  # Créditos
        contador += 1
        if contador > 200:
            tela = 2
            contador = 0

    elif tela == 2:  # Título
        contador += 1
        if contador > 200:
            tela = 3
            contador = 0

    elif tela == 3:  # Menu Principal
        if pyxel.btnp(pyxel.KEY_UP):
            opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_menu)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_menu)

        if pyxel.btnp(pyxel.KEY_ENTER):
            if opcao_selecionada == 0:  # Iniciar Jogo
                tela = 4
                reiniciar_jogo_tela()
            elif opcao_selecionada == 1:  # Sair
                pyxel.quit()

    elif tela == 4:  # Gameplay
        if is_game_over:
            tela = 5
            return

        if pyxel.btnp(pyxel.KEY_SPACE) and not pulando:
            velocidade_y = -2
            pulando = True

        atualizar_personagem_tela()
        atualizar_chao_tela()

        multiplicador_velocidade += 0.0001  # Aumenta a dificuldade gradualmente

        if len(obstaculos) == 0 or obstaculos[-1][0] < pyxel.width - 200:
            gerar_obstaculo_tela()

    elif tela == 5:  # Game Over
        if pyxel.btnp(pyxel.KEY_R):  # Reinicia o jogo
            reiniciar_jogo_tela()
            tela = 4
        elif pyxel.btnp(pyxel.KEY_ENTER):  # Voltar ao menu principal
            reiniciar_jogo_tela()
            tela = 3
        elif pyxel.btnp(pyxel.KEY_ESCAPE):  # Sair do jogo
            pyxel.quit()


# Função de desenho
def draw():
    pyxel.cls(0)

    if tela == 1:  # Créditos
        pyxel.text(25, 45, "Feito por:", 7)
        pyxel.text(25, 55, "Carlos Eduardo Xavier Campelo Junior", 7)
        pyxel.text(25, 65, "Nicolas Gauterio Xavier", 7)

    elif tela == 2:  # Título
        texto = "A La Cria"
        largura_texto = len(texto) * 4
        x = (pyxel.width - largura_texto) // 2
        y = pyxel.height // 2 - 10
        pyxel.text(x, y, texto, pyxel.frame_count % 16)

    elif tela == 3:  # Menu Principal
        pyxel.text(25, 25, "Menu Principal", 7)
        for i, opcao in enumerate(opcoes_menu):
            cor = 8 if i == opcao_selecionada else 7
            pyxel.text(35, 50 + i * 10, opcao, cor)

    elif tela == 4:  # Gameplay
        pyxel.rect(personagem_x, personagem_y, 17, 17, 9)
        for x in chao_x:
            pyxel.rect(x, chao_y, 170, 31, 3)
        for obstaculo in obstaculos:
            pyxel.rect(obstaculo[0], obstaculo[1], 17, 17, 6)

    elif tela == 5:  # Game Over
        pyxel.text(50, 50, "GAME OVER", pyxel.COLOR_RED)
        pyxel.text(40, 70, "R para Reiniciar", pyxel.COLOR_WHITE)
        pyxel.text(40, 90, "Enter para Menu", pyxel.COLOR_WHITE)
        pyxel.text(40, 110, "ESC para Sair", pyxel.COLOR_WHITE)


# Inicialização do Pyxel
pyxel.init(340, 180, title="A La Cria", fps=60)
pyxel.run(update, draw)
