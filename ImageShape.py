import cv2
import numpy as np
import os
import random
import operator
import math

class imageShape:

    def __init__(self,width,height):
        self.width = width
        self.height = height

    def generateShape(self):
        self.shape = np.zeros((self.height,self.width,3),np.uint8)
        numero = random.randint(0,3)
        figuras = ['triangulo','cuadrado','rectangulo','circulo']
        centro_imagen = np.array((int(self.width/2),int(self.height/2)))

        if figuras[numero] == 'triangulo':
            lado = int(min(self.width,self.height)/2)
            lado_medios = int(lado/2)
            altura_medios = int(math.sqrt(3)*lado/4)

            p1 = (lado_medios,-altura_medios)
            p2 = (-lado_medios,-altura_medios)
            p3 = (0,altura_medios)

            triangle_cnt = np.array([p1,p2,p3])
            triangle_cnt = triangle_cnt + centro_imagen
            triangle_cnt = triangle_cnt.astype(np.int)

            cv2.drawContours(self.shape, [triangle_cnt], 0, (255, 255, 0), -1)

        if figuras[numero] == 'cuadrado':
            lado = int(min(self.width,self.height)/2) #rotado 45 grados
            lado_medios = int(lado/2)
            p1 = (lado_medios,lado_medios)
            p2 = (lado_medios,-lado_medios)
            p3 = (-lado_medios,lado_medios)
            p4 = (-lado_medios,-lado_medios)

            square_cnt = np.array([p3,p1,p2,p4]) #matriz 4x2
            matriz_rotacion = np.array(((np.cos(np.pi / 4.),np.sin(-1 * np.pi / 4.)),(np.sin(np.pi / 4.),np.cos(np.pi / 4.))))
            square_cnt = np.dot(square_cnt,matriz_rotacion)
            square_cnt = square_cnt.astype(np.int)
            square_cnt = square_cnt + centro_imagen

            cv2.drawContours(self.shape, [square_cnt], 0, (255, 255, 0), -1)

        if figuras[numero] == 'rectangulo':
            lado_horizontal = int(self.width/2)
            lado_vertical = int(self.height/2)

            p1 = (int(lado_horizontal/2),int(lado_vertical/2))
            p2 = (int(lado_horizontal/2),-int(lado_vertical/2))
            p3 = (-int(lado_horizontal/2),int(lado_vertical/2))
            p4 = (-int(lado_horizontal/2),-int(lado_vertical/2))

            rectangle_cnt = np.array([p3, p1, p2, p4])
            rectangle_cnt = rectangle_cnt.astype(np.int)
            rectangle_cnt = rectangle_cnt + centro_imagen

            cv2.drawContours(self.shape, [rectangle_cnt], 0, (255, 255, 0), -1)

        if figuras[numero] == 'circulo':
            radio = int(min(self.width,self.height)/4)
            cv2.circle(self.shape,(int(self.width/2),int(self.height/2)),radio,(255,255,0),-1)

    def showShape(self):

        cv2.imshow('imagen',self.shape)
        cv2.waitKey(5000)