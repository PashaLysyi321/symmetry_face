import cv2
import skimage
import matplotlib.pyplot as plt
import dlib
import numpy as np
import math
import telebot
from matplotlib import pyplot as plt

checker = 60

def viewImage(image, name_of_window):
	    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
	    cv2.imshow(name_of_window, image)
	    cv2.waitKey(0)
	    cv2.destroyAllWindows()

def returnMass(image_path):
	global checker
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor('C:/Users/lysyi/Desktop/symmetry_face/shape_pred_68.dat')

	faces = detector(gray)
	faces_detected = "Лиц обнаружено: " + format(len(faces))
	print(faces_detected)
	mass = []
	mass1 = []

	x1 = faces[0].left()
	y1 = faces[0].top()
	x2 = faces[0].right()
	y2 = faces[0].bottom()
	
	#cv2.circle(image, (x1, y1), 3, (255, 0, 0), -1) 
	#cv2.circle(image, (x2, y2), 3, (255, 0, 0), -1) 
	cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 1)
	       
	landmarks = predictor(gray, faces[0])

	k = [7,6,5,4,3,2,1,0,17,18,19,20,21,39,38,37,36,41,40,31,32,48,49,59,58,67]
	m = [9,10,11,12,13,14,15,16,26,25,24,23,22,42,43,44,45,46,47,35,34,53,54,55,56,65]

	for n in k:
		x = landmarks.part(n).x
		y = landmarks.part(n).y
		cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
		#cv2.putText(image, str(n), (x+5,y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2) 
		mass.append((x,y))
	
	for n in m:
		x = landmarks.part(n).x
		y = landmarks.part(n).y
		cv2.circle(image, (x, y), 3, (255, 0, 100), -1)
		#cv2.putText(image, str(n), (x+5,y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2) 
		mass1.append((x,y))

	for n in [28,29,30]:
		x = landmarks.part(n).x
		y = landmarks.part(n).y
		cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
		#cv2.putText(image, str(n), (x+5,y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2) 
		
	mid_x = round((landmarks.part(28).x + landmarks.part(29).x + landmarks.part(30).x)/3)

    
	#cv2.putText(image, "Press ESC to close image", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
	#viewImage(image,"faces_detected")
	mass2 = []
	for i in range(0,len(mass)):
		mass2.append(2*mid_x-int(mass[i][0]))

	sum = 0
	for i in range(0,len(mass)):
		sum = sum + ((mass1[i][0]-mass2[i])**2 + (mass[i][1]-mass1[i][1])**2)**.5

	print(image_path[:-4])
	cv2.imwrite (image_path[:-4]+'worked.jpg' , image)
	#viewImage(image,"faces_detected")
	return(sum)

def text(summ):
	print('your distanse: '+str(summ))
	if summ <100:
		ans = 'your face is perfect, such does not exist in real life'
	elif summ < 150:
		ans = 'your face is perfect, 100 percent of beaty'
	elif summ < 200:
		ans = 'your face is perfect, 97.5 percent of beaty'
	elif summ < 250:
		ans = 'your face is perfect, 95 percent of beaty'
	elif summ < 300:
		ans = 'your face is perfect, 92.5 percent of beaty'
	elif summ < 350:
		ans = 'your face is rly good, 90 percent of beaty'
	elif summ < 400:
		ans = 'your face is perfect, 87.5 percent of beaty'
	elif summ < 450:
		ans = 'your face is rly good, 85 percent of beaty'
	elif summ < 500:
		ans = 'your face is perfect, 82.5 percent of beaty'
	elif summ < 550:
		ans = 'your face is good, 80 percent of beaty'
	elif summ < 600:
		ans = 'your face is perfect, 77.5 percent of beaty'
	elif summ < 650:
		ans = 'your face is good, 75 percent of beaty'
	else:
		ans = 'your photo does not fit, take another'
	return ans

image_path_doc = "C:/Users/lysyi/Desktop/symmetry_face/photo/"

bot = telebot.TeleBot('1086546188:AAGiy1yg-vTP2O9v3CPxkTHT5lDml_pfeGU')

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'hi, send photo 4 me')


@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
	global checker
	file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	src = 'C:/Users/lysyi/Desktop/symmetry_face/photo/' + str(checker) +'.jpg'
	with open(src, 'wb') as new_file:
		new_file.write(downloaded_file)
	bot.send_message(message.chat.id, 'load...')
	summ = returnMass(image_path_doc +str(checker)+".jpg")
	ans = text(summ)
	bot.send_photo(message.chat.id, open(image_path_doc+str(checker)+'worked.jpg', 'rb'));
	bot.send_message(message.chat.id, 'Your assymetry = '+str(summ) + ' pixels')
	bot.send_message(message.chat.id, str(ans))
	checker = checker + 1
	
bot.polling()
