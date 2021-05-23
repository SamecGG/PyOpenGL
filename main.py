from sys import flags
import pygame
import numpy as np
import pyrr
import os, math
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from pyrr.vector import normalize

from engine import Camera, Cube_Renderer, Player, Vector3
from Extensions import loaders
from Extensions import geometry

#region Pygam Init
pygame.init()
WIN_SIZE = WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode(WIN_SIZE, RESIZABLE|DOUBLEBUF|OPENGL)
WIN_active = False
#endregion

#region Shader Init
shader_vertex, shader_fragment = loaders.ShaderLoader.load(os.path.abspath("Assets/Shaders/basic.shader"))
shader = compileProgram(compileShader(shader_vertex, GL_VERTEX_SHADER), compileShader(shader_fragment, GL_FRAGMENT_SHADER))
#endregion

#region Geometry Creation
cube_model = geometry.Cube() 
cube_instancer = Cube_Renderer(cube_model.cube_map, cube_model.indices)

for x in range(10):
    for y in range(10):
        for z in range(10):
            cube_instancer.instantiate((x, y, z), 1)
#endregion

# Player init
camera = Camera(asp_ratio=WIDTH/HEIGHT)
player = Player(camera)

#region OpenGL settings
glUseProgram(shader)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Uniform location link
loc_model = glGetUniformLocation(shader, "model")
loc_proj = glGetUniformLocation(shader, "projection")
loc_view = glGetUniformLocation(shader, "view")
loc_atlas_rows = glGetUniformLocation(shader, "atlas_rows")
loc_atlas_offset  = glGetUniformLocation(shader, "atlas_offset")

# Load variables to uniform
glUniformMatrix4fv(loc_proj, 1, GL_FALSE, camera.projection)
#endregion

#region Bind actions
key_forward = pygame.K_w
key_backwards = pygame.K_s
key_left = pygame.K_a
key_right = pygame.K_d
key_jump = pygame.K_SPACE
key_shift = pygame.K_LCTRL
#endregion

#region Mouse toggle
def toggle_mouse(condition):
    global WIN_active
    WIN_active = condition
    pygame.mouse.set_visible(0 if condition else 1)

    pygame.event.set_grab(condition)

toggle_mouse(False)
#endregion

# Main loop
while True:
    #region Input Binds
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        if event.type == VIDEORESIZE:
            w, h = event.size
            projection = pyrr.matrix44.create_perspective_projection_matrix(45, w/h, 0.1, 200)
            glUniformMatrix4fv(loc_proj, 1, GL_FALSE, projection)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                toggle_mouse(False)
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not WIN_active:
                toggle_mouse(True)

    #region Key input
    # WSAD
    player_input = pyrr.Vector3([0, 0, 0])
    
    keys = pygame.key.get_pressed()

    if keys[key_forward]:
        player_input.z += 1
    if keys[key_backwards]:
        player_input.z -= 1
    if keys[key_left]:
        player_input.x -= 1
    if keys[key_right]:
        player_input.x += 1

    player_input = Vector3.isZero(player_input, lambda: pyrr.vector.normalize(player_input))

    if keys[key_jump]:
        player_input[1] += 1
    if keys[key_shift]:
        player_input[1] -= 1
    #endregion
    
    #region Mouse input
    mouse_input = (0, 0)
    if WIN_active:
        mouse_input = pygame.mouse.get_rel()
    #endregion

    #region Send inputs
    player.process_input(mouse_input, player_input)
    #endregion

    #endregion

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    cube_instancer.render_all(loc_model, loc_atlas_rows, loc_atlas_offset)

    glUniformMatrix4fv(loc_view, 1, GL_FALSE, camera.view)

    # Pygame rendering
    pygame.display.flip()
    pygame.time.wait(10)
