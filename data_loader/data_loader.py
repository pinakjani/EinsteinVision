import torch
import math
from torch.utils.data import DataLoader
from torch.utils.data import get_worker_info
from mmcv.parallel import collate
from functools import partial


def worker_init_fn(worker_id):
    worker_info = get_worker_info()
    dataset = worker_info.dataset  # the dataset copy in this worker process
    overall_start = dataset.start
    overall_end = dataset.end
    # configure the dataset to only process the split workload
    per_worker = int(math.ceil((overall_end - overall_start) / float(worker_info.num_workers)))
    dataset.start = overall_start + worker_id * per_worker
    dataset.end = min(dataset.start + per_worker, overall_end)

def build_dataloader(dataset, num_workers, batch_size, num_gpu=1):

    samples_per_gpu = batch_size // num_gpu
    return DataLoader(
                        dataset,
                        batch_size=batch_size,
                        shuffle=False,
                        num_workers=num_workers,
                        pin_memory=False,
                        drop_last=False,
                        collate_fn=partial(collate, samples_per_gpu=samples_per_gpu),
                        worker_init_fn=worker_init_fn)