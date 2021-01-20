#Кря
def on_border(n_rows, n_cols, point):
    """
    Parameters:
    :n_rows (int): x-shape
    :n_cols (int): y-shape
    :point (tuple): point with x and y for check
    :return: bool value that tells whether a point is on the border
    """
    if point[0] == 0 or point[1] == n_cols - 1 or point[1] == 0 or point[0] == n_rows - 1: #Проверяем всевозможные
        # print("find way")
        return True
    else:
        return False


def possible_neighbours(point):
    """
    Parameters:
    :point (tuple): point with x and y for possible neighbours
    :return: list of nearby neighbors for point
    """
    neighbours = []
    my_neighbour = (point[0], point[1] + 1)  # Клетка снизу
    neighbours.append(my_neighbour)
    my_neighbour = (point[0] + 1, point[1])  # Справа
    neighbours.append(my_neighbour)
    my_neighbour = (point[0], point[1] - 1)  # Сверху
    neighbours.append(my_neighbour)

    my_neighbour = (point[0] - 1, point[1])  # Слева
    neighbours.append(my_neighbour)

    return neighbours

# Рабочая функция для удобного вывода матрицы
# def print_list(my_list):
#     for elem in my_list:
#         print(elem)


def count_steps(n_cols, n_row, min_step, step_map):
    # Посколько выходов может быть несколько, алгоритм изменен
    """
   Parameters:
    :n_rows (int): x-shape
    :n_cols (int): y-shape
    :min_step(int): n_rows*n_cols as max way
    :prev_step_map(dict): the dictionary with previous step map
   :return: count steps
   """
    # Проходим по краям карты шагов, чтобы найти выходы с наименьшим количеством шагов
    for i in range(0, n_cols):  # Справа и слева
        if step_map[i][0] < min_step and step_map[i][0] != -1:
            min_step = step_map[i][0]
        if step_map[i][n_row - 1] < min_step and step_map[i][n_row - 1] != -1:
            min_step = step_map[i][n_row - 1]
    for i in range(0, n_row):  # Сверху и сверху
        if step_map[0][i] < min_step and step_map[0][i] != -1:
            min_step = step_map[0][i]
        if step_map[n_cols - 1][i] < min_step and step_map[n_cols - 1][i] != -1:
            min_step = step_map[n_cols - 1][i]
    return min_step + 1  # +1 так как сам выход из лабиринта тоже считается шагом


def my_step(n_row, n_cols, point, step_map, step, find_way, maze):
    # print(point)
    if not on_border(n_row, n_cols, point):  # Распространение волны
        my_neighbours = possible_neighbours(tuple(point))  # Смотрим всех возможных соседей
        for neighbour in my_neighbours:
            if step_map[neighbour[1]][neighbour[0]] > step or step_map[neighbour[1]][neighbour[0]] == -1 and \
                    maze[neighbour[1]][neighbour[0]] != 0:  # Смотрим что на соседе большее количество шагов, либо по
                # нему не ходили, и что на него можно наступить
                step_map[neighbour[1]][neighbour[0]] = step
                find_way = my_step(n_row, n_cols, neighbour, step_map, step + 1, find_way, maze)
    else:

        find_way = True
        # print(find_way)
    return find_way


def count_steps_to_exit(maze, start):
    """
    Parameters:
   :maze (list([])): the matrix with 0 and 1
   :start (tuple): start point with x and y
   :return: count steps
   """
    n_row = len(maze[0])  # Измеряем полученную матрицу
    n_cols = len(maze)

    step_map = [[-1 for j in range(n_row)] for i in range(n_cols)]  # Создаем массив для записи пути
    step = 0  # Cчитаем наш шаг
    my_point = list(start)
    step_map[my_point[1]][my_point[0]] = 0  # Начальная точка в матрице пути
    find_way = False
    find_way = my_step(n_row, n_cols, my_point, step_map, step + 1, find_way, maze)
    if not find_way:
        # print(0)
        return 0
    else:
        min_step = n_cols * n_row

        # print(min_step + 1)
        return count_steps(n_cols, n_row, min_step, step_map)

    # print_list(step_map)


maz = [[0, 0, 0, 0, 0],
       [0, 1, 1, 1, 0],
       [0, 1, 0, 1, 0],
       [0, 1, 1, 1, 0],
       [0, 0, 0, 1, 0]]
starts = (1, 1)
count_steps_to_exit(maz, starts)
