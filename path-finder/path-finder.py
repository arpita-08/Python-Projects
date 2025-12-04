import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze, stdscr, path=[]):
    WHITE = curses.color_pair(1)
    YELLOW = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", YELLOW)
            else:
                stdscr.addstr(i, j * 2, value, WHITE)

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors

def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    visited = set([start_pos])

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        # Visually animate the BFS
        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.refresh()
        time.sleep(0.1)

        if maze[row][col] == end:
            return path

        for neighbor in find_neighbors(maze, row, col):
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            visited.add(neighbor)
            q.put((neighbor, path + [neighbor]))

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()

wrapper(main)
