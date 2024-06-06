FROM python:3.10-buster

# 如果要清华源，就用下面这个
RUN (echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list) 

# 更新一下 apt 源，并更新软件
RUN (apt update) && (apt upgrade -y)

# 中文包
# RUN (apt install -y  lsb-release wget ttf-wqy-zenhei xfonts-intl-chinese wqy*)

# 解决僵尸进程
RUN (apt install -y  tini) 

WORKDIR /code
RUN mkdir /code/depends

# 删除冲突的包
RUN (echo y | apt-get remove libgdk-pixbuf-2.0-0) && (echo y | apt-get autoremove libgdk-pixbuf2.0-0)
# 记得使用 apt 安装 chrome，而不是 dpkg
# 下载并安装 chrome, TIPS: dpkg 不会处理依赖，要使用 apt 安装 deb
RUN (wget -P /code/depends https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) && (apt install -y /code/depends/google-chrome-stable_current_amd64.deb)
# 安装chrome
COPY install.py /code/
RUN python install.py


# 更新pip
RUN /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 安装依赖
COPY requirements-prd.txt /code/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# 复制项目
COPY . /code/

ENTRYPOINT ["/usr/bin/tini", "--"]

# 执行对应的爬虫命令
CMD scrapy crawl selenium


# 
# docker cp E:\work\test\python\scrapy\crawlerScrapy\. d70fb95e38fe:/code/

