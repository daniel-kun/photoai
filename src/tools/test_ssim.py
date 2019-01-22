from skimage.measure import compare_ssim, compare_mse
from scipy import ndimage
import numpy as np
import os

def test_ssim(root_folder):
    images = []
    for f in os.scandir(root_folder):
        if f.is_file():
            images.append((f.path, Image.open(f.path)))
    for i in range(len(images) - 1):
        (first, second) = ((images[i][0], images[i][1].resize((64, 64))), (images[i+1][0], images[i+1][1].resize((64, 64))))
        print((first, second))
        return
        print('Comparing {0} with {1}'.format(first[0], second[0]))
        first_pic = np.array(first[1].getdata()).reshape(64, 64, 3)
        second_pic = np.array(second[1].getdata()).reshape(64, 64, 3)
        print(compare_ssim(first_pic, second_pic, None, multichannel=True))
        print(compare_mse(first_pic, second_pic))

print('============= 1 (expecting differences)')
test_ssim('C:\\Projects\\photoai\\src\\SampleOutput\\2015-01-24-15-29-12')
print('============= 2 (NO differences expected)')
test_ssim('C:\\Projects\\photoai\\src\\SampleOutput\\2014-10-30-11-54-50')
print('============= 3 (NO differences expected)')
test_ssim('C:\\Projects\\photoai\\src\\SampleOutput\\2015-01-16-14-06-51')
print('============= 4 (NO differences expected)')
test_ssim('C:\\Projects\\photoai\\src\\SampleOutput\\2017-01-15-16-28-32')
print('============= 5 (NO differences expected)')
test_ssim('C:\\Projects\\photoai\\src\\SampleOutput\\2016-08-09-17-54-14')
print('============= 6 (expecting differences)')
test_ssim('C:\\Projects\\photoai\\src\\SampleOutput\\2016-06-05-17-15-58')
