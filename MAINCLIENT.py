import cv2
import time
import numpy
import socket
import threading
from pynput import keyboard

def onPress(keyEvent):
	try:
		global clientInput
		global count
		if str(keyEvent.char) not in clientInput and count<2:
			clientInput.append(keyEvent.char)
			clientInput.remove("O")
			count+=1
	except Exception as error:
		print("An error occurred with onPress().")
		print(f"Error is specifically {error}")

def onRelease(keyEvent):
	try:
		global clientInput
		global count
		if str(keyEvent.char) in clientInput:
			clientInput.remove(keyEvent.char)
			clientInput.append("O")
			count-=1
	except Exception as error:
		print("An error occurred with OnRelease().")
		print(f"Error is specifically {error}")

IP = "192.168.99.173"
PORT = 5050

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientInput = ['O', 'O']
count=0
disconnected = False

listener = keyboard.Listener(on_press=onPress, on_release=onRelease)
listener.start()

def commandHandlerClient():
	while True:
		newMsg = "".join(clientInput).encode("utf-8")
		print("Running: {0}".format("".join(clientInput)))
		CLIENT.send(newMsg)
		if "0" in clientInput:
			disconnected = True
			break
		time.sleep(0.1)

try:
	CLIENT.connect((IP, PORT))
	commandClientThread = threading.Thread(target=commandHandlerClient)
	commandClientThread.start()
	while True:

		encodedFrames = b""
		debounce = True

		while debounce:
			msg = CLIENT.recv(4096);
			if not msg:
				print("Message could not be retrieved!");
				break;
			encodedFrames += msg;
			encodedFrames = encodedFrames.split(b"<<END>>")

			for encodedFrame in encodedFrames[:-1]:
				parse = numpy.frombuffer(encodedFrame, numpy.uint8);
				frame = cv2.imdecode(parse, cv2.IMREAD_COLOR)
				cv2.imshow("Live Stream from "+IP, frame)
				if cv2.waitKey(1) & 0xFF == ord("q"):
					debounce = False
					break;
			encodedFrames = encodedFrames[-1]


except Exception as error:
	print(f"Error is specifically: {error}")
	listener.stop()

finally:
	if disconnected:
		CLIENT.close()

