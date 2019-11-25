import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

'''
Импортировать метод ShowModel - Принимает 4 аргумента: 
            1 - массив с координатама (x, y, z) вокселей
            2 - размер вокселя
            3 - крайние координаты объекта в виде (Желательно в классе "Tuple", для отлова непредвиденных изменений) 
                                                                            ->  ((Xmin, Ymin, Zmin), (Xmax, Ymax, Zmax))
            4 - debug_mod (True/False)
____________________________________________________________
Приоритеты в планах:
    - Добавить цвет
    - Переработать debug_mode
    - Доделать полноценное перемещение (На данный момент: вращение только по одной оси и зум)
'''


def _GetModel(voxel_size: float, voxels_coords: [], debug_mode: bool):
    model = (
        [],  # Вершины
        (  # Поверхности для debug_mode
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (8, 9, 10, 11),
            (12, 13, 14, 15),
            (16, 17, 18, 19),
            (20, 21, 22, 23)
        ),
        (  # Ребра для debug_mode
            (10, 30, 26, 9),  # Верх
            (26, 25, 8, 9),
            (25, 29, 11, 8),
            (29, 30, 10, 11),
            (31, 27, 13, 14),  # Низ
            (27, 13, 12, 24),
            (24, 12, 15, 28),
            (14, 15, 28, 31),
            (31, 30, 6, 7),  # Перед
            (30, 29, 5, 6),
            (29, 28, 4, 5),
            (7, 4, 28, 31),
            (27, 26, 2, 3),  # Зад
            (26, 25, 1, 2),
            (1, 0, 24, 25),
            (3, 0, 24, 27),
            (27, 26, 16, 17),  # Лево
            (26, 30, 19, 16),
            (19, 30, 31, 18),
            (17, 18, 31, 27),
            (28, 29, 22, 23),  # Право
            (29, 25, 21, 22),
            (25, 21, 20, 24),
            (24, 28, 23, 20)
        ),
        (  # Поверхности для нормального вокселя
            (0, 1, 2, 3),
            (3, 2, 6, 7),
            (7, 6, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 6, 2),
            (4, 0, 3, 7)
        )
    )

    for voxel_coords in voxels_coords:
        if debug_mode:
            model[0].append(_GetDebugVoxel(voxel_size, voxel_coords))
        else:
            model[0].append(_GetVoxel(voxel_size, voxel_coords))

    return model


def _GetVoxel(voxel_size: float, voxel_coord: []):
    x = voxel_coord[0] / voxel_size / 5
    y = voxel_coord[1] / voxel_size / 5
    z = voxel_coord[2] / voxel_size / 5
    half_side = 0.2 / 2

    return (
        (x + half_side, y - half_side, z - half_side),  # правый низ зад
        (x + half_side, y + half_side, z - half_side),  # правый верх зад
        (x - half_side, y + half_side, z - half_side),  # левый верх зад
        (x - half_side, y - half_side, z - half_side),  # левый низ зад
        (x + half_side, y - half_side, z + half_side),  # правый низ перед
        (x + half_side, y + half_side, z + half_side),  # правый верх перед
        (x - half_side, y + half_side, z + half_side),  # левый верх перед
        (x - half_side, y - half_side, z + half_side)  # левый низ перед
    )


def _GetDebugVoxel(voxel_size: float, voxel_coord: []):
    x = voxel_coord[0] / voxel_size / 5
    y = voxel_coord[1] / voxel_size / 5
    z = voxel_coord[2] / voxel_size / 5
    border = 0.01  # Ширина ребра
    half_side = 0.2 / 2

    return (
        # --Внутренние--
        # зад (0 - 3)
        (x + half_side - border, y - half_side + border, z - half_side),  # правый низ зад
        (x + half_side - border, y + half_side - border, z - half_side),  # правый верх зад
        (x - half_side + border, y + half_side - border, z - half_side),  # левый верх зад
        (x - half_side + border, y - half_side + border, z - half_side),  # левый низ зад

        # Перед (4 - 7)
        (x + half_side - border, y - half_side + border, z + half_side),  # правый низ перед
        (x + half_side - border, y + half_side - border, z + half_side),  # правый верх перед
        (x - half_side + border, y + half_side - border, z + half_side),  # левый верх перед
        (x - half_side + border, y - half_side + border, z + half_side),  # левый низ перед

        # Верх (8 - 11)
        (x + half_side - border, y + half_side, z - half_side + border),  # правый верх зад
        (x - half_side + border, y + half_side, z - half_side + border),  # левый верх зад
        (x - half_side + border, y + half_side, z + half_side - border),  # левый верх перед
        (x + half_side - border, y + half_side, z + half_side - border),  # правый верх перед

        # Низ (12 - 15)
        (x + half_side - border, y - half_side, z - half_side + border),  # правый низ зад
        (x - half_side + border, y - half_side, z - half_side + border),  # левый низ зад
        (x - half_side + border, y - half_side, z + half_side - border),  # левый низ перед
        (x + half_side - border, y - half_side, z + half_side - border),  # правый низ перед

        # Лево (16 - 19)
        (x - half_side, y + half_side - border, z - half_side + border),  # левый верх зад
        (x - half_side, y - half_side + border, z - half_side + border),  # левый низ зад
        (x - half_side, y - half_side + border, z + half_side - border),  # левый низ перед
        (x - half_side, y + half_side - border, z + half_side - border),  # левый верх перед

        # Право (20 - 23)
        (x + half_side, y - half_side + border, z - half_side + border),  # правый низ зад
        (x + half_side, y + half_side - border, z - half_side + border),  # правый верх зад
        (x + half_side, y + half_side - border, z + half_side - border),  # правый верх перед
        (x + half_side, y - half_side + border, z + half_side - border),  # правый низ перед

        # ------------------------------------------------------------------------------------

        # --Внешние-- (24 - 31)
        (x + half_side, y - half_side, z - half_side),  # правый низ зад
        (x + half_side, y + half_side, z - half_side),  # правый верх зад
        (x - half_side, y + half_side, z - half_side),  # левый верх зад
        (x - half_side, y - half_side, z - half_side),  # левый низ зад
        (x + half_side, y - half_side, z + half_side),  # правый низ перед
        (x + half_side, y + half_side, z + half_side),  # правый верх перед
        (x - half_side, y + half_side, z + half_side),  # левый верх перед
        (x - half_side, y - half_side, z + half_side),  # левый низ перед
    )


def _Model(model: [], debug_mode: bool):

    if debug_mode:
        # Отрисовка маленьких граней
        for verticies in model[0]:
            glBegin(GL_QUADS)
            glColor3ub(27, 171, 104)  # Выбор цвета
            for surface in model[1]:
                for vertex in surface:
                    glVertex3fv(verticies[vertex])
            glEnd()

        # Отрисовка ребер
        for verticies in model[0]:
            glBegin(GL_QUADS)
            glColor3ub(0, 0, 0)  # Выбор цвета
            for surface in model[2]:
                for vertex in surface:
                    glVertex3fv(verticies[vertex])
            glEnd()
    else:
        # Отрисовка больших граней
        for verticies in model[0]:
            glBegin(GL_QUADS)
            glColor3ub(27, 171, 104)  # Выбор цвета
            for surface in model[3]:
                for vertex in surface:
                    glVertex3fv(verticies[vertex])
            glEnd()


def _ModelCentering(voxels_coords: [], extreme_coordinates: (), voxel_size: float):
    """
    :param extreme_coordinates:  в виде  ->  ((Xmin, Ymin, Zmin), (Xmax, Ymax, Zmax))
    :return: ()
    """
    dif_x = extreme_coordinates[1][0] - extreme_coordinates[0][0] + voxel_size
    dif_y = extreme_coordinates[1][1] - extreme_coordinates[0][1] + voxel_size
    dif_z = extreme_coordinates[1][2] - extreme_coordinates[0][2] + voxel_size

    for voxel_coords in voxels_coords:
        voxel_coords[0] = voxel_coords[0] - extreme_coordinates[0][0] + voxel_size / 2 - (dif_x / 2)
        voxel_coords[1] = voxel_coords[1] - extreme_coordinates[0][1] + voxel_size / 2 - (dif_y / 2)
        voxel_coords[2] = voxel_coords[2] - extreme_coordinates[0][2] + voxel_size / 2 - (dif_z / 2)

    max_half = max(dif_x, dif_y, dif_z) / 2 / voxel_size
    return (max_half * 1.3, max_half * 10)


def ShowModel(voxels_coords: [], voxel_size: float, extreme_coordinates: (), debug_mode: bool):

    perspective = _ModelCentering(voxels_coords, extreme_coordinates, voxel_size)

    model = _GetModel(voxel_size, voxels_coords, debug_mode)

    pygame.init()
    display = (800, 600)  # Размер окна
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Result")  # Название окна

    glEnable(GL_DEPTH_TEST)  # Необходимо для корректного отображения без просветов
    if debug_mode:
        glClearColor(100 / 255, 100 / 255, 100 / 255, 1)  # Выбор цвета фона
    else:
        glClearColor(70 / 255, 70 / 255, 70 / 255, 1)  # Выбор цвета фона

    gluPerspective(45, (display[0] / display[1]), 0.1, perspective[1])
    glTranslatef(0, 0, -perspective[0])
    glRotatef(0, 0, 0, 0)

    x_move = 0
    y_move = 0
    z_move = 0

    x_rotate = 0
    y_rotate = 0
    z_rotate = 0
    step = 0

    # radians_axis_z = 0
    radians_axis_y = 0
    radians_axis_x = 0

    degrees_axis_y = 0  # Вращение право/лево
    degrees_axis_x = 0  # Вращение верх/низ
    # degrees_axis_z = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_rotate = -0.1
                    step = 1
                if event.key == pygame.K_RIGHT:
                    x_rotate = 0.1
                    step = 1

                # ВРЕМЕННО НЕ РАБОТАЕТ
                # if event.key == pygame.K_DOWN:
                #     y_rotate = 0.1
                #     step = 1
                # if event.key == pygame.K_UP:
                #     y_rotate = -0.1
                #     step = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_rotate = 0
                    step = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_rotate = 0
                    step = 0

            # Вращение вправо/влево
            z_move = -math.cos(radians_axis_y) * 0.1
            x_move = math.sin(radians_axis_y) * 0.1

            # Вращение вверх/вниз
            # z_move = math.cos(radians_axis_x) * -0.1
            # y_move = math.sin(radians_axis_x) * -0.1

            # Приближение/отдаление
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(x_move, y_move, z_move)
                if event.button == 5:
                    glTranslatef(-x_move, -y_move, -z_move)

        # Изменение оси Y (Вращение влево/вправо)
        degrees_axis_y += x_rotate * step * 10
        radians_axis_y += x_rotate * step * 10 / 180 * math.pi

        # Изменение оси X (Вращение вверх/вниз)
        degrees_axis_x += y_rotate * step * 10
        radians_axis_x += y_rotate * step * 10 / 180 * math.pi

        glRotatef(step, y_rotate, x_rotate, z_rotate)  # Изменение ориентации

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        _Model(model, debug_mode)
        pygame.display.flip()
        pygame.time.wait(10)