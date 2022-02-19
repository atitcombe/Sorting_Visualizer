import pygame
import random

pygame.init()  # starts the pygame


class SortingVisual:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    PURPLE = 125, 0, 125
    GREEN = 0, 255, 0

    GREY = 128, 128, 128
    BG_COLOUR = WHITE

    GRADIENTS = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 50)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.height = height
        self.width = width

        # pygame initializer
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algo Visualizers")
        self.ListComposition(lst)

    def ListComposition(self, lst):
        self.lst = lst
        self.minVal = min(lst)
        self.maxVal = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = round((self.height - self.TOP_PAD) / (self.maxVal - self.minVal))
        self.start_x = self.SIDE_PAD // 2
        # the coordinate system of the pygame has (0,0) at the top left corner


def listComposer(n, min_val, max_val):
    values = []

    for i in range(n):
        val = random.randint(min_val, max_val)
        values.append(val)

    return values


def bubble_sort(draw_info, ascending=True):
    values = draw_info.lst

    for i in range(len(values) - 1):
        for j in range(len(values) - 1 - i):
            num1 = values[j]
            num2 = values[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                values[j], values[j + 1] = values[j + 1], values[j]
                drawList(draw_info, {j: draw_info.PURPLE, j + 1: draw_info.GREEN}, True)

                yield True  # lets you pause the function and store the current state


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            drawList(draw_info, {i - 1: draw_info.PURPLE, i: draw_info.GREEN}, True)
            yield True

    return lst


def visualizeGraphic(graphicsData, graphAlgo, ascending):
    graphicsData.window.fill(graphicsData.BG_COLOUR)  # this helps basically clear the screen before anything starts

    title = graphicsData.FONT.render(f"{graphAlgo} - {'Ascending' if ascending else 'Descending'}", 1,
                                     graphicsData.PURPLE)
    graphicsData.window.blit(title, (graphicsData.width // 2 - title.get_width() // 2, 5))

    controls = graphicsData.FONT.render("R - Restart | SPACE - Let's Get Sorting! | A - Ascending | D - Descending", 1,
                                        (0,0,0))
    graphicsData.window.blit(controls, (graphicsData.width // 2 - controls.get_width() // 2, 45))

    sorting = graphicsData.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, (0,0,0))
    graphicsData.window.blit(sorting, (graphicsData.width // 2 - sorting.get_width() // 2, 75))

    drawList(graphicsData)
    pygame.display.update()


def drawList(draw_info, color_positions=dict(), clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BG_COLOUR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.minVal) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    minVal = 0
    maxVal = 100
    ascending = True
    sorting = False

    lst = listComposer(n, minVal, maxVal)
    draw_info = SortingVisual(1200, 700, lst)

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    # you always need a while loop so the program keeps running.
    while run:
        clock.tick(80)

        visualizeGraphic(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            visualizeGraphic(draw_info, sorting_algo_name, ascending)

        # always implement this to make sure you can actually quit the game

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False

            if i.type != pygame.KEYDOWN:
                continue

            if i.key == pygame.K_r:
                lst = listComposer(n, minVal, maxVal)
                draw_info.ListComposition(lst)
                sorting = False
            elif i.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif i.key == pygame.K_a and sorting == False:
                ascending = True
            elif i.key == pygame.K_d and sorting == False:
                ascending = False
            elif i.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif i.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
