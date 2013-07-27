import socket
import thread
import pygame
import time

from commandHandler import *
from player import *

from draw2d import *
from mainloop import *
from island import *



PORT = 50662


class Client(StdMain):
	def __init__(self):
		self.cmdObj = clientCommandHandlerObj(self)
		
		self.player = Player()
		self.msgToBeSent = []	#["Msg","Msg"...]
		self.sendclock = pygame.time.Clock()
		self.gameclock = pygame.time.Clock()
		self.gameState = "mainmenu"
		self.t = 0
	
	
	def update(self, dt):
		self.t += dt
		if self.gameState == "ingame":
			self.ingame_update(dt)
	
	
	
	def displayMsg(self, msg):
		pass
	
	def sendToServer(self, msg):
		print "sending: "+msg
		self.msgToBeSent.append(msg)
	
	
	def connectToServer(self, host, port = PORT):
		try:
			addr = ((host, port))
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(addr)
			thread.start_new_thread(self.chandle, (sock, addr))
			while 1:
				if self.msgToBeSent:
					msg = self.msgToBeSent[0]
					sock.send(msg)
					self.msgToBeSent.remove(msg)
				self.sendclock.tick(5)
		except Exception as e:
			print e
	
	def chandle(self, sock, addr):
		try:
			print "connected to", addr
			while 1:
				msg = sock.recv(1024)
				if msg:
					self.cmdObj.clientIncomingMsg(msg)
			
				else:
					print addr, "closed!"
					return
		except Exception as e:
			print e
	
	
	def ingame_update(self, dt):
		self.gameclock.tick(30)
		self.player.update(dt)
	
	def draw(self):
		if self.gameState == "mainmenu":
			self.mainmenu_draw()
		elif self.gameState == "changeNick":
			self.changeNick_draw()
		
		else:
			text("NO VALID GAMESTATE", font(100), (0,0))
			text("Current Gamestate: "+self.gameState, font(50), (0,100))
	
	
	def mainmenu_draw(self):
		text("Main Menu:", font(150), (0,0))
		text("1: Bonjour", font(75), (50, 100))
		text("2: Direct Connect", font(75), (50, 150))
		text("3: Change Nick", font(75), (50, 200))

		text("Current Nick: "+self.player.name, font(75), (50, 300))
	def changeNick_draw(self):
		if self.player.name == "":
			text("Type to change Nick", font(50), (50, 200))
		else:
			text("Press <ENTER> to finish your Name.", font(50), (50, 200))
		text("Current Nick: "+self.player.name, font(75), (50, 300))
	
	
	def onKey(self, event):
		if self.gameState == "mainmenu":
			if event.key == K_3:
				self.player.name = ""
				self.gameState = "changeNick"
			if event.key == K_2:
				self.gameState = "directConnect"
			if event.key == K_1:
				self.gameState = "bonjourScan"
		elif self.gameState == "changeNick":
			if event.key == K_RETURN:
				self.gameState = "mainmenu"
			else:
				self.player.name += event.unicode






if __name__ == "__main__":
	#host = raw_input("Connect To Host: ")
	#playerName = raw_input("Your Name: ")
	client = Client()
	mainloop(((800, 600), "FlyLands", 30), Client)
	#thread.start_new_thread(client.connectToServer, (host,))
	
	#client.mainloop()
