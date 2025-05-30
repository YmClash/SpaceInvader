import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module) :
    def __init__(self, input_size, hidden_size1,hidden_size2,hidden_size3, output_size) :
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size1)
        self.linear2 = nn.Linear(hidden_size1,hidden_size2)
        self.linear3 = nn.Linear(hidden_size2,hidden_size3)
        self.linear4 = nn.Linear(hidden_size3, output_size)

    def forward(self, x) :
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.relu(self.linear3(x))
        x = self.linear4(x)
        return x

    def save(self, file_name='model.pth') :
        model_folder_path = './model'
        if not os.path.exists(model_folder_path) :
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer :
    def __init__(self, model, lr, gamma) :
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        if torch.cuda.is_available() :
            self.model = self.model.cuda()
            self.criterion = self.criterion.cuda()



    def train_step(self, state, action, reward, next_state, done) :
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if torch.cuda.is_available():
            state = state.cuda()
            next_state = next_state.cuda()
            action = action.cuda()
            reward = reward.cuda()


        if len(state.shape) == 1 :
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)) :
            Q_new = reward[idx]
            if not done[idx] :
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()

    def save_model(self,filename='snake_model_weights.pth'):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'loss': self.criterion,
        }, filename)

    def load_model(self,filename='snake_model_weights.pth'):
        checkpoint = torch.load(filename)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.criterion = checkpoint['loss']