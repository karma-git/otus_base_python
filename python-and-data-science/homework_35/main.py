import sys
import re
import click
from PIL import Image
import numpy as np
from loguru import logger


@click.group()
@click.version_option()
def cli():
    """Naval Fate.
    This is the docopt example adopted to Click but with some actual
    commands implemented and not just the empty parsing which really
    is not all that interesting.
    """


@cli.command()
@click.option("-s", "--source", default='image.png', help="Image file")
@click.option("-t", "--target", default='dump.txt', help="File with array data")
def dump(source: str='image.png', target: str='dump.txt') -> np.ndarray:
    """
    dump_pixel_array
    Source file should be image.
    Target file should be txt
    """
    img = Image.open(source)
    logger.debug('source_file_name=<{}>, size=<{}>, mode=<{}>', source, img.size, img.mode)
    data = np.asarray(img)
    logger.debug('type={}, array_shape={}', type(data), data.shape)
    with open(target, 'w') as f:

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
@click.option("-s", "--source", default='dump.txt', help="File with array data")
@click.option("-t", "--target", default='result.png', help="Image file")
def create(source: str='dump.txt', target: str='result.png') -> None:
    """
    load_image_from_pixel_array
    """
    new_data = np.loadtxt(source, dtype='uint8')
    logger.debug('loaded_data_type=<{}>,shape=<{}>', type(new_data), new_data.shape)
    new_data = new_data.reshape(_read_array_shape_from_header(source='dump.txt'))  
    logger.debug('reshaped_data=<{}>', new_data.shape)
    img = Image.fromarray(new_data)
    img.save(target)

def _read_array_shape_from_header(source: str='dump.txt') -> list:
    """
    Service function. 
    Get file_name with ndarray, read ndarray shape from header and return it as list.
    """
    with open(source) as f:
        txt = f.readline()
    logger.debug('txt_line=<{}>', txt)
    txt = re.sub(r'[\(|\)|,]', '', txt)
    logger.debug('resub_result=<{}>', txt)
    shape = [int(char) for char in txt.split() if char.isdigit()]
    logger.debug('result_collection=<{}>,type={}', shape, type(shape))
    return shape
