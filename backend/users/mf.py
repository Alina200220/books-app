import numpy as np
import torch
import torch.nn as nn
#from tqdm.notebook import tqdm
from IPython.display import clear_output
import matplotlib.pyplot as plt


class MatrixFactorization(nn.Module):

    def __init__(self, n_items, n_users, embed_size):
        super().__init__()

        self.items = nn.Parameter(torch.randn((n_items, embed_size)), requires_grad=True)
        self.users = nn.Parameter(torch.randn((n_users, embed_size)), requires_grad=True)
        self.n_items = n_items
        self.n_users = n_users

    def forward(self, u, i):
                   
        return (self.items[i] * self.users[u]).sum(dim=-1)
            
    def add_user(self, n_new):        
        new_users = torch.randn((n_new, 32), requires_grad=True)
        all_users = torch.cat([self.users, new_users], dim=0)        
        # Assign the concatenated tensor back as a nn.Parameter        
        self.users = nn.Parameter(all_users, requires_grad=True)


class ALS(nn.Module):

    def __init__(self, alpha):
        self.alpha = alpha


    def one_epoch(self, model, optimizer, dataloader):
        losses = []
        for x, target in dataloader:
            optimizer.zero_grad()
            u, i = x
            outputs = model(u, i)
            loss = (-self.alpha*target*torch.log(torch.sigmoid(outputs)) - (1-target)*torch.log(torch.sigmoid(1-outputs))).mean()
            losses.append(loss.item())
            loss.backward()
            optimizer.step()

        return losses

    def evaluate(self, model, dataloader):
        losses = []
        for x, target in dataloader:
            with torch.no_grad():
                u, i = x
                outputs = model(u, i)
                loss = (-self.alpha*target*torch.log(torch.sigmoid(outputs)) - (1-target)*torch.log(torch.sigmoid(1-outputs))).mean()
                losses.append(loss.item())
        return losses
        

    def train(self, train_dataloader, test_dataloader, model, optimizer, n_epochs):
        losses_epochs_train = []
        losses_epochs_test = []
        for i in range(n_epochs):
            model.users.requires_grad = False
            model.items.requires_grad = True
            self.one_epoch(model, optimizer, train_dataloader)
    
            model.users.requires_grad = True
            model.items.requires_grad = False
            losses_train = self.one_epoch(model, optimizer, train_dataloader)
            losses_epochs_train.append(np.mean(losses_train))
            print(f'losses train: {np.mean(losses_train)}')
            losses_test = self.evaluate(model, test_dataloader)
            losses_epochs_test.append(np.mean(losses_test))
            print(f'losses test: {np.mean(losses_test)}')
            self.plot_losses(losses_epochs_train, losses_epochs_test)

        


    def finetrain(self, n_new, model, dataloader, n_epochs, optimizer):

        users_finetrain = torch.arange(model.n_users, model.n_users+n_new)
        model.add_user(n_new)

        model.users.requires_grad = True
        model.items.requires_grad = False

        for _ in range(n_epochs):
            self.one_epoch(model, optimizer, dataloader)


    def plot_losses(self, losses_train, losses_test):
        clear_output()
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
        axes[0].plot(losses_train)
        axes[1].plot(losses_test)

        axes[0].set_title('losses train')
        axes[1].set_title('losses test')
        plt.show()







            

