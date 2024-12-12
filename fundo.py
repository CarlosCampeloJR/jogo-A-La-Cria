import pyxel as px

nx  = [0, 180, 360, 540, 720, 900, 1080]
ny  = [150, 150, 150, 150, 150, 150, 150]
nvx = [1, 1, 1, 1, 1, 1, 1]

def update():
    for i in range(len(nx)):
        nvx[i] += 0.001  # Incrementa a velocidade gradualmente
        nx[i] = nx[i] + nvx[i] * 4
        if nx[i] > px.width:
            nx[i] = -180  # Reposiciona o objeto para o início da tela

def draw():
    px.cls(10)
    for i in range(len(nx)):
        x = nx[i]
        y = ny[i]
        px.blt(x, y, 1, 0, -1, 180, 31)  # Ajuste a largura da imagem para 180

px.init(340, 180, title='Hello', fps=60)
px.run(update, draw)

