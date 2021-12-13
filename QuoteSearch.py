# Created by Charles Vega
# Last Modified December 12, 2021
# This program is a quote finder given an article or txt file
# Given the url to a CNN, Fox News, or NBC News article,
# This program can output a select number of random quotes from the input,
# Or find a quote within the text that can serve as a summary through TextRank.

import requests
import random
# This library provides support for processing text from webpages
from bs4 import BeautifulSoup
# This library implements a TextRank algorithm which aims to summarize a given text
# For more information check https://github.com/summanlp/textrank
from summa import summarizer, keywords

# Given a url to a CNN article this function will return the headline, author, and body
# @url is the url to a CNN article
# Returns the headline, author, and body of the article in an array of strings
def cnn_pull(url):
    # Pull the source code from the article
    source = requests.get(url).text
    # Create a BeautifulSoup object using the source code
    soup = BeautifulSoup(source, 'lxml')
    # Find the source code inside the <article> tag
    article = soup.find('article')
    # Pull the headline from the article within the <h1> tag
    headline = article.h1.text
    # Find the author, located in the first paragraph of the class <l-container>
    author = article.find('div', class_='l-container').p.text
    # Pull the body of the article within the div class <pg-rail-tall__body>
    body = article.find('div', class_='pg-rail-tall__body').text
    return [headline, author, body]

# This function will print the headline, author, and body of a CNN article
# @cnn_data is a preprocessed array of strings containing the headline, author, and body of a CNN article
def cnn_print(cnn_data):
    print(cnn_data[0])
    print(cnn_data[1] + '\n')
    print(cnn_data[2] + '\n\n')

# Given a url to a Fox News article this function will return the headline, author, and body
# @url is the url to a Fox News article
# Returns the headline, author, and body of the article in an array of strings
def fox_pull(url):
    # Pull the source code from the article
    source = requests.get(url).text
    # Create a BeautifulSoup object using the source code
    soup = BeautifulSoup(source, 'lxml')
    # Find the source code inside the <article> tag
    article = soup.find('article')
    # Pull the headline from the article within the <h1> tag
    headline = article.h1.text
    # Find the author, located in the div class <author-byline>
    author = article.find('div', class_='author-byline').a.text
    # Pull the body of the article within the div class <article-body>
    body = article.find('div', class_='article-body').text
    return [headline, author, body]

# Given a url to an NBC News article this function will return the headline, author, and body
# @url is the url to a NBC News article
# Returns the headline, author, and body of the article in an array of strings
def nbc_pull(url):
    # Pull the source code from the article
    source = requests.get(url).text
    # Create a BeautifulSoup object using the source code
    soup = BeautifulSoup(source, 'lxml')
    # Find the source code for the header inside the <header> tag
    header = soup.find('header')
    # Pull the headline from the article within the <h1> tag
    headline = header.h1.text
    # Find the source code inside the <article> tag which contains the body
    article = soup.find('article')
    # Find the author, located in the div class <article-inline-byline>
    author = article.find('div', class_='article-inline-byline').text
    # Pull the body of the article within the div class <article-body__content>
    body = article.find('div', class_='article-body__content').text
    return [headline, author, body]

# Given a body of words this function will return every sentence as an array of strings
# A sentence is found when we find a period in the input
# @words is a string that should contain sentences
# Returns an array of strings which are all sentences from the given words
def get_sentences(words):
    # Create an empty array to store sentences and an empty string
    sentences = []
    sentence = ""
    # Iterate through each character in the input
    for c in words:
        # When the character is a period add the current sentence to the list of sentences
        if c == '.' or c == '!' or c == '?':
            if sentence != "":
                sentences.append(sentence)
                sentence = ""
        else:
            sentence = sentence + c
    if sentence != "":
        sentences.append(sentence)
    print(f"There are {len(sentences)} sentences in this article")
    return sentences

# When given a preprocessed string of text, this function will output a smart quote
# This function utilizes a TextRank algorithm implemented by summanlp
# @text is a preprocessed string indicating where sentences end through line breaks
# Will output a smart quote
def TextRanker(text):
    print(summarizer.summarize(text, words = 30))
    print("\nHere are some keywords from the text: ")
    print(keywords.keywords(text))

# This function will process a string containing sentences such that each sentence will end in a line break
# @words is a string containing sentences, where each sentence ends in a period
# Returns a string containing the same words as the input where each sentence ends in a line break
def find_sentences(words):
    new_words = ""
    for i in range(len(words)):
        if (words[i] == '.'):
            new_words = new_words + ". \n"
        else:
            new_words = new_words + words[i]
    return new_words

if __name__ == '__main__':
    # Request user input to read from a file or url
    choice = int(input("Enter 0 to fetch a quote from a file or 1 for a quote from a given url: "))
    while (choice < 0 or choice > 1):
        choice = int(input("Invalid choice! Try again: "))
    # When we want to pull quotes from a txt file
    if (choice == 0):
        choice = input("Enter the name of your file: ")
        # Append the extension if it is not given
        if (choice[-4:] != ".txt"):
            choice = choice + ".txt"
        with open(choice, encoding='utf8') as f:
            body = f.read()
            choice = int(input("Enter 0 for random quotes or 1 for a smart quote: "))
            while (choice < 0 or choice > 1):
                choice = int(input("Invalid choice! Try again: "))
            if (choice == 0):
                sentences = get_sentences(body)
                # Request input for the number of random quotes
                limit = int(input(f"Enter the number of random quotes to pull from {choice}: "))
                while (limit > len(sentences)):
                    limit = int(input(f"Number of random quotes, {limit}, exceeds number of sentences, {len(sentences)}. Try again: "))
                count = 1
                while (count <= limit):
                    sentence = random.choice(sentences)
                    # Make sure we don't repeat a sentence
                    sentences.remove(sentence)
                    print(f"Quote {count}:" + sentence + '\n')
                    count = count + 1
            else:
                print("Here is a smart quote from the given txt file:")
                body = find_sentences(body)
                TextRanker(body)
    # When we want to pull quotes from an article given a url
    else:
        # Below are some test articles for CNN, Fox News, and NBC News
        cnn_articles = ['https://www.cnn.com/2021/12/04/business/bitcoin-plunges-overnight/index.html',
                        'https://www.cnn.com/2021/12/04/media/cnn-fires-chris-cuomo/index.html?utm_source=optzlynewmarketribbon',
                        'https://www.cnn.com/2021/12/04/business/netflix-insider-trading-sentence/index.html?utm_source=optzlynewmarketribbon']

        fox_articles = ['https://www.foxnews.com/media/cnn-terminates-chris-cuomo-effective-immediately',
                        'https://www.foxnews.com/us/oregon-health-authority-moves-to-implement-permanent-indoor-mask-mandate',
                        'https://www.foxbusiness.com/politics/pelosi-snaps-at-fox']

        nbc_articles = ['https://www.nbcnews.com/news/us-news/cnn-fires-chris-cuomo-suspension-rcna7245',
                        'https://www.nbcnews.com/health/health-news/covid-cases-rise-still-delta-not-omicron-driving-surge-rcna7557',
                        'https://www.nbcnews.com/news/weather/forecasters-predicting-snow-hawaii-rcna7613']
        # Call the cnn_pull function to receive the headline, author, and body of a CNN article
        cnn = fox_pull(fox_articles[1])
        choice = int(input("Enter 0 for random quotes or 1 for a smart quote: "))
        while (choice < 0 or choice > 1):
            choice = int(input("Invalid choice! Try again: "))
        if (choice == 0):
            sentences = get_sentences(cnn[2])
            # Request input for the number of quotes
            limit = int(input(f"Enter the number of random quotes to pull from '{cnn[0]}': "))
            while (limit > len(sentences)):
                limit = int(input(f"Number of random quotes, {limit}, exceeds number of sentences, {len(sentences)}. Try again: "))
            count = 1
            while (count <= limit):
                sentence = random.choice(sentences)
                # Make sure we don't repeat a sentence
                sentences.remove(sentence)
                print(f"Quote {count}:" + sentence + '\n')
                count = count + 1
        else:
            print(f"Here is a smart quote from '{cnn[0]}':")
            cnn[2] = find_sentences(cnn[2])
            TextRanker(cnn[2])
    