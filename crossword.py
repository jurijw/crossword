import numpy as np
from user_input import hints_and_answers

# DEBUG ONLY
np.random.seed(0)


def clean_answers(answer):
    """Function that sanitizes answer input so that it can be displayed in
    a crossword-grid. Removes spaces and makes all characters upper-case."""
    return answer.replace(" ", "").upper()


answers = list(map(clean_answers, hints_and_answers.values()))
sorted_answers = list(reversed(sorted(answers, key=len)))
longest_length = len(sorted_answers[0])

grid = np.zeros((longest_length, longest_length), dtype=str)

# lists to track the start positions of already placed words
# this ensures that only one word can be placed in one spot going
# across and only one word can be placed in that spot going down
across_placed = []
down_placed = []


# Helper functions
def get_insert_spots(grid, word, insert_start_pos, left_to_right):
    x, y = insert_start_pos
    if left_to_right:
        return grid[y][x: x + len(word)]
    else:
        return grid[:, x][y: y + len(word)]


def word_goes_off_grid(grid, word, insert_start_pos, left_to_right):
    x, y = insert_start_pos
    if left_to_right:
        return x + len(word) > grid.shape[1]
    else:
        return y + len(word) > grid.shape[4]


@np.vectorize
def word_can_be_placed_at_pos(grid, word, insert_start_pos, left_to_right):
    # Ensure that no other word has been placed at INSERT_START_POS with the same
    # orientation. (e.g no two words go accross at (2,3))
    if left_to_right and insert_start_pos in across_placed:
        return False
    if not left_to_right and insert_start_pos in down_placed:
        return False
    # Ensure the word does not go off the grid
    if word_goes_off_grid(grid, word, insert_start_pos, left_to_right):
        return False

    x, y = insert_start_pos
    # Get a the set of chars where the word would go
    if left_to_right:
        chars = grid[y][x: x + len(word)]
    else:
        chars = grid[:, x][y: y + len(word)]
    # Compare all the words chars to the chars already on the grid. Only allow inserts
    # if the corresponding spot on the grid is free or if the chars match
    for word_char, grid_char in zip(word, chars):
        if word_char != grid_char and grid_char != "":
            return False
    return True


def place_word_at_pos(grid, word, insert_start_pos, left_to_right):
    # Check that the placement is allowed
    if not word_can_be_placed_at_pos(grid, word, insert_start_pos, left_to_right):
        return False
    else:
        # Place the word at the correct place character by character
        x, y = insert_start_pos
        if left_to_right:
            for i, char in enumerate(word):
                grid[y][x + i] = char
                # Record that the word has been placed
                across_placed.append(insert_start_pos)
        else:
            for j, char in enumerate(word):
                grid[y + j][x] = char
                down_placed.append(insert_start_pos)


def extend_grid(grid, horizontal):
    if horizontal:
        grid = np.hstack(grid, np.zeros((grid.shape[0], 1), dtype=str))
    else:
        grid = np.vstack(grid, np.zeros((1, grid.shape[1]), dtype=str))


def get_valid_word_placements(grid, word):
    return


def get_intersection_placements(grid, word):
    for char in word:
        intersections = zip(np.where(grid == char)[0], np.where(grid == char)[1])


def generate(grid, answers):
    np.random.shuffle(answers)
    while len(answers) > 0:
        # Get a random word
        for word in answers:
            chars = list(word)
            np.random.shuffle(chars)
            # Place the word randomly at an intersection
            for char in chars:


def main():
    pass


if __name__ == "__main__":
    main()
