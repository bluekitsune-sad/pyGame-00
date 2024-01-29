import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption(" FirstGame ")

# we can also make one by fliping a side to make the other side
walkRight = [pygame.image.load('art/R1.png'), pygame.image.load('art/R2.png'), pygame.image.load('art/R3.png'),
             pygame.image.load('art/R4.png'), pygame.image.load('art/R5.png'), pygame.image.load('art/R6.png'),
             pygame.image.load('art/R7.png'), pygame.image.load('art/R8.png'), pygame.image.load('art/R9.png')]
walkLeft = [pygame.image.load('art/L1.png'), pygame.image.load('art/L2.png'), pygame.image.load('art/L3.png'),
            pygame.image.load('art/L4.png'), pygame.image.load('art/L5.png'), pygame.image.load('art/L6.png'),
            pygame.image.load('art/L7.png'), pygame.image.load('art/L8.png'), pygame.image.load('art/L9.png')]
bg = pygame.image.load('art/bg.jpg')
# bgfrompath = pygame.image.load('../../New folder/Gmae/bg.jpg')
char = pygame.image.load('art/standing.png')

screenWidth = 500

clock = pygame.time.Clock()

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 1) #for unfilled


class enemy(object):
    walkRight = [pygame.image.load('art/R1E.png'), pygame.image.load('art/R2E.png'), pygame.image.load('art/R3E.png'),
                 pygame.image.load('art/R4E.png'), pygame.image.load('art/R5E.png'), pygame.image.load('art/R6E.png'),
                 pygame.image.load('art/R7E.png'), pygame.image.load('art/R8E.png'), pygame.image.load('art/R9E.png'),
                 pygame.image.load('art/R10E.png'), pygame.image.load('art/R11E.png')]
    walkLeft = [pygame.image.load('art/L1E.png'), pygame.image.load('art/L2E.png'), pygame.image.load('art/L3E.png'),
                pygame.image.load('art/L4E.png'), pygame.image.load('art/L5E.png'), pygame.image.load('art/L6E.png'),
                pygame.image.load('art/L7E.png'), pygame.image.load('art/L8E.png'), pygame.image.load('art/L9E.png'),
                pygame.image.load('art/L10E.png'), pygame.image.load('art/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        print("I am hurt")


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (350, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# mainLoop
man = player(300, 410, 64, 64)

goblin = enemy(100, 410, 64, 64, 450)

shootLoop = 0  # bullet cooldown
bullets = []

font = pygame.font.SysFont("comicsans", 30, True, True)
run = True
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        # if bullet.x < 500 and bullet.x > 0:
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(man.x + man.width // 2, round(man.y + man.height // 2), 6, (0, 0, 0), facing))
        shootLoop = 1

    if keys[pygame.K_a] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_d] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_w]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
