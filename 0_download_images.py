"""Originally made by dr. G. Spigler Tilburg Univeristy"""

import sys, os, multiprocessing, csv
import tqdm
from urllib import request, error
from PIL import Image
from io import BytesIO

os.chdir('c:/Users/flori/OneDrive/Documents/Uni/8_Master_thesis/code')
out_dir = 'c:/Users/flori/download'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

# Download images as <id>_<extendedname>.jpg
def download_image(data):
    filename = os.path.join(out_dir + '/new', '{}_{}.jpg'.format(data[0], data[1]))
    url = data[2]

    exists = os.path.exists(filename)
    if exists:
        # print('Image {} already exists. Skipping download.'.format(filename))
        return
    
    try:
        response = request.urlopen(url, timeout=10)
        image_data = response.read()
    except:
        print('Warning: Could not download image {} from {}'.format(filename, url))
        return

    try:
        pil_image = Image.open(BytesIO(image_data))
    except:
        print('Warning: Failed to parse image {}'.format(filename))
        return

    try:
        pil_image_rgb = pil_image.convert('RGB')
    except:
        print('Warning: Failed to convert image {} to RGB'.format(filename))
        return

    try:
        pil_image_rgb.save(filename, format='JPEG', quality=90)
    except:
        print('Warning: Failed to save image {}'.format(filename))
        return

dataset = []
with open('datasets/multimedia.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            row[2] = row[2].replace('/', '_')
            data = [row[0], row[2], row[5]]
            dataset.append(data)
            #### 
            if line_count==500000: #
                break
            line_count += 1
    print(f'Processed {line_count} lines.')

# _id, license, title, format, rightsHolder, identifier, type
# ['6612585', 'http://creativecommons.org/licenses/by/4.0/', 'Melitta_trimmerana-NHMUK010264804-syntype-female-dorsal_habitus-1', 'image/jpeg', 'The Trustees of the Natural History Museum, London', 'https://www.nhm.ac.uk/services/media-store/asset/68cd474b951593218fe18b6cfa39950d51d78fa8/contents/preview', 'StillImage']


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=16)  # Num of CPUs
    for _ in tqdm.tqdm(pool.imap_unordered(download_image, dataset), total=len(dataset)):
        pass
    # pool.map(download_image, dataset)
    # pool.close()
    # pool.terminate()



