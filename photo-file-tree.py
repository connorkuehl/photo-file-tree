# photo-file-tree organizes photos into a tree-hierarchy based on when the photo was taken.
#
# Example: RootFolder/YEAR/MONTH/DAY/image_name.jpg

import argparse
import datetime
import exifread
import os
import shutil

# get_exif_tags returns the EXIF information contained in the image.
def get_exif_tags(image_path):
    with open(image_path, 'rb') as image:
        exif = exifread.process_file(image, stop_tag='DateTimeOriginal')
        return exif

# date_to_path_str converts the string representation of the "DateTimeOriginal" tag
# into a file path-friendly version consisting of year/month/day. It discards the
# other time information such as hours, minutes, seconds.
#
# The goal is to produce a directory structure like: RootFolder/2018/08/25
def date_to_path_str(dt):
        day, _ = dt.split(" ", 1)
        year, month, day = day.split(":", 2)
        return f'{year}/{month.rjust(2, "0")}/{day.rjust(2, "0")}'

parser = argparse.ArgumentParser(description='Organize your photos in a tree hierarchy that corresponds to creation date.')
parser.add_argument(
    '--dry-run',
    required=False,
    action='store_true',
    help='Preview where the files will be moved without actually making changes on disk')
parser.add_argument(
    '--root',
    required=True,
    nargs=1,
    dest='root',
    help='The top-level folder of your photo collection')
parser.add_argument(
    'images',
    nargs='*',
    help='The images to sort into the hierarchy located at ROOT')
parser.add_argument(
    '--prune',
    required=False,
    action='store_true',
    help='Removes empty folders found under the photo ROOT')
args = parser.parse_args()

# argparse stores the arguments as a list. Even if it requires 1 argument, it is a list with
# one element.
root = args.root[0]

for old_image_path in args.images:
    exif_tags = get_exif_tags(old_image_path)
    date_time_original = exif_tags.get('EXIF DateTimeOriginal')
    if not date_time_original:
        print('[ERROR] Could not get creation date information from ' + old_image_path)
        continue
    # Convert the EXIF's string representation into a file path-friendly version
    date_taken = date_to_path_str(str(date_time_original))
    # Get the image's name without the leading directories it's contained in
    image_name = os.path.basename(old_image_path)
    # New path is contained under the specified ROOT, with the new date hierarchy structure + the original file name
    new_path = f'{root}/{date_taken}/{image_name}'
    # Make sure the path is friendly with the operating system
    new_path = os.path.abspath(new_path)
    # Move the file to its new home
    if not args.dry_run:
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.move(old_image_path, new_path)
    print(old_image_path + ' -> ' + new_path)

if args.dry_run:
    print('This was a dry run, nothing was moved.')