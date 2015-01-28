#!/usr/bin/env python
"""
This will create train and test txt files and a directory named images in flickr_likes parent directory, 
where all the folders exist. Then, run following commands to copy all files into the images directory
# find ./ -name '*.jpg' -exec cp '{}' ./ \; To copy all images in subdirectories into the parent directory
# mv *.jpg images/
"""
import os
import urllib
import hashlib
import argparse
import numpy as np
import pandas as pd
import multiprocessing

# Flickr returns a special image if the request is unavailable.
MISSING_IMAGE_SHA1 = '6a92790b1c2a301c6e7ddef645dca1f53ea97ac2'

example_dirname = os.path.abspath('/home/sharathc001/caffe-master/data/flickr_likes/')
caffe_dirname = os.path.abspath(os.path.join(example_dirname, '../..'))
training_dirname = os.path.abspath('/home/sharathc001/caffe-master/data/flickr_likes/')


def download_image(args_tuple):
    "For use with multiprocessing map. Returns filename on fail."
    try:
        url, filename = args_tuple
        if not os.path.exists(filename):
            urllib.urlretrieve(url, filename)
        with open(filename) as f:
            assert hashlib.sha1(f.read()).hexdigest() != MISSING_IMAGE_SHA1
        return True
    except KeyboardInterrupt:
        raise Exception()  # multiprocessing doesn't catch keyboard exceptions
    except:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download a subset of Flickr Style to a directory')
    parser.add_argument(
        '-s', '--seed', type=int, default=0,
        help="random seed")
    parser.add_argument(
        '-i', '--images', type=int, default=-1,
        help="number of images to use (-1 for all [default])",
    )
    parser.add_argument(
        '-w', '--workers', type=int, default=-1,
        help="num workers used to download images. -x uses (all - x) cores [-1 default]."
    )

    args = parser.parse_args()
    np.random.seed(args.seed)

    # Read data, shuffle order, and subsample.
    csv_filename = os.path.join(example_dirname, 'psychoflickr_originalset_output.csv')
    df = pd.read_csv(csv_filename, index_col=0)
    df = df.iloc[np.random.permutation(df.shape[0])]

    # Make directory for images and get local filenames.
    if training_dirname is None:
        training_dirname = os.path.join(caffe_dirname, 'data/flickr_style')
    images_dirname = os.path.join(training_dirname, 'images')
    if not os.path.exists(images_dirname):
        os.makedirs(images_dirname)
    df['image_filename'] = [os.path.join(images_dirname, _.split('/')[-1]) for _ in df['image_url']]

    # Only keep rows with valid images, and write out training file lists.
    for split in ['train', 'test']:
        split_df = df[df['_split'] == split]
        filename = os.path.join(training_dirname, '{}.txt'.format(split))
        split_df[['image_filename', 'label']].to_csv(filename, sep=' ', header=None, index=None)
    print('Writing train/val for {} successfully downloaded images.'.format(df.shape[0]))
