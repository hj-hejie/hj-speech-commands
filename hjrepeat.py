import os

dataset='datasets/speech_commands/'

for dir in os.listdir(dataset):
    dir2=os.path.join(dataset, dir)
    for dir3 in os.listdir(dir2):
        dir4=os.path.join(dir2, dir3)
        if dir3 != '_background_noise_':
            for file in os.listdir(dir4):
                for i in range(2000):
                    print os.path.join('.', file)+'-->'+os.path.join(dir4, 's'+str(i)+file)
                    os.symlink(os.path.join('.', file), os.path.join(dir4, 's'+str(i)+file))

