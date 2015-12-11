import nltk
from nltk.corpus import names
from nltk.tokenize import RegexpTokenizer
import os

DATABASE = './database/'

he = ['he', 'him', 'man', 'his', 'mr']
she = ['she', 'her', 'woman', 'ms']
prev_word = ['the'] # Words that do not appear before names

def main():

    text = []

    for article in os.listdir(DATABASE):
        f = open(DATABASE + article, 'r')
        tokenizer = RegexpTokenizer(r'\w+')
        text = nltk.word_tokenize(f.read())

        print('Article: ' + article)

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
                    print('implicit mention of ' + last_mention_man + ' (' + ' '.join(trigram) + ')')
            if len(last_mention_woman) > 0:
                if word in she:
                    mentions[last_mention_woman] += 1
                    print('implicit mention of ' + last_mention_woman + ' (' + ' '.join(trigram) + ')')

            gender = gender_classify_name(word)

            if gender is None:
                if word[0].isupper():
                    male = False
                    for male in males:
                        if word == male[1]:
                            print(word + ' mentioned by surname' + ' (' + ' '.join(trigram) + ')')
                            last_mention_man = word
                            mentions[word] += 1
                            male = True
                            break
                    if not male:
                        for female in females:
                            if word == female[1]:
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
                print('Woman: ' + str(name))
                last_mention_woman = surname
                is_in_database = False
                for woman in females:
                    if woman[1] == surname:
                        print(surname + ' already in database')
                        is_in_database = True
                if not is_in_database:
                    females.append(name)
                    mentions[name[1]] = 1
            elif (gender == 'm'):
                print('Man: ' + str(name))
                last_mention_man = surname
                is_in_database = False
                for man in males:
                    if man[1] == surname:
                        print(surname + ' already in database')
                        is_in_database = True
                if not is_in_database:
                    males.append(name)
                    mentions[name[1]] = 1

        print('-----------------')
        print('Men: ' + str(len(males)))
        print('Women: ' + str(len(females)))
        print('Female ratio : ' + str(len(females)/(len(females) + len(males))))
        print('Mentions: ')
        for person in mentions:
            print(person + ': ' + str(mentions[person]))


        print()
        print()

        '''for i, word in enumerate(text):
            if word in he:
                male.append(word)
            if word in she:
                female.append(word)
            trigram = []
            if i > 0:
                trigram = [text[i-1], text, text[i+1]]
            if trigram[1][0].isupper():
                if i > 1:
                    if trigram[0] in prev_word:
                        continue
                    tags = nltk.pos_tag(trigram)
                    g = gender_classify_name(word)
                    if g == 'f':
                        female.append(word)
                        surname = ''
                        if text[i + 1][0].isupper():
                            surname = text[i + 1]
                        person = word + ' ' + surname
                        if person not in distinct_persons:
                            distinct_persons.append(person)
                        print('Female name: ' + person)
                        print(tags)
                    if g == 'm':
                        male.append(word)
                        surname = ''
                        if text[i + 1][0].isupper():
                            surname = text[i + 1]
                        person = word + ' ' + surname
                        if person not in distinct_persons:
                            distinct_persons.append(person)
                        print('Male name: ' + person)
                        print(tags)
            i += 1

        print('Male words: ' + str(len(male)))
        print('Female words: ' + str(len(female)))
        print('Names: ' + str(len(names)))
        print('Distinct persons: ' + str(len(distinct_persons)))
        for p in distinct_persons:
            print(p)'''

def gender_classify_name(name):
    if name in nltk.corpus.names.words('female.txt'):
        return 'f'
    if name in nltk.corpus.names.words('male.txt'):
        return 'm'
    return None

main()
