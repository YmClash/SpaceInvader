import torch
import torch.nn as nn
import torch.optim as optim
from icecream import ic

class LiquidNeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LiquidNeuralNetwork, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        #creation des couches
        # self.output_layer = nn.Linear(self.hidden_size, self.output_size)
        self.hidden_layers = nn.ModuleList([nn.Linear(self.input_size if i == 0 else self.hidden_size, self.hidden_size) for i in range(5)])

        self.output_layer = nn.Linear(self.hidden_size,self.output_size)

    def forward(self,x):
        print(x.shape)
        x = x.view(x.size(0),-1)
        # x = torch.relu(self.input_layer(x))
        for hidden_layer in self.hidden_layers:
            x = torch.relu(hidden_layer(x))

        output = torch.sigmoid(self.output_layer(x))
        return output.view(x.size(0),1,7,7)

#paramettre  de notre reseau
input_size = 28*28
output_size = 7*7
hidden_size =  256 #int((input_size + output_size) / 2)
print(hidden_size)


lucie = LiquidNeuralNetwork(input_size,hidden_size,output_size)

input_data = (torch.randn(1000, input_size))
target_data = torch.randn(1000,1,7,7)

perte = nn.MSELoss()

optimizer = optim.Adam(lucie.parameters(),lr=0.001)


print("Input DATA:")
print(f'Input Size: {input_size}')
print(f'Hidden Size: {hidden_size}')
print(f'Output Size: {output_size}')

print(input_data)
output = lucie(input_data)

num_epochs = 100
batch_size = 32

for epoch in range(num_epochs):
    for i in range(0,len(input_data),batch_size):
        inputs = input_data[i:i+batch_size]
        targets = target_data[i:i+batch_size, :, :, :]

        #gradient   et   post propagation
        optimizer.zero_grad()
        outputs = lucie(inputs)

        loss = perte(outputs,targets)

        #retropropagation
        loss.backward()

        #mise a  jour des parametre
        optimizer.step()

        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')








print(f'Output Shape:{output.shape}')
print(output)
