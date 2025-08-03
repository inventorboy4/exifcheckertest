import os
import argparse
import shutil
from datetime import datetime
import filetype
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def ImageDate(fn):
    TTags = [('DateTimeOriginal', 'SubsecTimeOriginal'),
    ('DateTimeDigitized', 'SubsecTimeDigitized'),
    ('DateTime', 'SubsecTime')]
    exif = get_exif(fn)
    for i in TTags:
        dat, sub = exif.get(i[0]), exif.get(i[1], 0)
        dat = dat[0] if type(dat) == tuple else dat
        sub = sub[0] if type(sub) == tuple else sub
        if dat != None: break
    if dat == None: return
 
    T = datetime.strptime('{}.{}'.format(dat, sub), '%Y:%m:%d %H:%M:%S.%f').strftime('%Y-%m-%d_%H-%M-%S')
    return T

def image_sort(path, res):
    valid_extentions = ["jpg", "jpeg", "png", "gif", "bmp"]
    amounts = [0, 0]
    for address, dirs, files in os.walk(path):
        for filename in files:
            amounts[0] += 1
            full_path = address+"\\"+filename
            if not filetype.is_image(full_path):
                print(filename, "not valid")
                continue
#            print(datetime.fromtimestamp(os.path.getctime(full_path)).strftime('%Y-%m-%d %H:%M:%S'))
            if ImageDate(full_path) != None:
                amounts[1] += 1
                new_filename = ImageDate(full_path)+"."+filename.split(".")[-1].lower()
                res_path = res+address.removeprefix(path)+"\\"+new_filename[:4]
        #for dir in dirs:
            #new_amounts = image_sort(dir, res)
            #amounts[0]+=new_amounts[0]
            #amounts[1]+=new_amounts[1]
    return amounts

parser = argparse.ArgumentParser(prog="ImageSorter", 
                                 description="Simple image batch sorter", 
                                 epilog="If any argument is not given, it defaults to current folder.")
parser.add_argument("-f", "--file", help="Path to folder with images to sort.")
parser.add_argument("--files", action="extend", nargs="+", type=str, help="Path to multiple folders separated by space.")
parser.add_argument("-o", "--output", help="Output path to put sorted images in folders to.")

args = parser.parse_args()
path = args.files if (args.files != None) else [args.file] if (args.file != None) else [os.getcwd()]
output = args.output if (args.output != None) else os.getcwd()+"\\result"
print(path)
amounts = [0, 0]
for folder in path:
    new_amounts = image_sort(folder, output)
    amounts[0]+=new_amounts[0]
    amounts[1]+=new_amounts[1]
print("Images overall:", amounts[0])
print("Images with efix:", amounts[1])
