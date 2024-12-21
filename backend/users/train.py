
import pandas as pd
import numpy as np
import torch
import pickle

from preprocessing import SimpleEncoder
from mf import MatrixFactorization, ALS
from dataset import MFDataset
from utils import slc

def process():
    books_pd = pd.read_csv('Books.csv')
    users_pd = pd.read_csv('Users.csv')
    ratings_pd = pd.read_csv('Ratings.csv')

    books = {k:books_pd[k].values for k in books_pd.columns}
    users = {k:users_pd[k].values for k in users_pd.columns}
    ratings = {k:ratings_pd[k].values for k in ratings_pd.columns}

    encoder_users = SimpleEncoder()
    encoder_books = SimpleEncoder()

    users['User-ID'] = encoder_users.fit_transform(users['User-ID'])
    books['ISBN'] = encoder_books.fit_transform(books['ISBN'])
    ratings['User-ID'] = encoder_users.transform(ratings['User-ID'])
    ratings['ISBN'] = encoder_books.transform(ratings['ISBN'])

    mf = MatrixFactorization( encoder_books.encoder_max,encoder_users.encoder_max, 32)

    optimizer = torch.optim.SGD(params=mf.parameters(), lr=1e-1)

    count = {}
    for u in ratings['User-ID']:
        count[u] = count.get(u, 0) + 1

    mask = []
    count_train = {}
    for u in ratings['User-ID']:

        if count_train.get(u, 0)/count[u] > 0.7:
            mask.append(False)
        else:
            mask.append(True)
        count_train[u] = count_train.get(u, 0) + 1
    mask = np.array(mask)
    ratings_train = slc(ratings, mask)
    ratings_test = slc(ratings, ~mask)
    train_dataset = MFDataset(slc(ratings_train, [u>0 and i>0 for u, i in zip(ratings_train['User-ID'], ratings_train['ISBN'])]))
    test_dataset = MFDataset(slc(ratings_test, [u>0 and i>0 for u, i in zip(ratings_test['User-ID'], ratings_test['ISBN'])]))
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=256, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=256, shuffle=True)
    als = ALS(1)
    als.train(train_loader,test_loader, mf, optimizer, 100)
    with open('encoder.pkl', 'wb') as file:
        pickle.dump(encoder_users.decoder, file)
    with open('mf.pkl', 'wb') as file:
        pickle.dump(mf, file)
    
if __name__ == '__main__':
    process()

