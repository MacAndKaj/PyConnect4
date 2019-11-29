from PlayerAI import *

CR_BLACK = (0, 0, 0)
CR_WHITE = (255, 255, 255)
CR_RED = (255, 50, 50)
CR_BLUE = (150, 150, 255)
CR_GREEN = (100, 255, 100)
CR_GREE_END = (0, 255, 0)
CR_BLUE_END = (0, 0, 128)


class Board:

    def __init__(self):
        self._state = State([[None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None]])
        self._size = None
        self._position = None
        self._current_new_button = None
        self._new_button_pos = None
        self._actions = []
        self._changable = True
        self._winner = None

    def add_action(self, action):
        if action is not None:
            self._actions.append(action)

    def _handle_actions(self):
        if len(self._actions) != 0:
            pass

    def init(self, surface):
        self._size = (surface.get_size()[0] * 0.9, surface.get_size()[1] * 0.88)
        self._position = ((surface.get_size()[0] - self._size[0]) / 2, (surface.get_size()[1] - self._size[1]))
        self._space_for_button = (int(self._size[0] / 7), int(self._size[1] / 6))
        self._button_radius = int(self._position[1] / 2)

    def draw(self, surface: pygame.Surface):
        """
        Public draw board method. Computes needed informations and calls draw implementation.
        :param surface: pygame.Surface - surface to draw board
        :return: None
        """
        self._size = (surface.get_size()[0] * 0.9, surface.get_size()[1] * 0.88)
        self._position = ((surface.get_size()[0] - self._size[0]) / 2, (surface.get_size()[1] - self._size[1]))
        self._space_for_button = (int(self._size[0] / 7), int(self._size[1] / 6))
        self._button_radius = int(self._position[1] / 2)

        if self._new_button_pos is None:
            self._new_button_pos = int(self._size[0] / 2)

        self._draw(surface)

    def _draw(self, surface: pygame.Surface):
        """
        Implementation of draw method.
        :param surface: pygame.Surface - surface to draw.
        :return: None
        """
        bufferPosition, bufferSize = (self._position[0], 0), (self._size[0], self._position[1])
        pygame.draw.rect(surface, CR_BLUE, pygame.Rect(self._position, self._size))
        pygame.draw.rect(surface, CR_GREEN, pygame.Rect(bufferPosition, bufferSize))
        self._draw_new_button(surface)
        position = [int(self._position[0] + self._space_for_button[0] / 2),
                    int(self._position[1] + self._space_for_button[1] / 2)]
        start_x = position[0]
        for line in self._state.get():
            for _ in line:
                pygame.draw.circle(surface, CR_BLACK, position, self._button_radius)
                position[0] += self._space_for_button[0]
            position[1] += self._space_for_button[1]
            position[0] = start_x
        self._refresh_and_draw_buttons(surface)

    def _draw_new_button(self, surface: pygame.Surface):
        """
        Draws button that waits to drop. It is player's button that moves where mouse is.
        :param surface: Surface to draw
        :return: None
        """
        mouse_pos_x, _ = pygame.mouse.get_pos()
        left_border = self._position[0] + self._button_radius
        right_border = self._position[0] + self._size[0] - self._button_radius
        if left_border < mouse_pos_x < right_border:
            self._new_button_pos = mouse_pos_x

        pygame.draw.circle(surface, CR_RED, (self._new_button_pos, self._button_radius), self._button_radius)

    def mouse_click(self, mouse_position) -> str:
        if not self._changable:
            return 'FAIL'
        if self._position[0] < mouse_position[0] < self._position[0] + self._size[0]:
            column_nr = int((mouse_position[0] - self._position[0] / self._space_for_button[0]) / 100)
            if self._is_full(column_nr):
                return 'FAIL'
            self._drop_button(column_nr,
                              Button('PLAYER', [
                                  int(self._position[0] + (
                                          column_nr * self._space_for_button[0]) + self._button_radius / 2 + (
                                              self._space_for_button[0] - self._button_radius) / 2),
                                  int(self._position[1] + self._space_for_button[1] / 2)],
                                     self._button_radius))
        return 'SUCCESS'

    def pc_drop_button(self, column_nr):
        if self._is_full(column_nr) or not self._changable:
            return 'FAIL'
        self._drop_button(column_nr,
                          Button('COMPUTER', [
                              int(self._position[0] + (
                                      column_nr * self._space_for_button[0]) + self._button_radius / 2 + (
                                          self._space_for_button[0] - self._button_radius) / 2),
                              int(self._position[1] + self._space_for_button[1] / 2)],
                                 self._button_radius))
        return 'SUCCESS'

    def _drop_button(self, column: int, button):
        if self._state.get()[0][column] is None:
            self._state.get()[0][column] = button
            self._changable = False

    def _refresh_and_draw_buttons(self, surface):
        for col_nr in range(len(self._state.get()[0])):
            for row_nr in range(len(self._state.get()) - 1, 0, -1):
                if self._state.get()[row_nr - 1][col_nr] is not None and self._state.get()[row_nr][col_nr] is None:
                    self._state.get()[row_nr][col_nr] = self._state.get()[row_nr - 1][col_nr]
                    self._state.get()[row_nr][col_nr].move(self._space_for_button[1])
                    self._state.get()[row_nr - 1][col_nr] = None

        winner = None
        if not self._changable:
            winner = self._check_changability()

        for row in self._state.get():
            for element in row:
                if element is not None:
                    element.draw(surface)

        if winner is not None:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(str(winner) + ' wins!', True, CR_GREE_END, CR_BLUE_END)
            textRect = text.get_rect()
            textRect.center = (surface.get_size()[0] // 2, surface.get_size()[1] // 2)
            surface.blit(text, textRect)

    def _check_changability(self):
        for col_nr in range(len(self._state.get()[0])):
            for row_nr in range(len(self._state.get()) - 1, 0, -1):
                if self._state.get()[row_nr - 1][col_nr] is not None and self._state.get()[row_nr][col_nr] is None:
                    return
        if not self._are_4_connected():
            self._changable = True

        return self._winner

    def reset(self):
        for row in self._state.get():
            for col_nr in range(len(row)):
                row[col_nr] = None
        self._winner = None

    def _is_full(self, column_nr):
        for row in self._state.get():
            if row[column_nr] is None:
                return False
        return True

    def _are_4_connected(self):
        state = self._state.get()

        rows = len(state)
        for nr_of_row in range(rows):
            columns = len(state[nr_of_row])
            for nr_of_col in range(columns):

                if state[nr_of_row][nr_of_col] is not None:
                    if nr_of_col + 3 < columns:
                        if state[nr_of_row][nr_of_col + 1] == state[nr_of_row][nr_of_col]:
                            if state[nr_of_row][nr_of_col + 2] == state[nr_of_row][nr_of_col]:
                                if state[nr_of_row][nr_of_col + 3] == state[nr_of_row][nr_of_col]:
                                    self._winner = state[nr_of_row][nr_of_col]
                                    return True

                        if nr_of_row + 3 < rows:
                            if state[nr_of_row + 1][nr_of_col + 1] == state[nr_of_row][nr_of_col]:
                                if state[nr_of_row + 1][nr_of_col + 2] == state[nr_of_row][nr_of_col]:
                                    if state[nr_of_row + 1][nr_of_col + 3] == state[nr_of_row][nr_of_col]:
                                        self._winner = state[nr_of_row][nr_of_col]
                                        return True

                    if nr_of_row + 3 < rows:
                        if state[nr_of_row + 1][nr_of_col] == state[nr_of_row][nr_of_col]:
                            if state[nr_of_row + 2][nr_of_col] == state[nr_of_row][nr_of_col]:
                                if state[nr_of_row + 3][nr_of_col] == state[nr_of_row][nr_of_col]:
                                    self._winner = state[nr_of_row][nr_of_col]
                                    return True
                        if nr_of_col - 3 >= 0:
                            if state[nr_of_row + 1][nr_of_col - 1] == state[nr_of_row][nr_of_col]:
                                if state[nr_of_row + 2][nr_of_col - 2] == state[nr_of_row][nr_of_col]:
                                    if state[nr_of_row + 3][nr_of_col - 3] == state[nr_of_row][nr_of_col]:
                                        self._winner = state[nr_of_row][nr_of_col]
                                        return True
        return False

    def AI(self, move_owner):
        if self._changable:
            tree = Tree(Node(self._state, 0, 'MAX', None, move_owner))
            tree.construct(2)
            new_state = tree.minmax()
            return self._state.get_column_to_new_state(new_state[0].get_state().get())
        return None


class Game(object):
    def __init__(self, size=None) -> None:
        self._running = False
        self._displaySurface = None
        if size is not None:
            self._size = (self._width, self._height) = size
        else:
            self._size = (self._width, self._height) = (720, 580)
        self._board = None

        self._actions_def = {
            pygame.K_RIGHT: 'RIGHT',
            pygame.K_d: 'RIGHT',
            pygame.K_LEFT: 'LEFT',
            pygame.K_a: 'LEFT',
            pygame.K_SPACE: 'DROP',
        }
        self._clock = pygame.time.Clock()
        self._clock.tick()
        self._frameTime = self._clock.get_time()
        if random.randint(0, 1) == 0:
            self._move = 'PLAYER'
        else:
            self._move = 'COMPUTER'

    def init(self, name=None, icon=None):
        pygame.init()
        self._displaySurface: pygame.Surface = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self._board = Board()
        self._board.init(self._displaySurface)
        if name is not None:
            pygame.display.set_caption(name, name)
        if icon is not None:
            pygame.display.set_icon(icon)

    def run(self):
        self._running = True

        while self._running:
            self._displaySurface.fill(CR_WHITE)
            for event in pygame.event.get():
                self._handle_event(event)
            if self._move == 'COMPUTER':
                col = self._board.AI(self._move)
                if col is not None and self._board.pc_drop_button(col) == 'SUCCESS':
                    self._move = 'PLAYER'

            self._render()
            pygame.display.flip()

        pygame.quit()

    def _render(self):
        self._clock.tick(15)
        self._board.draw(self._displaySurface)

    def _handle_event(self, event: pygame.event):
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if self._board.mouse_click(pygame.mouse.get_pos()) == 'SUCCESS':
                self._move = 'COMPUTER'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self._board.reset()

        self._board.add_action(self._actions_def.get(event.type))

    def _end(self):
        self._board.reset()


if __name__ == '__main__':
    game = Game()

    game.init(name="Connect 4")
    game.run()
