# photo-file-tree 

A utility to organize your photos into a tree-hierarchy based on when the photo was taken.

Example: `RootFolder/YEAR/MONTH/DAY/image_name.jpg`

## Usage

`python photo-file-tree.py --root C:\Users\Connor\Pictures\Photos C:\Users\Connor\Downloads\Unsorted\*.jpg`

### Flags/Options

* `--dry-run` allows you to preview where the image will be moved without touching anything on disk.

* `--root` is a required argument that tells the script where the top-level directory is to begin sorting the images to. If you specify `--root C:\Users\Connor\Pictures` then it will sort images to `C:\Users\Connor\Pictures\YEAR\MONTH\DAY\image.jpg`