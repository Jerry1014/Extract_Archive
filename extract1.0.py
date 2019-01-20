# -*- coding: utf-8 -*-
# 密码文件最后一定要空出来一行，即最后一个字符为\n
import os

support_file = ['7Z', 'XZ', 'BZIP2', 'GZIP', 'TAR', 'ZIP', 'ARJ', 'CAB', 'CHM', 'CPIO', 'DEB', 'DMG', 'FAT', 'HFS',
                'ISO', 'LZH', 'LZMA', 'MBR', 'MSI', 'NSIS', 'NTFS', 'RAR', 'RPM', 'UDF', 'VHD', 'WIM', 'XAR', 'Z']


def extract_file():
    # 遍历工作文件夹下所有的文件
    all_filename = os.listdir()

    # 将第一个txt文件认定为密码文件
    pwd_file_name = None
    for i in all_filename:
        if i[-3:] == 'txt':
            pwd_file_name = i
            all_filename.remove(i)
            break
    if not pwd_file_name:
        print('无密码文件，文件必须以txt结尾')
        return

    # 按密码文件中存储的密码，解压文件夹下其他压缩文件
    with open(pwd_file_name, 'r') as pwd_file:
        all_fail_file = list()
        for i in all_filename:
            archive = i.split('.')
            # 当文件没有后缀名时
            if len(archive) < 2:
                continue

            if archive[-1].upper() in support_file:
                result = 1
                for psw in pwd_file.readlines():
                    print(psw)
                    psw = psw[:-1]
                    # x 完整路径释放 -aoa 直接覆盖现有文件，而没有任何提示 -o 输出文件夹 -p 密码
                    cmd_command = '7z x -aoa -o' + archive[0] + ' -p' + psw + ' ' + i
                    result = os.system(cmd_command)
                    if result == 0:
                        # 如果解压成功，则删除压缩文件
                        os.remove(i)
                        break

                if result != 0:
                    all_fail_file.append(i)

            else:
                print('文件' + i + '是不被支持的类型')
                continue

            pwd_file.seek(0, 0)

        if len(all_fail_file) > 0:
            print('以下文件解压失败')
            for i in all_fail_file:
                print(i + '\n')


if __name__ == '__main__':
    extract_file()
    input()
