# -*- coding: utf-8 -*-
import rarfile
#from threading import Thread
import threading


def extractFile(file,password,correct):
    """输入压缩文件(rarfile)，密码（str),是否解压成功标记(int)"""
    try:
        file.extractall(pwd=password)
        print("-----------------")
        print("SUCCEED!")
        print("The right password is %s"%password)
        print("-----------------")
        correct[0] = True
    except:
        pass


def cheakcrossing(passwordlist,order,begin_end):
    bookmark = 1
    while passwordlist[order] > begin_end[bookmark]:
        bookmark += 2

    if passwordlist[order] == begin_end[bookmark]:
        if bookmark+1 < len(begin_end):
            passwordlist[order] = begin_end[bookmark+1]
            return False
        else:
            passwordlist[order-1] += 1
            if order > 0:
                passwordlist[order] = begin_end[0]
                cheakcrossing(passwordlist,order-1,begin_end)
            return True

def calcutebegin_end(begin_end,ifsymbol,ifnumber,ifcaplet,ifsmalet):
    bookmark = 1
    if ifsymbol == 1:
        begin_end.append(32)
        bookmark += 1

    if (bookmark%2 != 0 and ifnumber == 1) or (bookmark%2 == 0 and ifnumber != 1):
        begin_end.append(48)
        bookmark += 1

    if (bookmark%2 != 0 and ifsymbol == 1) or (bookmark%2 == 0 and ifsymbol != 1):
        begin_end.append(58)
        bookmark += 1

    if (bookmark%2 != 0 and ifcaplet == 1) or (bookmark%2 == 0 and ifcaplet != 1):
        begin_end.append(65)
        bookmark += 1

    if (bookmark%2 != 0 and ifsymbol == 1) or (bookmark%2 == 0 and ifsymbol != 1):
        begin_end.append(91)
        bookmark += 1

    if (bookmark%2 != 0 and ifsmalet == 1) or (bookmark%2 == 0 and ifsmalet != 1):
        begin_end.append(97)
        bookmark += 1

    if (bookmark%2 != 0 and ifsymbol == 1) or (bookmark%2 == 0 and ifsymbol != 1):
        begin_end.append(123)
        bookmark += 1

    if bookmark%2 == 0:
        begin_end.append(127)

def main():
    while True:
        filename = input("输入压缩文件名（不需要后缀名）\n")
        try:
            file = rarfile.RarFile(filename+".rar")
            break
        except Exception as e:
            print(e)

    while True:
        ifdic = int(input("是否有字典文件？0. 否  1. 是\n"))
        if ifdic == 1:
            try:
                dname = input("输入字典文件名（不需要后缀名,默认txt文件）\n")
                print()
                passfile = open(dname+".txt")
                break
            except Exception as e:
                print(e)
        elif ifdic == 0:
            passwordinvail = 0
            while passwordinvail == 0:
                ifcaplet = 3
                while ifcaplet != 1 and ifcaplet != 0:
                    ifcaplet = int(input("密码是否包含大写字母？0. 否  1. 是\n"))
 
                ifsmalet = 3
                while ifsmalet != 1 and ifsmalet != 0:
                    ifsmalet = int(input("密码是否包含小写字母？0. 否  1. 是\n"))

                ifnumber = 3
                while ifnumber != 1 and ifnumber != 0:
                    ifnumber = int(input("密码是否包含数字？0. 否  1. 是\n"))

                ifsymbol = 3
                while ifsymbol != 1 and ifsymbol != 0:
                    ifsymbol = int(input("密码是否包含符号？0. 否  1. 是\n"))

                if ifcaplet == 0 and ifsmalet == 0 and ifnumber == 0 and ifsymbol == 0:
                    print("Invail number in input.")
                else:
                    passwordinvail = 1

            break
        else:
            print("Invail number in input.")

    correct = [False]
    if ifdic == 1:
        for line in passfile.readlines():
            password = line.strip('\n')

            t = threading.Thread(target=extractFile,args=(file,password,correct))
            while threading.activeCount() > 50:
                pass
            t.start()

            if correct[0]:
                break
    else:
        minimum = -1
        while minimum <= 0 or minimum > 13:
            minimum = int(input("请输入密码的最短长度（不大于13）\n"))

        maximum = -1
        while maximum < minimum or maximum > 13:
            maximum = int(input("请输入密码的最大长度（不大于13）\n"))

        begin_end = []
        calcutebegin_end(begin_end,ifsymbol,ifnumber,ifcaplet,ifsmalet)

        
        while minimum <= maximum:
            print("正在尝试%d位的破解密码"%minimum)
            passwordlist = []
            for i in range(minimum):
                passwordlist.append(begin_end[0])

            ifcarry = False
            passwordstr = []
            for i in range(minimum):
                passwordstr.append(chr(passwordlist[i]))

            while passwordlist[0] < begin_end[-1]:
                if ifcarry:
                    passwordstr = []
                    for i in range(minimum):
                        passwordstr.append(chr(passwordlist[i]))
                else:
                    passwordstr[-1] = chr(passwordlist[-1])
                ifcarry = False

                password = "".join(passwordstr)
                
                t = threading.Thread(target=extractFile,args=(file,password,correct))
                while threading.activeCount() > 50:
                    pass
                t.start()

                if correct[0]:
                    break

                passwordlist[minimum - 1] += 1
                ifcarry = cheakcrossing(passwordlist,minimum - 1,begin_end)

            if correct[0]:
                break
            minimum += 1

    if not correct[0] and threading.activeCount() == 0:
        print("密码破解失败")

    input()

if __name__ == '__main__':
    main()