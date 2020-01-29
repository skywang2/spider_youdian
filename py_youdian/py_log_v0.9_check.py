import re
import pandas as pd

extract_page_num = re.compile('https://ydy1.com/(\d*).html')

def get_page_num_list(txt):
    ret = re.findall(extract_page_num, txt)
    ret = [int(x) for x in ret]

    return ret

if __name__ == '__main__':
    log_v9 = ''
    log_v7 = ''

    with open('C:\\Users\\skywang\\Desktop\\登录\\Q&A\\log_v0.9.txt', 'r', encoding='utf-8') as f:
        log_v9 = f.read()

    with open('C:\\Users\\skywang\\Desktop\\登录\\Q&A\\log_v0.7_pianzi.txt', 'r', encoding='utf-8') as f:
        log_v7 = f.read()

    log_v9 = get_page_num_list(log_v9)
    log_v7 = get_page_num_list(log_v7)
    log_v9 = pd.DataFrame(log_v9)
    log_v7 = pd.DataFrame(log_v7)

    log_v7 = log_v7.drop_duplicates()
    log_v9 = log_v9.drop_duplicates()
    print("log_v7 row num:%d" %(len(log_v7)))
    print("log_v9 row num:%d" %(len(log_v9)))

    pass