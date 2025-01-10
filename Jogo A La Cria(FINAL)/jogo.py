import pyxel as px
import random
import time

# Variáveis do menu e telas
tela = 1  
contador = 0
opcao_selecionada = 0
opcoes_menu = ["Iniciar Jogo", "Sair"]

# Variáveis do jogo
nx = [0, 170, 340]  # Posições horizontais iniciais do chão
ny = [150] * 3  # Posições verticais do chão
nvx = [1] * 3  # Velocidades do chão

personagem_x = 6  # Posição horizontal do personagem
personagem_y = 134  # Posição vertical do personagem 
personagem_velocidade_vertical = 0  # Velocidade do pulo
personagem_no_chao = True  # Indica se o personagem está no chão

# Variáveis de obstáculos
obstaculos = []  
obstaculo_vx = 3  # Velocidade inicial dos obstáculos
obstaculo_tamanho = 17  
obstaculo_alturas = [134, 80]  # Alturas possíveis dos obstáculos

# aumenta velocidade dos obstáculos
multiplicador_velocidade = 1.5  

fim_de_jogo = False  # Flag de fim de jogo
inicio_jogo = None  # Marca o início do jogo
pontuacao = 0  

# Função para atualizar o chão
def atualizar_chao():
    global nx, nvx
    for i in range(len(nx)):
        nvx[i] += 0.001  # aumenta a velocidade do chão
        nx[i] -= nvx[i]  # Move o chão para a esquerda

        # Repete chão
        if nx[i] + 170 < 0:
            nx[i] = max(nx) + 170  # Reposiciona no final da tela

    #espaçamento do chão
    nx.sort()  
    for i in range(1, len(nx)):
        if nx[i] != nx[i - 1] + 170:
            nx[i] = nx[i - 1] + 170

# Função pulo do personagem
def pular():
    global personagem_velocidade_vertical, personagem_no_chao, pulo_tempo
    if personagem_no_chao:  # Inicia o pulo se estiver no chão
        personagem_velocidade_vertical = -2  # Velocidade inicial
        personagem_no_chao = False
        pulo_tempo = 1 

# Função para atualizar o personagem
def atualizar_personagem():
    global personagem_y, personagem_velocidade_vertical, personagem_no_chao, fim_de_jogo, pulo_tempo
    if not personagem_no_chao:  # Aplica gravidade durante o pulo
        personagem_y += personagem_velocidade_vertical
        personagem_velocidade_vertical += 0.5  # Gravidade

        # o personagem sobe enquanto a tecla for pressionada
        if pulo_tempo < 15:  # Tempo para segurar o pulo 
            pulo_tempo += 1
            if pulo_tempo < 15:  # Primeiro nível de pulo
                personagem_velocidade_vertical = -5  # Maior velocidade de pulo
            elif pulo_tempo < 20:  # Segundo nível de pulo
                personagem_velocidade_vertical = -3  # Menor velocidade de pulo
            else:  #o personagem começa a cair
                personagem_velocidade_vertical += 0.5  # Gravidade começa

        # colisão com o chão
        if personagem_y >= 133:  
            personagem_y = 134  
            personagem_no_chao = True
            personagem_velocidade_vertical = 0  
            pulo_tempo = 0  

    # Atualiza os obstáculos
    for obstaculo in obstaculos:
        obstaculo[0] -= obstaculo_vx * multiplicador_velocidade  

        # Remove o obstáculo se sair da tela
        if obstaculo[0] + obstaculo[2] < 0:  
            obstaculos.remove(obstaculo)

        # colisão com o personagem
        if (
            (personagem_x < obstaculo[0] + obstaculo[2]) and  
            (personagem_x + 17 > obstaculo[0]) and
            (personagem_y < obstaculo[1] + obstaculo[3]) and  
            (personagem_y + 17 > obstaculo[1])
        ):
            fim_de_jogo = True

# Função para adicionar um novo obstáculo
def gerar_obstaculo():
    global obstaculos
    if len(obstaculos) == 0 or obstaculos[-1][0] < px.width - 120:  
        x = px.width + random.randint(0, 50)  

        # Define o tipo do obstáculo (0 para chão, 1 para céu)
        tipo_obstaculo = random.choice([0, 1])  

        if tipo_obstaculo == 0:  
            y = 134  # Posição do chão 
            
            # Gerar obstáculos 
            tipo_2x1_ou_1x2 = random.choice([1, 2])  

            if tipo_2x1_ou_1x2 == 1:  # Obstáculo 1x2
                largura = 16
                altura = 32
                obstaculo = [x, y - altura + 16, largura, altura, tipo_obstaculo]  
            elif tipo_2x1_ou_1x2 == 2:  # Obstáculo 2x1
                largura = 32
                altura = 16
                obstaculo = [x, y, largura, altura, tipo_obstaculo]
        
        else:  # Obstáculo no céu
            y = random.choice(obstaculo_alturas)  # Altura do céu (134 ou 80)
            largura = 16  
            altura = 16  
            obstaculo = [x, y, largura, altura, tipo_obstaculo]

        
        obstaculos.append(obstaculo)

# Função desenhar o chão
def desenhar_chao():
    for i in range(len(nx)):
        px.blt(nx[i], (ny[i]), 2, 2, 190, 256, 167, 0)  # sprite do chão

# Função desenhar o personagem
def desenhar_personagem():
    global personagem_no_chao

    if not personagem_no_chao:  # Personagem pulando
        px.blt(personagem_x, personagem_y, 0, 63, 16, 16, 20, 0)  # Sprite de pulo
    else:  # Personagem no chão
        # Troca de sprite para gerar o efeito de andar 
        if px.frame_count % 10 < 5:  
            px.blt(personagem_x, personagem_y, 0, 32, 16, 17, 16, 0)  # sprite 1
        else:
             px.blt(personagem_x, personagem_y, 0, 49, 17, 13, 20, 0)  # sprite 2 

# Função desenhar os obstáculos
def desenhar_obstaculos():
    for obstaculo in obstaculos:
        x, y, largura, altura, tipo = obstaculo
        
        # Desenho de cada tipo de obstáculo
        if largura == 16 and altura == 16:  # Obstáculo 1x1

            # Troca de sprite efeito de voo
            if px.frame_count % 10 < 5:  
                px.blt(x, y, 0, 16, 129, 16, 16, 0)  # sprite 1
            else:
                px.blt(x, y, 0, 33, 129, 16, 16, 0)  # sprite 2
        elif largura == 16 and altura == 32:  # Obstáculo 1x2
            px.blt(x, y, 0, 21, 79, 16, 32, 0)  

        elif largura == 32 and altura == 16:  # Obstáculo 2x1
            px.blt(x, y, 0, 16, 48, 32, 16, 0)  

# Função de atualização
def update():
    global fim_de_jogo, multiplicador_velocidade, tela, opcao_selecionada, contador, inicio_jogo, pontuacao

    if tela == 1:  # Tela de créditos
        contador += 1
        if contador > 200:  
            tela = 2
            contador = 0  # Reseta o contador ao mudar de tela
    elif tela == 2:  # Tela do título
        contador += 1
        if contador > 200:  
            tela = 3
            contador = 0  
    elif tela == 3:  # Menu principal
        if px.btnp(px.KEY_UP):
            opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_menu)
        elif px.btnp(px.KEY_DOWN):
            opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_menu)

        if px.btnp(px.KEY_BACKSPACE):
            if opcao_selecionada == 0:  # Iniciar Jogo
                tela = 4  # Muda para a tela de jogo
                inicio_jogo = time.time()  # Marca o início do jogo
            elif opcao_selecionada == 1:  # Sai do jogo 
                px.quit()

    elif tela == 4:  # Tela de jogo
        if fim_de_jogo:
            if px.btnp(px.KEY_R):  # Reiniciar jogo
                reiniciar_jogo()
                return  

            elif px.btnp(px.KEY_ESCAPE):  # Sair do jogo
                tela = 3  # Volta para o menu
                reiniciar_jogo()
            return  

        if px.btnp(px.KEY_SPACE):  # Detecta tecla para pular
            pular()

        atualizar_personagem()
        atualizar_chao()

        multiplicador_velocidade += 0.0001  # Aumenta a velocidade com o tempo

        # Aumenta a pontuação com a velocidade
        pontuacao += multiplicador_velocidade * 0.1  

        if inicio_jogo and time.time() - inicio_jogo >= 4:  # Só gera obstáculos após 4 segundos
            if len(obstaculos) == 0 or obstaculos[-1][0] < px.width - 200:
                gerar_obstaculo()

# Função de desenho
def draw():
    global fim_de_jogo, tela, pontuacao

    px.cls(0)  

    if tela == 1:  # Créditos
        px.text(25, 45, "Feito por:", 7)
        px.text(25, 55, "Carlos Eduardo Xavier Campelo Junior", 7)
        px.text(25, 65, "Nicolas Gauterio Xavier", 7)
    elif tela == 2:  # Tela do título
        texto = "A La Cria"
        largura_texto = len(texto) * 4
        x = (px.width - largura_texto) // 2
        y = px.height // 2 - 10
        px.text(x, y, texto, px.frame_count % 16)
    elif tela == 3:  # Menu principal
        px.text(25, 25, "Menu Principal", 7)
        for i, opcao in enumerate(opcoes_menu):
            cor = 8 if i == opcao_selecionada else 7
            px.text(35, 50 + i * 10, opcao, cor)

        # Mensagem de como se movimentar no menu 
        texto_instrucao = "Use as setas para navegar e BACKSPACE para selecionar"
        largura_texto_instrucao = len(texto_instrucao) * 4
        x_instrucao = (px.width - largura_texto_instrucao) // 2
        y_instrucao = px.height - 20
        px.text(x_instrucao, y_instrucao, texto_instrucao, 7)

    elif tela == 4:  # Jogo
        if fim_de_jogo:
            texto_game_over = "FIM DE JOGO!"
            largura_texto_game_over = len(texto_game_over) * 4
            x_game_over = (px.width - largura_texto_game_over) // 2
            y_game_over = px.height // 2 - 20

            texto_pontos = f"Pontos: {int(pontuacao)}"
            largura_texto_pontos = len(texto_pontos) * 4
            x_pontos = (px.width - largura_texto_pontos) // 2
            y_pontos = px.height // 2

            texto_reiniciar = "Pressione R para Reiniciar"
            largura_texto_reiniciar = len(texto_reiniciar) * 4
            x_reiniciar = (px.width - largura_texto_reiniciar) // 2
            y_reiniciar = px.height // 2 + 10

            texto_sair = "Pressione ESC para Sair"
            largura_texto_sair = len(texto_sair) * 4
            x_sair = (px.width - largura_texto_sair) // 2
            y_sair = px.height // 2 + 20

            px.text(x_game_over, y_game_over, texto_game_over, px.COLOR_RED)
            px.text(x_pontos, y_pontos, texto_pontos, px.COLOR_WHITE)
            px.text(x_reiniciar, y_reiniciar, texto_reiniciar, px.COLOR_WHITE)
            px.text(x_sair, y_sair, texto_sair, px.COLOR_WHITE)
            return  
        
        # altera a cor conforme a pontuação 
        if (int(pontuacao) // 500) % 2 == 0:
            cor_fundo =6
        else:
            cor_fundo =5
        px.cls(cor_fundo)  

         # Desenha o céu 
        px.blt(50, -19, 1, 0, 0, 340, 240, 0)  

        desenhar_personagem()
        desenhar_chao()
        desenhar_obstaculos()

        # Desenha a pontuação na tela
        px.text(10, 10, f"Pontos: {int(pontuacao)}", 7)

def reiniciar_jogo():
    global personagem_x, personagem_y, personagem_velocidade_vertical, personagem_no_chao, obstaculos, fim_de_jogo, multiplicador_velocidade, inicio_jogo, pontuacao
    personagem_x = 6
    personagem_y = 134
    personagem_velocidade_vertical = 0
    personagem_no_chao = True
    obstaculos = []
    fim_de_jogo = False
    multiplicador_velocidade = 1.5  # Velocidade inicial dos obstáculos
    inicio_jogo = time.time()  # Reinicia o tempo do jogo
    pontuacao = 0  # Reinicia a pontuação

# Inicialização 
px.init(340, 180, title="A La Cria", fps=60)

# Carregando imagens
px.image(2).load(0, 0, "sprites/4.png")  # chao
px.image(1).load(0, 0, "sprites/ceu.png")  # Céu
px.image(0).load(0, 0, "sprites/pixel-256x256.png")  # Personagem e obstáculos
px.run(update, draw)