import utils
import os
from telegraph import Telegraph
import telegraph
import ujson as json
from PIL import Image
from PIL import ImageFile
from shutil import copyfile
import pandas as pd
def upload_all(path,tlg_obj):
    print(path)
    if not os.path.exists(path):
        return
    path_lst = os.listdir(path)
    res_lst = [] #得到所有非文件夹图片
    for pth in path_lst:
        if os.path.isdir(path +'//'+pth):
            upload_all(path + '//'+pth,tlg_obj)
        else:
            if pth.split(".")[-1] in ["jpeg","png","jpg","bmp","webp"]:
                res_lst.append(pth)
    for i in range(len(res_lst)):
        res_lst[i] = path + "//"+res_lst[i]
    if res_lst:
        print("上传"+path.split("/")[-1])
        if len(res_lst)>40:
            res = tlg_obj.upload_file(res_lst[:40])
            for i in range(1,len(res_lst)//40 +1):
                res += tlg_obj.upload_file(res_lst[i*40:min((i+1)*40,len(res_lst))])
        else:
            res = tlg_obj.upload_file(res_lst)
        res = [i["src"] for i in res]
        cnt = utils.get_content(res)
        tmp = tlg_obj.create_page(title = path.split("/")[-1],html_content= cnt,return_content= False)["url"]
        link_list.append([path.split("/")[-1],tmp])
        print(path.split("/")[-1],len(res),len(res_lst),tmp)
if __name__ == "__main__":
    tlg_obj = utils.__init__account(short_name= 'myt10', author_name= 'myt10', author_url= 'https://github.com/myt10')
    print("continue")

    input_path = "input"
    output_path = "output"

    if not os.path.exists(input_path):
        os.mkdir(input_path)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # 预处理，使得大小小于512kb
    utils.preprocess(input_path,output_path)
    print("mkdir complite")
    #上传函数
    link_list = []


    upload_all("output",tlg_obj)

    #保存
    if os.path.exists("result.xlsx"):
        df = pd.read_excel("result.xlsx")
        print(df.shape)
        df = pd.concat([df,pd.DataFrame(link_list,columns=["name","url"])])
        print(df.shape)
        df.to_excel("result.xlsx",index = None)
    else:
        df = pd.DataFrame(link_list,columns=["name","url"])
        df.to_excel("result.xlsx",index = None)