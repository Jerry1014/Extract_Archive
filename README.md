# Extract_Archive
## 注意事项：
    （如果有）密码文本最后必须空一行，即文本最后一个字符为\n
    support_file = ['7Z', 'XZ', 'BZIP2', 'GZIP', 'TAR', 'ZIP', 'ARJ', 'CAB', 'CHM', 'CPIO', 'DEB', 'DMG', 'FAT', 'HFS','ISO', 'LZH', 'LZMA', 'MBR', 'MSI', 'NSIS', 'NTFS', 'RAR', 'RPM', 'UDF', 'VHD', 'WIM', 'XAR', 'Z']

# 功能
    批量将压缩文件，按密码文本，逐一测试并解压
    压缩包的位置为当前脚本所在的路径
    解压依赖7z.dll与7z.exe