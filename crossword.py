import numpy as np
from user_input import hints_and_answers

# DEBUG ONLY
np.random.seed(0)


def clean_answers(answer):
    """Function that sanitizes answer input so that it can be displayed in
    a crossword-grid. Removes spaces and makes all characters upper-case."""
    return answer.replace(" ", "").upper()


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
def word_can_be_placed_at_pos(grid, word, insert_start_pos,
                              left_to_right, across_placed, down_placed):
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


def place_word_at_pos(grid, word, insert_start_pos,
                      left_to_right, across_placed, down_placed):
    # Check that the placement is allowed
    if not word_can_be_placed_at_pos(
            grid, word, insert_start_pos, left_to_right, across_placed, down_placed):
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


def get_grid_copy_with_word_at_pos(
        grid, word, insert_start_pos, left_to_right, across_placed, down_placed):
    # Create a grid copy
    grid_copy = np.copy(grid)
    # Place the word if possible and return the copy. If no placement is
    # possible return False
    if place_word_at_pos(grid_copy, word, insert_start_pos,
                         left_to_right, across_placed, down_placed):
        return grid_copy
    return False


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


def generate(grid, answers, across_placed=[], down_placed=[]):
    """Either modifies the existing grid by placing the answers into
    it in a crossword style or returns False if no crossword is possible"""
    # np.random.shuffle(answers)
    # while len(answers) > 0:
    # Get a random word
    for word in answers:
        # np.random.shuffle(chars) TODO: ensure some randomness in choosingn the
        # intersection
        for i, char in enumerate(word):
            occurences = np.where(grid == char)
            intersections = zip(occurences[0], occurences[1])
            for intersection in intersections:
                # Randomly choose to place the word either across or down
                left_to_right_choice = [True, False]
                np.random.shuffle(left_to_right_choice)

                for left_to_right in left_to_right_choice:
                    # Calculate the start positions for word placements
                    x, y = intersection
                    insert_start_pos = (x - i, y) if left_to_right else (x, y + i)

                    new_grid = get_grid_copy_with_word_at_pos(
                        grid, word, insert_start_pos, left_to_right, across_placed, down_placed)

                    if new_grid:
                        # If the word was able to be placed recursively call the
                        # generate function with the new grid (with the word placed)
                        # and a new answer list (with the word removed)
                        new_answers = answers.copy()
                        new_answers.remove(word)
                        if generate(new_grid, new_answers):
                            return new_grid
    return False


def main():
    answers = map(clean_answers, hints_and_answers.values())
    longest_answer_length = max(answers, key=len)
    sorted_answers = sorted(answers, key=len)

    grid = np.zeros((longest_answer_length, longest_answer_length), dtype=str)

    # Lists that store if words have been placed either across or down. This
    # is in order to prevent multiple words being placed at the same starting
    # position.
    across_placed, down_placed = [], []
    # place longest word across in center - TODO: change this in future
    first_word = sorted_answers.pop(0)
    place_word_at_pos(
        grid,
        word=first_word,
        insert_start_pos=(grid.shape[0] // 2, 0),
        left_to_right=True,
        across_placed=across_placed,
        down_placed=down_placed)

    print(grid)


if __name__ == "__main__":
    main()
