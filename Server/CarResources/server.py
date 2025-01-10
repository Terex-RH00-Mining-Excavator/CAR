import cv2
import time
import numpy
import socket
import threading
from CarResources import Tools

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "192.168.99.173"#socket.gethostbyname(socket.gethostname()) Should be "192.168.99.173"
PORT = 5050
CURRENTSOCKET = 0
disconnected = False
initialClock = time.time()

PIN_IN1 = 15  # INPUT 1 ON DRIVER 15
PIN_IN2 = 16 # INPUT 2 ON DRIVER 16
PIN_IN3 = 36 # INPUT 3 ON DRIVER 36
PIN_IN4 = 38 # INPUT 4 ON DRIVER 38
PIN_LED = 31 # LED VIA PIN 31 ON GPIO BUS
tPosition, xPosition, zPosition = 300, 300, 300
car = Tools.Car(PIN_IN1, PIN_IN2, PIN_IN3, PIN_IN4, PIN_LED);
car.setup();

def commandInterpreter(commandList):
	global tPosition
	global xPosition
	global zPosition
	
	if "w" in commandList:
		car.forward()
	if "s" in commandList:
		car.backward()
	if "a" in commandList:
		if tPosition <= 500:
					tPosition += 25
					car.Turn(0, tPosition);
	if "d" in commandList:
		if tPosition >= 100:
			tPosition -= 25
			car.Turn(0, tPosition);
	if "j" in commandList:
		if zPosition <= 500:
					zPosition += 25
					car.Turn(1, zPosition);
	if "l" in commandList:
		if zPosition >= 100:
			zPosition -= 25
			car.Turn(1, zPosition);
	if "i" in commandList:
		if xPosition <= 500:
					xPosition += 25
					car.Turn(2, xPosition);
	if "k" in commandList:
		if xPosition >= 100:
			xPosition -= 25
			car.Turn(2, xPosition);
	if "1" in commandList:
		car.ToggleLed()
	if "OO" in commandList:
		car.SetAllFalse()

def videoFeedHandler():
	try:
		global disconnected
		global CURRENTSOCKET
		global initialClock
		lens = cv2.VideoCapture(0)
		while True:
			ret, frame = lens.read()
			# !!!
			(height, width) = frame.shape[:2]
			OVERALLCOLOR = (255, 155, 0)
			
			valuePHI = (zPosition-100) * 0.45
			valueTHETA = (xPosition-100) * 0.45
			
			#radius, cThickness = 20, 2
			#cv2.circle(frame, (width//2, height//2), radius, OVERALLCOLOR, cThickness)
			#cv2.line(frame, (width//2-radius*2, height//2), (width//2+radius*2, height//2), OVERALLCOLOR, cThickness)
			#cv2.line(frame, (width//2, height//2-radius*2), (width//2, height//2+radius*2), OVERALLCOLOR, cThickness)
			
			
			#distanceText = "Distance {0}mm".format(-1 * round(15.54/math.cos(valueTHETA), 2))
			FONT = cv2.FONT_HERSHEY_SIMPLEX
			DFSCALE = 1
			DFTHICKNESS = 1
			#(textWidth, textHeight) = cv2.getTextSize(distanceText, FONT, DFSCALE, DFTHICKNESS)[0]
			#cv2.putText(frame, distanceText, (width//2-textWidth//2, height-height//20), FONT, DFSCALE, OVERALLCOLOR, DFTHICKNESS)
			
			thetaText = "Value(THETA) = {0}^".format(valueTHETA)
			phiText = "Value(PHI) = {0}^".format(valuePHI)
			cv2.putText(frame, phiText, (5, height-height//10), FONT, DFSCALE, (0, 0, 255), DFTHICKNESS)
			cv2.putText(frame, thetaText, (5, height-height//30), FONT, DFSCALE, (0, 0, 255), DFTHICKNESS)
			
			timeText = "{0}".format(round(time.time()-initialClock, 3))
			#timeTextWidth = cv2.getTextSize(timeText, FONT, DFSCALE, DFTHICKNESS)[1]
			cv2.putText(frame, timeText, (width-width//2, height-height//20), FONT, DFSCALE, (0,255,0), DFTHICKNESS)
			
			# !!!
			
			if not ret:
				break;
			_, img = cv2.imencode(".jpg", frame);
			encodedImg = img.tobytes();
			encodedImg += "<<END>>".encode("utf-8");
			CURRENTSOCKET.send(encodedImg)
			if disconnected or (cv2.waitKey(1) & 0xFF == ord("q")):
				break;
		lens.release();
		CV2.destroyAllWindows()
	except Exception as error:
		print("Within videoFeedHandler(): There was a " + type(error).__name__)

def commandHandler():
	c = 0
	while True:
		c+=1
		msg = CURRENTSOCKET.recv(2).decode('utf-8')
		if msg:
			print("{0}: {1}".format(msg, c));
			commandInterpreter(msg)
			if msg=="":
				print("NO INPUT!!!")
			if "0" in msg:
				disconnected = True
				break;
			time.sleep(0.1)

try:
	SERVER.bind((IP, PORT))
	SERVER.listen(1)
	print("Listening on "+IP+" "+str(PORT))
	CURRENTSOCKET, client = SERVER.accept()
	print("Established " + str(client))
	#while True:
	#	videoThread = threading.Thread(target=videoFeedHandler)
	#	videoThread.start()

	commandThread = threading.Thread(target = commandHandler);
	commandThread.start()

	videoFeedHandler();

	commandThread.end()
	#time.sleep(15);

	#except Exception as error:
	#	print("There was a " + type(error).__name__ + " within main")

finally:
	print("zam")
	SERVER.close()
	CURRENTSOCKET.close()
