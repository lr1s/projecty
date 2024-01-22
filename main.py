import pygame
import sqlite3

pygame.init()

screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)

FPS = 60  # Частота обновления экрана
XS = 0  # Координата Х корабля
XS2 = 0
YR = 650  # Координата У торпеды
XR = 640  # Координата Х Торпеды
XH = 640  # Координата Х попадания
XP = 640  # Координата Х прицела

# Вспомогательные переменные для вычисления траектории торпеды
XXP = 0
XYP = 0
XXR = 0
YYR = 0

FIRE = False  # True если запуск
PP = False  # True если попадание
PP2 = False
PRIGHT = False  # True если ВПРАВО
PLEFT = False  # True если ВЛЕВО
PESC = False
HITS = 0  # Кол-во попаданий
MISS = 0  # Кол-во Промахов
AMMO = 10  # Кол-во торпед
SKIPS = 0
LVL = 1
SHITS = 0
SMISS = 0
SSKIPS = 0

boom = pygame.mixer.Sound('Boom.mp3')
fire = pygame.mixer.Sound('Fire.mp3')


# Описание класса спрайта Корабля
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 370))


# Описание класса спрайта Перископ
class Pr(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 360))


# Описание класса спрайта Торпеда
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))


# Описание класса спрайта Попадания
class Hit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sheet = pygame.image.load('Hits.png')
        rows = 6
        columns = 8
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for k in range(columns):
                frame_location = (self.rect.w * k, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# Описание класса спрайта Торпеда
class Aim(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 420))


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))


def printtxt(txt, fnsz, x, y):
    fnt = pygame.font.Font(None, fnsz, )
    txt1 = fnt.render(txt, True, (255, 0, 0))
    screen.blit(txt1, (x, y))


def gameexit():
    kesc = True
    mpress = False
    nxtpress = False
    mnpress = False

    xesc = 638
    yesc = 198
    xnxt = 638
    ynxt = 298
    xmn = 638
    ymn = 398

    bgex = pygame.image.load('backgroundex.png')
    screen.blit(bgex, (0, 0))

    bexit = Button(xesc, yesc, 'Buttonexit.png')
    screen.blit(bexit.image, bexit.rect)

    bnxt = Button(xnxt, ynxt, 'Buttonnxt.png')
    screen.blit(bnxt.image, bnxt.rect)

    bmn = Button(xmn, ymn, 'Buttonmenu.png')
    screen.blit(bmn.image, bmn.rect)

    while kesc:
        for eventex in pygame.event.get():
            if eventex.type == pygame.KEYDOWN:
                if eventex.key == pygame.K_ESCAPE:  # выход при нажатии ESC
                    pygame.quit()
                    exit()
                elif eventex.key == pygame.K_RETURN:
                    kesc = False

            if eventex.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and bexit.rect.collidepoint(pygame.mouse.get_pos()):
                    mpress = True
                if pygame.mouse.get_pressed()[0] and bnxt.rect.collidepoint(pygame.mouse.get_pos()):
                    nxtpress = True
                if pygame.mouse.get_pressed()[0] and bmn.rect.collidepoint(pygame.mouse.get_pos()):
                    mnpress = True

            if eventex.type == pygame.MOUSEBUTTONUP:
                if mpress and bexit.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
                if nxtpress and bnxt.rect.collidepoint(pygame.mouse.get_pos()):
                    kesc = False
                if mnpress and bmn.rect.collidepoint(pygame.mouse.get_pos()):
                    kesc = False
                    menu()

                mpress = False
                nxtpress = False
                mnpress = False

        if mpress:
            xesc = 638
            yesc = 198
        else:
            xesc = 640
            yesc = 200

        if nxtpress:
            xnxt = 638
            ynxt = 298
        else:
            xnxt = 640
            ynxt = 300

        if mnpress:
            xmn = 638
            ymn = 398
        else:
            xmn = 640
            ymn = 400

        bgex = pygame.image.load('backgroundex.png')
        screen.blit(bgex, (0, 0))

        bexit = Button(xesc, yesc, 'Buttonexit.png')
        screen.blit(bexit.image, bexit.rect)

        bnxt = Button(xnxt, ynxt, 'Buttonnxt.png')
        screen.blit(bnxt.image, bnxt.rect)

        bmn = Button(xmn, ymn, 'Buttonmenu.png')
        screen.blit(bmn.image, bmn.rect)

        pygame.display.update()


def levelup():
    kesc = True
    xnxt = 1048
    ynxt = 648
    xext = 228
    yext = 648

    global HITS
    global MISS
    global AMMO
    global SKIPS
    global LVL
    global SHITS
    global SMISS
    global SSKIPS

    nxtpress = False
    extpress = False

    bgex = pygame.image.load('backgroundex.png')
    screen.blit(bgex, (0, 0))

    bnxt = Button(xnxt, ynxt, 'Buttonnxt.png')
    screen.blit(bnxt.image, bnxt.rect)

    bext = Button(xext, yext, 'Buttonexit.png')
    screen.blit(bext.image, bext.rect)

    while kesc:
        for eventex in pygame.event.get():
            if eventex.type == pygame.KEYDOWN:
                if eventex.key == pygame.K_ESCAPE:  # выход при нажатии ESC
                    pygame.quit()
                    exit()
                elif eventex.key == pygame.K_RETURN:
                    kesc = False

            if eventex.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and bnxt.rect.collidepoint(pygame.mouse.get_pos()):
                    nxtpress = True
                elif pygame.mouse.get_pressed()[0] and bext.rect.collidepoint(pygame.mouse.get_pos()):
                    extpress = True

            if eventex.type == pygame.MOUSEBUTTONUP:
                if nxtpress and bnxt.rect.collidepoint(pygame.mouse.get_pos()):
                    HITS = 0
                    MISS = 0
                    AMMO = 10
                    SKIPS = 0
                    LVL += 1
                    kesc = False

                if extpress and bext.rect.collidepoint(pygame.mouse.get_pos()):
                    HITS = 0
                    MISS = 0
                    AMMO = 10
                    SKIPS = 0
                    LVL = 1
                    SHITS = 0
                    SMISS = 0
                    SSKIPS = 0
                    kesc = False
                    menu()
                nxtpress = False
                extpress = False

            if nxtpress:
                xnxt = 1048
                ynxt = 648
            else:
                xnxt = 1050
                ynxt = 650

            if extpress:
                xext = 228
                yext = 648
            else:
                xext = 230
                yext = 650

        bgex = pygame.image.load('backgroundex.png')
        screen.blit(bgex, (0, 0))

        bnxt = Button(xnxt, ynxt, 'Buttonnxt.png')
        screen.blit(bnxt.image, bnxt.rect)

        bext = Button(xext, yext, 'Buttonexit.png')
        screen.blit(bext.image, bext.rect)

        fontex = pygame.font.Font(None, 60)
        text1 = fontex.render(('УРОВЕНЬ ' + str(LVL) + ' ПРОЙДЕН'), True, (255, 0, 0))
        text2 = fontex.render('РЕЗУЛЬТАТЫ:', True, (255, 0, 0))
        text3 = fontex.render(('ПОПАДАНИЙ: ' + str(HITS)), True, (255, 0, 0))
        text4 = fontex.render(('ПРОМАХОВ: ' + str(MISS)), True, (255, 0, 0))
        text5 = fontex.render(('ПРОПУЩЕНО: ' + str(SKIPS)), True, (255, 0, 0))
        a = text1.get_rect()
        a1 = 640 - a.width // 2
        screen.blit(text1, (a1, 150))
        screen.blit(text2, (50, 220))
        screen.blit(text3, (50, 300))
        screen.blit(text4, (50, 380))
        screen.blit(text5, (50, 460))

        pygame.display.update()


def gamedone():
    kesc = True
    xmn = 1048
    ymn = 648
    xext = 228
    yext = 648
    xsv = 228
    ysv = 548

    mnpress = False
    extpress = False
    svpress = False

    bgex = pygame.image.load('backgroundex.png')
    screen.blit(bgex, (0, 0))

    bmn = Button(xmn, ymn, 'Buttonmenu.png')
    screen.blit(bmn.image, bmn.rect)

    bext = Button(xext, yext, 'Buttonexit.png')
    screen.blit(bext.image, bext.rect)

    bsv = Button(xsv, ysv, 'Buttonsave.png')
    screen.blit(bsv.image, bsv.rect)

    while kesc:
        for eventex in pygame.event.get():
            if eventex.type == pygame.KEYDOWN:
                if eventex.key == pygame.K_ESCAPE:  # выход при нажатии ESC (потом сделать финальное окно)
                    pygame.quit()
                    exit()
                elif eventex.key == pygame.K_RETURN:
                    kesc = False

            if eventex.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and bmn.rect.collidepoint(pygame.mouse.get_pos()):
                    mnpress = True
                elif pygame.mouse.get_pressed()[0] and bext.rect.collidepoint(pygame.mouse.get_pos()):
                    extpress = True
                elif pygame.mouse.get_pressed()[0] and bsv.rect.collidepoint(pygame.mouse.get_pos()):
                    svpress = True

            if eventex.type == pygame.MOUSEBUTTONUP:
                if mnpress and bmn.rect.collidepoint(pygame.mouse.get_pos()):
                    kesc = False
                    menu()

                if svpress and bsv.rect.collidepoint(pygame.mouse.get_pos()):
                    save()
                if extpress and bext.rect.collidepoint(pygame.mouse.get_pos()):
                    kesc = False
                    gameexit()

                mnpress = False
                extpress = False
                svpress = False

            if mnpress:
                xmn = 1048
                ymn = 648
            else:
                xmn = 1050
                ymn = 650

            if extpress:
                xext = 228
                yext = 648
            else:
                xext = 230
                yext = 650

            if svpress:
                xsv = 228
                ysv = 548
            else:
                xsv = 230
                ysv = 550

        bgex = pygame.image.load('backgroundex.png')
        screen.blit(bgex, (0, 0))

        bnxt = Button(xmn, ymn, 'Buttonmenu.png')
        screen.blit(bnxt.image, bnxt.rect)

        bext = Button(xext, yext, 'Buttonexit.png')
        screen.blit(bext.image, bext.rect)

        bsv = Button(xsv, ysv, 'Buttonsave.png')
        screen.blit(bsv.image, bsv.rect)

        fontex = pygame.font.Font(None, 60)
        text1 = fontex.render('ИГРА ЗАВЕРШЕНА', True, (255, 0, 0))
        text2 = fontex.render('РЕЗУЛЬТАТЫ:', True, (255, 0, 0))
        text3 = fontex.render(('ПОПАДАНИЙ: ' + str(SHITS)), True, (255, 0, 0))
        text4 = fontex.render(('ПРОМАХОВ: ' + str(SMISS)), True, (255, 0, 0))
        text5 = fontex.render(('ПРОПУЩЕНО: ' + str(SSKIPS)), True, (255, 0, 0))
        a = text1.get_rect()
        a1 = 640 - a.width // 2
        screen.blit(text1, (a1, 150))
        screen.blit(text2, (50, 220))
        screen.blit(text3, (50, 300))
        screen.blit(text4, (50, 380))
        screen.blit(text5, (50, 460))

        pygame.display.update()


def addresult(name, hits, miss, skips):
    conn = sqlite3.connect('result.db')
    cur = conn.cursor()

    cur.execute('INSERT INTO Result (Gamer, Hits, Miss, Skips) VALUES (?, ?, ?, ?)', (name, hits, miss, skips))

    conn.commit()


def showresult():
    xmn = 1048
    ymn = 648

    kesc = True
    mnpress = False

    bgex = pygame.image.load('backgroundex.png')
    screen.blit(bgex, (0, 0))

    conn = sqlite3.connect('result.db')
    cur = conn.cursor()

    bmn = Button(xmn, ymn, 'Buttonmenu.png')
    screen.blit(bmn.image, bmn.rect)

    while kesc:
        for eventex in pygame.event.get():
            if eventex.type == pygame.KEYDOWN:
                if eventex.key == pygame.K_ESCAPE:
                    menu()
                    kesc = False
            if eventex.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and bmn.rect.collidepoint(pygame.mouse.get_pos()):
                    mnpress = True

            if eventex.type == pygame.MOUSEBUTTONUP:
                if mnpress and bmn.rect.collidepoint(pygame.mouse.get_pos()):
                    kesc = False
                    menu()

                mnpress = False

        if mnpress:
            xmn = 1048
            ymn = 648
        else:
            xmn = 1050
            ymn = 650

        bgex = pygame.image.load('backgroundex.png')
        screen.blit(bgex, (0, 0))

        printtxt('ИГРОК', 50, 50, 50)
        printtxt('ПОПАДАНИЯ', 50, 200, 50)
        printtxt('ПРОМАХИ', 50, 450, 50)
        printtxt('ПРОПУЩЕНО', 50, 650, 50)

        a = 100
        cur.execute('SELECT Gamer FROM Result')
        gamers = cur.fetchall()

        for gm in gamers:
            name = str(gm)[2:-3]
            printtxt(name, 40, 50, a)
            a += 40

        cur.execute('SELECT Hits FROM Result')
        hits = cur.fetchall()

        a = 100
        for h in hits:
            hit = str(h)[1:-2]
            printtxt(hit, 40, 250, a)
            a += 40

        cur.execute('SELECT Miss FROM Result')
        miss = cur.fetchall()

        a = 100
        for h in miss:
            mis = str(h)[1:-2]
            printtxt(mis, 40, 500, a)
            a += 40

        cur.execute('SELECT Skips FROM Result')
        skips = cur.fetchall()

        a = 100
        for h in skips:
            skip = str(h)[1:-2]
            printtxt(skip, 40, 700, a)
            a += 40

        bmn = Button(xmn, ymn, 'Buttonmenu.png')
        screen.blit(bmn.image, bmn.rect)

        pygame.display.update()

    conn.commit()


def save():
    xsv = 638
    ysv = 398

    kesc = True
    gamer = ''

    svpress = False

    bsv = Button(xsv, ysv, 'Buttonsave.png')
    screen.blit(bsv.image, bsv.rect)

    while kesc:
        for eventex in pygame.event.get():
            if eventex.type == pygame.KEYDOWN:
                if eventex.key == pygame.K_ESCAPE:  # выход при нажатии ESC
                    pygame.quit()
                    exit()
                elif eventex.key == pygame.K_RETURN:
                    addresult(gamer, SHITS, SMISS, SSKIPS)
                    kesc = False
                elif eventex.key == pygame.K_BACKSPACE:
                    gamer = gamer[:-1]
                else:
                    if len(gamer) < 16:
                        gamer += eventex.unicode

            if eventex.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and bsv.rect.collidepoint(pygame.mouse.get_pos()):
                    svpress = True

            if eventex.type == pygame.MOUSEBUTTONUP:
                if svpress and bsv.rect.collidepoint(pygame.mouse.get_pos()):
                    addresult(gamer, SHITS, SMISS, SSKIPS)
                    kesc = False

                svpress = False

        bgex = pygame.image.load('backgroundex.png')
        screen.blit(bgex, (0, 0))

        fontex = pygame.font.Font(None, 60)

        text1 = fontex.render('ВВЕДИТЕ ИМЯ', True, (255, 0, 0))
        a = text1.get_rect()
        a1 = 640 - a.width // 2
        screen.blit(text1, (a1, 150))

        pygame.draw.rect(screen, (255, 0, 0), (440, 300, 400, 50), 3)

        printtxt(gamer, 60, 445, 305)

        if svpress:
            xsv = 638
            ysv = 398
        else:
            xsv = 640
            ysv = 400

        bsv = Button(xsv, ysv, 'Buttonsave.png')
        screen.blit(bsv.image, bsv.rect)

        pygame.display.update()


def menu():
    kesc = True
    ngpress = False
    respress = False
    extpress = False

    xng = 638
    yng = 198
    xres = 638
    yres = 298
    xext = 638
    yext = 298

    global HITS
    global MISS
    global AMMO
    global SKIPS
    global LVL
    global SHITS
    global SMISS
    global SSKIPS
    global XS2

    bgex = pygame.image.load('backgroundex.png')
    screen.blit(bgex, (0, 0))

    bng = Button(xng, yng, 'Buttonng.png')
    screen.blit(bng.image, bng.rect)

    bres = Button(xres, yres, 'Buttonres.png')
    screen.blit(bres.image, bres.rect)

    bext = Button(xext, yext, 'Buttonexit.png')
    screen.blit(bext.image, bext.rect)

    while kesc:
        for eventex in pygame.event.get():
            if eventex.type == pygame.KEYDOWN:
                if eventex.key == pygame.K_ESCAPE:  # выход при нажатии ESC
                    pygame.quit()
                    exit()

            if eventex.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and bng.rect.collidepoint(pygame.mouse.get_pos()):
                    ngpress = True
                elif pygame.mouse.get_pressed()[0] and bres.rect.collidepoint(pygame.mouse.get_pos()):
                    respress = True
                elif pygame.mouse.get_pressed()[0] and bext.rect.collidepoint(pygame.mouse.get_pos()):
                    extpress = True

            if eventex.type == pygame.MOUSEBUTTONUP:
                if ngpress and bng.rect.collidepoint(pygame.mouse.get_pos()):
                    HITS = 0
                    MISS = 0
                    AMMO = 10
                    SKIPS = 0
                    LVL = 1
                    SHITS = 0
                    SMISS = 0
                    SSKIPS = 0
                    XS2 = 0
                    kesc = False
                if respress and bres.rect.collidepoint(pygame.mouse.get_pos()):
                    showresult()
                    kesc = False
                if extpress and bext.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()

                ngpress = False
                respress = False
                extpress = False

        if ngpress:
            xng = 638
            yng = 198
        else:
            xng = 640
            yng = 200

        if respress:
            xres = 638
            yres = 298
        else:
            xres = 640
            yres = 300

        if extpress:
            xext = 638
            yext = 398
        else:
            xext = 640
            yext = 400

        bgex = pygame.image.load('backgroundex.png')
        screen.blit(bgex, (0, 0))

        bng = Button(xng, yng, 'Buttonng.png')
        screen.blit(bng.image, bng.rect)

        bres = Button(xres, yres, 'Buttonres.png')
        screen.blit(bres.image, bres.rect)

        bext = Button(xext, yext, 'Buttonexit.png')
        screen.blit(bext.image, bext.rect)

        clock.tick(FPS)

        pygame.display.update()
        pygame.display.flip()


clock = pygame.time.Clock()

menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # выход при нажатии ESC
                PESC = True
            elif event.key == pygame.K_SPACE:  # Нажат пробел
                if not FIRE and AMMO > 0:
                    FIRE = True
                    fire.play()
                    AMMO -= 1
            elif event.key == pygame.K_RIGHT:  # Нажата клавиша ВПРАВО
                PRIGHT = True
            elif event.key == pygame.K_LEFT:  # Нажата клавиша ВЛЕВО
                PLEFT = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:  # Отпущена клавиша ВПРАВО
                PRIGHT = False
            if event.key == pygame.K_LEFT:  # Отпущена клавиша ВЛЕВО
                PLEFT = False
    if PESC:
        gameexit()
        PESC = False

    bg = pygame.image.load('background.png')  # Установка фона
    screen.blit(bg, (0, 0))

    # Создание спрайта Корабль
    Ship1 = Ship(XS, 'ship.png')
    screen.blit(Ship1.image, Ship1.rect)
    # Движение корабля
    if XS < 1280:
        if LVL == 1:
            XS += 5
        else:
            XS += 10
    else:
        XS = 0
        SKIPS += 1

    Ship2 = Ship(XS2, 'ship.png')
    screen.blit(Ship2.image, Ship2.rect)
    if LVL == 3:
        if XS > 800 and not PP:
            XS2 = XS - 800
        elif XS2 < 1280:
            XS2 += 10
        else:
            XS2 = 0
            SKIPS += 1

    # Создание спрайта Торпеда
    Rocket1 = Rocket(XR, YR, 'Rocket.png')
    screen.blit(Rocket1.image, Rocket1.rect)
    # Если был выстрел
    if FIRE:
        if YR < 410:
            # Проверка столкновения
            if Rocket1.rect.colliderect(Ship1.rect):  # Если было столкновение, то попал
                PP = True
                XH = XR
                HITS += 1
            elif Rocket1.rect.colliderect(Ship2.rect):
                PP2 = True
                XH = XR
                HITS += 1
            else:  # Если не было, то промах
                MISS += 1
            YR = 650
            FIRE = False
            XR = 640
        # Расчет траектории торпеды в зависимости от положения прицела
        else:
            XXP = XP - 640
            XYP = XXP / 230
            YYR = 650 - YR
            XR = XYP * YYR + 640
            YR -= 10

    # Если было попадание
    if PP:
        hit1 = Hit(XH - 100, 330)
        screen.blit(hit1.image, hit1.rect)
        my_group = pygame.sprite.Group(hit1)
        clock = pygame.time.Clock()
        boom.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            for i in range(48):
                hit1.update()
                my_group.draw(screen)
                pygame.display.update()
                clock.tick(20)
            XS = 0
            YR = 650
            PP = False
            break

    if PP2:
        hit1 = Hit(XH - 100, 330)
        screen.blit(hit1.image, hit1.rect)
        my_group = pygame.sprite.Group(hit1)
        clock = pygame.time.Clock()
        boom.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            for i in range(48):
                hit1.update()
                my_group.draw(screen)
                pygame.display.update()
                clock.tick(20)
            XS = 0
            YR = 650
            PP2 = False
            break

    # Создание спрайта Прицел
    Aim1 = Aim(XP, 'Aim.png')
    screen.blit(Aim1.image, Aim1.rect)
    # Перемещение прицела
    if PRIGHT and XP < 1150:
        XP += 10
    if PLEFT and XP > 130:
        XP -= 10

    # Создание спрайта Перископ
    Pr1 = Pr(640, 'Periscope.png')
    screen.blit(Pr1.image, Pr1.rect)

    # Вывод информации
    font = pygame.font.Font(None, 40)
    TEXT1 = font.render(('БОЕКОМПЛЕКТ: ' + str(AMMO)), True, (180, 0, 0))
    TEXT2 = font.render(('ПОПАДАНИЙ: ' + str(HITS)), True, (180, 0, 0))
    TEXT3 = font.render(('ПРОМАХОВ: ' + str(MISS)), True, (180, 0, 0))
    screen.blit(TEXT1, (120, 670))
    screen.blit(TEXT2, (520, 670))
    screen.blit(TEXT3, (920, 670))

    if AMMO == 0 and not FIRE and not (PP or PP2):
        SHITS += HITS
        SMISS += MISS
        SSKIPS += SKIPS
        if LVL < 3:

            levelup()
        else:
            gamedone()
    clock.tick(FPS)
    pygame.display.update()

    pygame.display.flip()
