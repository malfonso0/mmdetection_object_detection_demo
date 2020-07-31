from xml.dom import minidom
import os
import multiprocessing.dummy as mpd
from functools import partial
from collections import namedtuple
import glob

from resize_images import main as ChangeImageSize
def ChangeXmlSize(filename, newHeight, newWidth):
    try:
        mydoc = minidom.parse(filename)
    except:
        print('empty file %s'% filename)
        return

    items = mydoc.getElementsByTagName('size')
    size_prop=items[0]
    ## GET_UPDATEe SIZE
    width_prop = size_prop.getElementsByTagName('width')[0]
    height_prop = size_prop.getElementsByTagName('height')[0]


    img_width = int(width_prop.firstChild.nodeValue)
    img_height = int(height_prop.firstChild.nodeValue)

    if(img_width==0 or img_height==0):
        print('bad size in %s'% filename)
        return

    width_prop.firstChild.nodeValue = str(newWidth)
    height_prop.firstChild.nodeValue = str(newHeight)
    items = mydoc.getElementsByTagName('object')
    

    for elem in items:
        bbox = elem.getElementsByTagName('bndbox')
        bbox=bbox[0]
        
        bbox.childNodes[ 1 ].firstChild.nodeValue = str(int( int(bbox.childNodes[ 1 ].firstChild.nodeValue) * newWidth/img_width))
        bbox.childNodes[ 3 ].firstChild.nodeValue = str(int( int(bbox.childNodes[ 3 ].firstChild.nodeValue) * newHeight/img_height))
        bbox.childNodes[ 5 ].firstChild.nodeValue = str(int( int(bbox.childNodes[ 5 ].firstChild.nodeValue) * newWidth/img_width))
        bbox.childNodes[ 7 ].firstChild.nodeValue = str(int( int(bbox.childNodes[ 7 ].firstChild.nodeValue) * newHeight/img_height))

    with open(filename, 'w') as out_file:
        mydoc.writexml(out_file)

def ChangeImageSizeWrapper(h, w, in_folder, out_folder):
    chngsize_args = namedtuple('Argument', 'raw_dir save_dir in_ext out_ext target_size')
    args = chngsize_args(in_folder, out_folder, "jpg,png", "jpg", f"({w},{h})")
    ChangeImageSize(args)

if __name__ == "__main__":
    
    data_folder = "data/VOC2007"
    xml_folder = os.path.join(data_folder,'Annotations')
    in_folder = os.path.join(data_folder,"JPEGImages_raw")
    out_folder = os.path.join(data_folder,"JPEGImages")
    newHeight=400
    newWidth=1000


    #ChangeImageSizeWrapper(newHeight, newWidth, in_folder,out_folder)

    filenames = glob.glob(os.path.join(xml_folder, "*.xml" ) ) 

    with mpd.Pool() as pool:
        pool.map(partial(ChangeXmlSize, newHeight=newHeight, newWidth=newWidth), filenames)