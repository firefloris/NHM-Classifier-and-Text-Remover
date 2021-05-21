import sys, os, multiprocessing, csv
import tqdm
from urllib import request, error
from PIL import Image
from io import BytesIO

"""
Originally made by dr. G. Spigler Tilburg Univeristy

This script takes in multimedia.csv, which contains
download folder, puts all of the names of the files inside  of the file 
"""


os.chdir('c:/Users/flori/OneDrive/Documents/Uni/8_Master_thesis/code')

out_dir = 'c:/Users/flori/download/original'

# column names from 'occurrence' that we wish to keep in the extracted dataset
labels_to_load = ['phylum', # always 'Arthropoda;  you can ignore this field
                  'class', # always 'Insecta';     you can ignore this field for now
                  'order', # e.g., Coleoptera
                  'family', # e.g., Carabidae
                  'genus', # e.g., Notiobia
                  'specificEpithet', # species!

                  'continent', # e.g., Australia (...) --> see how they are all called
                  'country', # e.g., Australia
                  'sex' ] # many insects have sexual dimorphism, so male and female specimens may look very different!

# - Other labels may be 'decimalLatitude', 'decimalLongitude' (but few samples have them)
# - 'higherClassification' has the full name, but sometimes it seems incomplete; it may be worth exploring
# - 'lifeStage' : adult, or pupa or etc?
# - 'subgenus' ?
# - a few samples have a 'waterBody', in case of acquatic insects

## TODO: 'dynamicProperties' contains some json with potentially useful data;  e.g., 'preservative':'dry - pinned' -> this is most likely an image of a specimen pinned down)

# Reference: classification of species, in descending order: 'Domain', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'
"""Originally made by dr. G. Spigler Tilburg Univeristy"""
# The dataset we use is only insects at the moment, which all have the same PHYLUM 'Arthropoda' and CLASS 'Insecta'


dataset = []
ids = {} # for fast check if id in 'occurrence.csv' exists within the downloaded data;  fast lookup of key, and access to list of all indices with that id
print("Listing downloaded files...")
with open('datasets/multimedia.csv', encoding='utf-8') as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count != 0:
            row[2] = row[2].replace('/', '_')
            data = [row[0], row[2], '{}_{}.jpg'.format(row[0], row[2])] # 'id', 'fullnam', 'url', 'filename' (inside out_dir)
            filename = data[2]

            if os.path.exists(os.path.join(out_dir, filename)):
                if data[0] in ids:
                    ids[data[0]].append(len(dataset))
                else:
                    ids[data[0]] = [len(dataset)]
                dataset.append(data)
        line_count += 1
print(len(dataset))
outf = open('datasets/dataset.csv', 'w')
out = csv.writer(outf)
out.writerow(['id', 'file_description', 'filename']+labels_to_load)


# Loop over the downloaded files (in dataset), and add attributes as required
column_names = []
print("Generating the dataset...")
with open('datasets/occurrence.csv', encoding='utf-8') as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0
    new_labels_indices = []

    for row in csv_reader:
        if line_count % 10000 == 0:
            print(line_count)

        if line_count == 0:
            column_names = row[:]
            new_labels_indices = [column_names.index(l) for l in labels_to_load]
        else:
            id_ = row[0]
            if id_ in ids:
                # id found
                new_labels = [row[k].lower() for k in new_labels_indices]
                all_matching_indices = ids[id_]
                for index in all_matching_indices:
                    # TODO: you may want to process dataset[index][1] which contains the description of the sample,
                    # e.g. Melitta_trimmerana-NHMUK010264804-syntype-female-dorsal_habitus-1
                    # to extract more information to remove samples that don't contain speciments: e.g., 'dorsal' is most likely always a view of the inspect;  'habitus' is a picture of a specimen (sometimes it's just "label" or "habitus_and_label", so looking for these keywords --always look at the dataset!-- may simplify your life quite a lot!).  Another example: some species have 'indet' as indeterminate, when the species is missing.
                    # The extra features can be added to 'new_row' below;  DO NOT add them to 'new_labels', as there may be many pictures for the same specimen, and they will have different characteristics (dorsal, head, label/no-label, etc...)
                    new_row = dataset[index] + new_labels
                    out.writerow(new_row)

        line_count += 1
outf.close()


