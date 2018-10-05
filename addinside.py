#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re

header = open("_inside_header",'r')
footer = open("_footer",'r')
format_date = r"^[0-9]{1,2}-[0-9]{1,2}$"
content_template = """
                    <!-- 文件项目开始 -->
                    <article class="myitem">
                                    <section class="post-preview">
                                        <a class="my-a" href=":href:" title=":title:">
                                            <h2 class="mytitle">
                                                <!-- 文件标题生成 -->
                                                :title:
                                                <!-- 结束 -->
                                            </h2>
                                        </a>
                                    </section>
                                </article>
                    <!-- 文件项目结束 -->
    """
legal_folders = []
content = ""
for folder in os.listdir('.') :
    current = re.search(format_date,folder)
    if current != None:
        legal_folders.append(folder)
legal_folders = sorted(legal_folders,reverse=True)
for folder in legal_folders :
    for file_ in os.listdir(folder) :
        if file_ == 'index.html' :
            continue
        content += content_template.replace(":href:",("/homeworks/" +folder +"/" + file_)).replace(":title:",file_)
    header_ = header.read().replace(":folder:",folder)
    html = header_ + content + footer.read()
    index = open((folder + '/index.html'),'w')
    index.write(html)
    content = ''
    header_ = ''
    header.seek(0,0)
    footer.seek(0,0)