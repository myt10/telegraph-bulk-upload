import utils
import os
from telegraph import Telegraph
import telegraph
import ujson as json
from PIL import Image
from PIL import ImageFile
from shutil import copyfile


def get_imgs(path = "None"): #获取图片路径
    imgdir = path
    img_path = [os.path.join(imgdir,img) for img in (sorted([fn for fn in os.listdir(imgdir) if os.path.splitext(fn)[1] == '.jpg' or '.png'], key=lambda fn:os.path.splitext(fn)[0][-5:]))]
    return img_path
def create_account(short_name= 'myt10', author_name= 'myt10', author_url= 'https://github.com/myt10'): #创建账户
    tgh = Telegraph()
    account = tgh.create_account(short_name= short_name, author_name= author_name, author_url= author_url,replace_token=True)
    '''
    create_account:创建账户
    short_name:账户名称,帮助用户记住当前使用的账户
    author_name:作者名称,创建新文章时默认使用
    author_url:作者链接,点击作者名称时打开的链接
    replace_token:是否替换token
    '''
    with open('account.json',"w",encoding="utf-8") as f: #将账户信息写入json文件中
        f.write(json.dumps(account, indent=4,ensure_ascii=False))
    print(account)
def __init__account(short_name= 'myt10', author_name= 'myt10', author_url= 'https://github.com/myt10'): #初始化账户
    if not os.path.exists("account.json"):
        create_account(short_name= short_name, author_name= author_name, author_url= author_url)
    with open('account.json',"r",encoding="utf-8") as f:
        account = json.load(f)
    tlg = telegraph.api.Telegraph(access_token=account['access_token'], domain='telegra.ph')
    print(tlg.get_account_info(fields=["auth_url"])) #获取编辑权限链接
    print(type(tlg))
    return tlg


def get_content(img_url): #获取文章内容
    content = ''
    for url in img_url:
        content += f'<img src="{url}">\n'
    return content


def compress_image(input_path, output_path, mb=500, quality=75, k=0.9):
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    if os.path.exists(output_path):
        return
    o_size = os.path.getsize(input_path) // 1024
    if o_size <= mb:
        copyfile(input_path, output_path)
        return
        # ImageFile.LOAD_TRUNCATED_IMAGES = True
    im = Image.open(input_path)
    while o_size > mb:
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        try:
            out.save(output_path, quality=quality)
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(output_path) // 1024
        im = Image.open(output_path)
    return output_path


def preprocess(input_path,output_path): #图片压缩为webp格式
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    path_lst = os.listdir(input_path)
    for pth in path_lst:
        if os.path.isdir(input_path +'//'+pth):
            preprocess(input_path+'//'+pth,output_path+'//'+pth)
        else:
            if pth.split(".")[-1] in ["jpeg","png","jpg","bmp"]:
                compress_image(input_path+'//'+pth,output_path+'//'+pth)