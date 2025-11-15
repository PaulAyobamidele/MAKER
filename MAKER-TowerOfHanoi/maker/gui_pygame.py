import pygame
import sys
import time

class TowerOfHanoiPygame:
    def __init__(self, actions, num_disks, move_delay=0.8):
        """
        :param actions: List of moves [[disk, from_peg, to_peg], ...]
        :param num_disks: Total number of disks
        :param move_delay: Seconds between moves
        """
        self.actions = actions
        self.num_disks = num_disks
        self.move_delay = move_delay
        self.state = [list(range(num_disks, 0, -1)), [], []]

        # Pygame setup
        pygame.init()
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tower of Hanoi - MAKER Visualizer")
        self.clock = pygame.time.Clock()

        # Pegs
        self.peg_x = [self.width // 6, self.width // 2, 5 * self.width // 6]
        self.peg_y_bottom = self.height - 50
        self.disk_height = 20
        self.disk_width_factor = 20

        # Colors
        self.bg_color = (30, 30, 30)
        self.peg_color = (200, 200, 200)
        self.disk_color = (70, 130, 180)
        self.highlight_color = (255, 165, 0)

        # Font
        self.font = pygame.font.SysFont(None, 24)

        self.move_index = 0

        self.run_visualization()

    def draw_pegs(self):
        for x in self.peg_x:
            pygame.draw.line(self.screen, self.peg_color, (x, 50), (x, self.peg_y_bottom), 5)

    def draw_disks(self, highlight_disk=None):
        for peg_index, peg in enumerate(self.state):
            for disk_index, disk in enumerate(reversed(peg)):
                x = self.peg_x[peg_index]
                y = self.peg_y_bottom - disk_index * self.disk_height
                width = disk * self.disk_width_factor
                color = self.highlight_color if disk == highlight_disk else self.disk_color
                pygame.draw.rect(
                    self.screen, color,
                    pygame.Rect(x - width // 2, y - self.disk_height, width, self.disk_height)
                )
        # Step counter
        text = self.font.render(f"Step {self.move_index}/{len(self.actions)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def animate_move(self):
        if self.move_index >= len(self.actions):
            return False  # Finished
        disk, from_peg, to_peg = self.actions[self.move_index]
        self.state[from_peg].pop()
        self.state[to_peg].append(disk)
        self.move_index += 1
        return True

    def run_visualization(self):
        running = True
        last_move_time = time.time()

        while running:
            self.screen.fill(self.bg_color)
            self.draw_pegs()
            highlight_disk = None
            if self.move_index < len(self.actions):
                highlight_disk = self.actions[self.move_index][0]
            self.draw_disks(highlight_disk=highlight_disk)

            pygame.display.flip()
            self.clock.tick(60)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Animate moves with delay
            if self.move_index < len(self.actions) and (time.time() - last_move_time) >= self.move_delay:
                self.animate_move()
                last_move_time = time.time()

        pygame.quit()
        sys.exit()


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    example_actions = [
        [1, 0, 2],
        [2, 0, 1],
        [1, 2, 1],
        [3, 0, 2],
        [1, 1, 0],
        [2, 1, 2],
        [1, 0, 2]
    ]
    TowerOfHanoiPygame(example_actions, num_disks=3)
