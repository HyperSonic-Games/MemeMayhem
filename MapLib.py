import glfw
import numpy as np
import OpenGL.GL as gl
from PIL import Image
import Utils
import re

class MapLoader:
    def __init__(self, PathToMapFile: str):
        with open(PathToMapFile, 'r') as f:
            self.MapData = f.read().strip().split('\n')

        self.GridSize = self.GetGridSize()
        self.ImageSize = (16, 16)
        self.NumImages = self.GridSize[0] * self.GridSize[1]

        # Initialize GLFW without creating a visible window
        if not glfw.init():
            Utils.PopupManager().Error("Error: MapLib", "GLFW cannot be initialized!")
        
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(640, 480, "Hidden Window", None, None)
        if not self.window:
            glfw.terminate()
            Utils.PopupManager().Error("Error: MapLib", "GLFW Failed To Create A Window For The Shader")
        
        glfw.make_context_current(self.window)

        # Read the compute shader from a separate file
        self.ComputeShaderSource = self.ReadComputeShader("MapStitcher.comp")

        # Compile and link the compute shader
        self.Program = self.CompileComputeShader()

        # Create textures
        self.InputTexture = self.CreateInputTexture()
        self.OutputTexture = self.CreateOutputTexture()

    def ReadComputeShader(self, FilePath):
        with open(FilePath, 'r') as f:
            return f.read()

    def CompileComputeShader(self):
        # Compile the compute shader
        ComputeShader = gl.glCreateShader(gl.GL_COMPUTE_SHADER)
        gl.glShaderSource(ComputeShader, self.ComputeShaderSource)
        gl.glCompileShader(ComputeShader)

        # Check for compilation errors
        if not gl.glGetShaderiv(ComputeShader, gl.GL_COMPILE_STATUS):
            ErrorLog = gl.glGetShaderInfoLog(ComputeShader)
            raise RuntimeError(f"Shader compilation failed:\n{ErrorLog}")

        # Create and link the shader program
        Program = gl.glCreateProgram()
        gl.glAttachShader(Program, ComputeShader)
        gl.glLinkProgram(Program)

        # Check for linking errors
        if not gl.glGetProgramiv(Program, gl.GL_LINK_STATUS):
            ErrorLog = gl.glGetProgramInfoLog(Program)
            raise RuntimeError(f"Shader linking failed:\n{ErrorLog}")

        gl.glDeleteShader(ComputeShader)
        return Program

    def CreateInputTexture(self):
        # Create input texture array
        InputTexture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, InputTexture)
        gl.glTexStorage3D(gl.GL_TEXTURE_2D_ARRAY, 1, gl.GL_RGBA8, self.ImageSize[0], self.ImageSize[1], self.NumImages)

        # Fill the input texture array with dummy data
        Data = np.zeros((self.NumImages, self.ImageSize[1], self.ImageSize[0], 4), dtype=np.uint8)
        for i in range(self.NumImages):
            Data[i, :, :, :] = [0, 255, 0, 255]  # Green color for "Grass"
        gl.glTexSubImage3D(gl.GL_TEXTURE_2D_ARRAY, 0, 0, 0, 0, self.ImageSize[0], self.ImageSize[1], self.NumImages, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, Data)

        return InputTexture

    def CreateOutputTexture(self):
        # Create output texture
        OutputTexture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, OutputTexture)
        OutputSize = (self.ImageSize[0] * self.GridSize[0], self.ImageSize[1] * self.GridSize[1])
        gl.glTexStorage2D(gl.GL_TEXTURE_2D, 1, gl.GL_RGBA8, OutputSize[0], OutputSize[1])

        return OutputTexture

    def GetGridSize(self):
        return len(self.MapData), len(self.MapData[0].split(', '))

    def ParseMapSections(self):
        section_start_regex = re.compile(r'%(\w+)%')
        section_end_regex = re.compile(r'%END(\w+)%')

        sections = {
            'MAPLAYOUT': None,
            'MAPCOLIDERS': None,
            'MAPTRIGGERS': None
        }

        current_section = None

        for line in self.MapData:
            line = line.strip()

            section_start_match = section_start_regex.match(line)
            if section_start_match:
                current_section = section_start_match.group(1)
                sections[current_section] = []
                continue

            section_end_match = section_end_regex.match(line)
            if section_end_match:
                current_section = None
                continue

            if current_section and line:
                sections[current_section].append(line.split(','))

        return sections

    def RunComputeShader(self):
        gl.glUseProgram(self.Program)

        # Bind textures to image units
        gl.glBindImageTexture(0, self.InputTexture, 0, gl.GL_TRUE, 0, gl.GL_READ_ONLY, gl.GL_RGBA8)
        gl.glBindImageTexture(1, self.OutputTexture, 0, gl.GL_FALSE, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA8)

        # Set the uniform variables
        ImageSizeLoc = gl.glGetUniformLocation(self.Program, "imageSize")
        GridSizeLoc = gl.glGetUniformLocation(self.Program, "gridSize")
        gl.glUniform2i(ImageSizeLoc, *self.ImageSize)
        gl.glUniform2i(GridSizeLoc, *self.GridSize)

        # Dispatch the compute shader
        gl.glDispatchCompute(self.GridSize[0], self.GridSize[1], 1)

        # Ensure all work is done before proceeding
        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

    def GetOutputImage(self):
        # Read back the output texture data
        OutputSize = (self.ImageSize[0] * self.GridSize[0], self.ImageSize[1] * self.GridSize[1])
        OutputData = np.zeros((OutputSize[1], OutputSize[0], 4), dtype=np.uint8)
        gl.glGetTexImage(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, OutputData)

        # Save the output data as an image (requires Pillow library)
        ImageResult = Image.fromarray(OutputData, 'RGBA')
        return ImageResult

    def Cleanup(self):
        gl.glDeleteProgram(self.Program)
        gl.glDeleteTextures(1, [self.InputTexture])
        gl.glDeleteTextures(1, [self.OutputTexture])
        glfw.terminate()

# Example usage:
map_loader = MapLoader('path_to_your_map_file.txt')
parsed_map = map_loader.ParseMapSections()

