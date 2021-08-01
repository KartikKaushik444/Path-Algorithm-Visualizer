import pygame
import sys
import math
from queue import PriorityQueue
from queue import Queue 
from queue import LifoQueue

pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finder Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BLUE_GREEN = (0, 255, 170)

class Spot:
	def __init__(self, row, col, width, total_rows):              # In spot class width represents gap
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == PURPLE#RED

	def is_open(self):
		return self.color == TURQUOISE#GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == RED

	def is_path(self):
		return self.color == YELLOw#PURPLE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = PURPLE#RED

	def make_open(self):
		self.color = TURQUOISE#GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = RED#TURQUOISE

	def make_path(self):
		self.color = YELLOW#PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, start):
	while current in came_from:
		if current == start:
			break
		current = came_from[current]
		# if current.is_path == False:
		current.make_path()
		draw()


def dfs(draw, grid, start, end):
	count = 0
	# open_set = Queue()
	open_set = LifoQueue()
	open_set.put(start)
	came_from = {}
	# g_score = {spot: float("inf") for row in grid for spot in row}
	# g_score[start] = 0
	# f_score = {spot: float("inf") for row in grid for spot in row}
	# f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()
		open_set_hash.remove(current)

		for neighbor in current.neighbors:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()


			if neighbor.is_open() == True:
				continue
			if neighbor.is_closed() == True:
				continue
			came_from[neighbor] = current
			if neighbor not in open_set_hash:
				count += 1
				if neighbor == end:
					reconstruct_path(came_from, end, draw, start)
					end.make_end()
					start.make_start()
					return True
				open_set.put(neighbor)
				open_set_hash.add(neighbor)
				if neighbor.is_open() == False and neighbor.is_closed() == False:
					neighbor.make_open()
			# temp_g_score = g_score[current] + 1

			# if temp_g_score < g_score[neighbor]:
				# came_from[neighbor] = current
				# g_score[neighbor] = temp_g_score
				# f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				# if neighbor not in open_set_hash:
				# 	count += 1
				# 	open_set.put((f_score[neighbor], count, neighbor))
				# 	open_set_hash.add(neighbor)
				# 	neighbor.make_open()
  
		draw()
		if current != start:
			current.make_closed()
			# if current.is_open() == True and current.is_closed() == False:
			# 	current.make_closed()

	return False

def bfs(draw, grid, start, end):
	count = 0
	open_set = Queue()
	open_set.put(start)
	came_from = {}
	# g_score = {spot: float("inf") for row in grid for spot in row}
	# g_score[start] = 0
	# f_score = {spot: float("inf") for row in grid for spot in row}
	# f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()
		open_set_hash.remove(current)

		for neighbor in current.neighbors:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()


			if neighbor.is_open() == True:
				continue
			if neighbor.is_closed() == True:
				continue
			came_from[neighbor] = current
			if neighbor not in open_set_hash:
				count += 1
				if neighbor == end:
					reconstruct_path(came_from, end, draw, start)
					end.make_end()
					start.make_start()
					return True
				open_set.put(neighbor)
				open_set_hash.add(neighbor)
				if neighbor.is_open() == False and neighbor.is_closed() == False:
					neighbor.make_open()
			# temp_g_score = g_score[current] + 1

			# if temp_g_score < g_score[neighbor]:
				# came_from[neighbor] = current
				# g_score[neighbor] = temp_g_score
				# f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				# if neighbor not in open_set_hash:
				# 	count += 1
				# 	open_set.put((f_score[neighbor], count, neighbor))
				# 	open_set_hash.add(neighbor)
				# 	neighbor.make_open()
  
		draw()
		if current != start:
			current.make_closed()
			# if current.is_open() == True and current.is_closed() == False:
			# 	current.make_closed()

	return False

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw, start)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
  
		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):          # creates a 2-D array grid which stores spot
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))           # It is drawing horizontal lines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))         #It is drawing vertical lines


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def welcomeScreen(window):
	run = True
	
	window.fill(BLACK)
	welcome_font = pygame.font.SysFont("Times New Roman", 60, bold=True)
	font = pygame.font.SysFont("Times New Roman", 50, bold=False, italic=True)
	Welcome_text =  welcome_font.render("Welcome", True, WHITE, BLACK)
	DFS_text = font.render("For DFS Press 'd' button", True, WHITE, BLACK)
	BFS_text = font.render("For BFS Press 'b' button", True, WHITE, BLACK)
	AStar_text = font.render("For A Star Press 'a' button ", True, WHITE, BLACK)
	while run:
		window.blit(Welcome_text, (0.38 * WIDTH, 0.1 * WIDTH) )
		window.blit(AStar_text, (0.18 * WIDTH, 0.3 * WIDTH) )
		window.blit(BFS_text, (0.18 * WIDTH, 0.5 * WIDTH) )
		window.blit(DFS_text, (0.18 * WIDTH, 0.7 * WIDTH) )
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					pygame.display.set_caption("Pathfinder Visualizer : DFS (Depth First Search)")
					run = False
					return "DFS"

				if event.key == pygame.K_b:
					pygame.display.set_caption("Pathfinder Visualizer : BFS (Breadth First Search)")
					run = False
					return "BFS"

				if event.key == pygame.K_a:
					pygame.display.set_caption("Pathfinder Visualizer : A Star")
					run = False
					return "ASTAR"

		







def main(win, width):
	choice = welcomeScreen(win)
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					if choice == "ASTAR":
						algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					
					elif choice == "BFS":
						bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
					
					elif choice == "DFS":
						dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)