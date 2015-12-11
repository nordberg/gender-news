import nltk
from nltk.corpus import names
from nltk.tokenize import RegexpTokenizer
import os
import newspaper

DATABASE = './articles.data'
DEBUG = False

he = ['he', 'him', 'man', 'his', 'mr']
she = ['she', 'her', 'woman', 'ms']
prev_word = ['the'] # Words that do not appear before names

def main():
    males_tot = 0
    females_tot = 0

    text = []

    with open(DATABASE, 'r') as f:
        articles = f.readlines()

    for url in articles:
        article = newspaper.Article(url, language='en')

        article.download()

        article.parse()

        print('-----------------')
        print('Processing: ' + article.title)

        text = nltk.word_tokenize(article.text)

        males = []
        females = []
        surnames = []
        mentions = {}
        last_mention_man = ''
        last_mention_woman = ''

        for i, word in enumerate(text):
            if i == 0 or i == len(text)-1:
                continue
            trigram = [text[i-1], word, text[i+1]]

            #tag = nltk.pos_tag([word])

            if len(last_mention_man) > 0:
                if word in he:
                    mentions[last_mention_man] += 1
                    if DEBUG:
                        print('implicit mention of ' + last_mention_man + ' (' + ' '.join(trigram) + ')')
            if len(last_mention_woman) > 0:
                if word in she:
                    mentions[last_mention_woman] += 1
                    if DEBUG:
                        print('implicit mention of ' + last_mention_woman + ' (' + ' '.join(trigram) + ')')

            gender = gender_classify_name(word)

            if gender is None:
                if word[0].isupper():
                    male = False
                    for male in males:
                        if word == male[1]:
                            if DEBUG:
                                print(word + ' mentioned by surname' + ' (' + ' '.join(trigram) + ')')
                            last_mention_man = word
                            mentions[word] += 1
                            male = True
                            break
                    if not male:
                        for female in females:
                            if word == female[1]:
                                if DEBUG:
                                    print(word + ' mentioned by surname' + ' (' + ' '.join(trigram) + ')')
                                last_mention_woman = word
                                mentions[word] += 1
                                break
                continue

            surname = ''
            if trigram[2][0].isupper():
                surname = trigram[2]
                text[i+1] = 'SURNAME'
            else:
                continue
            name = [word, surname]

            if (gender == 'f'):
                if DEBUG:
                    print('Woman: ' + str(name))
                last_mention_woman = surname
                is_in_database = False
                for woman in females:
                    if woman[1] == surname:
                        if DEBUG:
                            print(surname + ' already in database')
                        is_in_database = True
                if not is_in_database:
                    females.append(name)
                    mentions[name[1]] = 1
            elif (gender == 'm'):
                if DEBUG:
                    print('Man: ' + str(name))
                last_mention_man = surname
                is_in_database = False
                for man in males:
                    if man[1] == surname:
                        if DEBUG:
                            print(surname + ' already in database')
                        is_in_database = True
                if not is_in_database:
                    males.append(name)
                    mentions[name[1]] = 1

        print('Men: ' + str(len(males)))
        males_tot += len(males)
        print('Women: ' + str(len(females)))
        females_tot += len(females)
        if len(females) + len(males) > 0:
            print('Female ratio : ' + str(len(females)/(len(females) + len(males))))
        print('Mentions: ')
        for person in mentions:
            print(' ' + person + ': ' + str(mentions[person]))
        print('-----------------')
        print()
        print()
    return females_tot, males_tot

def gender_classify_name(name):
    if name in nltk.corpus.names.words('female.txt'):
        return 'f'
    if name in nltk.corpus.names.words('male.txt'):
        return 'm'
    return None

f,m = main()

print('*-**--**--**--**--**-*')
print('(       SUMMARY      )')
print('Total women: ' + str(f))
print('Total men: ' + str(m))
print('Ratio: ' + str(f/(f + m)))
