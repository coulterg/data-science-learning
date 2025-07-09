import csv
import string
import math

from collections import defaultdict

emails = []
labels = []

with open('test_emails.csv', 'r', newline='\n') as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:

        text, label = row
        emails.append(text)
        labels.append(label.strip().lower())

def tokenize(text):
    # Convert to lowercase, remove punctuation, and split

    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    return tokens

tokenized_emails = [tokenize(email) for email in emails]

# need word count *per class* (spam/no spam) for frequencies

# let's set up a nested structure. Word_count_per_class is a dict which will contain two keys,
# spam and not spam, each of which will map to a dictionary of words with counted totals
word_counts_per_class = defaultdict(lambda: defaultdict(int))

for email, label in zip(tokenized_emails, labels):
    for word in email:
        word_counts_per_class[label][word] += 1

# print(word_counts_per_class)

'''
Naive Bayes - we want to compute the probability of a class of an email (spam or not spam)
given its contents. As there are two classes, the probs will sum to 1 so let's just look at spam.
P(spam | features) = P(spam) * P(features | spam) / P(features)
Naaive assumption that feature probabilities are independent of each otehr
P(features | spam) = product(P(word1 | spam),..., P(wordn | spam))
So we calculate score = P(class) * P(features | class) for each class. Whichever is larger is what we choose
If we want probability we normalise by dividing by sum of all scores
So we need:
    Prior: P(spam) and P(not spam)
    Likelihood: P(word | spam) and P(word | not spam)
                = word_count_spam / total_words_spam and etc'''

# Priors
    
classes = set(labels)  # unique classes (spam, not spam)
total_emails = len(emails)

prior_probabilities = {label: labels.count(label) / total_emails for label in classes}

print("Prior Probabilities:", prior_probabilities)

# Likelihoods

total_words_per_class = defaultdict(int)

for label, word_counts in word_counts_per_class.items():
    total_words_per_class[label] = sum(word_counts.values())
    
# print("Total words per class:", total_words_per_class)

likelihoods = defaultdict(lambda: defaultdict(float))
for label, word_counts in word_counts_per_class.items():
    for word, count in word_counts.items():
        likelihoods[label][word] = count / total_words_per_class[label]

# print("Likelihoods:", likelihoods)

def score(email):
    # returns dictionary of class: score

    tokens = tokenize(email)

    scores = defaultdict(float)

    # Need to calculate scores for each class given token features

    for label in classes:
        #P(class) * P(features | class)
        score = prior_probabilities[label]
        print(f'{label} prior: {score}')

        for feature in tokens:
            score *= likelihoods[label][feature]

            print(f'New score: {score}')

        scores[label] = score

    return scores

def classify(email):

    scores = score(email)

    print(scores)
    print(max(scores))

    return max(scores)


print('Email: ' + classify('to'))

