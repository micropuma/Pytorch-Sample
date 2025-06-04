import torch
import torch.nn as nn
from torchvision.models import resnet

# dynamo支持动态图捕获
import torch._dynamo
# pytorch提供的benchmark module
import torch.utils.benchmark as benchmark

device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
print(device)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(32, 64)

    def forward(self, x):
        x = self.fc1(x)
        x = torch.nn.functional.relu(x)
        return x

model = MLP()
input = torch.randn(8, 32)       # batchsize是8，特征维度是32

torch._dynamo.reset() # Only needed if you call this cell repeatedly
compiled_model = torch.compile(model)

# Alternatively you can also pass the backend
compiled_model = torch.compile(model, backend='inductor')  # 指定后端编译

output = model(input)
# triggers compilation of forward graph on the first run
# 编译后模型推理
output_compiled = compiled_model(input)

torch.all(output == output_compiled)

# ================================================= bench mark ===========================================
def run_batch_inference(model, batch=1):
    x = torch.randn(batch, 3, 224, 224).to(device)
    model(x)

def run_batch_train(model, optimizer, batch=16):
    x = torch.randn(batch, 3, 224, 224).to(device)
    optimizer.zero_grad()
    out = model(x)
    out.sum().backward()
    optimizer.step()
    
# benchmark resnet18
model = resnet.resnet18(weights=resnet.ResNet18_Weights.IMAGENET1K_V1).to(device)

batch = 16
torch._dynamo.reset()
compiled_model = torch.compile(model)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

t_model = benchmark.Timer(
    stmt='run_batch_train(model, optimizer, batch)',
    setup='from __main__ import run_batch_train',
    globals={'model': model,'optimizer':optimizer, 'batch':batch})

t_compiled_model = benchmark.Timer(
    stmt='run_batch_train(model, optimizer, batch)',
    setup='from __main__ import run_batch_train',
    globals={'model': compiled_model, 'optimizer':optimizer, 'batch':batch})

t_model_runs = t_model.timeit(100)
t_compiled_model_runs = t_compiled_model.timeit(100)

print(t_model_runs)
print(t_compiled_model_runs)

print(f"\nResnet18 Training speedup: {100*(t_model_runs.mean - t_compiled_model_runs.mean) / t_model_runs.mean: .2f}%")
