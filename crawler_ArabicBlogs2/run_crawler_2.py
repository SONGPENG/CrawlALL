import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_url_list(prefix, curr_suffix, n_jump, headers):
    with open('url_list.txt', 'w', encoding='utf-8') as f:
        suffix2store_list = list()
        for i in tqdm(range(n_jump), desc='jumping...'):
            curr_url = prefix + curr_suffix
            r = requests.get(curr_url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            curr_suffix2store = soup.find_all(name="h2", attrs={"class": "b-plainlist__title"})
            for item in curr_suffix2store:
                temp = prefix + item.find('a', href=True)['href']
                suffix2store_list.append(temp)
                f.write(temp + '\n')

            next_suffix = soup.find(name="li", attrs={"class": "b-plainlist__item", 'data-next': True})['data-next']

            if next_suffix:
                curr_url = prefix + next_suffix
                print('jump')
            else:
                break

    return suffix2store_list


def creal(url_list, headers, output_name):
    with open(output_name, 'w', encoding='utf-8') as f:
        for i in tqdm(range(len(url_list)), desc='writing'):
            print(url_list[i])
            try:
                r = requests.get(url_list[i], headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                #                 print(soup)
                articlBody = soup.find_all(name='div', attrs={'itemprop': 'articleBody', 'class': 'b-article__text'})
                print('aa ', len(articlBody))

                for ab in articlBody:

                    rtl = ab.find_all(name="p", attrs={"dir": "rtl"})
                    text2write = ''
                    for item in rtl:
                        text2write += item.text.strip() + '\n\n'
                    # print(text2write)
                    f.write(text2write)
                    print('rtl ', len(rtl))
            except IOError:
                print('network error ?')


if __name__ == '__main__':
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    cookie = '_fbp=fb.1.1614443924590.1589609919; __gads=ID=990aa06cabb795b2:T=1614443934:S=ALNI_MbKNnqEjgOc33mNhPavTEKbcOE84w'
    headers = {'user-agent': agent, 'cookie': cookie}

    try:
        url_list = get_url_list('https://arabic.sputniknews.com', '/blogs/more.html?id=1046248488&date=20200811T104443',
                                10000, headers)
    except IOError:
        print("url list error")
        with open('./url_list.txt', 'r', encoding='utf-8') as f:
            url_list = [url.strip('\n') for url in f.readlines()]

    creal(url_list, headers, 'data.txt')
