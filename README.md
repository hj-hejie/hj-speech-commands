/home/hejie/workspace/pytorch-speech-commands/datasets/speech_commands_dataset.py:69: RuntimeWarning: divide by zero encountered in true_divide
  weight_per_class = N / count
  0%|          | 0/480 [00:00<?, ?audios/s]use_gpu False
training vgg19_bn for Google speech commands...
epoch   0 with lr=1.00e-02
Traceback (most recent call last):
  File "train_speech_commands.py", line 279, in <module>
    train(epoch)
  File "train_speech_commands.py", line 163, in train
    outputs = model(inputs)
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 477, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/hejie/workspace/pytorch-speech-commands/models/vgg.py", line 49, in forward
    x = self.features(x)
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 477, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/nn/modules/container.py", line 91, in forward
    input = module(input)
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 477, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/nn/modules/pooling.py", line 142, in forward
    self.return_indices)
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/nn/functional.py", line 396, in max_pool2d
    ret = torch._C._nn.max_pool2d_with_indices(input, kernel_size, stride, padding, dilation, ceil_mode)
RuntimeError: Given input size: (64x32x1). Calculated output size: (64x16x0). Output size is too small at /pytorch/aten/src/THNN/generic/SpatialDilatedMaxPooling.c:67

((1+2*0-1*(2-1)-1+0)/2+1)=0.5
