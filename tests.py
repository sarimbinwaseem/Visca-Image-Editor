from PIL import Image, ImageEnhance
import os
from multiprocessing import Pool

pieces = []
effectedPieces = []
def imgcrop(inFile, xPieces, yPieces):
    filename, file_extension = os.path.splitext(inFile)
    im = Image.open(inFile)
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            a = im.crop(box)
            try:
                # a.save(filename + "-" + str(i) + "-" + str(j) + file_extension)
                pieces.append(a)
            except:
                pass

def effectit(piece):
    bright = ImageEnhance.Brightness(piece)
    image = bright.enhance(2.0)
    # effectedPieces.append(image)
    return image

imgcrop("largeImage.jpg", 5, 5)

with Pool(processes = 4) as pool:
    m = pool.map_async(effectit, pieces)
    effectedPieces.extend(m.get())

print(effectedPieces)
print("saving")
e = 0
for i in effectedPieces:
    i.save(f"/home/rapidswords/Desktop/image{e}.jpg")
    e += 1