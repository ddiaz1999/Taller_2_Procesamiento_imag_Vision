from ImageShape import *

if __name__ == '__main__':
    height_image = int(input('ingrese el alto de la imagen: '))
    width_image = int(input('ingrese el ancho de la imagen: '))
    image = imageShape(height_image, width_image)
    image.generateShape()
    image.showShape()
    generated_image, image_class = image.getShape()
    classification = image.whatShape(generated_image)
    print(f'La figura se clasificó en: {classification}')
    print('clasificacion existosa') if classification == image_class else print('clasificacion fallida')
