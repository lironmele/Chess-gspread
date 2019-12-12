#importing
import pygame, sys, gspread
from oauth2client.service_account import ServiceAccountCredentials

#setting up basic stuff and variables
pygame.init()
loop = True
size = width, height = 752, 752
screen = pygame.display.set_mode((width, height))
white = (255,255,255)
black = (0,0,0)
brown = (185,122,87)
green = (102,255,0)
red = (255,40,0)
pieces = []
selected = None
turn = 1

#google sheets stuff to work with two computers
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("ChessCom").sheet1

class piece:
    def __init__(self, image, pos, team):
        self.char = pygame.image.load("{}.png".format(image))
        self.pos = pos
        self.team = team
        self.king = False
        pieces.append(self)
    def move(self, new_pos):
        for p in pieces:
            if new_pos[0] == p.pos[0] and new_pos[1] == p.pos[1]:
                if self.team != p.team:
                    pieces.remove(p)
                    break
                else: return
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
    def blop(self):
        screen.blit(self.char, self.pos)
class King(piece):
    def __init__(self,image,pos,team):
        piece.__init__(self,image,pos,team)
        self.movement = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
        self.king = True
    def move(self, new_pos):
        global turn
        check = False
        for m in self.movement:
            if self.pos[0]//94 + m[0] == new_pos[0]//94 and self.pos[1]//94 + m[1] == new_pos[1]//94: check = True
        if check == False: return
        for p in pieces:
            if new_pos[0] == p.pos[0] and new_pos[1] == p.pos[1]:
                if self.team != p.team:
                    pieces.remove(p)
                    break
                else: return
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
        turn = turn * -1
class Queen(piece):
    def __init__(self,image,pos,team):
        piece.__init__(self,image,pos,team)
        self.movement = [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7]],[[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7]],[[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]],[[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]],[[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7]],[[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0]],[[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]]
    def move(self, new_pos):
        global turn
        for g in self.movement:
            for m in g:
                if self.pos[0]//94 + m[0] == new_pos[0]//94 and self.pos[1]//94 + m[1] == new_pos[1]//94:
                    for m2 in g[0:g.index(m)+1]:
                        for p in pieces:
                            if self.pos[0]//94 + m2[0] == p.pos[0]//94 and self.pos[1]//94 + m2[1] == p.pos[1]//94:
                                if p is self: continue
                                if self.team == p.team:
                                    if g.index(m2) == 0: return
                                    else:
                                        self.pos[0] = self.pos[0] + (g[g.index(m2) - 1][0] * 94)
                                        self.pos[1] = self.pos[1] + (g[g.index(m2) - 1][1] * 94)
                                        turn = turn * -1
                                        return
                                else:
                                    self.pos = p.pos
                                    turn = turn * -1
                                    pieces.remove(p)
                                    return
        for g in self.movement:
            for m in g:
                if self.pos[0] // 94 + m[0] == new_pos[0] // 94 and self.pos[1] // 94 + m[1] == new_pos[1] // 94:
                    self.pos = new_pos
                    turn = turn * -1
                    return
class Bishop(piece):
    def __init__(self,image,pos,team):
        piece.__init__(self,image,pos,team)
        self.movement = [[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7]],[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]],[[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7]],[[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]]
    def move(self, new_pos):
        global turn
        for g in self.movement:
            for m in g:
                if self.pos[0]//94 + m[0] == new_pos[0]//94 and self.pos[1]//94 + m[1] == new_pos[1]//94:
                    for m2 in g[0:g.index(m)+1]:
                        for p in pieces:
                            if self.pos[0]//94 + m2[0] == p.pos[0]//94 and self.pos[1]//94 + m2[1] == p.pos[1]//94:
                                if p is self: continue
                                if self.team == p.team:
                                    if g.index(m2) == 0: return
                                    else:
                                        self.pos[0] = self.pos[0] + (g[g.index(m2) - 1][0] * 94)
                                        self.pos[1] = self.pos[1] + (g[g.index(m2) - 1][1] * 94)
                                        turn = turn * -1
                                        return
                                else:
                                    self.pos = p.pos
                                    turn = turn * -1
                                    pieces.remove(p)
                                    return
        for g in self.movement:
            for m in g:
                if self.pos[0] // 94 + m[0] == new_pos[0] // 94 and self.pos[1] // 94 + m[1] == new_pos[1] // 94:
                    self.pos = new_pos
                    turn = turn * -1
                    return
class Knight(piece):
    def __init__(self,image,pos,team):
        piece.__init__(self,image,pos,team)
        self.movement = [[1,-2],[2,-1],[2,1],[1,2],[-1,2],[-2,1],[-2,-1],[-1,-2]]
    def move(self, new_pos):
        global turn
        check = False
        for m in self.movement:
            if self.pos[0]//94 + m[0] == new_pos[0]//94 and self.pos[1]//94 + m[1] == new_pos[1]//94: check = True
        if check == False: return
        for p in pieces:
            if new_pos[0] == p.pos[0] and new_pos[1] == p.pos[1]:
                if self.team != p.team:
                    pieces.remove(p)
                    break
                else: return
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
        turn = turn * -1
class Rook(piece):
    def __init__(self,image,pos,team):
        piece.__init__(self,image,pos,team)
        self.movement = [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7]],[[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],[[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]],[[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0]]
    def move(self, new_pos):
        global turn
        for g in self.movement:
            for m in g:
                if self.pos[0]//94 + m[0] == new_pos[0]//94 and self.pos[1]//94 + m[1] == new_pos[1]//94:
                    for m2 in g[0:g.index(m)+1]:
                        for p in pieces:
                            if self.pos[0]//94 + m2[0] == p.pos[0]//94 and self.pos[1]//94 + m2[1] == p.pos[1]//94:
                                if p is self: continue
                                if self.team == p.team:
                                    if g.index(m2) == 0: return
                                    else:
                                        self.pos[0] = self.pos[0] + (g[g.index(m2) - 1][0] * 94)
                                        self.pos[1] = self.pos[1] + (g[g.index(m2) - 1][1] * 94)
                                        turn = turn * -1
                                        return
                                else:
                                    self.pos = p.pos
                                    turn = turn * -1
                                    pieces.remove(p)
                                    return
        for g in self.movement:
            for m in g:
                if self.pos[0] // 94 + m[0] == new_pos[0] // 94 and self.pos[1] // 94 + m[1] == new_pos[1] // 94:
                    self.pos = new_pos
                    turn = turn * -1
                    return
class Pawn(piece):
    def __init__(self,image,pos,team):
        piece.__init__(self,image,pos,team)
        self.first = True
        self.queen = False
        self.movement = [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7]],[[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7]],[[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]],[[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]],[[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7]],[[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0]],[[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]]
    def move(self, new_pos):
        global turn
        if self.queen == True:
            for g in self.movement:
                for m in g:
                    if self.pos[0] // 94 + m[0] == new_pos[0] // 94 and self.pos[1] // 94 + m[1] == new_pos[1] // 94:
                        for m2 in g[0:g.index(m) + 1]:
                            for p in pieces:
                                if self.pos[0] // 94 + m2[0] == p.pos[0] // 94 and self.pos[1] // 94 + m2[1] == p.pos[
                                    1] // 94:
                                    if p is self: continue
                                    if self.team == p.team:
                                        if g.index(m2) == 0:
                                            return
                                        else:
                                            self.pos[0] = self.pos[0] + (g[g.index(m2) - 1][0] * 94)
                                            self.pos[1] = self.pos[1] + (g[g.index(m2) - 1][1] * 94)
                                            turn = turn * -1
                                            return
                                    else:
                                        self.pos = p.pos
                                        turn = turn * -1
                                        pieces.remove(p)
                                        return
            for g in self.movement:
                for m in g:
                    if self.pos[0] // 94 + m[0] == new_pos[0] // 94 and self.pos[1] // 94 + m[1] == new_pos[1] // 94:
                        self.pos = new_pos
                        turn = turn * -1
                        return
        elif self.queen == False:
            if self.team == "b":
                if self.first == True:
                    self.first = False
                    if self.pos[0] == new_pos[0] and self.pos[1] + 188 == new_pos[1]:
                        self.pos = new_pos
                        turn = turn * -1
                        return
                for p in pieces:
                    if self is p: continue
                    elif self.team != p.team:
                        if p.pos == new_pos:
                            if self.pos[0] - 94 == p.pos[0] and self.pos[1] + 94 == p.pos[1] or self.pos[0] + 94 == p.pos[0] and self.pos[1] + 94 == p.pos[1]:
                                self.pos = p.pos
                                turn = turn * -1
                                pieces.remove(p)
                                return
                    if new_pos[0] == p.pos[0] and new_pos[1] == p.pos[1]: return
                if self.pos[0] == new_pos[0] and self.pos[1] + 94 == new_pos[1]:
                    self.pos = new_pos
                    turn = turn * -1
                    if self.queen == False:
                        if new_pos[1] == 658:
                            self.queen = True
                            self.char = pygame.image.load("{}.png".format("B_Queen"))
            elif self.team == "w":
                if self.first == True:
                    self.first = False
                    if self.pos[0] == new_pos[0] and self.pos[1] - 188 == new_pos[1]:
                        self.pos = new_pos
                        turn = turn * -1
                        return
                for p in pieces:
                    if self is p: continue
                    elif self.team != p.team:
                        if p.pos == new_pos:
                            if self.pos[0] - 94 == p.pos[0] and self.pos[1] - 94 == p.pos[1] or self.pos[0] + 94 == p.pos[0] and self.pos[1] - 94 == p.pos[1]:
                                self.pos = p.pos
                                turn = turn * -1
                                pieces.remove(p)
                                if self.queen == False:
                                    if new_pos[1] == 0:
                                        self.queen = True
                                        self.char = pygame.image.load("{}.png".format("W_Queen"))
                                        print(self.char)
                                return
                    if new_pos[0] == p.pos[0] and new_pos[1] == p.pos[1]:return
                if self.pos[0] == new_pos[0] and self.pos[1] - 94 == new_pos[1]:
                    self.pos = new_pos
                    turn = turn * -1
                if self.queen == False:
                    if new_pos[1] == 0:
                        self.queen = True
                        self.char = pygame.image.load("{}.png".format("W_Queen"))
                        print(self.char)

wKing = King("W_King",[94*4,94*7], "w")
wQueen = Queen("W_Queen",[94*3,94*7], "w")
wBishop = Bishop("W_Bishop",[94*2,94*7], "w")
wBishop2 = Bishop("W_Bishop", [94*5,94*7], "w")
wKnight = Knight("W_Knight",[94,94*7], "w")
wKnight2 = Knight("W_Knight", [94*6,94*7], "w")
wRook = Rook("W_Rook",[0,94*7], "w")
wRook2 = Rook("W_Rook", [94*7,94*7], "w")
wPawn = Pawn("W_Pawn",[0,94*6], "w")
wPawn2 = Pawn("W_Pawn", [94,94*6], "w")
wPawn3 = Pawn("W_Pawn", [94*2,94*6], "w")
wPawn4 = Pawn("W_Pawn",[94*3,94*6], "w")
wPawn5 = Pawn("W_Pawn", [94*4,94*6], "w")
wPawn6 = Pawn("W_Pawn", [94*5,94*6], "w")
wPawn7 = Pawn("W_Pawn",[94*6,94*6], "w")
wPawn8 = Pawn("W_Pawn", [94*7,94*6], "w")
bKing = King("B_King",[94*4,0], "b")
bQueen = Queen("B_Queen",[94*3,0], "b")
bBishop = Bishop("B_Bishop",[94*2,0], "b")
bBishop2 = Bishop("B_Bishop", [94*5,0], "b")
bKnight = Knight("B_Knight",[94,0], "b")
bKnight2 = Knight("B_Knight", [94*6,0], "b")
bRook = Rook("B_Rook",[0,0], "b")
bRook2 = Rook("B_Rook", [94*7,0], "b")
bPawn = Pawn("B_Pawn",[0,94], "b")
bPawn2 = Pawn("B_Pawn", [94,94], "b")
bPawn3 = Pawn("B_Pawn", [94*2,94], "b")
bPawn4 = Pawn("B_Pawn",[94*3,94], "b")
bPawn5 = Pawn("B_Pawn", [94*4,94], "b")
bPawn6 = Pawn("B_Pawn", [94*5,94], "b")
bPawn7 = Pawn("B_Pawn",[94*6,94], "b")
bPawn8 = Pawn("B_Pawn", [94*7,94], "b")

def draw_board():
    for i in range(64):
        if (i // 8) % 2 == 0:
            if i % 2 == 1:
                screen.fill((248,222,126), (i % 8 * width // 8, i // 8 * height // 8, 94, 94))
        else:
            if i % 2 == 0:
                screen.fill((248,222,126), (i % 8 * width // 8, i // 8 * height // 8, 94, 94))
    for x in range(9):
        pygame.draw.line(screen, black, (x*(width//8) ,0), (x*(width//8), height), 5)
    for y in range(9):
        pygame.draw.line(screen, black, (0 ,y*(height//8)), (width, y*(height//8)), 5)

def display_mouse():
    if selected is not None:
        pygame.draw.rect(screen, red, [selected.pos[0],selected.pos[1],94,94],7)
    if pygame.mouse.get_focused():
        pygame.draw.rect(screen, green, [pygame.mouse.get_pos()[0]//94*94, pygame.mouse.get_pos()[1]//94*94,94,94], 7)

def search(x,y):
    global selected, turn
    for p in pieces:
        if p == selected: continue
        if turn == 1 and p.team == "b": continue
        elif turn == -1 and p.team == "w":continue
        if p.pos[0] == x and p.pos[1] == y:
            if selected == None:
                selected = p
                return
            elif selected == p:
                selected = None
                return
    if selected == None: return
    selected.move([x,y])
    selected = None

def check_kings():
    b_king = False
    w_king = False
    for p in pieces:
        if p.king == True:
            if p.team == "w": w_king = True
            elif p.team == "b": b_king = True
    if b_king == False: pygame.display.flip(), game_over("Brown")
    elif w_king == False: pygame.display.flip(), game_over("White")

checker = []
def update():
    global checker
    if checker != sheet.get_all_values():
        checker = sheet.get_all_values()
        search(int(sheet.cell(1,1).value),int(sheet.cell(1,2).value))

def game_over(team):
    global loop
    loop = False
    overfont = pygame.font.SysFont('agencyfb', 75)
    overtext = overfont.render("Game Over!", True, (black))
    screen.blit(overtext, (225, 265))
    pygame.display.flip()
    pygame.time.delay(1000)
    winteamfont = pygame.font.SysFont('agencyfb', 75)
    winteamtext = winteamfont.render('{} team wins!'.format(team), True, (black))
    screen.blit(overtext, (225, 265))
    screen.blit(winteamtext, (160, 380))
    pygame.display.flip()
    pygame.time.delay(2500)
x = 0
# Game loop.
while loop == True:
    screen.fill(white)
    draw_board()
    display_mouse()
    for i in pieces: i.blop()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == -1:
                search(pygame.mouse.get_pos()[0]//94*94,pygame.mouse.get_pos()[1]//94*94)
                pygame.display.flip()
                sheet.update_cell(1,1,pygame.mouse.get_pos()[0]//94*94)
                sheet.update_cell(1,2,pygame.mouse.get_pos()[1]//94*94)
                checker = sheet.get_all_values()
        if event.type == pygame.QUIT:sheet.clear(), pygame.quit(), sys.exit()
    #mendatory display commands
    if turn == 1:
        x += 1
        if x == 180:
            update()
            x = 0
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    check_kings()
