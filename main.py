import pygame as pg
import random
from pygame.display import flip as refresh
from time import sleep

pg.init()
pg.display.set_caption("2D Minecraft")

scrnx, scrny = 1200, 700
window = pg.display.set_mode((scrnx, scrny))

from data import Data
from asset_holder import *

class Game:
	def __init__(self, size:int, window:pg.Surface) -> None:

		clock = pg.time.Clock()
		running = True

		self.window = window

		self.data = {}
		self.render = 30	# Renders only these many blocks around the player
		self.blocks = {
			"stone"      : stone.img      ,
			"cobblestone": cobblestone.img,
			"diamondore" : diamondore.img ,
			"goldore"    : goldore.img    ,
			"empty"      : empty.img
		}
		self.display = []
		self.block_list = ["stone"] * stone.rate + ["diamondore"] * diamondore.rate + ["goldore"] * goldore.rate + ["cobblestone"] * cobblestone.rate

		self.offset_x = self.offset_y = 0
		self.size = size

		font = pg.font.Font('freesansbold.ttf', 32)
		text = font.render(f"Loading Blocks...", True, (0, 255, 0))
		
		self.window.blit(text, (window.get_width()//8, window.get_height()//2))
		refresh()

		self.render_world()
		self.display_update(False)
		sleep(2)
		refresh()

		while running:
			for event in pg.event.get():

				if event.type == pg.KEYDOWN:
					if event.key == pg.K_a or event.key == pg.K_LEFT:
						self.map_update("left")

					elif event.key == pg.K_w or event.key == pg.K_UP:
						self.map_update("up")

					elif event.key == pg.K_d or event.key == pg.K_RIGHT:
						self.map_update("right")

					elif event.key == pg.K_s or event.key == pg.K_DOWN:
						self.map_update("down")

				if event.type == pg.QUIT:
					running = False

			clock.tick(Data.fps)


	def map_update(self, direction:str):		# Moves the map in the opposite direction of the player 

		self.data[f"x{player.pos['x']}y{player.pos['y']}"] = "empty"

		if direction == "up":
			player.pos["y"] -= self.size
			self.offset_y += self.size
				
		elif direction == "right":
			player.pos["x"] += self.size
			self.offset_x -= self.size
			
		elif direction == "down":
			player.pos["y"] += self.size
			self.offset_y -= self.size
			
		elif direction == "left":
			player.pos["x"] -= self.size
			self.offset_x += self.size

		self.render_world()
		self.display_update()

	
	def render_world(self):						# Stores the blocks to be rendered in a list

		for y in range(player.pos["y"]+self.render*self.size, player.pos["y"]-(self.render+1)*self.size, -self.size):
			for x in range(player.pos["x"]-self.render*self.size, player.pos["x"]+(self.render*self.size), self.size):
				point = f"x{x}y{y}"
				self.display.append(point)


	def display_update(self, auto_render=True):	# Automatically assigns a random block to a coordinate
												# if it doesn't exist & renders the whole map
												# including the player.

		for block in self.display:
			x, y = self.read_axises(block)

			try:
				block_img = self.blocks[self.data[block]]
			except KeyError:
				new_block = random.choice(self.block_list)
				self.data[block] = new_block
				block_img = self.blocks[new_block]
				
			self.window.blit(block_img, (x+self.offset_x, y+self.offset_y))
			self.window.blit(player.img, (player.pos["x"] + self.offset_x, player.pos["y"] + self.offset_y))
			
			self.display = []
		
		if auto_render is True:
			refresh()


	def read_axises(self, coords:str):			# Converts a string of coordinate (xNyN where N is the
												# coordinate of it's respective axis) to a tuple where
												# the fist index is of X axis and second of Y axis
		xval = yval = ""
		ycount = False
		
		for x in coords: 	# For counting the X value
			if x == "y":
				break
			if x != "x":
				xval = f"{xval}{x}"

		for y in coords: 	# For counting the Y value
			if ycount:
				yval =f"{yval}{y}"
			if y == "y":
				ycount = True
			
		xval = int(xval.strip())
		yval = int(yval.strip())
		return (xval, yval)

Game(Data.block_size, window)