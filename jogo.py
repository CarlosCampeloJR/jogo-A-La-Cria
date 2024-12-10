                   #codigo Principal do Jogo#
import pyxel

# Variável global para controlar a tela
tela = 1
contador = 0

# Opções do menu
opcao_selecionada = 0
opcoes_menu = ["Iniciar Jogo", "Sair"]  # Configurações removidas

def update():
    global tela, contador, opcao_selecionada

    if tela == 1:  # Tela de créditos
        contador += 1
        if contador > 200:  # Aproximadamente 3 segundos (60 FPS)
            tela = 2
            contador = 0  # Reseta o contador ao mudar de tela
    elif tela == 2:  # Tela do título
        contador += 1
        if contador > 200:  # Aproximadamente 3 segundos
            tela = 3
            contador = 0  # Reseta o contador ao mudar de tela
    elif tela == 3:  # Menu principal
        # Navegação no menu
        if pyxel.btnp(pyxel.KEY_UP):
            opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_menu)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_menu)

        # Seleção de uma opção
        if pyxel.btnp(pyxel.KEY_ENTER):
            if opcao_selecionada == 0:  # "Iniciar Jogo"
                tela = 4  # Pode ser a tela de jogo (não implementada ainda)
            elif opcao_selecionada == 1:  # "Sair"
                pyxel.quit()

def draw():
    pyxel.cls(0)  # Limpa a tela com a cor 0 (preto)

    if tela == 1:  # Tela de créditos
        pyxel.text(25, 45, "Feito por:", 7)
        pyxel.text(25, 55, "Carlos Eduardo Xavier Campelo Junior", 7)
        pyxel.text(25, 65, "Nicolas Gauterio Xavier", 7)
    elif tela == 2:  # Tela do título
        # Centralizar o texto
        texto = "A La Cria"
        largura_texto = len(texto) * 4  # Cada caractere tem 4px de largura
        x = (pyxel.width - largura_texto) // 2
        y = pyxel.height // 2 - 10

        # Desenhar apenas o texto
        pyxel.text(x, y, texto, pyxel.frame_count % 16)  # Texto colorido animado
    elif tela == 3:  # Menu principal
        pyxel.text(25, 25, "Menu Principal", 7)
        for i, opcao in enumerate(opcoes_menu):
            cor = 9 if i == opcao_selecionada else 7  # Destaque para a opção selecionada
            pyxel.text(35, 50 + i * 10, opcao, cor)

# Inicializa o Pyxel
pyxel.init(180, 120, title="A La Cria")
pyxel.run(update, draw)
