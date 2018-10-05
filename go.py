#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import time
import platform
import datetime
import re
import sys

# 文件夹格式（月-日）
format_date = r"^[0-9]{1,2}-[0-9]{1,2}$"

# 配置文件项
configurations = ['url_prefix','link_title','subjects','directory']

# First check system type
if 'Linux' not in platform.system() :
    print "You're not running in Linux.\nGet the fuck out!"
    exit ( -1 )

# 设置 UTF-8 环境以实现中文显示
reload(sys)
sys.setdefaultencoding('utf-8')

if 'config.json' not in os.listdir("."):
    print "未找到配置文件。请确认 config.json 在该目录下。"
    exit(127)

configfile = open('config.json','r')
# 检查配置文件完整性
config_txt = configfile.read()
for item in configurations :
    if item not in config_txt :
        print "配置文件不完整。退出。"
        exit(127)
configfile.seek(0,0)
config = json.load(configfile)

header = open('_header','r')
footer = open('_footer','r')
content = open('_content','r+')
notice = open('_notice','w+')
insideheader = open('_inside_header','r')
content.seek(0,0)
# 更改文件权限，避免 " 403 Forbidden " 问题
def chmod(folders) :
    for folder in folders :
        os.chdir(folder)
        for file in os.listdir('.'):
            os.chmod(file,0644)
        os.chdir("..")
    

# 添加作业链接
def add_content(href,title,desc) :
    # 旧的内容
    old_data = content.read()

    # 处理作业项目的提示内容
    content_data = """
                    <!-- 作业项目开始 -->
                    <article class="myitem">
                                    <section class="post-preview">
                                        <a class="my-a" href=":href:" title=":title:">
                                            <h2 class="mytitle">
                                                <!-- 作业标题生成 -->
                                                :title:
                                                <!-- 结束 -->
                                            </h2>

                                            <h3 class="mydesc">
                                                <!-- 作业详情在这里生成 -->
                                                :desc:
                                                <!-- 结束 -->
                                                <br>
                                            </h3>
                                        </a>
                                    </section>
                                </article>
                    <!-- 作业项目结束 -->
    """
    # 处理作业描述（语文：... ，数学： ... ， ... ）

    content_data = content_data.replace(':href:',href,1)
    content_data = content_data.replace(':title:',title,2)
    content_data = content_data.replace(':desc:',desc,1)
    content.seek(0,0)
    content.write(content_data + old_data)
    content.seek(0,0)
    content.close()

def add_notice(text=None,NoNotice=False):
    # 处理公告内容
    notice_data = ''
    if NoNotice == True :
        notice_data = '                <audio controls="" class="myaudio" name="media"  ><source src="http://104.216.111.162:8080/radio" type="application/ogg"></audio>'
    else :
        notice_data = """
                        <article class="mynotice">
                                    <marquee>
                                        <h3 class="mynoticetext"> :notice: </h3>
                                    </marquee>
                        </article> 
                        <audio controls="" class="myaudio" name="media"><source src="http://104.216.111.162:8080/radio" type="application/ogg"></audio>
        """
        notice_data = notice_data.replace(":notice:",text,1)
    # 写入 _notice
    
    notice.seek(0,0)
    notice.write(notice_data)
    notice.seek(0,0)
    notice.close()

def main() :
    sub_homework = ''
    print ("\t\t========= Cyanoxygen 班级作业发布 ========")
    legal_folders = []
    for folder in os.listdir('.') :
        current = re.search(format_date,folder)
        if current != None:
            legal_folders.append(folder)
    legal_folders = sorted(legal_folders,reverse=True)
    print ("探测到的符合条件的文件夹：" + str(legal_folders))
    print ("生成对应的 index.html ...")
    os.system('./addinside.py')
    print ("更改权限...")
    chmod(legal_folders)
    print ("\n")
    target_folder = legal_folders[0]
    question1 = raw_input("启用公告 (Y/n) ? ")
    if question1 == "" or question1 == "Y" or question1 == "y" :
        while True:
            notice_ = raw_input("输入公告内容：")
            question2 =  raw_input("以上内容正确么 (Y/n) ?") 
            if question2 == "" or question2 == "Y" or question2 == "y" :
                add_notice(text=notice_)
                print ("公告已添加。")
                break
    else:
        add_notice(NoNotice=True)
        print ("公告已禁用。")
    ques3 = raw_input("写入详细作业 (Y/n) ?")
    if ques3 == "" or ques3 == "Y" or ques3 == "y" :
        while True:
            for temp_subject in config["subjects"] :
                sub_homework  += ( temp_subject + "：" +  raw_input(temp_subject + ": ") + " <br/>")
            ques4 = raw_input("以上内容正确么 (Y/n) ?")
            if ques4 == "" or ques4 == "Y" or ques4 == "y" : 
                break
    else :
        sub_homework = "今天有点懒, 什么都没有写"
    _href = config["url_prefix"] + target_folder 
    _title = config["link_title"]
    month = target_folder.split("-",1)[0]
    day = target_folder.split("-",1)[1]
    _title = _title.replace(":month:",month)
    _title = _title.replace(":day:",day)
    add_content(_href,_title,sub_homework)
    print ("正在生成 index.html ...")
    files = ['_header','_notice','_content','_footer']
    with open('index.html', 'w') as outfile:
        for fname in files:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    outfile.close()
    
    print ("复制文件到目标目录...")
    for _folder in legal_folders :
            os.system('cp -r ./' + _folder + ' ' + config['directory'])
            print('cp -r ./' + _folder + ' ' + config['directory'])

    print('cp -r ./index.html ' + config['directory'])
    print ("完成。")
        



if __name__ == "__main__":
    main()
