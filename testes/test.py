import pyxel as px
import random

# Variáveis do jogo
nx = [0, 170, 340]  # Posições horizontais iniciais do chão
ny = [150] * 3  # Posições verticais (fixas) do chão
nvx = [1] * 3  # Velocidades do chão

personagem_x = 0  # Posição horizontal do personagem
personagem_y = 134  # Posição vertical do personagem (ajustada para que a base fique no topo do chão)
personagem_velocidade_vertical = 0  # Velocidade do pulo
personagem_no_chao = True  # Indica se o personagem está no chão

# Variáveis de obstáculos
obstaculos = []  # Lista de obstáculos
obstaculo_vx = 3  # Velocidade inicial dos obstáculos
obstaculo_tamanho = 17  # Tamanho dos obstáculos
obstaculo_alturas = [134]  # Alturas possíveis dos obstáculos

# Variáveis para o multiplicador
multiplicador_velocidade = 5  # Multiplicador de velocidade dos obstáculos

is_game_over = False  # Flag de game over

# Função para atualizar o chão
def atualizar_chao():
    global nx, nvx
    for i in range(len(nx)):
        nvx[i] += 0.001  # Incrementa gradualmente a velocidade do chão
        nx[i] -= nvx[i]  # Move o chão para a esquerda

        # Reposiciona o segmento do chão se sair da tela
        if nx[i] + 170 < 0:
            nx[i] = max(nx) + 170  # Reposiciona no final da sequência fora da tela

    # Garante que os segmentos do chão estão alinhados sem buracos
    nx.sort()  # Ordena as posições para consistência
    for i in range(1, len(nx)):
        if nx[i] != nx[i - 1] + 170:
            nx[i] = nx[i - 1] + 170

# Função para fazer o personagem pular
def pular():
    global personagem_velocidade_vertical, personagem_no_chao, pulo_time
    if personagem_no_chao:  # Inicia o pulo somente se estiver no chão
        personagem_velocidade_vertical = -2  # Velocidade inicial reduzida para um pulo mais curto
        personagem_no_chao = False
        pulo_time = 1  # Começa o contador de tempo de pulo

# Função para atualizar o personagem
def atualizar_personagem():
    global personagem_y, personagem_velocidade_vertical, personagem_no_chao, is_game_over, pulo_time
    if not personagem_no_chao:  # Aplica gravidade durante o pulo
        personagem_y += personagem_velocidade_vertical
        personagem_velocidade_vertical += 0.5  # Gravidade

        # Graduação do pulo: o personagem sobe enquanto a tecla for pressionada (até certo limite)
        if pulo_time < 15:  # Tempo para segurar o pulo (quanto mais tempo pressionado, maior o pulo)
            pulo_time += 1
            if pulo_time < 15:  # Primeiro nível de pulo
                personagem_velocidade_vertical = -5  # Maior velocidade de pulo
            elif pulo_time < 20:  # Segundo nível de pulo
                personagem_velocidade_vertical = -3  # Menor velocidade de pulo
            else:  # Depois de 25 frames, o personagem começa a cair
                personagem_velocidade_vertical += 0.5  # Gravidade começa a influenciar

        # Detecta o contato com o chão
        if personagem_y >= 133:  # Posição corrigida para coincidir com o topo do chão
            personagem_y = 134  # Ajusta para o topo do chão
            personagem_no_chao = True
            personagem_velocidade_vertical = 0  # Resetar a velocidade vertical ao tocar o chão
            pulo_time = 0  # Resetar o tempo do pulo

    # Atualiza os obstáculos
    for obstaculo in obstaculos:
        obstaculo[0] -= obstaculo_vx * multiplicador_velocidade  # Aplica o multiplicador de velocidade

        # Remove o obstáculo se sair da tela
        if obstaculo[0] + obstaculo_tamanho < 0:
            obstaculos.remove(obstaculo)

        # Verifica colisão com o personagem
        if (
            (personagem_x < obstaculo[0] + obstaculo_tamanho) and
            (personagem_x + 17 > obstaculo[0]) and
            (personagem_y < obstaculo[1] + obstaculo_tamanho) and
            (personagem_y + 17 > obstaculo[1])
        ):
            is_game_over = True

# Função para adicionar um novo obstáculo
def gerar_obstaculo():
    if len(obstaculos) < 5:
        x = px.width  # Posição inicial do obstáculo na lateral direita
        y = random.choice(obstaculo_alturas)  # Escolhe uma altura aleatória para o obstáculo
        obstaculos.append([x, y])  # Adiciona o obstáculo à lista

# Função para desenhar o chão
def desenhar_chao():
    for i in range(len(nx)):
        px.rect(nx[i], ny[i], 170, 31, 3)  # Desenha o chão

# Função para desenhar o personagem
def desenhar_personagem():
    px.rect(personagem_x, personagem_y, 17, 17, 9)  # Desenha o personagem como um retângulo

# Função para desenhar os obstáculos
def desenhar_obstaculos():
    for obstaculo in obstaculos:
        px.rect(obstaculo[0], obstaculo[1], obstaculo_tamanho, obstaculo_tamanho, 6)  # Desenha o obstáculo

# Função de atualização
def update():
    global is_game_over, multiplicador_velocidade

    if is_game_over:
        if px.btnp(px.KEY_R):  # Reiniciar jogo
            reiniciar_jogo()
        elif px.btnp(px.KEY_ESCAPE):  # Sair do jogo
            px.quit()
        return  # Não faz mais atualizações quando o jogo acabou

    if px.btnp(px.KEY_SPACE):  # Detecta tecla para pular
        pular()

    atualizar_personagem()
    atualizar_chao()

    # Aumenta o multiplicador de velocidade gradualmente com o tempo
    multiplicador_velocidade += 0.0001  # Ajuste a taxa conforme necessário

    # Temporizador para gerar obstáculos
    if len(obstaculos) == 0 or obstaculos[-1][0] < px.width - 200:
        gerar_obstaculo()

# Função de desenho
def draw():
    global is_game_over

    px.cls(10)  # Limpa a tela com cor de fundo

    if is_game_over:
        # Texto do título "GAME OVER"
        texto_game_over = "GAME OVER!"
        largura_texto_game_over = len(texto_game_over) * 4  # Calcula a largura do texto
        x_game_over = (px.width - largura_texto_game_over) // 2  # Centraliza o texto horizontalmente
        y_game_over = px.height // 2 - 20  # Centraliza o texto verticalmente

        # Texto para reiniciar ou sair
        texto_reiniciar = "Press R to Restart"
        largura_texto_reiniciar = len(texto_reiniciar) * 4  # Calcula a largura do texto
        x_reiniciar = (px.width - largura_texto_reiniciar) // 2  # Centraliza o texto horizontalmente
        y_reiniciar = px.height // 2 + 10  # Posição ajustada para o texto de reiniciar

        texto_sair = "Press ESC to Quit"
        largura_texto_sair = len(texto_sair) * 4  # Calcula a largura do texto
        x_sair = (px.width - largura_texto_sair) // 2  # Centraliza o texto horizontalmente
        y_sair = px.height // 2 + 20  # Posição ajustada para o texto de sair

        # Desenha os textos centralizados
        px.text(x_game_over, y_game_over, texto_game_over, px.COLOR_RED)
        px.text(x_reiniciar, y_reiniciar, texto_reiniciar, px.COLOR_WHITE)
        px.text(x_sair, y_sair, texto_sair, px.COLOR_WHITE)

        return  # Não desenha mais nada depois do "Game Over"
    
    desenhar_personagem()  # Desenha o personagem
    desenhar_chao()  # Desenha o chão
    desenhar_obstaculos()  # Desenha os obstáculos

# Função para reiniciar o jogo
def reiniciar_jogo():
    global personagem_x, personagem_y, personagem_velocidade_vertical, personagem_no_chao, obstaculos, is_game_over, multiplicador_velocidade
    personagem_x = 0  # Posição horizontal do personagem
    personagem_y = 133  # Posição vertical do personagem (ajustada para que a base fique no topo do chão)
    personagem_velocidade_vertical = 0  # Velocidade do pulo
    personagem_no_chao = True  # Indica se o personagem está no chão
    obstaculos = []  # Limpa a lista de obstáculos
    is_game_over = False  # Reseta o flag de game over
    multiplicador_velocidade = 3.0  # Reseta o multiplicador de velocidade

# Inicializa Pyxel
px.init(340, 180, title='A-La-Cria', fps=60)

# Executa o jogo
px.run(update, draw)
