from torch.utils.data import Dataset
import numpy as np

class MFDataset(Dataset):
    def __init__(self, ratings):

        self.users = np.array(ratings['User-ID'])
        self.items = np.array(ratings['ISBN'])

        self.target = np.clip(ratings['Book-Rating'], 0, 1)


    def __len__(self):
        return len(self.users)

    def __getitem__(self, j):
        return (self.users[j], self.items[j]), self.target[j]