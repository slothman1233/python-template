import subprocess

# 安装 chromedriver
# output: str = (subprocess.check_output(
#     'google-chrome --version', shell=True)).decode()

# version = output.removeprefix('Google Chrome').strip()
# version = int(version.split('.', maxsplit=1)[0])

# print(version)

subprocess.run(
    f'cd ./depends && wget https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_linux64.zip',
    shell=True
)
subprocess.run(
    f'cd ./depends && unzip chromedriver_linux64.zip',
    shell=True
)