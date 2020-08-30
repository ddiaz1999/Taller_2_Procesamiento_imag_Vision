from ImageShape import *

if __name__ == '__main__':
    height_image = int(input('ingrese el alto de la imagen: ')) #se pide al usuario que ingrese el alto deseado de la imagen
    width_image = int(input('ingrese el ancho de la imagen: ')) #se pide al usuario que ingrese el ancho deseado de la imagen
    image = imageShape(height_image, width_image) #se hace un llamado a la clase y se ingresan como parametros el tamaño de la imagen
    image.generateShape() #se genera la imagen y la figura
    image.showShape() #se muestra la figura por 5 segundos
    generated_image, image_class = image.getShape() #se almacena en generated_image la imagen generada y en image_class el nombre de la figura
    classification = image.whatShape(generated_image) #se almacena en classification el resultado del metodo de clasificacion
    print(f'La figura se clasificó en: {classification}')
    print('clasificacion existosa') if classification == image_class else print('clasificacion fallida') #se verifica si la clasificacion fue exitosa
