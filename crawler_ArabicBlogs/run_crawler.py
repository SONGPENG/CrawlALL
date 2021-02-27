import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_url_list(init_url, start_index, end_index, headers):
    blogs_url_list = list()
    for curr_index in tqdm(range(start_index, end_index + 1), desc='url collecting...'):
        curr_url = init_url.format(curr_index)
        print(curr_url)
        try:
            r = requests.get(curr_url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            blog_field = soup.find(name="div", attrs={"class": "blogs-list"})
            title_list = blog_field.find_all(name="h2", attrs={"class": "title title--small"})
            temp_url_list = list()
            for title in title_list:
                temp_url = title.find('a', href=True)['href']
                temp_url_list.append(temp_url)
            print(len(temp_url_list))
            blogs_url_list += temp_url_list
        except IOError:
            print('error')
            print(temp_url_list)

    with open('./url_list.txt', 'w', encoding='utf-8') as f:
        for url in blogs_url_list:
            f.write(url + '\n')

    return blogs_url_list


def creal(url_list, headers, output_name):
    with open(output_name, 'w', encoding='utf-8') as f:
        for i in tqdm(range(len(url_list)), desc='writing'):
            try:
                r = requests.get(url_list[i], headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                text2write = soup.find(name='h2', attrs={'class': 'title title--middle unshrink'}).text + '\n\n'

                content_field = soup.find(name='div', attrs={'class': 'the-content'})
                for content in content_field.findAll(name='p', attrs={'style': 'text-align: justify;'}):
                    temp = content.text.strip()
                    text2write += temp + '\n\n'

                f.write(text2write)
            except IOError:
                print('network error ?')


if __name__ == '__main__':
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    cookie = 'cf_clearance=300693ca350aa8cf7e0dad8bb92de9a0d23c04bd-1614433391-0-150; __cfduid=d66fa258de51ce569e946698faa896d631614433391; advanced_ads_pro_visitor_referrer=https://www.echoroukonline.com/; _ga=GA1.2.241808547.1614433393; _gid=GA1.2.1921167813.1614433393; __asc=6077df66177e3ba98cdfdb0ab10; __auc=6077df66177e3ba98cdfdb0ab10; __gads=ID=e92c77afc2700ace-22d398b130c600d3:T=1614433395:RT=1614433395:S=ALNI_MYi_GXja7ww3fB3ygWphNwBXLzNVw; __cf_bm=803f618d861f56aa998cb3c00fd070aac446b0f3-1614434709-1800-AZOaG+9ZzawV5AExAZdu/1KSsEk7yjIlD/9cZFRhKI5XRtsYtcAl+E5JAml+AZchZ3rfudNm3AIRKZeeT8QD4pQ=; advanced_ads_page_impressions=14; advanced_ads_browser_width=886'
    headers = {'user-agent': agent, 'cookie': cookie}

    url_list = get_url_list('https://www.echoroukonline.com/blogs/page/{}/', 2, 79, headers)
    creal(url_list, headers, './data.txt')
