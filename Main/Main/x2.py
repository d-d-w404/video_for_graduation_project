#这个程序是为了把我之前的数据都x2，和我新写的程序匹配

import os, shutil,re

if __name__=='__main__':
    work_dir = r'C:\Users\Wander\Desktop\w'
    new_dir = 'C:/Users/Wander/Desktop/output/'
    for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            file = open(file_path,"r+",encoding='UTF-8')
            newFile = open(new_dir+filename,"w",encoding='UTF-8')
            #print(new_dir+filename)
            i=1
            for line in file.readlines():
                # if("@dimen/dp" in line):
                #     num = re.sub("\D", "", line)
                #     newNum = int(num)/3
                #     newNum = ("%.1f" % newNum)
                #     ori = line.split("\"")
                #     line = line.replace(ori[1],str(newNum)+"dp")
                if len(line.split(',')) == 2:
                    newFile.writelines(line)
                    #print("2")

                if len(line.split(','))==4:
                    s1=line.split(',')[0]
                    s2 = line.split(',')[1]
                    s3 = line.split(',')[2]
                    s4 = line.split(',')[3]

                    n1=int(s1)
                    n2 = int(s2)
                    n3 = int(s3)
                    n4 = int(s4)

                    n1=n1*2
                    n2 = n2 * 2
                    n3 = n3 * 2
                    n4 = n4 * 2
                    #print('==================================================')
                    #print(s1+','+s2+','+s3+','+s4)
                    string=str(n1)+','+str(n2)+','+str(n3)+','+str(n4)
                    #print(string)
                    #print('==================================================')

                    #print(s1+','+s2+','+s3+','+s4)
                    line=string
                    #print(line)
                    if i==4:
                        print("4")
                        print(string)
                        newFile.writelines(line)
                    else:
                        newFile.writelines(line+'\n')
                i=i+1

            #newFile.write(line)
            newFile.close()
            file.close()
