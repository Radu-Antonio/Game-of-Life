import pygame, sys, copy

pygame.init()
pygame.display.set_caption('Game Of Life')
SCREEN_SIZE, SQUARE_SIZE = 800, 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (179, 179, 179)

fps = 1000
started = 0
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
grid = [[False] * (SCREEN_SIZE // SQUARE_SIZE) for _ in range(SCREEN_SIZE // SQUARE_SIZE)]
prevGrid = [[False] * (SCREEN_SIZE // SQUARE_SIZE) for _ in range(SCREEN_SIZE // SQUARE_SIZE)]
neighbours = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
size = len(grid)
fpsclock = pygame.time.Clock()

def update():
	global grid, prevGrid

	for i in range(size):
		for j in range(size):
			liveNeighbours = 0
			for x, y in neighbours:
				if 0 <= i + x < size and 0 <= j + y < size and prevGrid[i+x][j+y]:
					liveNeighbours += 1
			grid[i][j] = True if (prevGrid[i][j] and 2 <= liveNeighbours <= 3) or (not prevGrid[i][j] and liveNeighbours == 3) else False

		fpsclock.tick(fps)
		pygame.display.update()

	prevGrid = copy.deepcopy(grid)

def draw():
	screen.fill(GRAY)
	for i in range(size):
		for j in range(size):
			pygame.draw.rect(screen, BLACK if grid[i][j] else WHITE, (i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

def main():
	global started, grid, prevGrid
	draw()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
			if event.type == pygame.KEYDOWN and event.key == pygame.K_r and started:
				grid = [[False] * (SCREEN_SIZE // SQUARE_SIZE) for _ in range(SCREEN_SIZE // SQUARE_SIZE)]
				prevGrid = [[False] * (SCREEN_SIZE // SQUARE_SIZE) for _ in range(SCREEN_SIZE // SQUARE_SIZE)]
				started = 0
				draw()
			
			if started == 0:
				mouse = pygame.mouse.get_pressed()
				x, y = pygame.mouse.get_pos()
				x //= SQUARE_SIZE
				y //= SQUARE_SIZE
			
				if mouse[0]:
					grid[x][y] = True
					prevGrid[x][y] = True
					pygame.draw.rect(screen, BLACK, (x * SQUARE_SIZE + 1, y * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

				if mouse[2]:
					grid[x][y] = False
					prevGrid[x][y] = False
					pygame.draw.rect(screen, WHITE, (x * SQUARE_SIZE + 1, y * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				started += 1

		if started:
			update()
			draw()

		fpsclock.tick(fps)
		pygame.display.update()

if __name__ == "__main__":
	main()