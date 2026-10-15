from bs4 import BeautifulSoup
text = '''<div data-v-d575652c="" class="tags"><span data-v-d575652c="">
                  汽车电子
                </span><span data-v-d575652c="">
                  医疗电子
                </span><span data-v-d575652c="">
                  工业控制
                </span></div>
        '''
soup = BeautifulSoup(text,'lxml')
companyTags = []
tags_div = soup.find(class_="tags")

if tags_div:
    span_tags = tags_div.find_all('span') # type: ignore
    for span in span_tags:
        companyTags.append(span.string.strip())
print(companyTags)