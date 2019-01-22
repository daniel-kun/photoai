import os
from PIL import Image, ExifTags

thumbnail_sizes = [256, 384]

def normalize_orientation(image):
    try :
        for orientation in ExifTags.TAGS.keys() :
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(image._getexif().items())
        if not orientation in exif:
            return image

        exif_orientation = exif[orientation]
        if exif_orientation == 3 :
            return image.transpose(Image.ROTATE_180)
        elif exif_orientation == 6 :
            return image.transpose(Image.ROTATE_270)
        elif exif_orientation == 8 :
            return image.transpose(Image.ROTATE_90)
        else:
            return image
    except:
        traceback.print_exc()

def calc_box(orig_box, desired_size):
    if orig_box[0] <= orig_box[1]:
        # The pictures is portrait
        return (0, (orig_box[1] / 4), orig_box[0], (orig_box[1] - orig_box[1] / 4))
    else:
        # The pictures is landscape
        return ((orig_box[0] / 4), 0, (orig_box[0] - orig_box[0] / 4), orig_box[1])

def make_thumbnails(root_dir):
    for root, dirs, files in os.walk(root_dir):
        (_, leaf_dir) = os.path.split(root)
        if not leaf_dir.startswith('thumbnails_'):
            print('Creating thumbnails in {dir}'.format(dir=root))
            for file_base_name in files:
                source_file = os.path.join(root, file_base_name)
                source_img = normalize_orientation(Image.open(source_file))
                for size in thumbnail_sizes:
                    thumb_dir = os.path.join(root, 'thumbnails_{0}'.format(size))
                    if not(os.path.isdir(thumb_dir) and os.path.exists(thumb_dir)):
                        os.makedirs(thumb_dir)
                    thumb_name = os.path.join(thumb_dir, file_base_name)
                    source_img.resize((size, size), Image.NEAREST, calc_box(source_img.size, size)).save(thumb_name)

make_thumbnails('SampleOutput')

