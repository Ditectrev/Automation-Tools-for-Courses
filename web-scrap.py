from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import regex_spm

# define global parameters
URL = 'https://www.exam4training.com/what-should-you-do-3433/'
MASTER_LIST = []

def find_correct_answer(correct_answer_text):
    isCorreactA = False
    isCorreactB = False
    isCorreactC = False
    isCorreactD = False
    match regex_spm.fullmatch_in(correct_answer_text):
        case r'A . (.+?)':
            isCorreactA = True
        case r'B . (.+?)':
            isCorreactB = True
        case r'C . (.+?)':
            isCorreactC = True
        case r'D . (.+?)':
            isCorreactD = True
        case default:
            print('Different answer than A, B, C, D - investigate the question manually')
    return isCorreactA, isCorreactB, isCorreactC, isCorreactD

def parse_question(content):
    isCorreactA = False
    isCorreactB = False
    isCorreactC = False
    isCorreactD = False
    # Let's set E to H to always False, for now.
    isCorreactE = False
    isCorreactF = False
    isCorreactG = False
    isCorreactH = False

    question = content.find('p').text
    correct_answer = content.find('span', {'class': 'correct_answer'})
    if (correct_answer is not None):
        isCorreactA, isCorreactB, isCorreactC, isCorreactD = find_correct_answer(correct_answer.text)

    question2 = ''
    answerA = ''
    answerB = ''
    answerC = ''
    answerD = ''
    answerE = ''
    answerF = ''
    answerG = ''
    answerH = ''
    try:
        # Whenever there's a second part of the question in a new paragraph, it's being missed. It could be improved.
        question2 = re.search('(.+?)\n', question).group(0)
        #question2 = re.search('(?=.*\?)', question).group(0) # one of the ideas to improve it was to look for a string until "?".
        answerA = re.search('A . (.+?)B . ', question).group(1)
        answerB = re.search('B . (.+?)C . ', question).group(1)
        answerC = re.search('C . (.+?)D . ', question).group(1)
        # This needs to be improved, as it takes everything from 'D . ', 'E . ', etc., till end of the line = it takes all answers. For now, it's just to catch all answers further than D and see if there are many of those. The pattern starts here, as most questions have answers till D.
        answerD = re.search('D . .*(?:\r?\n.*)*', question).group(0)
        answerE = re.search('E . .*(?:\r?\n.*)*', question).group(0)
        answerF = re.search('F . .*(?:\r?\n.*)*', question).group(0)
        answerG = re.search('G . .*(?:\r?\n.*)*', question).group(0)
        answerH = re.search('H . .*(?:\r?\n.*)*', question).group(0)

    except:
        pass
    outdf = pd.DataFrame({
        'question': '\n### ' + question2 + '\n',
        'answerA': '\n- [x] ' + answerA if isCorreactA else '\n- [ ] ' + answerA if answerA else '\n- [ ] PLEASE_DELETE_ME',
        'answerB': '\n- [x] ' + answerB if isCorreactB else '\n- [ ] ' + answerB if answerB else '\n- [ ] PLEASE_DELETE_ME',
        'answerC': '\n- [x] ' + answerC if isCorreactC else '\n- [ ] ' + answerC if answerC else '\n- [ ] PLEASE_DELETE_ME',
        'answerD': '\n- [x] ' + answerD if isCorreactD else '\n- [ ] ' + answerD if answerD else '\n- [ ] PLEASE_DELETE_ME',
        'answerE': '\n- [x] ' + answerE if isCorreactE else '\n- [ ] ' + answerE if answerE else '\n- [ ] PLEASE_DELETE_ME',
        'answerF': '\n- [x] ' + answerF if isCorreactF else '\n- [ ] ' + answerF if answerF else '\n- [ ] PLEASE_DELETE_ME',
        'answerG': '\n- [x] ' + answerG if isCorreactG else '\n- [ ] ' + answerG if answerG else '\n- [ ] PLEASE_DELETE_ME',
        'answerH': '\n- [x] ' + answerH if isCorreactH else '\n- [ ] ' + answerH if answerH else '\n- [ ] PLEASE_DELETE_ME',
    }, index=[0])

    return outdf

def return_next_page(soup):
    next_url = None
    cur_page = soup.find('div', {'class': 'content-area'})
    search_next = cur_page.findNext('div', {'class': 'nav-next'})

    if search_next:
      next_url = search_next.findNext('a')['href']
    return next_url

def scrap_next_question(url):
    global MASTER_LIST
    req = requests.get(url, headers={'User-Agent': 'Chrome'})
    soup = BeautifulSoup(req.content, 'html.parser')
    question = soup.findAll('div', {'class': 'content-area'})
    content_list = [parse_question(content) for content in question]
    MASTER_LIST.extend(content_list)
    next_url = return_next_page(soup)
    finaldf = pd.concat(MASTER_LIST)
    finaldf.shape # (339, 6)
    finaldf.head(2)
    finaldf.to_csv('web-scrap.csv', index=False, encoding='utf-8')
    if next_url is not None:
        scrap_next_question(next_url)


scrap_next_question(URL)


finaldf = pd.concat(MASTER_LIST)
finaldf.shape # (339, 6)

finaldf.head(2)
finaldf.to_csv('web-scrap.csv', index=False, encoding='utf-8')
