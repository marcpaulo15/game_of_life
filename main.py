import random
import os
import time
from typing import NewType, Any, List, Tuple, Set, Dict

import yaml
import pygame
import numpy as np


 # A Cell is represented by a (column, row) pair
Cell = NewType('Cell', Tuple[int, int])

class GameOfLife:
    """
    Implementation of the Conway's Game of Life using Pygame.

    ATTRIBUTES:
        - _config: configuration dictionary (from 'config.yml')
        - _n_cols: number of columns in the grid
        - _n_rows: number of rows in the grid
        - _n_cells: total number of cells in the grid (_n_cols * _n_rows)
        - _screen: pygame surface where the simulation is displayed
        - clock: pygame clock to control the speed of the simulation
        - _living_cells: set of living cells {(col, row)} in current timestep
        - _is_paused: whether the simulation is running or frozen
        - _run_next_step: whether to run just the next step (only if _is_paused)
        - _current_pattern: Pattern seed id or 'Rand' if random pattern

    METHODS:
        - process_events: Translate mouse clicks and keyboard actions (from
            the user) to specific events in the simulation.
        - run_logic:  Update the grid following the Rules of the game.
        - draw: Display the elements of the simulations on '_screen' attribute.
    """

    def __init__(self) -> None:
        """
        Initialize a GameOfLife instance
        """

        # Read the configuration file
        self._config = self._get_config()

        # If provided, set the random seed (to create initial random patterns)
        if self._config['random_seed'] is not None:
            random.seed(self._config['random_seed'])

        # Size of the grid:
        self._n_cols = self._config['width'] // self._config['cell_size']
        self._n_rows = self._config['height'] // self._config['cell_size']
        self._n_cells = self._n_rows * self._n_cols

        # Initialize the Pygame elements
        pygame.init()
        self._screen = pygame.display.set_mode(
            (self._config['width'], self._config['height'])
        )
        pygame.display.set_caption(
            self._config['screen_caption'].format(pat='None', paused='paused')
        )
        self.clock = pygame.time.Clock()

        # Elements of the simulation:
        self._living_cells = set()  # set of (x,y) positions of living cells
        self._is_paused = True  # whether the simulation is running or frozen
        self._run_next_step = False
        self._current_pattern = None  # information found in the caption


    @staticmethod
    def _get_config() -> Dict[str, Any]:
        """
        Read the configuration file called 'config.yml' and return it as a
        python dictionary.

        :return: configuration dictionary
        """

        this_file_path = os.path.abspath(__file__)
        project_path = '/'.join(this_file_path.split('/')[:-1])
        config_path = project_path + '/config.yml'

        with open(config_path, 'r') as yml_file:
            config = yaml.safe_load(yml_file)[0]['config']
        return config


    def _generate_random_init_grid(self) -> Set[Cell]:
        """
        Generate an initial random pattern to start the simulation.

        :return: set of living cells representing the initial pattern
        """

        self._current_pattern = 'Rand'
        # Random percentage of living cells. Max and Min values are in config.
        pct_living_cells = random.randrange(
            start=self._config['gen_min_pct_living_cells'],
            stop=self._config['gen_max_pct_living_cells']
        )
        new_living_cells = set()  # init living cells
        n_cells_to_gen = (self._n_cells * pct_living_cells) // 100
        for _ in range(n_cells_to_gen):
            row = random.randrange(start=0, stop=self._n_rows)
            col = random.randrange(start=0, stop=self._n_cols)
            new_living_cells.add(Cell((col, row)))
        return new_living_cells


    def _generate_seed_pattern(self, id_: int) -> Set[Cell]:
        """
        Load the initial pattern with the given 'id_' from the file
        'seed_patterns.yml'. There are 9 different 'id_' values.
        The patterns are centered to the middle of the grid.

        :param id_: identifier of one of the available patterns (from 1 to 9)
        :raise: ValueError if the given 'id_' is not valid
        :return: set of initial living cells, setting up the pattern
        """

        if not (1 <= id_ <= 9):
            raise ValueError("the given pattern 'id_' must be between 1 and 9")

        this_file_path = os.path.abspath(__file__)
        project_path = '/'.join(this_file_path.split('/')[:-1])
        seed_patterns_path = project_path + '/seed_patterns.yml'

        with open(seed_patterns_path, 'r') as yml_file:
            binary_pattern = yaml.safe_load(yml_file)[0]['patterns'][id_]
        # Create a binary two-dimensional array {zeros: dead; ones: living}
        binary_pattern = np.array(binary_pattern)
        # Compute the top-left corner to place the pattern in the center
        top_left_col = (self._n_cols - len(binary_pattern[0])) // 2
        top_left_row = (self._n_rows - len(binary_pattern)) // 2

        # Get the Cells [(col, row)] with ones (living cells)
        # Pair the two tuples from the 'where' funtion (lists rows and cols)
        seed_pattern_living_cells = zip(*np.where(binary_pattern))
        pattern_living_cells = set()
        for row, col in seed_pattern_living_cells:
            pattern_living_cells.add(
                Cell((col+top_left_col, row+top_left_row))
            )
        return pattern_living_cells


    def process_events(self) -> bool:
        """
        Process the actions carried out by the user:
            - Mouse click: to set cells to dead/living states
            - KeyBoard:
                - 'space_bar': pause/resume the simulation
                - 'g': generate an initial random pattern
                - 'c': clear the screen, empty the grid (kill all the cells)
                - '->' (right arrow): run the next step of the simulation
                - from '0' to '9': generate one of the available pre-defined
                    initial patterns (found in 'seed_patterns.yml')
        :return: whether to go on with the simulation
        """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False  # quit the simulation

            if event.type == pygame.MOUSEBUTTONDOWN:  # TODO:
                # kill living cells or bring dead cells back to life
                x, y = pygame.mouse.get_pos()
                col = x // self._config['cell_size']
                row = y // self._config['cell_size']
                cell = Cell((col, row))
                if cell in self._living_cells:  # kill a living cell
                    self._living_cells.remove(cell)  # TODO:
                else:  # bring the dead cell back to livr
                    self._living_cells.add(cell)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pause/resume the simulation
                    self._is_paused = not self._is_paused
                elif event.key == pygame.K_RIGHT and self._is_paused:
                    # run the next step of the simulation
                    self._run_next_step = True
                elif event.key == pygame.K_c:
                    # clear the screen, empty the grid (kill all the cells)
                    self._living_cells.clear()
                    self._is_paused = True
                elif event.key == pygame.K_g:
                    # generate an initial random pattern
                    self._living_cells = self._generate_random_init_grid()
                    self._is_paused, self._current_pattern = True, 'Rand'
                elif event.key == pygame.K_1:  # pattern 1 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=1)
                    self._is_paused, self._current_pattern = True, '1'
                elif event.key == pygame.K_2:  # pattern 2 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=2)
                    self._is_paused, self._current_pattern = True, '2'
                elif event.key == pygame.K_3:  # pattern 3 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=3)
                    self._is_paused, self._current_pattern = True, '3'
                elif event.key == pygame.K_4:  # pattern 4 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=4)
                    self._is_paused, self._current_pattern = True, '4'
                elif event.key == pygame.K_5:  # pattern 5 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=5)
                    self._is_paused, self._current_pattern = True, '5'
                elif event.key == pygame.K_6:  # pattern 6 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=6)
                    self._is_paused, self._current_pattern = True, '6'
                elif event.key == pygame.K_7:  # pattern 7 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=7)
                    self._is_paused, self._current_pattern = True, '7'
                elif event.key == pygame.K_8:  # pattern 8 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=8)
                    self._is_paused, self._current_pattern = True, '8'
                elif event.key == pygame.K_9:  # pattern 9 (seed_patterns.yml)
                    self._living_cells = self._generate_seed_pattern(id_=9)
                    self._is_paused, self._current_pattern = True, '9'
        return True  # go on with the simulation


    def run_logic(self) -> None:
        """
        Update the grid following the Rules of the game.
        At each step in time, the following transitions occur:
            - Underpopulation:
                Any living cell with fewer than two living neighbours dies.
            - Survival:
                Any living cell with two or three living neighbours lives on to
                the next generation
            - Overpopulation:
                Any living cell with more than three living neighbours dies.
            - Reproduction:
                Any dead cell with exactly three living neighbours becomes a
                living cell.
        NOTE: the exact values of these parameters can be changed in the
        configuration file 'config.yml'. Feel free to test different settings.

        :return: None. The '_living_cells' attribute is updated
        """

        pygame.display.set_caption(
            self._config['screen_caption'].format(
                pat=self._current_pattern,
                paused='paused' if self._is_paused else 'running')
        )

        if self._is_paused and not self._run_next_step:
                return  # do nothing, wait until the simulation is resumed

        if self._config['sleep'] is not None:  # slow down the simulation
            time.sleep(self._config['sleep'])

        # Set containing all the neighbors of the currently living cells
        all_neighbors = set()
        # Set of the next generation cells, the next '_living_cells'
        new_living_cells = set()

        # For each living cell, get the neighbors and check if the cell will
        # live on to the next generation (survive).
        for cell in self._living_cells:
            cell_neighbors = self._get_neighbors(cell=cell)
            all_neighbors.update(cell_neighbors)
            cell_living_neighbors = list(
                filter(
                    lambda cell_: cell_ in self._living_cells, cell_neighbors
                )
            )
            if (self._config['underpopulation'] <=
                    len(cell_living_neighbors) <=
                    self._config['overpopulation']):
                new_living_cells.add(cell)
            # ELSE: the cell dies by underpopulation or overpopulation

        # For each neighbor of the currently living cells, check if it will be
        # brought back to life (reproduction)
        for cell in all_neighbors:
            cell_neighbors = self._get_neighbors(cell=cell)
            cell_living_neighbors = list(
                filter(
                    lambda cell_: cell_ in self._living_cells, cell_neighbors
                )
            )
            if len(cell_living_neighbors) == self._config['reproduction']:
                new_living_cells.add(cell)
        # Update the '_living_cells' attribute with the new generation
        self._living_cells = new_living_cells
        self._run_next_step = False  # it might be already False


    def _get_neighbors(self, cell: Cell) -> List[Cell]:
        """
        Returns the list of (at most) 8 neighbor of the given 'cell'.
        Each cell is represented by the pair (col, row).
        The grid is either infinite (unbounded) or finite (bounded),
        [See config].

        :param cell: (col, row)
        :return: set of neighbors of the given 'cell'
        """

        col, row = cell
        grid_is_infinite = self._config['grid_is_infinite']
        delta_row_vals, delta_col_vals = [-1, 0, 1], [-1, 0, 1]

        # Update the delta values if the cell is on the edge of the grid
        if row == self._n_rows-1:  # if 'row' is the bottom row
            if grid_is_infinite:  # unbounded grid, bottom neighbor at the top
                delta_row_vals[-1] = - self._n_rows + 1
            else:  # bounded grid, 'row' has no neighbors below.
                delta_row_vals.pop()  # remove last delta_row value

        elif row == 0:  # if 'row' is the top row
            if grid_is_infinite:  # unbounded grid, top neighbor at the bottom
                delta_row_vals[0] = self._n_rows - 1
            else:  # bounded grid, 'row' has no neighbors above.
                delta_row_vals.pop(0)  # remove the first delta_row value

        if col == self._n_cols-1:  # if 'col' is the rightmost column
            if grid_is_infinite:  # unbounded grid, right neighbor on the left
                delta_col_vals[-1] = - self._n_cols + 1
            else:  # bounded grid, 'col' has no neighbors on the right side
                delta_col_vals.pop()  # remove the last delta_col value
        elif col == 0:  # if 'col' is the leftmost column
            if grid_is_infinite:  # unbounded grid, left neighbor on the right
                delta_col_vals[0] = self._n_cols - 1
            else:  # bounded grid, 'col' as no neighbors on the left side
                delta_col_vals.pop(0)  # remove the first delta_col value

        neighbors = []  # neighbors of the given 'cell' (living or dead)
        for delta_col in delta_col_vals:
            for delta_row in delta_row_vals:
                if delta_col == 0 and delta_row == 0:
                    continue  # this iteration is the given 'cell' itself
                neighbors.append(Cell((col+delta_col, row+delta_row)))
        return neighbors


    def draw(self) -> None:
        """
        Display the simulation elements on the screen (pygame surface).
        NOTE that the colors can be customized in the configuration file.
        Feel free to test different colors

        :return: None. Updates the screen content.
        """

        self._screen.fill(self._config['dead_cell_color'])  # background
        cell_size = self._config['cell_size']

        # Draw the living cells (using a different color)
        for col, row in self._living_cells:
            pygame.draw.rect(
                surface=self._screen,
                color=self._config['living_cell_color'],
                rect=(col*cell_size, row*cell_size, cell_size, cell_size)
            )

        # Draw the horizontal lines of the grid
        for row in range(self._n_rows):
            pygame.draw.line(
                surface=self._screen,
                color=self._config['grid_line_color'],
                start_pos=(0, row*cell_size),
                end_pos=(self._config['width'], row*cell_size)
            )

        # Draw the vertical lines of the grid
        for col in range(self._n_cols):
            pygame.draw.line(
                surface=self._screen,
                color=self._config['grid_line_color'],
                start_pos=(col*cell_size, 0),
                end_pos=(col*cell_size, self._config['height'])
            )
        pygame.display.update()  # Update the content of the screem


if __name__ == '__main__':
    simulation = GameOfLife()

    running = True
    while running:
        running = simulation.process_events()
        simulation.run_logic()
        simulation.draw()
        simulation.clock.tick()

    pygame.quit()
