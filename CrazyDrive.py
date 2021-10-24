import pygame as pg
from pygame import mixer
import random
from CrazyDriveObjs import TextButton, Vehicle, SpecialVehicle

trendy_green = (25, 150, 25)
arabian_green = (10, 100, 43)
green = (0,255,0)
valentine_red = (212, 31, 58)
abarian_red = (163, 11, 46)
red = (255, 0, 0)
white = (255,255,255)
black = (0,0,0)

screen_width = 1000
screen_height = 600
background = pg.image.load('IMG/background.png')
orangecar = pg.image.load('IMG/orangecar.png')
bluetruck = pg.image.load('IMG/bluetruck.png')
bus = pg.image.load('IMG/bus.png')
blacktruck = pg.image.load('IMG/blacktruck.png')
orangetruck = pg.image.load('IMG/orangetruck.png')
redtruck = pg.image.load('IMG/redtruck.png')
taxi = pg.image.load('IMG/taxi.png')
motorbike = pg.image.load('IMG/motorbike.png')
policecar = pg.image.load('IMG/policecar.png')
redcar = pg.image.load('IMG/redcar.png')
blackcar = pg.image.load('IMG/blackcar.png')
redmotorbike = pg.image.load('IMG/redmotorbike.png')
vehicle_type = [bus, bluetruck, blacktruck, taxi, orangetruck, redtruck, redcar, blackcar, policecar, motorbike, redmotorbike]

pg.init()

screen = pg.display.set_mode((screen_width,screen_height)) # tạo màn hình
pg.display.set_caption("Crazy Drive - Journey to the graveyard!") # tạo tiêu đề

clock = pg.time.Clock() # đồng hồ trong pygame
# các loại font
tiny_font = pg.font.SysFont('ocrastdopentype', 16)
small_font = pg.font.SysFont('ocrastdopentype', 32)
big_font = pg.font.SysFont('ocrastdopentype', 64)

# âm thanh
brake = mixer.Sound('SOU/brake.wav')
crash = mixer.Sound('SOU/crash.wav')
horn = mixer.Sound('SOU/horn.wav')
vinhbiet = mixer.Sound('SOU/xin_vinh_biet.wav')

def playingScreen():
	'''Hiển thị màn hình chơi game'''
	running_vehicles = [] # tạo list chứa các xe trên đường

	mixer.music.load('SOU/tokyo-drift.mp3') # nhạc nền
	mixer.music.play(-1) # lặp nhạc nền

	pause = False # biến pause kiểm tra có pause game không
	start = False # biến start để xe chạy đoạn đầu game
	time, tic = 0, 0 # 2 biến để đếm thời gian chơi
	speed, level = 4, 1 # speed để điều chỉnh tốc độ của xe, level để điều chỉnh độ khó
	background_scroll_x = 0 # để tạo hiệu ứng xe đang chạy

	mycar = SpecialVehicle(-150,random.choice([75,225,375]),orangecar) # tạo đối tượng SpecialVehicle (là cái xe người chơi điều khiển)
	# đoạn này vẽ tạo các đối tượng Vehicle (các xe đi trên đường) và đưa chúng vào list, vị trí các xe cách nhau 420px
	for i in range(3):
		temp = Vehicle(1000+i*420,random.choice([75,225,375]),random.choice(vehicle_type))
		running_vehicles.append(temp)

	# Game tips để hiện thị khi dừng game
	game_tips = ['The horn button is just for fun :)','Press ENTER to UNPAUSE','If you quit now, your score may not been saved','Remember your vehicle always automatically speeds up','Press and hold A to control your speed']
	tip = ''

	# vòng lặp game
	while True:
		if not pause:
			tic = clock.tick(60)/1000 # đổi về đơn vị giây (fps = 60)

			# hiển thị màn hình chơi (background, thanh thời gian, lời nhắn, xe)
			time_bar = small_font.render('Time: '+'{:.2f}'.format(time)+'s',True, white)
			screen.blit(background,(background_scroll_x,0))
			screen.blit(time_bar,(380,10))
			screen.blit(tiny_font.render('Press ENTER to PAUSE',True,white),(25,540))
			screen.blit(tiny_font.render('Press SPACE to HONK the horn',True,white),(25, 565))

			# vẽ xe của người chơi và mũi tên chỉ hướng
			mycar.draw(screen)
			if mycar.y == 75:
				mycar.drawDownArrow(screen,green)
			elif mycar.y == 225:
				mycar.drawUpArrow(screen,green)
				mycar.drawDownArrow(screen,green)
			elif mycar.y == 375:
				mycar.drawUpArrow(screen,green)

			if time>=level*10: # tăng độ khó lên 1 sau mỗi 10 giây
				speed+=1
				level+=1

			if not start: # xe chạy đoạn đầu game
				mycar.speedUp(5)
				if mycar.getPos()[0]>=300:
					start = True
			else:
				time += tic # cộng thời gian

				# tạo hiệu ứng xe chạy trên đường
				background_scroll_x -= (speed*2) 
				if background_scroll_x <= -1000:
					background_scroll_x = 0

				# hiển thị các xe trên đường
				for vehicle in running_vehicles:
					vehicle.draw(screen)
					vehicle.moveBackward(speed)

					# kiểm tra nếu có va chạm,  trả về thông tin vụ tai nạn (một danh sách gồm vị trí các xe, thời gian chạy)
					if mycar.getPos()[1] == vehicle.getPos()[1]:
						if mycar.getPos()[0]>=vehicle.getPos()[0]-vehicle.getSize()[0] and mycar.getPos()[0]<=vehicle.getPos()[0]+vehicle.getSize()[0]:
							brake.stop()
							mixer.music.stop()
							crash.play()
							return background_scroll_x, mycar.getPos(), time, running_vehicles

				# nếu xe đầu trong danh sách các xe trên đường đi hết màn hình, lập tức xóa xe đó và thêm xe mới vào danh sách
				if running_vehicles[0].getPos()[0] <= -200:
					running_vehicles.pop(0)
					running_vehicles.append(Vehicle(running_vehicles[-1].getPos()[0]+420, random.choice([75,225,375]), random.choice(vehicle_type)))	
				
				if mycar.x<600: # xe của người chơi luôn tiến lên phía trước nếu vị trí nhỏ hơn 600px
					mycar.speedUp(2) 
				if mycar.isSlowDown and mycar.x>0: # kiểm tra nếu xe muốn phanh và vị trí xe lớn hơn 0 thì chậm lại
					mycar.moveBackward(5)

				# bắt sự kiện
				for event in pg.event.get():
					if event.type == pg.QUIT:
						raise SystemExit()
					elif event.type == pg.KEYDOWN:
						if event.key == pg.K_s and mycar.y<375:
							mycar.turnRight(150)
						elif event.key == pg.K_w and mycar.y>75:
							mycar.turnLeft(150)
						elif event.key == pg.K_a:
							brake.play()
							mycar.isSlowDown = True
						elif event.key == pg.K_SPACE:
							horn.play()
						elif event.key == pg.K_RETURN:
							tip = random.choice(game_tips) # chọn 1 tip để hiển thị
							mixer.music.pause()
							pause = True
					elif event.type == pg.KEYUP:
						if event.key == pg.K_a:
							mycar.isSlowDown = False
							brake.stop()
		else:
			# màn hình khi đang pause game
			time_bar = small_font.render('Time: '+'{:.2f}'.format(time)+'s',True, white)
			screen.blit(background,(background_scroll_x,0))
			screen.blit(time_bar,(380,10))
			mycar.draw(screen)
			for vehicle in running_vehicles:
				vehicle.draw(screen)
			screen.blit(pg.image.load('IMG/opacity.png'),[0,0])
			pause_message = small_font.render('DO YOU WANT TO CONTINUE?',True,green)
			screen.blit(pause_message,(screen_width/2-pause_message.get_width()/2,200))
			screen.blit(tiny_font.render(tip,True,white),(25,550))

			yes_button = TextButton((310,350),(120,70),'YES',pg.font.SysFont('ocrastdopentype',18),white,white,trendy_green,arabian_green,0,10)
			no_button = TextButton((560,350),(120,70),'NO',pg.font.SysFont('ocrastdopentype',18),white,white,valentine_red,abarian_red,0,10)

			mouse_pos = pg.mouse.get_pos()
			yes_button.draw(screen,mouse_pos)
			no_button.draw(screen,mouse_pos)

			# bắt sự kiện
			for event in pg.event.get():
					if event.type == pg.QUIT:
						raise SystemExit()
					elif event.type == pg.KEYDOWN:
						if event.key == pg.K_RETURN:
							mixer.music.unpause()
							pause = False
					elif event.type == pg.MOUSEBUTTONDOWN:
						if event.button == 1:
							if pg.Rect(yes_button.coordinate,yes_button.size).collidepoint(mouse_pos):
								mixer.music.unpause()
								pause = False
							elif pg.Rect(no_button.coordinate,no_button.size).collidepoint(mouse_pos):
								raise SystemExit()
					
		pg.display.update()

def gameOverScreen(accident):
	'''Hiển thị màn hình game over, nhận đầu vào là thông tin vụ tai nạn được trả về từ hàm playingScreen'''
	big_message = big_font.render(random.choice(['YOU DIED!','NICE DRIVE!','XIN VINH BIET!']),True, red)
	small_message = small_font.render('Time survive: '+'{:.2f}'.format(accident[2])+"s", True, green)
	x, y = 1000, 1000 # hai biến tạo hiệu ứng di chuyển vào
	vinhbiet.play()
	while True:

		# vẽ màn hình khi game over
		mouse_pos = pg.mouse.get_pos()
		screen.blit(background,[accident[0],0])
		for vehicle in accident[3]:
			vehicle.draw(screen)
		screen.blit(orangecar,[accident[1][0],accident[1][1]])
		screen.blit(pg.image.load('IMG/flame.png'),[accident[1][0],accident[1][1]])
		screen.blit(pg.image.load('IMG/opacity.png'),[0,0])
		screen.blit(pg.image.load('IMG/rip.png'),[x,220])
		screen.blit(big_message,(screen_width/2-big_message.get_width()/2,120)) # căn big_message giữa màn hình
		screen.blit(small_message,(120, 250))

		# tạo 2 nút là replay và back
		replay_button = TextButton((120,y),(120,70),'REPLAY',pg.font.SysFont('ocrastdopentype',18),white,white,trendy_green,arabian_green,0,10)
		replay_button.draw(screen,mouse_pos)
		back_button = TextButton((420,y),(120,70),'BACK',pg.font.SysFont('ocrastdopentype',18),white,white,valentine_red,abarian_red,0,10)
		back_button.draw(screen,mouse_pos)
		
		# tạo hiệu ứng cho ảnh rip và 2 nút
		if x>700:
			x-=10
		if y>400:
			y-=10

		# bắt sự kiện
		for event in pg.event.get():
			if event.type == pg.QUIT:
				raise SystemExit()
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					if pg.Rect(back_button.coordinate,back_button.size).collidepoint(mouse_pos):
						mixer.Sound('SOU/select.wav').play()
						return 0
					elif pg.Rect(replay_button.coordinate,replay_button.size).collidepoint(mouse_pos):
						mixer.Sound('SOU/select.wav').play()
						return 1

		pg.display.update()

def main():
	while True:
		accident = playingScreen()
		after_accident = gameOverScreen(accident)
		if after_accident == 0:
			break

main()