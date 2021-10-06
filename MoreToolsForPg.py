import pygame

screen = pygame.display.set_mode((800,600))

class Score():
    def __init__(self, x, y, font, size, color, unit):
        self.data = 0
        self.x = x
        self.y = y
        self.font = font
        self.size = size
        self.color = color
        self.unit = unit

    def draw(self):
        f = pygame.font.SysFont(self.font, self.size)
        screen.blit(f.render("SCORE: " + str(self.data),True,self.color),(self.x,self.y))

    def update(self):
        self.data += self.unit 

class Button():
    
    def __init__(self, x, y, w, h, button_color, hover_color, name, font, name_size, name_color, name_color_hover, border, rounded):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.button_color = button_color # màu của nút
        self.name = name 
        self.font = font
        self.name_size = name_size 
        self.name_color = name_color # màu của tên nút
        self.hover_color = hover_color # màu của nút khi con trỏ chuột nằm trong phạm vi nút
        self.name_color_hover = name_color_hover # màu của tên nút khi con trỏ chuột nằm trong phạm vi nút
        self.border = border # viền của nút
        self.rounded = rounded # bo góc hình chữ nhật

    def draw(self, x_mouse, y_mouse): # Vẽ nút
        f = pygame.font.SysFont(self.font,self.name_size)
        # Tạo hiệu ứng đổi màu khi vị trí con trỏ chuột nằm trong phạm vi của nút bấm (hover)
        if x_mouse>=self.x and x_mouse<=self.x+self.width and y_mouse>=self.y and y_mouse<=self.y+self.height:
            pygame.draw.rect(screen,self.hover_color,(self.x,self.y,self.width,self.height),self.border,self.rounded)
            name = f.render(self.name,True,self.name_color_hover)
        else:
            pygame.draw.rect(screen,self.button_color,(self.x,self.y,self.width,self.height),self.border,self.rounded)
            name = f.render(self.name,True,self.name_color)
        text_w, text_h = name.get_size()
        screen.blit(name,[self.x + self.width/2 - text_w/2, self.y + self.height/2 - text_h/2]) # Công thức căn chỉnh sao cho tên nút được vẽ ở chính giữa nút

class PopUpWindow():
    def __init__(self,x,y,w,h,background_color,name,font,name_size,name_color,border,rounded):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.background_color = background_color
        self.name = name
        self.font = font
        self.name_size = name_size
        self.name_color = name_color # Màu chữ trong của sổ
        self.border = border
        self.rounded = rounded
        self.button_list = [] # danh sách các nút trong cửa sổ pop-up

    def draw(self,x_mouse,y_mouse):
        # Vẽ khung cửa sổ pop-up
        pygame.draw.rect(screen,self.background_color,(self.x,self.y,self.width,self.height),self.border,self.rounded)
        pygame.draw.line(screen,self.name_color,(self.x,self.y+25),(self.x+self.width,self.y+25))
        # Vẽ chữ trong cửa sổ
        f = pygame.font.SysFont(self.font,self.name_size)
        name = f.render(self.name,True,self.name_color)
        screen.blit(name,[self.x+25,self.y+self.height/3])
        screen.blit(f.render("Message!",True,self.name_color),[self.x+5,self.y+5])

        # Khởi tạo, vẽ và đẩy 3 cái nút vào danh sách
        Close_button = Button(self.x+self.width-25,self.y,25,25,self.background_color,(255,0,0),"X",None,24,self.name_color,(255,255,255),0,0)
        Close_button.draw(x_mouse,y_mouse)
        self.button_list.append(Close_button)
        Agree_button = Button(self.x+self.width-200,self.y+self.height-40,80,30,(0,0,0),(0,204,255),"Agree",None,20,self.name_color,(0,204,255),1,10)
        Agree_button.draw(x_mouse,y_mouse)
        self.button_list.append(Agree_button)
        Cancel_button = Button(self.x+self.width-100,self.y+self.height-40,80,30,self.name_color,(255,0,0),"Cancel",None,20,self.name_color,(255,0,0),1,10)
        Cancel_button.draw(x_mouse,y_mouse)
        self.button_list.append(Cancel_button)

class HpBar():
    def __init__(self,x,y,w,h,color1,color2,color3,is_horizontal):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.is_horizontal = is_horizontal
        self.remain = w

    def draw(self):
        f = pygame.font.SysFont("consolas",20)
        name = f.render(str(round((self.remain/self.width)*100,2))+"%",True,self.color3)
        text_w, text_h = name.get_size()
        if self.is_horizontal:
            pygame.draw.rect(screen,self.color2,[self.x,self.y,self.width,self.height])
            pygame.draw.rect(screen,self.color1,[self.x,self.y,self.remain,self.height])
        
            screen.blit(name,[self.x + self.width/2 - text_w/2, self.y + self.height/2 - text_h/2])
        else:
            pygame.draw.rect(screen,self.color2,[self.x,self.y,self.height,self.width])
            pygame.draw.rect(screen,self.color1,[self.x,self.y+self.width-self.remain,self.height,self.remain])

            screen.blit(name,[self.x + self.height/2 - text_w/2, self.y + self.width + 10])
