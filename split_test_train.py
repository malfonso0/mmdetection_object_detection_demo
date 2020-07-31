import random
import os

files= os.listdir("data/VOC2007/Annotations")

files = [os.path.splitext(file)[0] for file in files]
random.shuffle(files)


train_perc = .8

thres = int(len(files) * train_perc)
train=files[:thres]
test=files[thres+1:]

outfolder = "data/VOC2007/ImageSets/Main"
with open(os.path.join(outfolder, 'test.txt'), "w") as f:
    f.write('\n'.join(test))
with open(os.path.join(outfolder, 'trainval.txt'), "w") as f:
    f.write('\n'.join(train))
