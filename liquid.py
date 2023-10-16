import torch
import torch.nn as nn
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
        # x = torch.relu(self.input_layer(x))
        for hidden_layer in self.hidden_layers:
            x = torch.relu(hidden_layer(x))

        output = self.output_layer(x)
        return output


#paramettre  de notre reseau
input_size = 10
hidden_size = 20
output_size = 5

lucie = LiquidNeuralNetwork(input_size,hidden_size,output_size)

input_data = (torch.randn(1, input_size))
print("Input DATA:")
print(input_data)

output = lucie(input_data)


print(output)
