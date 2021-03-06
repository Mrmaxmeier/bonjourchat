from OpenGL.GL import *
import pygame

class Texture():
# simple texture class
# designed for 32 bit png images (with alpha channel)
	def __init__(self,pathOrSurface):
		self.texID=0
		if type(pathOrSurface) == str:
			surface = pygame.image.load(pathOrSurface)
		else:
			surface = pathOrSurface
		self.LoadTexture(surface)
	def LoadTexture(self,textureSurface):
		try:
			textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
			
			self.w, self.h = textureSurface.get_width(), textureSurface.get_height()
			
			self.texID=glGenTextures(1)
			
			glBindTexture(GL_TEXTURE_2D, self.texID)
			glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA,
						textureSurface.get_width(), textureSurface.get_height(),
						0, GL_RGBA, GL_UNSIGNED_BYTE, textureData )
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
		except:
			print "can't open the texture: %s"%(textureSurface)
	def __del__(self):
		glDeleteTextures(self.texID)
