import glfw
import numpy as np
import OpenGL.GL as gl
from PIL import Image
import Utils
import os

class MapLoader:
    def __init__(self, pathToMapFile):
        with open(pathToMapFile, 'r') as f:
            self.MapData = f.read().strip().split('\n')

        self.GridSize = self.GetGridSize()
        self.ImageSize = (16, 16)
        self.NumImages = self.GridSize[0] * self.GridSize[1]
        self.ImagePaths = self._GetImagePaths()
        self.ImagesData = {name: self._LoadTexture(path) for name, path in self.ImagePaths.items()}
        self.Program = None
        self.InputTexture = None
        self.OutputTexture = None

    def __del__(self):
        self._Cleanup()

    def GetGridSize(self):
        return len(self.MapData), len(self.MapData[0].split(', '))

    def _GetImagePaths(self):
        imageSet = set()
        for row in self.MapData:
            for item in row.split(', '):
                imageSet.add(item)

        return {image: f"Assets/Images/Map/{image}.png" for image in imageSet}

    def _LoadTexture(self, filePath):
        if not os.path.exists(filePath):
            Utils.PopupManager().Error("Error: MapLib", f"Texture file not found: {filePath}")
            return None

        image = Image.open(filePath)
        imageData = np.array(image, dtype=np.uint8)
        return imageData

    def _ReadComputeShader(self, filePath):
        with open(filePath, 'r') as f:
            return f.read()

    def _Cleanup(self):
        if self.Program:
            gl.glDeleteProgram(self.Program)
            self.Program = None
        if self.InputTexture:
            gl.glDeleteTextures(1, [self.InputTexture])
            self.InputTexture = None
        if self.OutputTexture:
            gl.glDeleteTextures(1, [self.OutputTexture])
            self.OutputTexture = None
        glfw.terminate()

    def RunTextureShader(self, shaderPath):
        if not glfw.init():
            Utils.PopupManager().Error("Error: MapLib", "GLFW cannot be initialized!")
        
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(640, 480, "Hidden Window", None, None)
        if not window:
            glfw.terminate()
            Utils.PopupManager().Error("Error: MapLib", "GLFW Failed To Create A Window For The Shader")
        
        glfw.make_context_current(window)

        computeShaderSource = self._ReadComputeShader(shaderPath)

        computeShader = gl.glCreateShader(gl.GL_COMPUTE_SHADER)
        gl.glShaderSource(computeShader, computeShaderSource)
        gl.glCompileShader(computeShader)

        if not gl.glGetShaderiv(computeShader, gl.GL_COMPILE_STATUS):
            errorLog = gl.glGetShaderInfoLog(computeShader)
            raise RuntimeError(f"Shader compilation failed:\n{errorLog}")

        self.Program = gl.glCreateProgram()
        gl.glAttachShader(self.Program, computeShader)
        gl.glLinkProgram(self.Program)

        if not gl.glGetProgramiv(self.Program, gl.GL_LINK_STATUS):
            errorLog = gl.glGetProgramInfoLog(self.Program)
            raise RuntimeError(f"Shader linking failed:\n{errorLog}")

        gl.glDeleteShader(computeShader)

        self.InputTexture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.InputTexture)
        gl.glTexStorage3D(gl.GL_TEXTURE_2D_ARRAY, 1, gl.GL_RGBA8, self.ImageSize[0], self.ImageSize[1], self.NumImages)

        data = np.zeros((self.NumImages, self.ImageSize[1], self.ImageSize[0], 4), dtype=np.uint8)
        for i, imageName in enumerate(self.ImagePaths.keys()):
            if imageName in self.ImagesData:
                imageData = self.ImagesData[imageName]
                if imageData is not None:
                    data[i, :imageData.shape[0], :imageData.shape[1], :] = imageData

        gl.glTexSubImage3D(gl.GL_TEXTURE_2D_ARRAY, 0, 0, 0, 0, self.ImageSize[0], self.ImageSize[1], self.NumImages, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)

        self.OutputTexture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.OutputTexture)
        outputSize = (self.ImageSize[0] * self.GridSize[0], self.ImageSize[1] * self.GridSize[1])
        gl.glTexStorage2D(gl.GL_TEXTURE_2D, 1, gl.GL_RGBA8, outputSize[0], outputSize[1])

        gl.glBindImageTexture(0, self.InputTexture, 0, gl.GL_TRUE, 0, gl.GL_READ_ONLY, gl.GL_RGBA8)
        gl.glBindImageTexture(1, self.OutputTexture, 0, gl.GL_FALSE, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA8)

        gl.glUseProgram(self.Program)

        imageSizeLoc = gl.glGetUniformLocation(self.Program, "imageSize")
        gridSizeLoc = gl.glGetUniformLocation(self.Program, "gridSize")
        gl.glUniform2i(imageSizeLoc, *self.ImageSize)
        gl.glUniform2i(gridSizeLoc, *self.GridSize)

        gl.glDispatchCompute(self.GridSize[0], self.GridSize[1], 1)

        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        outputData = np.zeros((outputSize[1], outputSize[0], 4), dtype=np.uint8)
        gl.glGetTexImage(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, outputData)

        imageResult = Image.fromarray(outputData, 'RGBA')

        self._Cleanup()
        
        return imageResult

    def RunColliderShader(self, shaderPath):
        if not glfw.init():
            Utils.PopupManager().Error("Error: MapLib", "GLFW cannot be initialized!")
        
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(640, 480, "Hidden Window", None, None)
        if not window:
            glfw.terminate()
            Utils.PopupManager().Error("Error: MapLib", "GLFW Failed To Create A Window For The Shader")
        
        glfw.make_context_current(window)

        computeShaderSource = self._ReadComputeShader(shaderPath)

        computeShader = gl.glCreateShader(gl.GL_COMPUTE_SHADER)
        gl.glShaderSource(computeShader, computeShaderSource)
        gl.glCompileShader(computeShader)

        if not gl.glGetShaderiv(computeShader, gl.GL_COMPILE_STATUS):
            errorLog = gl.glGetShaderInfoLog(computeShader)
            raise RuntimeError(f"Shader compilation failed:\n{errorLog}")

        self.Program = gl.glCreateProgram()
        gl.glAttachShader(self.Program, computeShader)
        gl.glLinkProgram(self.Program)

        if not gl.glGetProgramiv(self.Program, gl.GL_LINK_STATUS):
            errorLog = gl.glGetProgramInfoLog(self.Program)
            raise RuntimeError(f"Shader linking failed:\n{errorLog}")

        gl.glDeleteShader(computeShader)

        self.InputTexture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.InputTexture)
        gl.glTexStorage3D(gl.GL_TEXTURE_2D_ARRAY, 1, gl.GL_RGBA8, self.ImageSize[0], self.ImageSize[1], self.NumImages)

        colliderColors = {
            "PlayerAndBullet": [255, 0, 0, 255],
            "None": [0, 0, 0, 0],
            "Player": [0, 0, 255, 255],
            "Bullet": [0, 255, 0, 255]
        }

        data = np.zeros((self.NumImages, self.ImageSize[1], self.ImageSize[0], 4), dtype=np.uint8)
        for i, row in enumerate(self.MapData):
            for j, item in enumerate(row.split(', ')):
                color = colliderColors.get(item, [0, 0, 0, 0])
                index = i * self.GridSize[1] + j
                data[index, :, :, :] = color

        gl.glTexSubImage3D(gl.GL_TEXTURE_2D_ARRAY, 0, 0, 0, 0, self.ImageSize[0], self.ImageSize[1], self.NumImages, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)

        self.OutputTexture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.OutputTexture)
        outputSize = (self.ImageSize[0] * self.GridSize[0], self.ImageSize[1] * self.GridSize[1])
        gl.glTexStorage2D(gl.GL_TEXTURE_2D, 1, gl.GL_RGBA8, outputSize[0], outputSize[1])

        gl.glBindImageTexture(0, self.InputTexture, 0, gl.GL_TRUE, 0, gl.GL_READ_ONLY, gl.GL_RGBA8)
        gl.glBindImageTexture(1, self.OutputTexture, 0, gl.GL_FALSE, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA8)

        gl.glUseProgram(self.Program)

        imageSizeLoc = gl.glGetUniformLocation(self.Program, "imageSize")
        gridSizeLoc = gl.glGetUniformLocation(self.Program, "gridSize")
        gl.glUniform2i(imageSizeLoc, *self.ImageSize)
        gl.glUniform2i(gridSizeLoc, *self.GridSize)

        gl.glDispatchCompute(self.GridSize[0], self.GridSize[1], 1)

        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        outputData = np.zeros((outputSize[1], outputSize[0], 4), dtype=np.uint8)
        gl.glGetTexImage(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, outputData)

        imageResult = Image.fromarray(outputData, 'RGBA')

        self._Cleanup()
        
        return imageResult


