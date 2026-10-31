import random
import threading
import tkinter as tk
import winsound

numeros_megasena = list(range(1, 61))

# ---------------- Sons (nativos do Windows, sem instalar nada) ----------------
SOM_ATIVADO = True


def _beep_async(frequencia, duracao_ms):
    """Toca um beep em thread separada para não travar a animação."""
    def tocar():
        try:
            winsound.Beep(frequencia, duracao_ms)
        except RuntimeError:
            pass
    threading.Thread(target=tocar, daemon=True).start()


def som_tique():
    """Tique curto durante o embaralhamento."""
    if SOM_ATIVADO:
        _beep_async(1200, 40)


def som_bola_revelada():
    """Plim mais agudo quando cada bola trava."""
    if SOM_ATIVADO:
        _beep_async(880, 120)


def som_fanfarra():
    """Fanfarra de vitória: sequência de notas (dó-mi-sol-dó)."""
    if not SOM_ATIVADO:
        return

    def tocar():
        try:
            for freq, dur in [(523, 150), (659, 150), (784, 150),
                              (1047, 400), (784, 150), (1047, 500)]:
                winsound.Beep(freq, dur)
        except RuntimeError:
            pass
    threading.Thread(target=tocar, daemon=True).start()


# ---------------- Lógica do sorteio (mantida) ----------------
def sortear():
    """Sorteia 6 números únicos de 1 a 60, ordenados."""
    return sorted(random.sample(numeros_megasena, 6))


# ---------------- Interface gráfica ----------------
# Cores estilo Mega-Sena (bolas brancas com número azul sobre fundo verde)
COR_FUNDO = "#006341"      # verde loteria
COR_BOLA = "white"
COR_BOLA_OCULTA = "#c8d6cc"  # bola ainda não revelada
COR_BORDA_BOLA = "#00442d"
COR_NUMERO = "#003399"
COR_NUMERO_TEMP = "#4a6b5d"  # número temporário durante o embaralhamento
COR_TEXTO = "white"
COR_BOTAO = "#FFC107"      # amarelo destaque
COR_BOTAO_TEXTO = "#003300"

NUM_BOLAS = 6
RAIO_BOLA = 45
ESPACO_ENTRE_BOLAS = 30
ALTURA_QUIQUE = 28        # quantos pixels a bola sobe ao quicar
TEMPO_EMBARALHAR_MS = 90  # velocidade do embaralhamento
PASSOS_POR_BOLA = 9       # quantas trocas antes de travar cada bola

janela = tk.Tk()
janela.title("Sorteio da Mega-Sena 🍀")
janela.configure(bg=COR_FUNDO)
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="🍀 Números da Sorte 🍀",
    font=("Arial", 22, "bold"),
    bg=COR_FUNDO,
    fg=COR_TEXTO,
)
titulo.pack(pady=(20, 5))

subtitulo = tk.Label(
    janela,
    text="Mega-Sena — 6 números de 1 a 60",
    font=("Arial", 11),
    bg=COR_FUNDO,
    fg=COR_TEXTO,
)
subtitulo.pack(pady=(0, 15))

largura_canvas = NUM_BOLAS * (RAIO_BOLA * 2) + (NUM_BOLAS - 1) * ESPACO_ENTRE_BOLAS + 40
altura_canvas = RAIO_BOLA * 2 + ALTURA_QUIQUE + 50
canvas = tk.Canvas(
    janela,
    width=largura_canvas,
    height=altura_canvas,
    bg=COR_FUNDO,
    highlightthickness=0,
)
canvas.pack(padx=20)

# Confete: desenhado no MESMO canvas das bolas (com tag "confete").
# Motivo: a classe Canvas sobrescreve lift/tkraise para tag_raise
# (vide tkinter/__init__.py: lift = tkraise = tag_raise), então um
# segundo canvas quebra ao tentar trazer para frente. Com tag não
# precisa de lift — item criado depois já fica por cima.
CORES_CONFETE = ["#FF5252", "#FFD740", "#69F0AE", "#40C4FF",
                 "#E040FB", "#FF6E40", "#FFFFFF", "#FFEB3B"]
QTD_CONFETES = 120
confetes = []
confete_animando = False

# Guarda os IDs dos desenhos para poder redesenhar a cada frame
bolas_ids = []

# Estado da animação (estilo globo da Mega-Sena)
animando = False
sorteio_final = []
indice_revelado = 0
passo_atual = 0


def centro_da_bola(i):
    """Posição base (x, y) da bola i — y já com folga para o quique."""
    x = 20 + RAIO_BOLA + i * (RAIO_BOLA * 2 + ESPACO_ENTRE_BOLAS)
    y = ALTURA_QUIQUE + 20 + RAIO_BOLA
    return x, y


def desenhar_uma_bola(x, y, texto, revelada=True):
    """Desenha uma única bola de loteria e devolve os IDs criados."""
    ids = []
    ids.append(canvas.create_oval(
        x - RAIO_BOLA + 3, y - RAIO_BOLA + 5,
        x + RAIO_BOLA + 3, y + RAIO_BOLA + 5,
        fill="#00331f", outline="", tags=("bola",),
    ))
    ids.append(canvas.create_oval(
        x - RAIO_BOLA, y - RAIO_BOLA,
        x + RAIO_BOLA, y + RAIO_BOLA,
        fill=COR_BOLA if revelada else COR_BOLA_OCULTA,
        outline=COR_BORDA_BOLA, width=4, tags=("bola",),
    ))
    ids.append(canvas.create_oval(
        x - RAIO_BOLA + 12, y - RAIO_BOLA + 8,
        x - RAIO_BOLA + 38, y - RAIO_BOLA + 30,
        fill="#e8f0ff", outline="", tags=("bola",),
    ))
    ids.append(canvas.create_text(
        x, y + 2,
        text=str(texto),
        font=("Arial", 26, "bold"),
        fill=COR_NUMERO if revelada else COR_NUMERO_TEMP,
        tags=("bola",),
    ))
    return ids


def limpar_bolas():
    global bolas_ids
    canvas.delete("bola")  # apaga só as bolas, preserva o confete
    bolas_ids = []


def desenhar_frame(numeros_visiveis, reveladas, offsets_y):
    """Redesenha todas as bolas (um frame da animação)."""
    limpar_bolas()
    for i in range(NUM_BOLAS):
        x_base, y_base = centro_da_bola(i)
        y = y_base + offsets_y[i]
        for _id in desenhar_uma_bola(x_base, y, numeros_visiveis[i], revelada=reveladas[i]):
            bolas_ids.append(_id)


def etapa_animacao():
    """Um passo da animação: bolas não reveladas quicam com números girando."""
    global indice_revelado, passo_atual, animando
    numeros_visiveis = []
    reveladas = []
    offsets_y = []
    for i in range(NUM_BOLAS):
        if i < indice_revelado:
            numeros_visiveis.append(sorteio_final[i])
            reveladas.append(True)
            offsets_y.append(0)
        elif i == indice_revelado:
            if passo_atual < PASSOS_POR_BOLA:
                numeros_visiveis.append(random.randint(1, 60))
                reveladas.append(False)
                offsets_y.append(-random.randint(0, ALTURA_QUIQUE))
            else:
                numeros_visiveis.append(sorteio_final[i])
                reveladas.append(True)
                offsets_y.append(-12)
        else:
            numeros_visiveis.append("?")
            reveladas.append(False)
            offsets_y.append(-random.randint(0, ALTURA_QUIQUE // 2))
    desenhar_frame(numeros_visiveis, reveladas, offsets_y)
    som_tique()
    if passo_atual < PASSOS_POR_BOLA:
        passo_atual += 1
        janela.after(TEMPO_EMBARALHAR_MS, etapa_animacao)
    else:
        passo_atual = 0
        indice_revelado += 1
        som_bola_revelada()
        if indice_revelado < NUM_BOLAS:
            resultado_label.config(text=f"Revelando bola {indice_revelado + 1} de {NUM_BOLAS}... 🎱")
            janela.after(350, etapa_animacao)
        else:
            finalizar_sorteio()


def iniciar_confete():
    """Cria 120 pedacinhos de confete no topo e inicia a queda."""
    global confetes, confete_animando
    parar_confete()
    # Desenha no MESMO canvas, com tag "confete": criado depois das
    # bolas, já fica por cima. Sem segundo canvas, sem lift, sem erro.
    for _ in range(QTD_CONFETES):
        x = random.randint(0, largura_canvas)
        y = random.randint(-altura_canvas, 0)
        tamanho = random.randint(5, 10)
        cor = random.choice(CORES_CONFETE)
        forma = random.choice(["rect", "oval"])
        if forma == "rect":
            _id = canvas.create_rectangle(
                x, y, x + tamanho, y + tamanho * 2 // 3,
                fill=cor, outline="", tags=("confete",))
        else:
            _id = canvas.create_oval(
                x, y, x + tamanho, y + tamanho,
                fill=cor, outline="", tags=("confete",))
        confetes.append({
            "id": _id,
            "vy": random.uniform(2.0, 5.5),   # velocidade de queda
            "vx": random.uniform(-1.5, 1.5),  # deriva lateral
            "giro": random.uniform(-8, 8),    # balanço lateral
            "fase": random.uniform(0, 6.28),
        })
    confete_animando = True
    animar_confete()


def animar_confete():
    """Um frame da queda do confete."""
    global confete_animando
    if not confete_animando:
        return
    import math
    vivos = False
    for c in confetes:
        c["fase"] += 0.15
        dx = c["vx"] + math.sin(c["fase"]) * 1.2
        canvas.move(c["id"], dx, c["vy"])
        x1, y1, x2, y2 = canvas.coords(c["id"])
        if y1 < altura_canvas + 20:
            vivos = True
        else:
            # Recicla para o topo para a festa continuar
            canvas.move(c["id"], random.randint(0, largura_canvas) - x1,
                        -altura_canvas - 20)
            vivos = True
    if vivos and confete_animando:
        janela.after(30, animar_confete)


def parar_confete():
    """Limpa o confete da tela."""
    global confetes, confete_animando
    confete_animando = False
    canvas.delete("confete")  # apaga só os itens com a tag
    confetes = []


def finalizar_sorteio():
    """Termina a animação: fixa as bolas, toca fanfarra e solta confete."""
    global animando
    desenhar_frame(sorteio_final, [True] * NUM_BOLAS, [0] * NUM_BOLAS)
    resultado_label.config(text="🎉 Boa sorte! 🍀 🎉")
    botao_sortear.config(state="normal", text="🎲 Sortear Novamente")
    animando = False
    som_fanfarra()
    iniciar_confete()


def novo_sorteio():
    """Sorteia novos números e inicia a animação estilo globo."""
    global animando, sorteio_final, indice_revelado, passo_atual
    if animando:
        return
    sorteio_final = sortear()
    print(sorteio_final)
    animando = True
    indice_revelado = 0
    passo_atual = 0
    parar_confete()
    botao_sortear.config(state="disabled", text="🎱 Sorteando...")
    resultado_label.config(text="Sorteando... 🎱")
    etapa_animacao()


resultado_label = tk.Label(
    janela,
    text="Sorteando... 🎱",
    font=("Arial", 12, "italic"),
    bg=COR_FUNDO,
    fg=COR_TEXTO,
)
resultado_label.pack(pady=(10, 5))

botao_sortear = tk.Button(
    janela,
    text="🎱 Sorteando...",
    font=("Arial", 14, "bold"),
    bg=COR_BOTAO,
    fg=COR_BOTAO_TEXTO,
    activebackground="#ffda4d",
    relief="raised",
    bd=3,
    padx=20,
    pady=10,
    cursor="hand2",
    command=novo_sorteio,
)
botao_sortear.pack(pady=(5, 5))


def alternar_som():
    """Liga/desliga todos os sons."""
    global SOM_ATIVADO
    SOM_ATIVADO = not SOM_ATIVADO
    botao_som.config(text="🔊 Som: ON" if SOM_ATIVADO else "🔇 Som: OFF")


botao_som = tk.Button(
    janela,
    text="🔊 Som: ON",
    font=("Arial", 10),
    bg="#00442d",
    fg=COR_TEXTO,
    activebackground="#005a3c",
    activeforeground=COR_TEXTO,
    relief="flat",
    padx=10,
    pady=5,
    cursor="hand2",
    command=alternar_som,
)
botao_som.pack(pady=(0, 15))

# Sorteio inicial já com animação (também exibido no terminal)
janela.after(500, novo_sorteio)

janela.mainloop()
