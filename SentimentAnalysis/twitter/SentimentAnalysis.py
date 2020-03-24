from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import pickle

import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def train_test_evaluation():
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    print('Total number of positive_tweets are : ',len(positive_tweets))
    print('Total number of negative_tweets are : ', len(negative_tweets))
    print('-------------------------')
    print('one smaple of positive_tweets : ',positive_tweets[0])
    print('one smaple of negative_tweets : ', negative_tweets[0])
    print('-------------------------\n\n')

    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
    print('Total number of positive_tweet_tokens are : ',len(positive_tweet_tokens))
    print('Total number of negative_tweet_tokens are : ', len(negative_tweet_tokens))
    print('-------------------------')
    print('one smaple of positive_tweet_tokens : ',positive_tweet_tokens[0])
    print('one smaple of negative_tweet_tokens : ', negative_tweet_tokens[0])
    print('-------------------------\n\n')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    # all_pos_words = get_all_words(positive_cleaned_tokens_list)
    # freq_dist_pos = FreqDist(all_pos_words)
    # print('Most Frequent Items in Positive Tweets',freq_dist_pos.most_common(10))
    #
    # all_neg_words = get_all_words(negative_cleaned_tokens_list)
    # freq_dist_neg = FreqDist(all_neg_words)
    # print('Most Frequent Items in negative Tweets',freq_dist_neg.most_common(10))
    # print('-------------------------')

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:9000]
    test_data = dataset[9000:]


    print('Length of Train Data is : ',len(train_data))
    print(' A sample of Traing Data : ',train_data[0])
    print('-------------------------')
    print('Length of Test Data is : ',len(train_data))
    print(' A sample of Test Data : ',test_data[0])
    print('-------------------------')


    classifier = NaiveBayesClassifier.train(train_data)


    print("\n\n Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    f = open('tweeter_trained_cls.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()

    return classifier


def run_live_example(classifier,custom_tweet):


    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    result = classifier.classify(dict([token, True] for token in custom_tokens))
    return result

if __name__ == "__main__":

    #samples gotthe from
    # https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk


    classifier = train_test_evaluation()
    f = open('tweeter_trained_cls.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    custom_tweet = "i'm the most complete fighter in the world "
    print('\n\n\n Live Testing on \n','\t'+custom_tweet)
    result = run_live_example(classifier=classifier,custom_tweet= custom_tweet)
    if (result.__eq__('Negative')):
        print('\n',result,'  :(((( ')
    if (result.__eq__('Positive')):
        print('\n',result, '  :)))) ')
