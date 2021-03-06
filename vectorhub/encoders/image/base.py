from typing import Union
from ...base import Base2Vec
from ...import_utils import is_all_dependency_installed
# TODO: Change encoders-image-tfhub into general encoders-image
if is_all_dependency_installed('encoders-image'):
    import io
    import imageio
    import numpy as np
    import matplotlib.pyplot as plt
    from urllib.request import urlopen, Request
    from urllib.parse import quote
    from skimage import transform

class BaseImage2Vec(Base2Vec):
    def read(self, image: str):
        """
            An method to read images. 
            Args:
                image: An image link/bytes/io Bytesio data format.
                as_gray: read in the image as black and white
        """
        if type(image) == str:
            if 'http' in image:
                b = io.BytesIO(urlopen(Request(
                    quote(image, safe=':/?*=\''), headers={'User-Agent': "Mozilla/5.0"})).read())
            else:
                b = image
        elif type(image) == bytes:
            b = io.BytesIO(image)
        elif type(image) == io.BytesIO:
            b = image
        else:
            raise ValueError("Cannot process data type. Ensure it is is string/bytes or BytesIO.")
        try:
            return np.array(imageio.imread(b, pilmode="RGB"))
        # TODO: Flesh out exceptions
        except:
            return np.array(imageio.imread(b)[:, :, :3])
    
    def to_grayscale(self, sample, rgb_weights: list=None):
        """
            Converting an image from RGB to Grayscale
        """
        if rgb_weights is None:
            return np.repeat(np.dot(sample[...,:3], self.rgb_weights)[..., np.newaxis], 3, -1)
        else:
            return np.repeat(np.dot(sample[...,:3], rgb_weights)[..., np.newaxis], 3, -1)
    
    @property
    def rgb_weights(self):
        """
            Get RGB weights for grayscaling.
        """
        return [0.2989, 0.5870, 0.1140]

    def show_image(self, sample, cmap=None, is_grayscale=True):
        """
            Show an image once it is read. 
            Arg:
                sample: Image that is read (numpy array)
        """
        if is_grayscale:
            return plt.imshow(sample, cmap=plt.get_cmap("gray"))
        return plt.imshow(sample, cmap=cmap)
    
    def image_resize(self, image_array, width=0, height=0, rescale=0, resize_mode='symmetric'):
        if width and height:
            image_array = transform.resize(image_array, (width, height), mode=resize_mode, preserve_range=True)
        if rescale:
            image_array = transform.rescale(image_array, rescale, preserve_range=True, anti_aliasing=True)
        return np.array(image_array)
