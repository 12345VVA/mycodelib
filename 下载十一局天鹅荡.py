import os
import time
from ftplib import FTP


def download_file(ftp, filename):
    local_filename = os.path.join('./image/ztsyj', filename)  # 设置文件保存的本地路径
    with open(local_filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)
    print(f'Downloaded {filename}')


def delete_file(ftp, filename):
    ftp.delete(filename)
    print(f'Deleted {filename} from FTP server')


def poll_ftp_server():
    ftp = FTP('39.108.141.49')  # 替换为实际的 FTP 服务器地址
    ftp.login('TOT', 'Lt@2021')  # 替换为实际的用户名和密码
    ftp.set_pasv(True)

    ftp.cwd('/ztsyj/ted1')  # 替换为实际的 FTP 文件夹路径

    files = ftp.nlst()  # 获取文件列表
    print(files)

    for filename in files:
        if not filename.startswith('.'):  # 忽略隐藏文件
            try:
                download_file(ftp, filename)
                delete_file(ftp, filename)
            except:
                print('Error')
                time.sleep(10)
                ftp.close()
                ftp = FTP('39.108.141.49')  # 替换为实际的 FTP 服务器地址
                ftp.login('TOT', 'Lt@2021')  # 替换为实际的用户名和密码
                ftp.set_pasv(True)
                ftp.cwd('/ztsyj/ted1')  # 替换为实际的 FTP 文件夹路径
                files = ftp.nlst()  # 获取文件列表
                print(files)
                break
    ftp.quit()


# 定时轮询
while True:
    try:
        poll_ftp_server()
        time.sleep(60)  # 每隔60秒执行一次轮询
    except:
        time.sleep(10)
