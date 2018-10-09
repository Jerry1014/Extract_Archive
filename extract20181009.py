# -*- coding: utf-8 -*-
# 密码文件最后一定要空出来一行，即最后一个字符为\n
import rarfile
import zipfile36 as zipfile
import os


def extract_file():
    # 遍历工作文件夹下所有的文件
    all_filename = os.listdir()

    # 将第一个txt文件认定为密码文件
    for i in all_filename:
        if i[-3:] == 'txt':
            pwd_file_name = i
            all_filename.remove(i)
            break

    # 按密码文件中存储的密码，解压文件夹下其他压缩文件
    with open(pwd_file_name, 'r') as pwd_file:
        for i in all_filename:
            archive = i.split('.')
            # 当文件没有后缀名时
            if len(archive) != 2:
                continue
            result = 1  # 解压结果，0为成功

            if archive[-1] == '7z':
                for psw in pwd_file.readlines():
                    psw = psw[:-1]
                    cmd_command = '7z e -aoa -p' + psw + ' ' + i
                    result = os.system(cmd_command)
                    if result == 0:
                        break

            elif archive[-1] == 'zip':
                z = zipfile.ZipFile(i)
                for psw in pwd_file.readlines():
                    psw = psw[:-1]
                    try:
                        z.extractall(pwd=bytes(psw, encoding='utf-8'))
                        result = 0
                        break
                    except RuntimeError:
                        continue

            elif archive[-1] == 'rar':
                r = rarfile.RarFile(i)
                for psw in pwd_file.readlines():
                    psw = psw[:-1]
                    try:
                        r.extractall(pwd=psw)
                        result = 0
                        break
                    except:
                        continue
            else:
                continue

            # 如果解压成功，则删除压缩文件
            if result == 0:
                os.remove(i)
            pwd_file.seek(0, 0)


if __name__ == '__main__':
    extract_file()
