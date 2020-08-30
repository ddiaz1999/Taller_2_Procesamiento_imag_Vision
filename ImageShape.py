import cv2
import numpy as np
import os
import random
import math

class imageShape:

    def __init__(self,height,width):
        self.width = width
        self.height = height
        self.image_available = 0

    def generateShape(self):
        self.shape = np.zeros((self.height,self.width,3),np.uint8)
        random_number = random.randint(0,3)
        figures = ['triangulo','cuadrado','rectangulo','circulo']
        self.image_name = figures[random_number]
        image_center = np.array((int(self.width/2),int(self.height/2)))

        if self.image_name == 'triangulo':
            side_length = int(min(self.width,self.height)/2)
            half_side = int(side_length/2)
            half_height = int(math.sqrt(3)*side_length/4)

            p1 = (half_side,-half_height)
            p2 = (-half_side,-half_height)
            p3 = (0,half_height)

            triangle_cnt = np.array([p1,p2,p3])
            triangle_cnt = triangle_cnt + image_center
            triangle_cnt = triangle_cnt.astype(np.int)

            cv2.drawContours(self.shape, [triangle_cnt], 0, (255, 255, 0), -1)

        if self.image_name == 'cuadrado':
            side_length = int(min(self.width,self.height)/2) 
            half_side = int(side_length/2)
            p1 = (half_side,half_side)
            p2 = (half_side,-half_side)
            p3 = (-half_side,half_side)
            p4 = (-half_side,-half_side)

            square_cnt = np.array([p3,p1,p2,p4]) #matriz 4x2
            rotation_matrix = np.array(((np.cos(np.pi / 4.),np.sin(-1 * np.pi / 4.)),(np.sin(np.pi / 4.),np.cos(np.pi / 4.))))
            square_cnt = np.dot(square_cnt,rotation_matrix)
            square_cnt = square_cnt.astype(np.int)
            square_cnt = square_cnt + image_center

            cv2.drawContours(self.shape, [square_cnt], 0, (255, 255, 0), -1)

        if self.image_name == 'rectangulo':
            horizontal_side = int(self.width/2)
            vertical_side = int(self.height/2)

            p1 = (int(horizontal_side/2),int(vertical_side/2))
            p2 = (int(horizontal_side/2),-int(vertical_side/2))
            p3 = (-int(horizontal_side/2),int(vertical_side/2))
            p4 = (-int(horizontal_side/2),-int(vertical_side/2))

            rectangle_cnt = np.array([p3, p1, p2, p4])
            rectangle_cnt = rectangle_cnt.astype(np.int)
            rectangle_cnt = rectangle_cnt + image_center

            cv2.drawContours(self.shape, [rectangle_cnt], 0, (255, 255, 0), -1)

        if self.image_name == 'circulo':
            radius = int(min(self.width,self.height)/4)
            cv2.circle(self.shape,(int(self.width/2),int(self.height/2)),radius,(255,255,0),-1)

        self.image_available = 1

    def showShape(self):
        if self.image_available == 1:
            self.image_available = 0
            cv2.imshow('Figura generada',self.shape)
            cv2.waitKey(5000)
        else:
            cv2.imshow('imagen',np.zeros((self.height,self.width,3),np.uint8))
            cv2.waitKey(5000)

    def getShape(self):
        return self.shape, self.image_name

    def whatShape(self,input_image):
        image_draw = input_image.copy()
        image_gray = cv2.cvtColor(image_draw, cv2.COLOR_BGR2GRAY)
        ret, image_Binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(image_Binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        perimeter = cv2.arcLength(contours[0], True)
        figure_approximation = cv2.approxPolyDP(contours[0], 0.04 * perimeter, True)

        if len(figure_approximation) == 3:
            return 'triangulo'

        elif len(figure_approximation) == 4:
            (x, y, w, h) = cv2.boundingRect(figure_approximation)
            aspect_ratio = float(w)/h

            if aspect_ratio == 1:
                return 'cuadrado'
            else:
                return 'rectangulo'

        else:
            return 'circulo'