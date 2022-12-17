from PIL import Image
import os
working_dir = r'C:/Users/Ros/Магистратура/NIR/dataset/'
out_dir = r'C:/Users/Ros/Магистратура/NIR/dataset/NIR/Final'
f = open(working_dir+'coco_few_data_train.json')
fnew=open(out_dir+'newtrain.json', 'w')
file_id=0
arr=[]
j=0
point0=0
point1=0
point2=0
point3=0
fnew.write('{"images": [')
line=f.read();
while line.find('"file_name":')>-1: 
        i=line.find('"file_name":')+14
        file_name=''
        while line[i]!='"':
            file_name+=line[i]
            i+=1
        arr.append(file_name)
        i=line.find('}')
        line=line[i+1:]
cat=', "categories": [{'
i=line.find('"supercategory"')
j=line.find('{"segmentation"')
cat+=line[i:j-1]
line=line[j-1:]
arr_segm=[]
segm=[]
arr_area=[]
s=''
arr_bbox=[]
bbox=[]
arr_im=[]
arr_cat=[]
i=0
while line.find('"segmentation":')>-1:
    i=line.find('[[')+2
    segm=[]
    bbox=[]
    coord=0
    while line[i-1]!=']':
        while line[i]<='9' and line[i]>='0':
            coord=coord*10+ord(line[i])-ord('0')
            i+=1
        segm.append(coord)
        coord=0
        i+=2
    arr_segm.append(segm)
    s=''
    i+=10
    while line[i]!=',':
        s+=line[i]
        i+=1
    arr_area.append(s)
    i+=11
    while line[i-2]!=']':
        while line[i]<='9' and line[i]>='0':
            coord=coord*10+ord(line[i])-ord('0')
            i+=1
        bbox.append(coord)
        coord=0
        i+=2
    arr_bbox.append(bbox)
    i+=13
    while line[i]<='9' and line[i]>='0':
            coord=coord*10+ord(line[i])-ord('0')
            i+=1
    arr_im.append(coord)
    coord=0
    i+=17
    while line[i]<='9' and line[i]>='0':
            coord=coord*10+ord(line[i])-ord('0')
            i+=1
    arr_cat.append(coord)
    i=line.find('}')
    line=line[i+1:]
i=0
arr_new=[]
x=[]
y=[]
width=[]
height=[]
new_j=[]
while arr_cat[i]!=8 and arr_cat[i]!=10 and arr_cat[i]!=5 and i<len(arr_im):
    i+=1
fnew.write('{"file_name": "'+arr[arr_im[i]]+'", "id": '+str(0)+', "width": '+str(arr_bbox[i][2])+', "height": '+str(arr_bbox[i][3])+'}')
arr_new.append(arr_im[i])
x.append(arr_bbox[i][0])
y.append(arr_bbox[i][1])
width.append(arr_bbox[i][2])
height.append(arr_bbox[i][3])
seg='{"segmentation": [['
seg+=str(arr_segm[i][0]-x[0])
j=1
while j<len(arr_segm[i]):
                    seg+=', '
                    if j%2==0:
                        seg+=str(arr_segm[i][j]-x[0])
                    else:
                        seg+=str(arr_segm[i][j]-y[0])
                    j+=1
seg+=']], "area": '+arr_area[i]+', "bbox": ['
seg+=str(arr_bbox[i][0]-x[0])+', '+str(arr_bbox[i][1]-y[0])+', '+str(arr_bbox[i][2])+', '+str(arr_bbox[i][3])+'], "image_id": '+str(0)+', "category_id": '+str(arr_cat[i])
seg+=', "id": 0, "iscrowd": 0}'
arr_ann=[]
arr_ann.append(seg)
id_new=1
sym="a"
new_j.append(0)
os.chdir(working_dir)
im=Image.open(arr[arr_im[i]])
im_crop=im.crop((arr_bbox[i][0], arr_bbox[i][1], arr_bbox[i][0]+arr_bbox[i][2], arr_bbox[i][1]+arr_bbox[i][3]))
os.chdir(out_dir)
im_crop.save(arr[arr_im[i]], quality=95)
i+=1
while i<len(arr_im):
    if arr_cat[i]==8 or arr_cat[i]==10 or arr_cat[i]==5:
        if arr_im[i]==arr_new[id_new-1]:
            newname=arr[arr_im[i]][:len(arr[arr_im[i]])-4]+sym+arr[arr_im[i]][len(arr[arr_im[i]])-4:]
            sym=chr(ord(sym)+1)
        else:
            sym="a"
            newname=arr[arr_im[i]]
        fnew.write(', {"file_name": "'+newname+'", "id": '+str(id_new)+', "width": '+str(arr_bbox[i][2])+', "height": '+str(arr_bbox[i][3])+'}')
        arr_new.append(arr_im[i])
        x.append(arr_bbox[i][0])
        y.append(arr_bbox[i][1])
        width.append(arr_bbox[i][2])
        height.append(arr_bbox[i][3])
        seg='{"segmentation": [['
        seg+=str(arr_segm[i][0]-x[id_new])
        j=1
        while j<len(arr_segm[i]):
                    seg+=', '
                    if j%2==0:
                        seg+=str(arr_segm[i][j]-x[id_new])
                    else:
                        seg+=str(arr_segm[i][j]-y[id_new])
                    j+=1
        seg+=']], "area": '+arr_area[i]+', "bbox": ['
        seg+=str(arr_bbox[i][0]-x[id_new])+', '+str(arr_bbox[i][1]-y[id_new])+', '+str(arr_bbox[i][2])+', '+str(arr_bbox[i][3])+'], "image_id": '+str(id_new)+', "category_id": '+str(arr_cat[i])
        seg+=', "id": '+str(id_new)+'000, "iscrowd": 0}'
        arr_ann.append(seg)
        new_j.append(0)
        id_new+=1
        os.chdir(working_dir)
        im=Image.open(arr[arr_im[i]])
        im_crop=im.crop((arr_bbox[i][0], arr_bbox[i][1], arr_bbox[i][0]+arr_bbox[i][2], arr_bbox[i][1]+arr_bbox[i][3]))
        os.chdir(out_dir)
        im_crop.save(newname, quality=95)
    i+=1
fnew.write(']')
fnew.write(cat+'[')
i=0
cat=''
while i<len(arr_im):
    if arr_cat[i]==1 or arr_cat[i]==6 or arr_cat[i]==9:
        id_new=0
        while arr_im[i]>arr_new[id_new]:
            id_new+=1
        while id_new<len(arr_new) and arr_im[i]==arr_new[id_new]:
            if x[id_new]<=arr_bbox[i][0] and y[id_new]<=arr_bbox[i][1] and width[id_new] + x[id_new]>= arr_bbox[i][2]+arr_bbox[i][0] and y[id_new]+height[id_new]>=arr_bbox[i][1]+arr_bbox[i][3]:
                new_j[id_new]+=1
                cat=', {"segmentation": [['
                cat+=str(arr_segm[i][0]-x[id_new])
                j=1
                while j<len(arr_segm[i]):
                    cat+=', '
                    if j%2==0:
                        cat+=str(arr_segm[i][j]-x[id_new])
                    else:
                        cat+=str(arr_segm[i][j]-y[id_new])
                    j+=1
                cat+=']], "area": '+arr_area[i]+', "bbox": ['
                cat+=str(arr_bbox[i][0]-x[id_new])+', '+str(arr_bbox[i][1]-y[id_new])+', '+str(arr_bbox[i][2])+', '+str(arr_bbox[i][3])+'], "image_id": '+str(id_new)+', "category_id": '+str(arr_cat[i])
                if id_new!=0:
                    cat+=', "id": '+str(id_new)+'00'+str(new_j[id_new])+', "iscrowd": 0}'
                else:
                    cat+=', "id": '+str(new_j[id_new])+', "iscrowd": 0}'
                arr_ann[id_new]+=cat
            id_new+=1
    i+=1
i=1
fnew.write(arr_ann[0])
while i<len(arr_ann):
    fnew.write(', '+arr_ann[i])
    i+=1
fnew.write(']}')
f.close()
fnew.close()