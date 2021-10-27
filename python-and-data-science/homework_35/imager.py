import sys
import re
import click
from PIL import Image
import numpy as np
from loguru import logger


@click.group()
@click.version_option()
def cli():
    """img -- saves pixels array of an image or recreate an image from file with pixels array.
    """


@cli.command()
@click.argument("source")
@click.argument("destination")
def dump(source: str='image.png', destination: str='dump.txt') -> np.ndarray:
    """
    The function saves an array of pixels from image into file.
    Param <source> -> should be a path to an image.
    Param <destination> should be a path to an array.
    """
    img = Image.open(source)
    logger.debug('source_file_name=<{}>, size=<{}>, mode=<{}>', source, img.size, img.mode)
    data = np.asarray(img)
    logger.debug('type={}, array_shape={}', type(data), data.shape)
    with open(destination, 'w') as f:

        # Any line starting with "#" will be ignored by np.loadtxt
        # Save array shape at the top of the dump file
        
        f.write('# Array shape: {0}\n'.format(data.shape))
        # Iterating through a ndimensional array produces slices along the last axis. 
        # This is equivalent to data[i,:,:] in this case
        
        for data_slice in data:
            np.savetxt(f, data_slice, fmt='%-7.0f')
            
            # Writing out a break to indicate different slices
            f.write('# New slice\n')
    
    # Easy option to reshape our 3D ndarray to 2D and save, (not human readable)
    # img_reshaped = data.reshape(data.shape[0], -1) # instead of looping and slicing through channels shape
    # np.savetxt('test.csv', img_reshaped, delimiter=',') # save it as numpy array in csv file
    return data


@cli.command()
@click.argument("source")
@click.argument("destination")
def recreate(source: str='dump.txt', destination: str='result.png') -> None:
    """
    The function loads pixels array from a file and saves it as an image.
    Param <source> -> should be a path to pixels array.
    Param <destination> -> should be a path for a new image.
    """
    new_data = np.loadtxt(source, dtype='uint8')
    logger.debug('loaded_data_type=<{}>,shape=<{}>', type(new_data), new_data.shape)
    new_data = new_data.reshape(_read_array_shape_from_header(source='dump.txt'))  
    logger.debug('reshaped_data=<{}>', new_data.shape)
    img = Image.fromarray(new_data)
    img.save(destination)


@cli.command()
@click.argument("source")
@click.argument("destination")
@click.option('-c', '--color',
              type=click.Choice(['red', 'green', 'blue', None]), help='choose color')
def single(source: str='image.png', destination: str='result.png', color: str | None = None ) -> None:
    """
    The function modifies source image to the chosen channel (RED, GREEN, BLUE):
    If color param is not specified, all 3 cases will be concatenated.
    """
    logger.debug("color=<{}>", color)
    img = np.array(Image.open(source))

    match color:
        case "red":
            img = img.copy()
            img[:, :, (1, 2)] = 0
        case "green":
            img = img.copy()
            img[:, :, (0, 2)] = 0
        case "blue":
            img = img.copy()
            img[:, :, (0, 1)] = 0
        case _:
            img_R = img.copy()
            img_R[:, :, (1, 2)] = 0
            img_G = img.copy()
            img_G[:, :, (0, 2)] = 0
            img_B = img.copy()
            img_B[:, :, (0, 1)] = 0
            img = np.concatenate((img_R, img_G, img_B), axis=1)
    
    img = Image.fromarray(img)
    img.save(destination)


def _read_array_shape_from_header(source: str='dump.txt') -> list:
    """
    Service function. 
    Get file_name with ndarray, read ndarray shape from header and return it as python-list.
    """
    with open(source) as f:
        txt = f.readline()
    logger.debug('txt_line=<{}>', txt)
    txt = re.sub(r'[\(|\)|,]', '', txt)
    logger.debug('resub_result=<{}>', txt)
    shape = [int(char) for char in txt.split() if char.isdigit()]
    logger.debug('result_collection=<{}>,type={}', shape, type(shape))
    return shape
