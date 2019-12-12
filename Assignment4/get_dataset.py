# coding=utf-8
# coding=utf-8

import os
import requests
import imghdr

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print(path+' was created successfully')
        return True
    else:
        print(path+' has existed')
        return False
 
train_path="./train"
test_path="./test"

mkdir(train_path)
mkdir(test_path)

set_url = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09428293"

lists = requests.get(set_url)

count =0
for i in lists.text.split('\n'):
    print(i)
    try:
        img = requests.get(i).content
        if imghdr.what(None, img) in ["jpeg", "png"]:
            if count >= 0 and count < 10000:
                with open(train_path+"/"+str(count)+".jpg", "wb") as f:
                    f.write(img)

            if count < 11000 and count >=10000:
                with open(test_path+"/"+str(count)+".jpg", "wb") as f:
                    f.write(img)

            if count >=11000:
                break

    except Exception as e:
        print(e)

    count = count + 1

