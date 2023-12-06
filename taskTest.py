import multiprocessing
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


def poll_ftp_server(q,):
    ftp = FTP('39.108.141.49')  # 替换为实际的 FTP 服务器地址
    ftp.login('TOT', 'Lt@2021')  # 替换为实际的用户名和密码
    ftp.set_pasv(True)
    ftp.cwd('/ztsyj/ted1')  # 替换为实际的 FTP 文件夹路径
    while True:
        filename = q.get()
        if filename is None:
            break
        try:
            download_file(ftp, filename)
            delete_file(ftp, filename)
        except:
            print('Error')
            time.sleep(10)
            break
    ftp.quit()


if __name__ == "__main__":
    ftp = FTP('39.108.141.49')  # 替换为实际的 FTP 服务器地址
    ftp.login('TOT', 'Lt@2021')  # 替换为实际的用户名和密码
    ftp.set_pasv(True)
    ftp.cwd('/ztsyj/ted1')  # 替换为实际的 FTP 文件夹路径
    files = ftp.nlst()  # 获取文件列表
    ftp.quit()
    print('获取列表成功\n')
    q = multiprocessing.Queue()
    d1 = multiprocessing.Process(target=poll_ftp_server, args=(q, ))
    d2 = multiprocessing.Process(target=poll_ftp_server, args=(q, ))
    d1.start()
    d2.start()
    for item in files:
        q.put(item)
    d1.join()
    d2.join()
