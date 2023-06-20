import os
import numpy as np
from torch.utils.data import Dataset
import cv2
import logging
import pickle as pkl
from mmcv.parallel import DataContainer as DC
import torch

class Tesla(Dataset):
    def __init__(self, data_root):
        self.logger = logging.getLogger(__name__)
        self.data_root = data_root
        # self.cfg = cfg
        self.load_annotations()
        self.start = 0
        self.end = len(self.data_infos)

    def __len__(self):
        return len(self.data_infos)
    
    def __getitem__(self, idx):
        data = self.data_infos[idx]
        img = cv2.imread(data['img_path'])
        # Cut the top part of the image to reduce the skyline
        img = img[270:, :, :]
        sample = {}
        sample.update({'img': img})
        resize = (800,320)
        sample['img'] = cv2.resize(sample['img'],
                                   resize,
                                   interpolation=cv2.INTER_CUBIC)
        sample['img'] = sample['img'].astype(np.float32) / 255.
        sample['img'] = torch.from_numpy(sample['img'])
        sample['img'] = sample['img'].permute(2, 0, 1)


        meta = {'full_img_path': data['img_path'],
                'img_name': data['img_name']}
        meta = DC(meta, cpu_only=True)
        sample.update({'meta': meta})
        return sample

    def load_annotations(self):
        self.logger.info('Loading Tesla annotations...')
        # Waiting for the dataset to load is tedious, let's cache it
        os.makedirs('cache', exist_ok=True)
        cache_path = 'cache/tesla_{}.pkl'.format('dataset')
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as cache_file:
                self.data_infos = pkl.load(cache_file)
                return

        self.data_infos = []
        for subdir, dirs, files in os.walk(self.data_root):
            for file in files:
                line = os.path.join(subdir, file)
                infos = self.load_annotation(line.split('/'))
                self.data_infos.append(infos)
        print("Data loaded")
        # cache data infos to file
        with open(cache_path, 'wb') as cache_file:
            pkl.dump(self.data_infos, cache_file)

    def load_annotation(self, line):
        infos = {}
        img_line = "{}/{}/{}".format(line[-3], line[-2], line[-1])
        img_path = os.path.join(self.data_root, img_line)
        infos['img_name'] = img_line
        infos['img_path'] = img_path
        return infos