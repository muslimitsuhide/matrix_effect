import pygame
import numpy 


class Matrix:
    def __init__(self, app, font_size=7):
        self.app = app
        self.FONT_SIZE = font_size
        self.SIZE = self.ROWS, self.COLS = app.HEIGHT // font_size, app.WIDTH // font_size
        self.letters = numpy.array([chr(int('35', 8) + i) for i in range(125)])
        self.font = pygame.font.Font('font/MS_Mincho.ttf', 8)

        self.matrix = numpy.random.choice(self.letters, self.SIZE)
        self.char_intervals = numpy.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = numpy.random.randint(1, 500, size=self.SIZE)
        self.prerendered_chars = self.get_prerendered_chars()

        self.image = self.get_image('img/test.png')


    def get_image(self, path_to_file):
        image = pygame.image.load(path_to_file)
        image = pygame.transform.scale(image, self.app.RES)
        pixel_array = pygame.pixelarray.PixelArray(image)
        return pixel_array

    def get_prerendered_chars(self):
        char_colors = [(0, green, 0) for green in range(256)]
        prerendered_chars = {}
        for char in self.letters:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars

    def run(self):
        frames = pygame.time.get_ticks()
        self.change_chars(frames)
        self.shift_column(frames)
        self.draw()

    def shift_column(self, frames):
        num_cols = numpy.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = numpy.unique(num_cols)
        self.matrix[:, num_cols] = numpy.roll(self.matrix[:, num_cols], shift=1, axis=0)

    def change_chars(self, frames):
        mask = numpy.argwhere(frames % self.char_intervals == 0)
        new_chars = numpy.random.choice(self.letters, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    def draw(self):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.FONT_SIZE, y * self.FONT_SIZE
                    _, red, green, blue = pygame.Color(self.image[pos])
                    if red and green and blue:
                        color = (red + green + blue) // 3
                        color = 220 if 160 < color < 220 else color
                        char = self.prerendered_chars[(char, (0, color, 0))]
                        char.set_alpha(color + 5)
                        self.app.surface.blit(char, pos)


class MatrixSett:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 690, 830
        pygame.init()
        self.screen = pygame.display.set_mode(self.RES)
        self.surface = pygame.Surface(self.RES)
        self.clock = pygame.time.Clock()
        self.matrix = Matrix(self)

    def draw(self):
        self.surface.fill(pygame.Color('black'))
        self.matrix.run()
        self.screen.blit(self.surface, (0, 0))

    def run(self):
        while True:
            self.draw()
            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            pygame.display.flip()
            self.clock.tick(10)


if __name__ == '__main__':
    app = MatrixSett()
    app.run()

