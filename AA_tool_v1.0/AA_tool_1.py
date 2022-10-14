## AA TOOL 1 ##

#Modules
from math import sqrt, pi
import pygame
pygame.init()

#Display
infoObject = pygame.display.Info()
correction = 800
screen_width = infoObject.current_w - correction
screen_height = int((9*screen_width)/16)


win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AA Tool 1")

#Text Input
text_io_w = 0.45 * screen_width
text_io_h = 0.2 * int((0.3 * screen_width * screen_height) / screen_width)
text_v_spacing = 0.15 * screen_height
text_h_spacing = 0.05 * screen_width

#Fonts
big = int(0.045 * screen_height)
big_font = pygame.font.Font("texture/font.ttf", big)
small = int(0.8 * text_io_h)
small_font = pygame.font.Font("texture/font.ttf", small)

#Textures
bg = pygame.image.load("texture/bg.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

text_input_color = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]

#Text Input
class TextInput(object):

    def __init__(self, x, y, width, height, color, header):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outer_color = color
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.state = 0
        self.initialised = False
        self.header_texture = small_font.render(header, 1, self.outer_color)
        self.text = ""
        self.text_texture = small_font.render(self.text, 1, self.outer_color)

    def draw(self, win):
        pygame.draw.rect(win, text_input_color[self.state], self.hitbox, 0)
        pygame.draw.rect(win, self.outer_color, self.hitbox, 2)
        win.blit(self.header_texture, (self.x, self.y - self.header_texture.get_height()))
        win.blit(self.text_texture, (self.x, self.y))

    def getState(self):
        return self.state

    def setState(self, new_state):
        self.state = new_state
    
    def setInitialised(self, new_init):
        self.initialised = new_init

    def update(self, mx, my, click, event):
        #Click
        if click:
            if self.hitbox.collidepoint((mx,my)):
                self.setState(2)
            else:
                self.setState(0)
        #Keydown
        elif event.type == pygame.KEYDOWN:
            if self.state == 2:
                if event.key == pygame.K_RETURN:
                    self.setState(0)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.setInitialised(True)
                    self.text += event.unicode
                # Re-render the text.
                self.text_texture = small_font.render(self.text, 1, self.outer_color)
        #
        else:
            if self.state != 2:
                if self.hitbox.collidepoint((mx,my)):
                    self.setState(1)
                else:
                    self.setState(0)
        
    def reset(self):
        self.initialised = False
        self.text = ""
        self.text_texture = small_font.render(self.text, 1, self.outer_color)

#Text Output
class TextOuput(object):

    def __init__(self, x, y, width, height, color, header):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outer_color = color
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.header_texture = small_font.render(header, 1, self.outer_color)
        self.text = ""
        self.text_texture = small_font.render(self.text, 1, self.outer_color)

    def draw(self, win):
        pygame.draw.rect(win, (255,100,0), self.hitbox, 0)
        pygame.draw.rect(win, self.outer_color, self.hitbox, 2)
        win.blit(self.header_texture, (self.x, self.y - self.header_texture.get_height()))
        win.blit(self.text_texture, (self.x, self.y))

    def update(self, new_text):
        self.text = new_text
        self.text_texture = small_font.render(self.text, 1, self.outer_color)

#Reset Button
class ResetButton(object):

    def __init__(self, x, y, width, height, outer_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inner_color = (255,0,0)
        self.outer_color = outer_color
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_texture = small_font.render("RESET", 1, self.outer_color)

    def draw(self, win):
        pygame.draw.rect(win, self.inner_color, self.hitbox, 0)
        pygame.draw.rect(win, self.outer_color, self.hitbox, 2)
        win.blit(self.text_texture, (self.x + ((self.width - self.text_texture.get_width()) / 2), self.y))

def computeSpeed(density, mass_flow, outer_diameter, thickness):
    '''Compute the speed in m/s of a fluid caracterised by its density: density (kg/m3), in a pipe of outer diameter: outer_diameter (mm), and thickness:  thickness (mm), where the mass flow is mass_flow (kg/h)'''
    volumetric_flow = (mass_flow / density) / 3600

    inner_radius = (outer_diameter / 2000) - (thickness / 1000) #Handles conversion from mm to m
    inner_section = pi * inner_radius**2

    return volumetric_flow / inner_section

def reset(text_inputs, result):
    for text_input in text_inputs:
        text_input.reset()
    result.update("")

def redrawWindow(title, text_inputs, result, reset_button):
    win.blit(bg, (0, 0))
    win.blit(title, ((screen_width - title.get_width())/2, 0.04 * screen_height))
    for text_input in text_inputs:
        text_input.draw(win)
    result.draw(win)
    reset_button.draw(win)
    pygame.display.update()

#Main
def main():
    print(pi)
    title = big_font.render("Calcul de vitesse dans une conduite de diamètre nominal ANSI", 1, (0,0,0))

    y = 0.04 * screen_height + 1.25 * text_v_spacing
    text_inputs = [TextInput(10, y, text_io_w, text_io_h, (0,0,0), "Masse volumique (kg/m3)"), 
                   TextInput(10, y + text_v_spacing, text_io_w, text_io_h, (0,0,0), "Débit massique (kg/h)"),
                   TextInput(10, y + 2 * text_v_spacing, text_io_w, text_io_h, (0,0,0), "Diamètre extérieur de la conduite (mm)"),
                   TextInput(10, y + 3 * text_v_spacing, text_io_w, text_io_h, (0,0,0), "Epaisseur de la conduite (mm)")]

    result = TextOuput(10, y + 4.25 * text_v_spacing, text_io_w, text_io_h, (0,0,0), "Vitesse (m/s)")

    reset_button = ResetButton(10 + text_io_w + text_h_spacing, y + 4.25 * text_v_spacing, text_io_w, text_io_h, (0,0,0))

    run = True
    run_compute = False
    while run:
        mx, my = pygame.mouse.get_pos()
        click=False
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if keys[pygame.K_ESCAPE]:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    click=True
            if reset_button.hitbox.collidepoint((mx,my)):
                if click:
                    reset(text_inputs, result)
            for text_input in text_inputs:
                text_input.update(mx, my, click, event)
                run_compute = True
                if run_compute and text_input.initialised == False:
                    run_compute = False
            if run_compute:
                speed = computeSpeed(float(text_inputs[0].text),
                                    float(text_inputs[1].text),
                                    float(text_inputs[2].text),
                                    float(text_inputs[3].text))
                result.update(str(speed))
            
        redrawWindow(title, text_inputs, result, reset_button)
        pygame.time.delay(int(100/6))
    pygame.quit()

main()