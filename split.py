import os

path = '/Users/xuliduo/Downloads/data'
files = os.listdir(path)
files = [f for f in files if f.endswith('.md')]

num_files = len(files)
num_dirs = num_files // 5 + 1
if num_files % 5 == 0:
    num_dirs -= 1

dirs = [f'{path}/doc'+ str(i) for i in range(1, num_dirs +1)]

for dir in dirs:
    os.mkdir(dir) # 创建每个目录

for i in range(num_files):
    dir = dirs[i % num_dirs]
    os.rename(f'{path}/{files[i]}', os.path.join(dir, files[i]))