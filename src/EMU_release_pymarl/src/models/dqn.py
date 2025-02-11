import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self,input_shape,n_actions):
        super(DQN,self).__init__()
        self.conv=nn.Sequential(
        nn.Conv2d(input_shape[0],32,8,stride= 4),
        nn.ReLU(),
        nn.Conv2d(32,64,4,stride=2),
        nn.ReLU(),
        nn.Conv2d(64,64,3,stride=1),
        nn.ReLU(),
        )
    
        conv_out_size=self._get_conv_out(input_shape)
        
        self.fc=nn.Sequential(
            nn.Linear(conv_out_size+512,512),
            nn.ReLU(),
            nn.Linear(512,n_actions),                  
            )

    def _get_conv_out(self,shape):
        o=self.conv(torch.zeros(1,*shape))
        return int(torch.prod(torch.tensor(o.size())))
    
    def forward(self,x, memory):
        conv_out= self.conv(x).view(x.size()[0],-1)
        return self.fc(torch.cat([conv_out,memory],dim=1))
