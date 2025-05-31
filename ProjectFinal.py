from google_images_search import GoogleImagesSearch
from PIL import Image
import numpy as np
import random

creds=GoogleImagesSearch(
    '', #API dev key
    '', #Project CX
)

query=input("Enter Search Query: ")
filepath=[]
imgdata=[]
markmatr=np.matrix([[0,0],[0,0]],dtype=float)
width=50
height=50
newimg=Image.new('RGB',(width,height))
newimgdata=[]

searchparams={
    'q':query,
    'num':20,
    'fileType':'jpg',
    'imgType':'clipart',
    'imgColorType':'mono'
}

creds.search(search_params=searchparams)
for img in creds.results():
    img.download('C:/Users/Maxwell Chen/Pictures/temp')
    img.resize(width,height)
    filepath.append(img.path)

'''
im=Image.open(filepath[0])
width, height = im.size
print(list(im.getdata()))
print(str(width)+" "+str(height))

imag = Image.new('RGB', (width, height))
imag.putdata(list(im.getdata()))
imag.show()
'''

blacktotal=0.0
whitetotal=0.0
bwillblack=0.0
bwillwhite=0.0
wwillblack=0.0
wwillwhite=0.0

def randbw(x):
    global blacktotal,whitetotal,bwillblack,bwillwhite,wwillblack,wwillwhite

    if x==0:
        rand=random.randint(0,1)
        if rand==1:
            wwillwhite+=1
        if rand==0:
            wwillblack+=1
    if x==1:
        rand=random.randint(0,1)
        if rand==1:
            bwillwhite+=1
        if rand==0:
            bwillblack+=1
    if x==2:
        rand=random.randint(0,1)
        if rand==1:
            whitetotal+=1
            rand=random.randint(0,1)
            if rand==1:
                wwillwhite+=1
            if rand==0:
                wwillblack+=1
        if rand==0:
            blacktotal+=1
            rand=random.randint(0,1)
            if rand==1:
                bwillwhite+=1
            if rand==0:
                bwillblack+=1

for loop in range(width*height):
    if loop==(width*height)-1:
        break

    blacktotal=0.0
    whitetotal=0.0
    bwillblack=0.0
    bwillwhite=0.0
    wwillblack=0.0
    wwillwhite=0.0

    if loop!=0:
        for iter in filepath:
            im=Image.open(iter)
            imgdata=list(im.getdata())
            if imgdata[loop-1]==(255,255,255,255):
                whitetotal+=1
                if imgdata[loop]==(255,255,255,255):
                    wwillwhite+=1
                if imgdata[loop]==(0,0,0,255):
                    wwillblack+=1
                if (imgdata[loop]!=(0,0,0,255))and(imgdata[loop]!=(255,255,255,255)):
                    randbw(0)
            if imgdata[loop-1]==(0,0,0,255):
                blacktotal+=1
                if imgdata[loop]==(255,255,255,255):
                    bwillwhite+=1
                if imgdata[loop]==(0,0,0,255):
                    bwillblack+=1
                if (imgdata[loop]!=(0,0,0,255))and(imgdata[loop]!=(255,255,255,255)):
                    randbw(1)
            if (imgdata[loop-1]!=(0,0,0,255))and(imgdata[loop-1]!=(255,255,255,255)):
                randbw(2)

    #creating markov matrix for the pixel
    try:
        markmatr[0,0]=bwillblack/blacktotal
    except ZeroDivisionError:
        markmatr[0,0]=0
    try:
        markmatr[1,0]=bwillwhite/blacktotal
    except ZeroDivisionError:
        markmatr[1,0]=0
    try:
        markmatr[0,1]=wwillblack/whitetotal
    except ZeroDivisionError:
        markmatr[0,1]=0
    try:
        markmatr[1,1]=wwillwhite/whitetotal
    except ZeroDivisionError:
        markmatr[1,1]=0

    if loop==0:
        for iter in filepath:
            im=Image.open(iter)
            imgdata=list(im.getdata())
            if imgdata[loop]==(255,255,255,255):
                whitetotal+=1
            if imgdata[loop]==(0,0,0,255):
                blacktotal+=1
        if blacktotal>whitetotal:
            newimgdata.append((0,0,0,255))
        if blacktotal<whitetotal:
            newimgdata.append((255,255,255,255))

    if loop!=0:
        if newimgdata[loop-1]==(255,255,255,255):
            bwprob=np.matmul(markmatr,[[1],[0]],dtype=float)
            rand=random.randint(0,100)
            if rand<=(bwprob[0,0]*100):
                newimgdata.append((255,255,255,255))
            if rand>(bwprob[0,0]*100):
                newimgdata.append((0,0,0,255))
        if newimgdata[loop-1]==(0,0,0,255):
            bwprob=np.matmul(markmatr,[[0],[1]],dtype=float)
            rand=random.randint(0,100)
            if rand<=(bwprob[1,0]*100):
                newimgdata.append((255,255,255,255))
            if rand>(bwprob[1,0]*100):
                newimgdata.append((0,0,0,255))
    print(loop)
newimg.putdata(newimgdata)
newimg.show()