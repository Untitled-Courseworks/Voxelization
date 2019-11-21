import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

'''
Импортировать метод ShowModel - Принимает 3 аргумента: 
            1 - массив с координатама (x, y, z) вокселей
            2 - размер вокселя
            3 - debug_mod (True/False)
____________________________________________________________
Приоритеты в планах:
    - Добавить цвет
    - Переработать debug_mode
    - Доделать полноценное перемещение
'''


def _GetModel(voxel_size: float, voxels_coords: []):
    model = (
        [],  # Вершины
        (  # Грани
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)
        ),
        (  # Поверхности
            (0, 1, 2, 3),
            (3, 2, 7, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (4, 0, 3, 6)
        )
    )

    for voxel_coords in voxels_coords:
        model[0].append(_GetVoxel(voxel_size, voxel_coords))

    return model


def _GetVoxel(voxel_size: float, voxel: []):
    x = voxel[0] / voxel_size / 5
    y = voxel[1] / voxel_size / 5
    z = voxel[2] / voxel_size / 5

    return (
        (x + 0.1, y - 0.1, z - 0.1),  # правый низ зад
        (x + 0.1, y + 0.1, z - 0.1),  # правый верх зад
        (x - 0.1, y + 0.1, z - 0.1),  # левый верх зад
        (x - 0.1, y - 0.1, z - 0.1),  # левый низ зад
        (x + 0.1, y - 0.1, z + 0.1),  # правый низ перед
        (x + 0.1, y + 0.1, z + 0.1),  # правый верх перед
        (x - 0.1, y - 0.1, z + 0.1),  # левый низ перед
        (x - 0.1, y + 0.1, z + 0.1)  # левый верх перед
    )


def _Model(model: [], debug_mode: bool):
    for verticies in model[0]:
        glBegin(GL_QUADS)
        glColor3f(1, 0, 0)
        for surface in model[2]:
            for vertex in surface:
                glVertex3fv(verticies[vertex])
        glEnd()

        if debug_mode:
            glBegin(GL_LINES)  # Отображение границ
            for edge in model[1]:
                for vertex in edge:
                    glColor3f(1, 1, 0)
                    glVertex3fv(verticies[vertex])
            glEnd()


def ShowModel(voxels_coords: [], voxel_size: float, debug_mode: bool):

    model = _GetModel(voxel_size, voxels_coords)

    pygame.init()
    display = (800, 600)  # Размер окна
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    pygame.display.set_caption("Result")  # Название окна

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0, 0, -2)

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
