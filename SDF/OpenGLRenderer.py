from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def make_buffer(target, buffer_data, buffer_size):
    buff = glGenBuffers(1)
    glBindBuffer(target, buff)
    glBufferData(target, buffer_size, buffer_data, GL_STATIC_DRAW)
    return buff


g_vertex = [[-1, -1],
            [1, -1],
            [-1, 1],
            [1, 1]]
g_element = [0, 1, 2, 3]

vertex_buffer = make_buffer(GL_ARRAY_BUFFER, g_vertex, sizeof(g_vertex))
element_buffer = make_buffer(GL_ELEMENT_ARRAY_BUFFER, g_element, sizeof(g_element))


def update_fade_factor():
    pass


def render():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(400, 300)
    glutCreateWindow("Hello World")
    glutIdleFunc(update_fade_factor)
    glutDisplayFunc(render)

    glutMainLoop()
