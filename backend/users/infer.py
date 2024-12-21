from collections import defaultdict
import torch
import pickle

import numpy as np
import torch

from .preprocessing import SimpleEncoder
from .mf import MatrixFactorization, ALS
from .dataset import MFDataset
from .utils import slc

def load_model(path2model):
    with open(path2model, 'rb') as f:
        mf = pickle.load(f)
    return mf

def load_encoder(path2encoder):
    with open(path2encoder, 'rb') as f:
        encoder = pickle.load(f)
    return encoder

def load_decoder(path2encoder):
    with open(path2encoder, 'rb') as f:
        encoder = pickle.load(f)
    return encoder

def get_result_user(isbns, items, encoder, decoder):
    model = MatrixFactorization(1, 271360, 32)
    model.items = items
    rating_ = defaultdict(list)
    isbn = [encoder[i] for i in isbns]
    num_user = model.users.shape[0]
    for i in isbn:

        rating_["User-ID"].append(num_user)
        rating_["ISBN"].append(i)
        rating_["Book-Rating"].append(1)
    
    als = ALS(1)
    test_dataset = MFDataset(rating_)
    infer_loader = torch.utils.data.DataLoader(test_dataset, batch_size=256, shuffle=True)
    optimizer = torch.optim.SGD(params=model.parameters(), lr=1e-1)
    als.finetrain(1, model, infer_loader, 1000, optimizer)
    result = [decoder[i] for i in (torch.argsort((model.users[-1]*model.items).sum(dim=-1))[-3:].detach().numpy().tolist())]
    
    
    return result


"""from collections import defaultdict
import torch
import pickle
#import numpy as np
#import torch

from .preprocessing import SimpleEncoder
from .mf import MatrixFactorization, ALS
from .dataset import MFDataset
from .utils import slc

def load_model(path2model):
    with open(path2model, 'rb') as f:
        model = pickle.load(f)
    return model

def load_encoder(path2encoder):
    with open(path2encoder, 'rb') as f:
        encoder = pickle.load(f)
    return encoder

def get_result_user(isbns, model, encoder):
    model.add_user(1)
    rating_ = defaultdict(list)
    num_user = model.users.shape[0]
    for i in isbns:

        rating_["User-ID"].append(num_user)
        rating_["ISBN"].append(i)
        rating_["Book-Rating"].append(1)
    als = ALS(1)
    test_dataset = MFDataset(rating_)
    infer_loader = torch.utils.data.DataLoader(test_dataset, batch_size=256, shuffle=True)
    optimizer = torch.optim.SGD(params=model.parameters(), lr=1e-1)
    als.finetrain(1, model, infer_loader, 200, optimizer)
    result = [encoder[i] for i in (torch.argsort((model.users[-1]*model.items).sum(dim=-1))[-3:].detach().numpy().tolist())]
    return result"""