import pygame

class RectangleButton():
    '''Lớp các nút bấm với tọa độ và phạm vi cho trước'''
    def __init__(self,coordinate,size):
        self.coordinate = coordinate
        self.size = size

class ImageButton(RectangleButton):
    '''Định nghĩa lớp nút bấm hiển thị dạng ảnh'''
    def __init__(self,coordinate,size,image):
        super().__init__(coordinate, size)
        self.image = image

    def draw(self, screen):
        screen.blit(self.image,self.coordinate)

class TextButton(RectangleButton):
    '''Định nghĩa lớp nút bấm hiện thị dạng chữ'''
    def __init__(self, coordinate, size, text, font, text_color, text_hover_color ,button_color, button_hover_color, border_size, border_radius):
        super().__init__(coordinate,size)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_hover_color = text_hover_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.border_size = border_size
        self.border_radius = border_radius

    def draw(self, screen, mouse_point):
        button_area = pygame.Rect(self.coordinate,self.size)
        text = self.font.render(self.text,True,self.text_color)
        text_size = text.get_size()
        # Công thức tính tọa độ của chữ trên nút bấm sao cho chữ được căn giữa nút
        text_coordinate = [self.coordinate[0] + self.size[0]/2 - text_size[0]/2, self.coordinate[1] + self.size[1]/2 - text_size[1]/2]
        pygame.draw.rect(screen,self.button_color,button_area,self.border_size,self.border_radius)
        
        if button_area.collidepoint(mouse_point):
            pygame.draw.rect(screen,self.button_hover_color,button_area,self.border_size,self.border_radius)
            text = self.font.render(self.text,True,self.text_hover_color)

        screen.blit(text,text_coordinate)

class Vehicle():
    '''định nghĩa phương tiện giao thông trong game gồm vị trí, thể loại'''
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
    def draw(self,screen):
        screen.blit(self.kind,[self.x, self.y])
    def moveBackward(self, speed):
        self.x -= speed
    def getPos(self):
        return self.x, self.y

class SpecialVehicle(Vehicle):
    '''định nghĩa phương tiện giao thông người chơi có thể điều khiển (kế thừa lớp Vehicle)'''
    def __init__(self, x, y, kind):
        super().__init__(x,y,kind)
        self.isSlowDown = False
    def speedUp(self, move):
            self.x+=move
    def turnLeft(self, move):
        self.y-=move
    def turnRight(self, move):
        self.y+=move
    def speedControl(self,down):
        self.isSlowDown = down
    def checkSpeed(self):
        return self.isSlowDown
    def drawUpArrow(self,screen,color):
        pygame.draw.polygon(screen,color,[(self.x+60, self.y+30), (self.x+90, self.y+30), (self.x+75, self.y+10)])
    def drawDownArrow(self,screen,color):
        pygame.draw.polygon(screen,color,[(self.x+60, self.y+120), (self.x+90, self.y+120), (self.x+75, self.y+140)])
        
