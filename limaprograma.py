import pygame
import random
from pygame.locals import *
import time
from sys import exit

pygame.init()
clock = pygame.time.Clock()
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Múltiplas Abas no Pygame")

input_box = pygame.Rect(70, 150, 500, 40)
cor_input = (255, 255, 255)
cor_borda_ativa = (0, 120, 215)
cor_borda_inativa = (200, 200, 200)
ativo = False
texto_input = ''
nomes_jogadores = []
time1 = []
time2 = []
pontuacao_time1 = 0
pontuacao_time2 = 0

pontuacao_jogadores = {}

pygame.mouse.set_visible(False)

try:
    cursor_img = pygame.image.load("cursor.png").convert_alpha()
    cursor_img = pygame.transform.scale(cursor_img, (100, 100))
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    exit()

fundo_menu = pygame.image.load("fundo.png.png").convert()
fundo_tela = pygame.image.load("LIpE 2.0.png").convert()

cor_botao = (0, 255, 0)
cor_botao_hover = (0, 200, 0)
cor_texto = (255, 255, 255)
fonte = pygame.font.Font(None, 36)

botao_rect = pygame.Rect(240, 280, 180, 50)
texto_botao = fonte.render("Clique Aqui", True, cor_texto)

botao_jogo = pygame.Rect(420, 0, 230, 50)
texto_jogo = fonte.render("Ir para o JOGO", True, cor_texto)

botao_voltar = pygame.Rect(200,400,240,50)
texto_voltar = fonte.render("Voltar", True, cor_texto)

botao_menu = pygame.Rect(200, 400, 240, 50)
botao_chamada = pygame.Rect(200, 400, 240, 50)
texto_chamada = fonte.render("Iniciar Chamada", True, cor_texto)

texto_menu = fonte.render("Voltar ao Menu", True, cor_texto)

botao_sortear = pygame.Rect(70, 300, 180, 40)
texto_sortear = fonte.render("Sortear Times", True, cor_texto)

botao_ver_times = pygame.Rect(400, 300, 140, 40)
texto_ver_times = fonte.render("Ver Times", True, cor_texto)

botao_chamar = pygame.Rect(400, 36, 300, 40)
texto_chamar = fonte.render("Chamar Jogadores", True, cor_texto)

botao_acertou = pygame.Rect(150, 400, 150, 50)
texto_acertou = fonte.render("Acertou", True, cor_texto)

botao_errou = pygame.Rect(340, 400, 150, 50)
texto_errou = fonte.render("Errou", True, cor_texto)

tela_atual = "menu"
indice_chamada = 0
tempo_ultimo_nome = 0
mostrar_fim = False

# Chamada de jogadores
chamada_jogadores = []

jogo_finalizado = False
sobreviventes_time1 = []
sobreviventes_time2 = []

def sortear_times():
    global time1, time2, pontuacao_jogadores
    nomes_embaralhados = nomes_jogadores.copy()
    random.shuffle(nomes_embaralhados)
    meio = len(nomes_embaralhados) // 2
    time1 = nomes_embaralhados[:meio]
    time2 = nomes_embaralhados[meio:]

    if len(time1) != len(time2):
        if len(time1) < len(time2):
            time1.append(time1[0])  # Dá uma vida extra
        else:
            time2.append(time2[0])

    pontuacao_jogadores = {nome: 0 for nome in time1 + time2}

def desenhar_menu():
    tela.blit(fundo_menu, (0, 0))
    cor = cor_botao_hover if botao_jogo.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor, botao_jogo)
    tela.blit(texto_jogo, (botao_jogo.x + 30, botao_jogo.y + 10))

    cor2 = cor_botao_hover if botao_rect.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor2, botao_rect)
    tela.blit(texto_botao, (botao_rect.x + 20, botao_rect.y + 10))

def desenhar_tela2():
    tela.blit(fundo_tela, (0, 0))
    instrucoes = fonte.render("Digite o nome de todos os players e clique OK:", True, cor_texto)
    tela.blit(instrucoes, (70, 100))

    borda = cor_borda_ativa if ativo else cor_borda_inativa
    pygame.draw.rect(tela, borda, input_box, 2)
    texto_renderizado = fonte.render(texto_input, True, (0, 0, 0))
    tela.fill(cor_input, input_box)
    tela.blit(texto_renderizado, (input_box.x + 5, input_box.y + 5))

    y_base = input_box.y + 60
    ultimos_nomes = nomes_jogadores[-3:]
    for i, nome in enumerate(ultimos_nomes):
        indice_jogador = len(nomes_jogadores) - len(ultimos_nomes) + i
        nome_renderizado = fonte.render(f"{indice_jogador+1}. {nome}", True, cor_texto)
        tela.blit(nome_renderizado, (input_box.x, y_base + i * 30))

    cor = cor_botao_hover if botao_menu.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor, botao_menu)
    tela.blit(texto_menu, (botao_menu.x + 20, botao_menu.y + 10))

    cor3 = cor_botao_hover if botao_sortear.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor3, botao_sortear)
    tela.blit(texto_sortear, (botao_sortear.x + 10, botao_sortear.y + 5))

    cor4 = cor_botao_hover if botao_ver_times.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor4, botao_ver_times)
    tela.blit(texto_ver_times, (botao_ver_times.x + 10, botao_ver_times.y + 5))

    cor5 = cor_botao_hover if botao_chamar.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor5, botao_chamar)
    tela.blit(texto_chamar, (botao_chamar.x + 10, botao_chamar.y + 5))

def desenhar_tela_times():
    tela.blit(fundo_tela, (0, 0))
    titulo = fonte.render("Times Sorteados", True, cor_texto)
    tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 40))

    cor5 = cor_botao_hover if botao_chamada.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor5, botao_chamada)
    tela.blit(texto_chamada, (botao_chamada.x + 10, botao_chamada.y + 10))

    tela.blit(fonte.render("Time Vermelho:", True, (255, 0, 0)), (100, 100))
    for i, nome in enumerate(time1):
        tela.blit(fonte.render(nome, True, cor_texto), (120, 130 + i * 30))

    tela.blit(fonte.render("Time Azul:", True, (0, 0, 255)), (400, 100))
    for i, nome in enumerate(time2):
        tela.blit(fonte.render(nome, True, cor_texto), (420, 130 + i * 30))

    cor = cor_botao_hover if botao_voltar.collidepoint(pygame.mouse.get_pos()) else cor_botao
    pygame.draw.rect(tela, cor, botao_voltar)
    tela.blit(texto_voltar, (botao_voltar.x +80, botao_voltar.y + 10))

def preparar_chamada():
    global chamada_jogadores, indice_chamada, jogo_finalizado
    chamada_jogadores = time1 + time2
    random.shuffle(chamada_jogadores)
    indice_chamada = 0
    jogo_finalizado = False

def desenhar_fim():
    global pontuacao_time1, pontuacao_time2
    tela.blit(fundo_tela, (0, 0))
    titulo = fonte.render("FIM DE JOGO!", True, cor_texto)
    tela.blit(titulo, (largura//2 - titulo.get_width()//2, 30))

    tela.blit(fonte.render("Time Vermelho:", True, (255, 0, 0)), (50, 80))
    y = 120
    for nome in pontuacao_jogadores:
        if nome in sobreviventes_time1:
            texto = fonte.render(f"{nome} + {pontuacao_jogadores[nome]} pontos", True, (255,0,0))
            tela.blit(texto, (60, y))
            y += 30

    tela.blit(fonte.render("Time Azul:", True, (255, 255, 255)), (350, 80))
    y = 120
    for nome in pontuacao_jogadores:
        if nome in sobreviventes_time2:
            texto = fonte.render(f"{nome} + {pontuacao_jogadores[nome]} pontos", True, cor_texto)
            tela.blit(texto, (360, y))
            y += 30

def desenhar_tela_chamada():
    global jogo_finalizado
    tela.blit(fundo_tela, (0, 0))

    if not jogo_finalizado and chamada_jogadores:
        nome = chamada_jogadores[indice_chamada]
        cor_texto_nome = (255, 0, 0) if nome in time1 else (0, 0, 255)
        texto = fonte.render(nome, True, cor_texto_nome)
        tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))

        pygame.draw.rect(tela, cor_botao_hover, botao_acertou)
        tela.blit(texto_acertou, (botao_acertou.x + 10, botao_acertou.y + 10))

        pygame.draw.rect(tela, cor_botao_hover, botao_errou)
        tela.blit(texto_errou, (botao_errou.x + 10, botao_errou.y + 10))
    else:
        desenhar_fim()

def finalizar_jogo():
    global jogo_finalizado, sobreviventes_time1, sobreviventes_time2
    jogo_finalizado = True
    sobreviventes_time1 = [nome for nome in pontuacao_jogadores if nome in time1]
    sobreviventes_time2 = [nome for nome in pontuacao_jogadores if nome in time2]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if tela_atual == "menu":
                if botao_jogo.collidepoint(event.pos):
                    tela_atual = "jogo"

            elif tela_atual == "jogo":
                if botao_sortear.collidepoint(event.pos):
                    if len(nomes_jogadores) >= 2:
                        sortear_times()
                elif botao_ver_times.collidepoint(event.pos):
                    if time1 or time2:
                        tela_atual = "times"
                elif botao_menu.collidepoint(event.pos):
                    tela_atual = "menu"
                elif botao_chamar.collidepoint(event.pos):
                    if time1 and time2:
                        preparar_chamada()
                        tela_atual = "chamada"
                elif input_box.collidepoint(event.pos):
                    ativo = True
                else:
                    ativo = False

            elif tela_atual == "times":
                if botao_menu.collidepoint(event.pos):
                    tela_atual = "jogo"
                elif botao_chamada.collidepoint(event.pos):
                    preparar_chamada()
                    tela_atual = "chamada"

            elif tela_atual == "chamada" and not jogo_finalizado:
                nome = chamada_jogadores[indice_chamada]
                if botao_acertou.collidepoint(event.pos):
                    pontuacao_jogadores[nome] += 1
                    indice_chamada = (indice_chamada + 1) % len(chamada_jogadores)
                elif botao_errou.collidepoint(event.pos):
                    chamada_jogadores.remove(nome)
                    if not chamada_jogadores:
                        finalizar_jogo()
                    else:
                        indice_chamada = indice_chamada % len(chamada_jogadores)

        if event.type == KEYDOWN and tela_atual == "jogo":
            if ativo:
                if event.key == K_RETURN:
                    if texto_input.strip():
                        nomes_jogadores.append(texto_input.strip())
                        texto_input = ''
                elif event.key == K_BACKSPACE:
                    texto_input = texto_input[:-1]
                else:
                    texto_input += event.unicode

    if tela_atual == "menu":
        desenhar_menu()
    elif tela_atual == "jogo":
        desenhar_tela2()
    elif tela_atual == "times":
        desenhar_tela_times()
    elif tela_atual == "chamada":
        desenhar_tela_chamada()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    tela.blit(cursor_img, (mouse_x - 50, mouse_y - 50))

    pygame.display.update()
    clock.tick(60)
