import cv2
import numpy as np
import os
import random
import math

class imageShape: #Se crea la clase imageShape

    def __init__(self,height,width): #se define el constructor
        self.width = width
        self.height = height #se guardan en self.width y self.height el ancho y el alto deseado respectivamente
        self.image_available = 0 #se crea este atributo para indicar si hay o no imagen disponible

    def generateShape(self): #metodo para generar figura
        self.shape = np.zeros((self.height,self.width,3),np.uint8) #se genera una imagen en negro con las dimensiones respectivas y se almacena en self.shape
        random_number = random.randint(0,3) #se genera un un numero aleatorio uniformemente distribuido
        shapes = ['triangulo','cuadrado','rectangulo','circulo'] #se crea una lista con las figuras posibles a generar
        self.image_name = shapes[random_number] #se almacena en self.image_name el nombre de la figura a generar
        image_center = np.array((int(self.width/2),int(self.height/2))) #centro de la imagen

        if self.image_name == 'triangulo':
            side_length = int(min(self.width,self.height)/2) #longitud de los lados del triangulo
            half_side = int(side_length/2) #longitud de la mitad de un lado
            half_height = int(math.sqrt(3)*side_length/4) #longitud de la mitad de altura

            #ubicacion de los vertices del triangulo
            p1 = (half_side,-half_height)
            p2 = (-half_side,-half_height)
            p3 = (0,half_height)

            triangle_cnt = np.array([p1,p2,p3]) #arreglo 3x2 con los vertices
            triangle_cnt = triangle_cnt.astype(np.int)

            triangle_cnt = triangle_cnt + image_center #se centra la figura en la imagen
            cv2.drawContours(self.shape, [triangle_cnt], 0, (255, 255, 0), -1) #dibuja la figura en la imagen

        if self.image_name == 'cuadrado':
            side_length = int(min(self.width,self.height)/2) #longitud de los lados del cuadrado
            half_side = int(side_length/2) #longitud de la mitad de un lado

            #ubicacion de los vertices del cuadrado sin rotar
            p1 = (half_side,half_side)
            p2 = (half_side,-half_side)
            p3 = (-half_side,half_side)
            p4 = (-half_side,-half_side)

            square_cnt = np.array([p3,p1,p2,p4]) #matriz 4x2 cada fila es un vertice

            rotation_angle = np.pi / 4. #angulo de 45 grados en radianes
            #se genera la representacion matricial estandar de la transformacion rotacion en R^2 (matriz 2x2)
            rotation_matrix = np.array(((np.cos(rotation_angle),np.sin(-1 * rotation_angle)),(np.sin(rotation_angle),np.cos(rotation_angle))))
            square_cnt = np.dot(square_cnt,rotation_matrix) #el resultado sera una matriz 4x2 y en cada fila estaran los nuevos vertices rotados
            square_cnt = square_cnt.astype(np.int)

            square_cnt = square_cnt + image_center #se centra la figura en la imagen
            cv2.drawContours(self.shape, [square_cnt], 0, (255, 255, 0), -1) #se dibuja la figura en la imagen

        if self.image_name == 'rectangulo':
            horizontal_side = int(self.width/2) #longitud lado horizontal
            vertical_side = int(self.height/2) #longitud lado vertical

            #ubicacion de los vertices del rectangulo
            p1 = (int(horizontal_side/2),int(vertical_side/2))
            p2 = (int(horizontal_side/2),-int(vertical_side/2))
            p3 = (-int(horizontal_side/2),int(vertical_side/2))
            p4 = (-int(horizontal_side/2),-int(vertical_side/2))

            rectangle_cnt = np.array([p3, p1, p2, p4]) #matriz 4x2 cada fila es un vertice
            rectangle_cnt = rectangle_cnt.astype(np.int)

            rectangle_cnt = rectangle_cnt + image_center #se centra la figura en la imagen
            cv2.drawContours(self.shape, [rectangle_cnt], 0, (255, 255, 0), -1) #se dibuja la figura en la imagen

        if self.image_name == 'circulo':
            radius = int(min(self.width,self.height)/4) #longitud del radio de la circunferencia
            cv2.circle(self.shape,(int(self.width/2),int(self.height/2)),radius,(255,255,0),-1) #se centra y dibuja la figura en la imagen

        self.image_available = 1 #se actualiza la bandera para indicar que hay imagen disponible

    def showShape(self): #metodo para mostrar figura
        if self.image_available == 1:
            self.image_available = 0 #se actualiza el estado de self.image_available
            cv2.imshow('Figura generada',self.shape) #se muestra la figura
            cv2.waitKey(5000)
        else:
            #si no hay imagen disponible se muestra imagen en negro
            cv2.imshow('imagen',np.zeros((self.height,self.width,3),np.uint8))
            cv2.waitKey(5000)

    def getShape(self): #metodo retorna la imagen el nombre de la figura
        return self.shape, self.image_name

    def whatShape(self,input_image): #metodo de clasificacion
        image_draw = input_image.copy()

        #umbralizacion por metodo OTSU
        image_gray = cv2.cvtColor(image_draw, cv2.COLOR_BGR2GRAY)
        ret, image_Binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #se almacena en contours los contornos en la imagen (se espera solo un contorno)
        contours, hierarchy = cv2.findContours(image_Binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        perimeter = cv2.arcLength(contours[0], True) #perimetro del contorno
        figure_approximation = cv2.approxPolyDP(contours[0], 0.04 * perimeter, True) #esta funcion reduce el numero de puntos de un contorno

        if len(figure_approximation) == 3: #si la figura es un triangulo tendra 3 vertices
            return 'triangulo'

        elif len(figure_approximation) == 4: #si la figura tiene 4 vertices
            shape_name = ''
            
            #se calcula el aspect ratio de la figura
            (x, y, w, h) = cv2.boundingRect(figure_approximation)
            aspect_ratio = float(w)/h

            #si el aspect ratio es 1 significa que la figura es un cuadrado
            shape_name = 'cuadrado' if aspect_ratio == 1 else 'rectangulo'
            return shape_name

        else: #de otra forma se asumira que la figura es un circulo
            return 'circulo'
