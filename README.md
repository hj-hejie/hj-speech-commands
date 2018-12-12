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

T outputSize = ((inputSize + 2 * pad - dilation * (kernelSize - 1) - 1 + (ceil_mode ? stride - 1 : 0)) / stride + 1);
  0%|          | 0/480 [00:00<?, ?audios/s]use_gpu False
training vgg19_bn for Google speech commands...
epoch   0 with lr=1.00e-02
Exception ignored in: <bound method _DataLoaderIter.__del__ of <torch.utils.data.dataloader._DataLoaderIter object at 0x7f26716c9208>>
Traceback (most recent call last):
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/utils/data/dataloader.py", line 399, in __del__
    self._shutdown_workers()
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/utils/data/dataloader.py", line 378, in _shutdown_workers
    self.worker_result_queue.get()
  File "/usr/lib/python3.6/multiprocessing/queues.py", line 337, in get
    return _ForkingPickler.loads(res)
  File "/home/hejie/.local/lib/python3.6/site-packages/torch/multiprocessing/reductions.py", line 151, in rebuild_storage_fd
    fd = df.detach()
  File "/usr/lib/python3.6/multiprocessing/resource_sharer.py", line 58, in detach
    return reduction.recv_handle(conn)
  File "/usr/lib/python3.6/multiprocessing/reduction.py", line 182, in recv_handle
    return recvfds(s, 1)[0]
  File "/usr/lib/python3.6/multiprocessing/reduction.py", line 153, in recvfds
    msg, ancdata, flags, addr = sock.recvmsg(1, socket.CMSG_LEN(bytes_size))
ConnectionResetError: [Errno 104] Connection reset by peer
Traceback (most recent call last):
  File "train_speech_commands.py", line 276, in <module>
    train(epoch)
  File "train_speech_commands.py", line 160, in train
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
RuntimeError: Given input size: (512x1x5). Calculated output size: (512x0x2). Output size is too small at /pytorch/aten/src/THNN/generic/SpatialDilatedMaxPooling.c:67
