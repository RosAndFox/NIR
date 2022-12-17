import math
import cv2
import os
working_dir = "C:/Users/Ros/Магистратура/NIR/dataset/"
out_dir = "C:/Users/Ros/Магистратура/NIR/dataset/NIR/Decrease2/"
f = open(working_dir+'coco_few_data_train.json')
fnew=open(out_dir+'dectrain.txt', 'w')
j=0
file_id=0
fnew.write('{"images": [')
line=f.read();
while line.find('"file_name":')>-1:
        fnew.write('{"file_name": "') 
        i=line.find('"file_name":')+14
        file_name=''
        while line[i]!='"':
            file_name+=line[i]
            i+=1
        img=cv2.imread(working_dir+file_name, cv2.IMREAD_UNCHANGED)
        #cv2.imshow("Img", img)
        fnew.write(file_name+'", "id": '+str(file_id)+', "width": ')
        file_id+=1
        height=0
        width=0
        i=line.find('"width": ')+9
        while line[i]<='9' and line[i]>='0':
            width=width*10+ord(line[i])-ord('0')
            i+=1
        width=width//2
        i=line.find('"height": ')+10
        while line[i]<='9' and line[i]>='0':
            height=height*10+ord(line[i])-ord('0')
            i+=1
        height=height//2
        dim=(width, height)
        #resized=cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        #cv2.imwrite(out_dir+file_name, resized)
        i=line.find('}')
        fnew.write(str(width)+', "height": '+str(height))
        if line[i+1]!=']':
            fnew.write('}, ')
        line=line[i+1:]
fnew.write('}], "categories": [{')
i=line.find('"supercategory"')
j=line.find('{"segmentation"')
fnew.write(line[i:j-1])
line=line[j-1:]
x=-1
flag=0
i=0
while i<len(line):
    sym=line[i]
    if sym>='0' and sym<='9' and flag>0:
        x=x*10+ord(sym)-ord('0')
        if line[i+1]<'0' or line[i+1]>'9':
            if flag==1:
                fnew.write(str(x//2))
            if flag==2:
                fnew.write(str(x//4))
            x=0
    else:
        if sym==']':
            flag=2
        if sym=='[':
            flag=1
        if sym=='_':
            flag=0
        fnew.write(sym)
    i+=1
f.close()
fnew.close()

