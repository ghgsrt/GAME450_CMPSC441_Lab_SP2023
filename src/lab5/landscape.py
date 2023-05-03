import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np

def get_elevation(size):
    xpix, ypix = size

    octaves = [3, 6, 12, 24]

    noises = {}
    for octave in octaves:
        noises[octave] = PerlinNoise(octaves=octave)

    noise = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            coords = [i/xpix, j/ypix]

            noise_val = 0
            for octave in octaves:
                noise_val += (octaves[0] / octave) * noises[octave](coords)

            row.append(noise_val)
        noise.append(row)

    return np.array(noise)

def elevation_to_rgba(elevation):
    xpix, ypix = np.array(elevation).shape
    colormap = plt.cm.get_cmap('jet')
    elevation = (elevation - elevation.min())/(elevation.max()-elevation.min())
    ''' You can play around with colormap to get a landscape of your preference if you want '''
    landscape = np.array([colormap(elevation[i, j])[0:3] for i in range(xpix) for j in range(ypix)]).reshape(xpix, ypix, 3)*255
    landscape = landscape.astype('uint8')
    return landscape

get_landscape = lambda size: elevation_to_rgba(get_elevation(size))


if __name__ == '__main__':
    size = 640, 480
    pic = elevation_to_rgba(get_elevation(size))
    plt.imshow(pic, cmap='gray')
    plt.show()
