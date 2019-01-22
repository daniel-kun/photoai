import os
from PIL import Image

thumbnail_sizes = [256, 384]

def make_thumbnails(root_dir):
    i = 0
    for root, dirs, files in os.walk(root_dir):
        for file_base_name in files:
            source_file = os.path.join(root, file_base_name)
            source_img = Image.open(source_file)
            for size in thumbnail_sizes:
                thumb_dir = os.path.join(root, 'thumbnails_{0}'.format(size))
                if not(os.path.isdir(thumb_dir) and os.path.exists(thumb_dir)):
                    os.makedirs(thumb_dir)
                thumb_name = os.path.join(thumb_dir, file_base_name)
                source_img.resize((size, size)).save(thumb_name)
                print(thumb_name)
                i = i + 1
                if i > 20:
                    os.exit(1)


make_thumbnails('SampleOutput')

