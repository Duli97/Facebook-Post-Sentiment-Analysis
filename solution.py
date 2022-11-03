# -*- coding: utf-8 -*-
"""Solution.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IcVzHWNo9ix8n-ohH0F3Lg-hFXAVbgYE

# **Preprocessing**
"""

from google.colab import drive
drive.mount('/content/drive')

#Importing the libraries

import nltk                                # Python library for NLP
from nltk.corpus import twitter_samples    # sample Twitter dataset from NLTK
import matplotlib.pyplot as plt            # library for visualization
import random                              # pseudo-random number generator

import numpy as np 
import pandas as pd

import re                                  # library for regular expression operations
import string                              # for string operations
from nltk.tokenize import TweetTokenizer   # module for tokenizing strings

"""## Importing the Dataset and Put those into lists"""

df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/NLP/Singlish.csv')
df

#Removing the last negative row so there will be equall negatives and positives
df = df.drop(1094)
df

"""In the above table first 547 statements are positive and the other 547 statements are negative.

47 statements from each positive and negative are removed in order to get 500 statements for each.
"""

#First, removes the negative 47 statements
df = df.drop(df.index[1047:])

df

#Remove the positive columns
df = df.drop(df.index[501:548])

df

all_posts = df['Statement'].tolist()

all_positive_posts = all_posts[:500]
all_negative_posts = all_posts[500:]

"""Remove further"""

all_positive_posts = all_positive_posts[150:500]
all_negative_posts = all_negative_posts[:270] + all_negative_posts[280:360]
all_posts = all_positive_posts + all_negative_posts

"""A [pie chart](https://matplotlib.org/3.2.1/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py) to show the same information as above."""

# Declare a figure with a custom size
fig = plt.figure(figsize=(5, 5))

# labels for the two classes
labels = 'Positives', 'Negative'

# Sizes for each slide
sizes = [len(all_positive_posts), len(all_negative_posts)] 

# Declare pie chart, where the slices will be ordered and plotted counter-clockwise:
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')  

# Display the chart
plt.show()

# print a positive in greeen
print('\033[92m', all_positive_posts[:10])

# print a negative in red
print('\u001b[31m', all_negative_posts[:10])

"""## Preprocess raw text for Sentiment analysis

* Tokenizing the string
* Lowercasing
* Removing stop words and punctuation
* Stemming
"""

!pip install googletrans==4.0.0rc1

import googletrans
print(googletrans.LANGUAGES)

dir(googletrans)

#Install sinling library for sinhala words processing

!pip install sinling

import sinling
dir(sinling)

import pandas as pd
stopwords_sinhala_df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/NLP/stop-words.csv', header=None)

stopwords_sinhala = stopwords_sinhala_df[0].tolist()

print(stopwords_sinhala)

#Replace 'හෝ\u200d' with 'හෝ'
stopwords_sinhala[17]='හෝ'
print(stopwords_sinhala)

from googletrans import Translator

def process_post(post):
    """Process tweet function.
    Input:
        tweet: a string containing a tweet
    Output:
        tweets_clean: a list of words containing the processed tweet

    """
    stemmer_sinhala = sinling.SinhalaStemmer()
    translator = Translator()
    stopwords_sinhala

    
    
    # remove stock market tickers like $GE
    post = re.sub(r'\$\w*', '', post)
    
    # remove old style retweet text "RT"
    post = re.sub(r'^RT[\s]+', '', post)
    
    # remove hyperlinks
    post = re.sub(r'http\S+', '', post)
    
    # removing the hash #, @ and ellipses 
    post = re.sub("@[A-Za-z0-9_]+","", post)
    post = re.sub("#[A-Za-z0-9_]+","", post)
    post = post.replace("..."," ")

    post = translator.translate(post, dest='en').text
    post = translator.translate(post, dest='si').text

    #print(post)

    # tokenize tweets
    #tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               #reduce_len=True)
    tokenizer = sinling.SinhalaTokenizer()
    post_tokens = tokenizer.tokenize(post)

    

    posts_clean = []
    for word in post_tokens:
        if (word not in stopwords_sinhala and   word not in string.punctuation):  # remove punctuation and stopwords

            stemmed_word = stemmer_sinhala.stem(word)
            
            if(stemmed_word[0] != ''):
                posts_clean.append(stemmed_word[0])
                stemmed_word=[]

    return posts_clean

# choose a post as an example
post_eg = all_positive_posts[18]

print()
print('\033[92m')
print(post_eg)
print('\033[94m')

posts_lem = process_post(post_eg); # Preprocess a given tweet

print('preprocessed tweet:')
print(posts_lem) # Print the result

"""## Word frequency dictionary

Function that creates the dictionary containing the word counts from each corpus.
"""

def build_freqs(posts, ys):
    
    """Build frequencies.
    Input:
        tweets: a list of tweets
        ys: an m x 1 array with the sentiment label of each tweet
            (either 0 or 1)
    Output:
        freqs: a dictionary mapping each (word, sentiment) pair to its
        frequency
    """
    # Convert np array to list since zip needs an iterable.
    # The squeeze is necessary or the list ends up with one element.
    # Also note that this is just a NOP if ys is already a list.
    yslist = np.squeeze(ys).tolist()

    # Start with an empty dictionary and populate it by looping over all tweets
    # and over all processed words in each tweet.
    freqs = {}
    for y, post in zip(yslist, posts):
        #print(post)
        for word in process_post(post):
            pair = (word, y)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1  
        
                    
    return freqs

# let's see how many tweets we have
print("Number of tweets: ", len(all_posts))

# make a numpy array representing labels of the tweets
labels = np.append(np.ones((len(all_positive_posts))), np.zeros((len(all_negative_posts))))

labels

# create frequency dictionary
freqs = build_freqs(all_posts, labels)

# check data type
print(f'type(freqs) = {type(freqs)}')

# check length of the dictionary
print(f'len(freqs) = {len(freqs)}')

print(freqs)

"""## Table of word counts"""

# select some words to appear and we will assume that each word is unique (i.e. no duplicates)
keys = ['කතන්දර', 'ඔබ', 'යටත', 'ළඟ', 'පැතිකඩ', 'ඉතිරි']

# list representing our table of word counts.
# each element consist of a sublist with this pattern: [<word>, <positive_count>, <negative_count>]
data = []

# loop through our selected words
for word in keys:
    
    # initialize positive and negative counts
    pos = 0
    neg = 0
    
    # retrieve number of positive counts
    if (word, 1) in freqs:
        pos = freqs[(word, 1)]
        
    # retrieve number of negative counts
    if (word, 0) in freqs:
        neg = freqs[(word, 0)]
        
    # append the word counts to the table
    data.append([word, pos, neg])
    
data

fig, ax = plt.subplots(figsize = (8, 8))

# convert positive raw counts to logarithmic scale. we add 1 to avoid log(0)
x = np.log([x[1] + 1 for x in data])  

# do the same for the negative counts
y = np.log([x[2] + 1 for x in data]) 

# Plot a dot for each pair of words
ax.scatter(x, y)  

# assign axis labels
plt.xlabel("Log Positive count")
plt.ylabel("Log Negative count")

# Add the word as the label at the same position as you added the points just before
for i in range(0, len(data)):
    ax.annotate(data[i][0], (x[i], y[i]), fontsize=12)

ax.plot([0, 9], [0, 9], color = 'red') # Plot the red line that divides the 2 areas.
plt.show()

"""# **Naive Bayes Model**

* Train a naive bayes model on a sentiment analysis task
* Test the model
* Compute ratios of positive words to negative words
* Do some error analysis
* Predict on your own tweet
"""

# split the data into two pieces, one for training and one for testing (validation set)
test_pos = all_positive_posts[300:]
train_pos = all_positive_posts[:300]
test_neg = all_negative_posts[300:]
train_neg = all_negative_posts[:300]

train_x = train_pos + train_neg
test_x = test_pos + test_neg

# avoid assumptions about the length of all_positive_tweets
train_y = np.append(np.ones(len(train_pos)), np.zeros(len(train_neg)))
test_y = np.append(np.ones(len(test_pos)), np.zeros(len(test_neg)))

"""## Implementing your helper functions

To help train naive bayes model, need to build a dictionary where the keys are a (word, label) tuple and the values are the corresponding frequency.  Note that the labels we'll use here are 1 for positive and 0 for negative.

For example: given a list of tweets `["i am rather excited", "you are rather happy"]` and the label 1, the function will return a dictionary that contains the following key-value pairs:

{
    ("rather", 1): 2
    ("happi", 1) : 1
    ("excit", 1) : 1
}
"""

def count_posts(result, posts, ys):
    '''
    Input:
        result: a dictionary that will be used to map each pair to its frequency
        tweets: a list of tweets
        ys: a list corresponding to the sentiment of each tweet (either 0 or 1)
    Output:
        result: a dictionary mapping each pair to its frequency
    '''

    ## -- YOUR CODE -- ##
    # Convert np array to list since zip needs an iterable.
    # The squeeze is necessary or the list ends up with one element.
    # Also note that this is just a NOP if ys is already a list.
    yslist = np.squeeze(ys).tolist()

    # Start with an empty dictionary and populate it by looping over all tweets
    # and over all processed words in each tweet.
    freqs = {}
    for y, post in zip(yslist, posts):
        for word in process_post(post):
            pair = (word, y)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1    

    result = freqs

    return result

result = {}
posts = ['i am happy', 'i am tricked', 'i am sad', 'i am tired', 'i am tired']
ys = [1, 0, 0, 0, 0]
count_posts(result, posts, ys)

"""# **Train your model using Naive Bayes**

Naive bayes algorithm could be used for sentiment analysis. It takes a short time to train and also has a short prediction time.

- The first part of training a naive bayes classifier is to identify the number of classes that you have.
- You will create a probability for each class.
$P(D_{pos})$ is the probability that the document is positive.
$P(D_{neg})$ is the probability that the document is negative.
Use the formulas as follows and store the values in a dictionary:

$$P(D_{pos}) = \frac{D_{pos}}{D}\tag{1}$$

$$P(D_{neg}) = \frac{D_{neg}}{D}\tag{2}$$

Where $D$ is the total number of documents, or tweets in this case, $D_{pos}$ is the total number of positive tweets and $D_{neg}$ is the total number of negative tweets.

#### Prior and Logprior

The prior probability represents the underlying probability in the target population that a tweet is positive versus negative.  In other words, if we had no specific information and blindly picked a tweet out of the population set, what is the probability that it will be positive versus that it will be negative? That is the "prior".

The prior is the ratio of the probabilities $\frac{P(D_{pos})}{P(D_{neg})}$.
We can take the log of the prior to rescale it, and we'll call this the logprior

$$\text{logprior} = log \left( \frac{P(D_{pos})}{P(D_{neg})} \right) = log \left( \frac{D_{pos}}{D_{neg}} \right)$$.

Note that $log(\frac{A}{B})$ is the same as $log(A) - log(B)$.  So the logprior can also be calculated as the difference between two logs:

$$\text{logprior} = \log (P(D_{pos})) - \log (P(D_{neg})) = \log (D_{pos}) - \log (D_{neg})\tag{3}$$

#### Positive and Negative Probability of a Word
To compute the positive probability and the negative probability for a specific word in the vocabulary, we'll use the following inputs:

- $freq_{pos}$ and $freq_{neg}$ are the frequencies of that specific word in the positive or negative class. In other words, the positive frequency of a word is the number of times the word is counted with the label of 1.
- $N_{pos}$ and $N_{neg}$ are the total number of positive and negative words for all documents (for all tweets), respectively.
- $V$ is the number of unique words in the entire set of documents, for all classes, whether positive or negative.

We'll use these to compute the positive and negative probability for a specific word using this formula:

$$ P(W_{pos}) = \frac{freq_{pos} + 1}{N_{pos} + V}\tag{4} $$
$$ P(W_{neg}) = \frac{freq_{neg} + 1}{N_{neg} + V}\tag{5} $$

Notice that we add the "+1" in the numerator for additive smoothing.  This [wiki article](https://en.wikipedia.org/wiki/Additive_smoothing) explains more about additive smoothing.

#### Log likelihood
To compute the loglikelihood of that very same word, we can implement the following equations:

$$\text{loglikelihood} = \log \left(\frac{P(W_{pos})}{P(W_{neg})} \right)\tag{6}$$

##### Create `freqs` dictionary
- Given your `count_tweets()` function, you can compute a dictionary called `freqs` that contains all the frequencies.
- In this `freqs` dictionary, the key is the tuple (word, label)
- The value is the number of times it has appeared.
"""

# Build the freqs dictionary 
freqs = count_posts({}, train_x, train_y)

"""Given a freqs dictionary, `train_x` (a list of tweets) and a `train_y` (a list of labels for each tweet), implement a naive bayes classifier.

##### Calculate $V$
- You can then compute the number of unique words that appear in the `freqs` dictionary to get your $V$ (you can use the `set` function).

##### Calculate $freq_{pos}$ and $freq_{neg}$
- Using your `freqs` dictionary, you can compute the positive and negative frequency of each word $freq_{pos}$ and $freq_{neg}$.

##### Calculate $N_{pos}$, $N_{neg}$, $V_{pos}$, and $V_{neg}$
- Using `freqs` dictionary, you can also compute the total number of positive words and total number of negative words $N_{pos}$ and $N_{neg}$.
- Similarly, use `freqs` dictionary to compute the total number of **unique** positive words, $V_{pos}$, and total **unique** negative words $V_{neg}$.

##### Calculate $D$, $D_{pos}$, $D_{neg}$
- Using the `train_y` input list of labels, calculate the number of documents (tweets) $D$, as well as the number of positive documents (tweets) $D_{pos}$ and number of negative documents (tweets) $D_{neg}$.
- Calculate the probability that a document (tweet) is positive $P(D_{pos})$, and the probability that a document (tweet) is negative $P(D_{neg})$

##### Calculate the logprior
- the logprior is $log(D_{pos}) - log(D_{neg})$

##### Calculate log likelihood
- Finally, you can iterate over each word in the vocabulary, use your `lookup` function to get the positive frequencies, $freq_{pos}$, and the negative frequencies, $freq_{neg}$, for that specific word.
- Compute the positive probability of each word $P(W_{pos})$, negative probability of each word $P(W_{neg})$ using equations 4 & 5.

$$ P(W_{pos}) = \frac{freq_{pos} + 1}{N_{pos} + V}\tag{4} $$
$$ P(W_{neg}) = \frac{freq_{neg} + 1}{N_{neg} + V}\tag{5} $$

**Note:** We'll use a dictionary to store the log likelihoods for each word.  The key is the word, the value is the log likelihood of that word).

- You can then compute the loglikelihood: $log \left( \frac{P(W_{pos})}{P(W_{neg})} \right)$.
"""

import math

def train_naive_bayes(freqs, train_x, train_y):
    '''
    Input:
        freqs: dictionary from (word, label) to how often the word appears
        train_x: a list of tweets
        train_y: a list of labels correponding to the tweets (0,1)
    Output:
        logprior: the log prior. (equation 3 above)
        loglikelihood: the log likelihood of you Naive bayes equation.
    '''
    loglikelihood = {}
    logprior = 0

    # calculate V, the number of unique words in the vocabulary
    vocab = set([pair[0] for pair in freqs.keys()])
    V = len(vocab)

    # calculate N_pos, N_neg, V_pos, V_neg
    N_pos = N_neg = V_pos = V_neg = 0
    
    for pair in freqs.keys():
        # if the label is positive (greater than zero)
        if pair[1] > 0:
            # increment the count of unique positive words by 1
            V_pos += 1

            # Increment the number of positive words by the count for this (word, label) pair
            N_pos += freqs[pair]

        # else, the label is negative
        else:
            # increment the count of unique negative words by 1
            V_neg += 1

            # increment the number of negative words by the count for this (word,label) pair
            N_neg += freqs[pair]

    # Calculate D, the number of documents
    D = len(train_y)

    # Calculate D_pos, the number of positive documents
    D_pos = (len(list(filter(lambda x: x > 0, train_y))))

    # Calculate D_neg, the number of negative documents
    D_neg = (len(list(filter(lambda x: x <= 0, train_y))))

    # Calculate logprior
    logprior = math.log(D_pos) - math.log(D_neg)

    # For each word in the vocabulary...
    for word in vocab:
        # get the positive and negative frequency of the word
        freq_pos = lookup(freqs,word,1)
        freq_neg = lookup(freqs,word,0)

        # calculate the probability that each word is positive, and negative
        p_w_pos = (freq_pos + 1) / (N_pos + V)
        p_w_neg = (freq_neg + 1) / (N_neg + V)

        # calculate the log likelihood of the word
        loglikelihood[word] = math.log(p_w_pos) - math.log(p_w_neg)

    return logprior, loglikelihood

def lookup(freqs, word, label):
    '''
    Input:
        freqs: a dictionary with the frequency of each pair (or tuple)
        word: the word to look up
        label: the label corresponding to the word
    Output:
        n: the number of times the word with its corresponding label appears.
    '''
    n = 0  
    n = freqs.get((word, label), 0)

    ## -- YOUR CODE -- ##

    return n

logprior, loglikelihood = train_naive_bayes(freqs, train_x, train_y)

print(logprior)
print(len(loglikelihood))

"""# **Test your naive bayes**

Now that we have the `logprior` and `loglikelihood`, we can test the naive bayes function by making predicting on some tweets!

#### Implement `naive_bayes_predict`
Implement the `naive_bayes_predict` function to make predictions on tweets.
* The function takes in the `tweet`, `logprior`, `loglikelihood`.
* It returns the probability that the tweet belongs to the positive or negative class.
* For each tweet, sum up loglikelihoods of each word in the tweet.
* Also add the logprior to this sum to get the predicted sentiment of that tweet.

$$ p = logprior + \sum_i^N (loglikelihood_i)$$

#### Note
Note we calculate the prior from the training data, and that the training data is evenly split between positive and negative labels (4000 positive and 4000 negative tweets).  This means that the ratio of positive to negative 1, and the logprior is 0.

The value of 0.0 means that when we add the logprior to the log likelihood, we're just adding zero to the log likelihood.  However, please remember to include the logprior, because whenever the data is not perfectly balanced, the logprior will be a non-zero value.
"""

def naive_bayes_predict(post, logprior, loglikelihood):
    '''
    Input:
        tweet: a string
        logprior: a number
        loglikelihood: a dictionary of words mapping to numbers
    Output:
        p: the sum of all the logliklihoods of each word in the tweet (if found in the dictionary) + logprior (a number)

    '''
    # process the tweet to get a list of words
    word_l = process_post(post)

    # initialize probability to zero
    p = 0

    # add the logprior
    p += logprior

    for word in word_l:

        # check if the word exists in the loglikelihood dictionary
        if word in loglikelihood:
            # add the log likelihood of that word to the probability
            p += loglikelihood[word]

    return p

# Experiment with your own post.
my_post = 'She smiled.'
p = naive_bayes_predict(my_post, logprior, loglikelihood)
print('The expected output is', p)

def test_naive_bayes(test_x, test_y, logprior, loglikelihood):
    """
    Input:
        test_x: A list of tweets
        test_y: the corresponding labels for the list of tweets
        logprior: the logprior
        loglikelihood: a dictionary with the loglikelihoods for each word
    Output:
        accuracy: (# of tweets classified correctly)/(total # of tweets)
    """
    accuracy = 0  # return this properly

    y_hats = []
    for post in test_x:
        # if the prediction is > 0
        if naive_bayes_predict(post, logprior, loglikelihood) > 0:
            # the predicted class is 1
            y_hat_i = 1
        else:
            # otherwise the predicted class is 0
            y_hat_i = 0

        # append the predicted class to the list y_hats
        y_hats.append(y_hat_i)

    # error is the average of the absolute values of the differences between y_hats and test_y
    differences = []
    for i in range(len(y_hats)):
      differences.append(np.absolute(test_y[i] - y_hats[i]))
    error = sum(differences) / len(differences)

    # Accuracy is 1 minus the error
    accuracy = 1 - error

    return accuracy

print("Naive Bayes accuracy = %0.4f" % (test_naive_bayes(test_x, test_y, logprior, loglikelihood)))

# Run this cell to test your function
for post in ['I am happy', 'I am bad', 'this movie should have been great.', 'great', 'great great', 'great great great', 'great great great great', 'bad worst bad worst bad worst', 'bad worst bad great bad worst']:
    # print( '%s -> %f' % (tweet, naive_bayes_predict(tweet, logprior, loglikelihood)))
    p = naive_bayes_predict(post, logprior, loglikelihood)
#     print(f'{tweet} -> {p:.2f} ({p_category})')
    print(f'{post} -> {p:.2f}')

"""# **Error Analysis**

In this part you will see some tweets that your model missclassified. Why do you think the misclassifications happened? Were there any assumptions made by the naive bayes model?
"""

# Some error analysis done for you
print('Truth Predicted Tweet')
for x, y in zip(test_x, test_y):
    y_hat = naive_bayes_predict(x, logprior, loglikelihood)
    if y != (np.sign(y_hat) > 0):
        print('%d\t%0.2f\t%s' % (y, np.sign(y_hat) > 0, ' '.join(
            process_post(x)).encode('ascii', 'ignore')))

"""# **Predict with your own tweet**"""

# Test with your own tweet - feel free to modify `my_tweet`
my_post = 'I am happy because I am learning :)'

p = naive_bayes_predict(my_post, logprior, loglikelihood)
print(p)

