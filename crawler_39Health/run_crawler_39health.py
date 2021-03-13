import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse
import time
import os


def get_suffix_list(section_url, headers):
    r = requests.get(section_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    suffix_class = soup.find(name="ul", attrs={"class": "list_ask list_ask2"})
    suffix_list = [a['href'] for a in suffix_class.find_all('a', href=True)]
    return suffix_list


# def get_section_all_suffix(basic_section_url, n_page, headers, output_path):
#     section_all_suffix_list = list()
#     for i in tqdm(range(n_page), desc='url collecting...'):
#         section_url = basic_section_url.format(i + 1)
#         suffix_list = get_suffix_list(section_url, headers)
#         section_all_suffix_list += suffix_list
#
#     with open(output_path, 'w', encoding='utf-8') as f:
#         for suffix in section_all_suffix_list:
#             f.write(suffix + '\n')
#     return section_all_suffix_list


def section_all_url_2_txt(root, basic_section_url, n_page, output_url_name, output_data_name, output_log_name, headers):
    with open(output_url_name, 'w', encoding='utf-8') as f0:
        with open(output_log_name, 'w', encoding='utf-8') as f1:
            with open(output_data_name, 'w', encoding='utf-8') as f2:
                for i in tqdm(range(n_page), desc='{:<50} url collecting...'.format(output_data_name)):
                    section_url = basic_section_url.format(i + 1)
                    suffix_list = get_suffix_list(section_url, headers)
                    url_list = [root + suffix for suffix in suffix_list]

                    for i in range(len(url_list)):
                        f0.write(url_list[i] + '\n')
                        r = requests.get(url_list[i], headers=headers)
                        soup = BeautifulSoup(r.text, "html.parser")
                        question = soup.find(name="p", attrs={"class": "txt_ms"}).text.strip()
                        answers = soup.findAll(name="p", attrs={"class": "sele_txt"})
                        answers = [answer.text.strip() for answer in answers]
                        if answers:
                            text = question + '\n'
                            for answer in answers:
                                text = text + answer + '\n'
                            text += '\n'
                            f2.write(text)
                        else:
                            print(url_list[i])
                        time.sleep(1)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--basic_section_url", type=str)
    parser.add_argument("--section_name", type=str)
    parser.add_argument("--n_page", type=int, default=1000)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    root = 'http://ask.39.net'
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    cookie = '__utrace=232ece06c4e0790c42930d18411a9801; _ga=GA1.2.2144272332.1614328782; Hm_lvt_ab2e5965345c61109c5e97c34de8026a=1614328777,1614333894,1614334014; Hm_lpvt_ab2e5965345c61109c5e97c34de8026a=1614334014; BAIDU_SSP_lcr=https://www.baidu.com/link?url=0q47OhMfpV1WeCyWBwsYQXS3CNSH4Pr1GEi1CUKRe1a&wd=&eqid=c0fb8bf000011e25000000066038c83c; money=0; picurl=; pid=38812812; username=X56825294; DomainName=X56825294; nickname=P******; verify=4082433064; asp_furl=http://localhost:8888/; Hm_lvt_9840601cb51320c55bca4fa0f4949efe=1614363023,1614363037,1614363063,1614363109; _gat=1; Hm_lpvt_9840601cb51320c55bca4fa0f4949efe=1614363376'
    headers = {'user-agent': agent, 'cookie': cookie}

    # section_all_suffix_list = get_section_all_suffix(basic_section_url, n_page, headers, '妇产科url.txt')
    # section_all_url = [root + suffix for suffix in section_all_suffix_list]
    n_page = args.n_page
    # http://ask.39.net/news/313-{}.html
    # 内科

    basic_section_url, section_name = args.basic_section_url, args.section_name
    os.mkdir(os.path.join('./data', section_name))
    output_url_name = os.path.join('./data', section_name, '{}_url.txt'.format(section_name))
    output_data_name = os.path.join('./data', section_name, '{}_qa.txt'.format(section_name))
    output_log_name = os.path.join('./data', section_name, '{}_log.txt'.format(section_name))
    section_all_url_2_txt(root, basic_section_url, n_page, output_url_name, output_data_name, output_log_name, headers)


if __name__ == '__main__':
    main()
