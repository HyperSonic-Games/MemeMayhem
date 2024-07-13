import glfw
import numpy as np
import OpenGL.GL as gl
from PIL import Image
import Utils
import re

class MapLoader:
    # Color mappings for colliders
    COLOR_NONE = [0.0, 0.0, 0.0, 0.0]
    COLOR_PLAYER = [1.0, 0.0, 0.0, 1.0]
    COLOR_BULLET = [0.0, 1.0, 0.0, 1.0]
    COLOR_PLAYER_AND_BULLET = [0.0, 0.0, 1.0, 1.0]

    # Color mappings for triggers
    TRIGGER_COLOR_NONE = [0.0, 0.0, 0.0, 0.0]
    TRIGGER_COLOR_PLAYER_SPAWN = [1.0, 1.0, 0.0, 1.0]
    TRIGGER_COLOR_HP_LARGE_SPAWN = [1.0, 0.0, 1.0, 1.0]
    TRIGGER_COLOR_AMMO_LARGE_SPAWN = [0.0, 1.0, 1.0, 1.0]
    TRIGGER_COLOR_AMMO_SMALL_SPAWN = [1.0, 0.5, 0.0, 1.0]
    TRIGGER_COLOR_HP_SMALL_SPAWN = [0.5, 0.0, 1.0, 1.0]

    def __init__(self):
        self.image_size = (16, 16)
        self.grid_size = None
        self.num_images = None
        self.textures = {}
        self.colliders = []
        self.triggers = []

    def LoadMap(self, path_to_map_file):
        with open(path_to_map_file, 'r') as f:
            lines = f.read().strip().split('\n')

        self.textures, self.colliders, self.triggers = self._ParseMapFile(lines)
        self.grid_size = (len(self.colliders), len(self.colliders[0]))
        self.num_images = self.grid_size[0] * self.grid_size[1]

    def _ParseMapFile(self, lines):
        textures = []
        colliders = []
        triggers = []

        current_section = None
        for line in lines:
            line = line.strip()
            if line == '[Textures]':
                current_section = 'textures'
                continue
            elif line == '[Colliders]':
                current_section = 'colliders'
                continue
            elif line == '[Triggers]':
                current_section = 'triggers'
                continue

            if current_section == 'textures':
                textures.append(line)
            elif current_section == 'colliders':
                colliders.append(list(map(int, line.split(', '))))
            elif current_section == 'triggers':
                triggers.append(list(map(int, line.split(', '))))

        return textures, colliders, triggers

    def _RunShader(self, shader_path, input_data, color_mappings):
        # Initialize GLFW without creating a visible window
        if not glfw.init():
            Utils.PopupManager().Error("Error: MapLib", "GLFW cannot be initialized!")
            return

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(640, 480, "Hidden Window", None, None)
        if not window:
            glfw.terminate()
            Utils.PopupManager().Error("Error: MapLib", "GLFW Failed To Create A Window For The Shader")
            return

        glfw.make_context_current(window)

        # Read the compute shader from a separate file
        with open(shader_path, 'r') as f:
            shader_source = f.read()

        # Compile the compute shader
        compute_shader = gl.glCreateShader(gl.GL_COMPUTE_SHADER)
        gl.glShaderSource(compute_shader, shader_source)
        gl.glCompileShader(compute_shader)

        # Check for compilation errors
        if not gl.glGetShaderiv(compute_shader, gl.GL_COMPILE_STATUS):
            error_log = gl.glGetShaderInfoLog(compute_shader)
            raise RuntimeError(f"Shader compilation failed:\n{error_log}")

        # Create and link the shader program
        program = gl.glCreateProgram()
        gl.glAttachShader(program, compute_shader)
        gl.glLinkProgram(program)

        # Check for linking errors
        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            error_log = gl.glGetProgramInfoLog(program)
            raise RuntimeError(f"Shader linking failed:\n{error_log}")

        gl.glDeleteShader(compute_shader)

        # Create input texture array
        input_texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, input_texture)
        gl.glTexStorage3D(gl.GL_TEXTURE_2D_ARRAY, 1, gl.GL_RGBA8, self.image_size[0], self.image_size[1], self.num_images)
        
        # Fill the input texture array with input data
        data = np.zeros((self.num_images, self.image_size[1], self.image_size[0], 4), dtype=np.uint8)
        for i in range(self.num_images):
            data[i, :, :, :] = input_data[i]  # Input data

        gl.glTexSubImage3D(gl.GL_TEXTURE_2D_ARRAY, 0, 0, 0, 0, self.image_size[0], self.image_size[1], self.num_images, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)

        # Create output texture
        output_texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, output_texture)
        output_size = (self.image_size[0] * self.grid_size[0], self.image_size[1] * self.grid_size[1])
        gl.glTexStorage2D(gl.GL_TEXTURE_2D, 1, gl.GL_RGBA8, output_size[0], output_size[1])

        # Bind textures to image units
        gl.glBindImageTexture(0, input_texture, 0, gl.GL_TRUE, 0, gl.GL_READ_ONLY, gl.GL_RGBA8)
        gl.glBindImageTexture(1, output_texture, 0, gl.GL_FALSE, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA8)

        # Use the shader program
        gl.glUseProgram(program)

        # Set uniform variables for the shader
        gl.glUniform2i(gl.glGetUniformLocation(program, "imageSize"), *self.image_size)
        gl.glUniform2i(gl.glGetUniformLocation(program, "gridSize"), *self.grid_size)
        for name, color in color_mappings.items():
            loc = gl.glGetUniformLocation(program, name)
            gl.glUniform4f(loc, *color)

        # Dispatch the compute shader
        gl.glDispatchCompute(self.grid_size[0], self.grid_size[1], 1)
        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        # Retrieve the output data
        output_data = np.zeros((output_size[1], output_size[0], 4), dtype=np.uint8)
        gl.glGetTexImage(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, output_data)

        # Convert the output data to an image
        output_image = Image.fromarray(output_data, 'RGBA')

        # Clean up
        gl.glDeleteProgram(program)
        gl.glDeleteTextures([input_texture, output_texture])
        glfw.terminate()

        return output_image

    def GetMapTexture(self):
        texture_images = [Image.open(f"Assets/Images/Map/{texture}.png").convert("RGBA") for texture in self.textures]
        return self._run_shader("Assets/Shaders/TextureStitcher.comp", texture_images, {})

    def GetMapColider(self):
        colliders_array = np.array(self.colliders).astype(np.uint8).reshape(-1, 1, 1, 1)
        color_mappings = {
            "colorNone": self.COLOR_NONE,
            "colorPlayer": self.COLOR_PLAYER,
            "colorBullet": self.COLOR_BULLET,
            "colorPlayerAndBullet": self.COLOR_PLAYER_AND_BULLET,
        }
        return self._run_shader("Assets/Shaders/ColliderStitcher.comp", colliders_array, color_mappings)

    def GetMapTrigger(self):
        triggers_array = np.array(self.triggers).astype(np.uint8).reshape(-1, 1, 1, 1)
        color_mappings = {
            "colorNone": self.TRIGGER_COLOR_NONE,
            "colorPlayerSpawn": self.TRIGGER_COLOR_PLAYER_SPAWN,
            "colorHpLargeSpawn": self.TRIGGER_COLOR_HP_LARGE_SPAWN,
            "colorAmmoLargeSpawn": self.TRIGGER_COLOR_AMMO_LARGE_SPAWN,
            "colorAmmoSmallSpawn": self.TRIGGER_COLOR_AMMO_SMALL_SPAWN,
            "colorHpSmallSpawn": self.TRIGGER_COLOR_HP_SMALL_SPAWN,
        }
        return self._run_shader("Assets/Shaders/TriggerStitcher.comp", triggers_array, color_mappings)
