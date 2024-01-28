import requests
import re
import sys
import gzip
import os
import shutil
import tempfile

header1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

def allname():
    url = "https://katagotraining.org/networks/kata1/"
    x = requests.get(url, headers=header1)
    with open('url.html', 'w') as f1:
        f1.write(x.text)
    
    with open('url.html', 'r') as f2:
        fread = f2.read()
    
    r = r'kata1-b\d{2}c\d{3}-s\d{10}-d\d{10}|kata1-b\d{2}c\d{3}nbt-s\d{10}-d\d{10}|kata1-b\d{1}c\d{2}-s\d{7}-d\d{7}|kata1-b\d{2}c\d{3}-s\d{9}-d\d{10}|kata1-b\d{2}c\d{3}-s\d{9}-d\d{8}|kata1-b\d{2}c\d{3}x2-s\d{10}-d\d{10}'
    n = re.findall(r, fread)
    names = list(set(n))
    for name in names:
        print(name)

def gzip_compress_file(file_path):
    with open(file_path, 'rb') as f_in, gzip.open(file_path + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)    

def newname(file, name):
    if '.gz' in file:
        temp_file = file.strip('.gz')
        with gzip.open(file, 'rb') as f_in:
            with open(temp_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        with open(temp_file, 'rb+') as f_out:
            lines = f_out.readlines()
            f_out.seek(0)
            lines[0] = (name + '\n').encode('cp1252')
            f_out.writelines(lines)
        gzip_compress_file(temp_file)
    else:
        with open(file, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            lines[0] = (name + '\n').encode('utf-8')
            f.writelines(lines)
            print("修改成功")


def download(modelname):
    url = "https://media.katagotraining.org/uploaded/networks/models/kata1/" + modelname + '.bin.gz'
    with open(modelname + '.bin.gz', 'wb') as f:
        x = requests.get(url, headers=header1)
        f.write(x.content)
        print("下载完毕")

def fileurl(file):
    with open(file, 'rb') as f:
        lines = f.readlines()
    url = "https://media.katagotraining.org/uploaded/networks/models/kata1/" + str(lines[0].strip(),encoding='utf-8') + '.bin.gz'
    return url

run = sys.argv[1] if len(sys.argv) > 1 else 'allname'

if run == 'allname':
     allname()
elif run == 'newname':
    file = sys.argv[2]
    name = sys.argv[3]
    newname(file, name)
elif run == 'download':
    modelname = sys.argv[2]
    download(modelname)
elif run == 'fileurl':
    file = sys.argv[2]
    print(fileurl(file))
else:
    raise Exception("没有这个功能")
