import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy
from random import randint, random
folder = "D:/ProgrammingBigFiles/Generated Numbers/"
myDigits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# myDigits = [5, 6, 7]
# myDigits = [6, 7]

class ImageGenerator:

    def __init__(self, fontName):
        self.fonts = [ImageFont.truetype(fontName.lower() + ".ttf", 20), ImageFont.truetype("arialbd.ttf", 20)]
        self.counter = 0

    def generateImages(self, amount):
        for i in range(amount):
            self.generateImage()

    def generateImage(self):
        digit = str(myDigits[randint(0, len(myDigits) - 1)])
        font = self.fonts[randint(0, len(self.fonts) - 1)]
        f = open(folder + str(self.counter) + ".ans", "w")
        print(digit, file=f)
        f.close()
        image = Image.new("L", (28, 28))
        draw = ImageDraw.Draw(image)
        numberWidth, numberHeight = font.getsize(digit)
        dx, dy = randint(-3, 3), randint(-2, 2)
        draw.text([13 - numberWidth // 2 + dx, 13 - numberHeight // 2 + dy], digit, fill=255, font=font)
        image = image.rotate( 45*( (2*random() - 1)**1 ) )
        image.save(folder + str(self.counter) + ".png")
        self.counter += 1

    def imageToMatrix(self, imageId):
        with Image.open(folder + str(imageId) + ".png", "r") as image:
            return(numpy.array(numpy.matrix(numpy.fromstring(image.tobytes(), dtype=numpy.uint8)).transpose()))