import random
lines= []


import os

files= os.listdir("data/VOC2007/Annotations")

files = [os.path.splitext(file)[0] for file in files]
random.shuffle(lines)


train_perc = .8

thres = int(len(lines) * train_perc)
train=lines[:thres]
test=lines[thres+1:]

outfolder = "data/VOC2007/ImageSets"
with open(os.path.join(outfolder, '/test.txt'), "w") as f:
    f.writelines(test)

with open(os.path.join(outfolder, 'trainval.txt'), "w") as f:
    f.writelines(train)
