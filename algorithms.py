import pygame
import math
from queue import PriorityQueue, Queue, LifoQueue

WIDTH = 800

WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* path finding algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
	def __init__(self, row, col, width, total_rows):
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
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

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


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def astar(draw, grid, start, end):
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
			reconstruct_path(came_from, end, draw)
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

def bfs(draw, start, end):
	q = Queue()
	came_from = {start: None}
	q.put(start)

	while not q.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = q.get()

		if current == end:
			if end in came_from:
				reconstruct_path(came_from, end, draw)
			end.make_end()
			return True
		
		for neighbor in current.neighbors:
			if neighbor not in came_from:
				q.put(neighbor)
				came_from[neighbor] = current
				neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def dfs(draw,start,end):

	stack = LifoQueue()
	came_from = {}
	stack.put(start)

	while not stack.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = stack.get()

		if current == end:
			if end in came_from:
				reconstruct_path(came_from, end, draw)
			end.make_end()
			return True
		
		for cell in current.neighbors:
			if cell not in came_from:
				stack.put(cell)
				came_from[cell] = current
				cell.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def dijkstra(draw,grid,start,end):

	distance = {spot: float("inf") for row in grid for spot in row}
	distance[start] = 0 

	priority_queue = PriorityQueue()
	priority_queue.put((0, start))  

	while not priority_queue.empty():
		current_distance, current = priority_queue.get()

		if current == end:
			return True

		for neighbor in current.neighbors:
			if neighbor.is_barrier():
				continue

			temp_distance = current_distance + 1

			if temp_distance < distance[neighbor]:
				distance[neighbor] = temp_distance
				priority_queue.put((temp_distance, neighbor))
				neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def ucs(draw,grid,start,end):

	cost = {spot: float("inf") for row in grid for spot in row}
	cost[start] = 0

	priority_queue = PriorityQueue()
	priority_queue.put((0, start))

	while not priority_queue.empty():
		current_cost, current = priority_queue.get()

		if current == end:
			return True

		for neighbor in current.neighbors:
			if neighbor.is_barrier():
				continue

			temp_cost = current_cost + 1

			if temp_cost < cost[neighbor]:
				cost[neighbor] = temp_cost
				priority_queue.put((temp_cost, neighbor))
				neighbor.make_open()
		
		draw()

		if current != start:
			current.make_closed()

	return False

def make_grid(rows, width):
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
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


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


def main(win, width):
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

					astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_d and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					dfs(lambda: draw(win, grid, ROWS, width), start, end)

				if event.key == pygame.K_b and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					bfs(lambda: draw(win, grid, ROWS, width), start, end)

				if event.key == pygame.K_u and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					ucs(lambda: draw(win, grid, ROWS, width), grid, start, end)
				
				if event.key == pygame.K_h and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)