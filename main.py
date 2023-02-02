#####
# for this to ever work at scale, the logfiles cannot actually be loaded into memory all at once,
# but instead wrapped behind an iterable generator that dynamically loads, reads, and unloads
# them as the fitting takes place. What to do with the featurized text, I do not know.
#
# also, as more rxns are added their numbers in the filenames will need to be increased
#####

import time


def print_time_since(in_time):
    out_time = time.time()
    print("Execution time: {:.2f} seconds".format(out_time - in_time))
    return out_time


import numpy as np

import pickle

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix

from preprocess_logs import preprocess_logs

# start tracking the time
curr_time = time.time()

# pre-processing data
print("\nPreprocessing data", flush=True)
logfile_text, target_bools = preprocess_logs()
curr_time = print_time_since(curr_time)

# calling CountVectorizer
print("\nCalling CountVectorizer", flush=True)
count_vect = CountVectorizer(analyzer="char")
x_train_counts = count_vect.fit_transform(logfile_text)
curr_time = print_time_since(curr_time)

# calling TfidTransformer
print("\nCalling TfidTransformer", flush=True)
tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
curr_time = print_time_since(curr_time)

# splitting into training and testing data
print("\nCalling train_test_split", flush=True)
train_x, test_x, train_y, test_y = train_test_split(
    x_train_tfidf, target_bools, test_size=0.3
)
curr_time = print_time_since(curr_time)

# MultinomialNaiveBayes
print("\nCalling MultinomialNaiveBayes", flush=True)
clf = MultinomialNB().fit(train_x, train_y)
curr_time = print_time_since(curr_time)

# another, more different model which is reported to also work well
# clf = SVC(kernel='linear').fit(train_x, train_y)

# clf = pickle.load(open('/home/jwburns/nlp-dft/saved_models/MultinomialNB_trained_oo-only_20230127-111309.savedmodel', 'rb'))

print("\nCalling predict", flush=True)
y_score = clf.predict(test_x)
curr_time = print_time_since(curr_time)

# tabulate the results
n_right = 0
for i in range(len(y_score)):
    if y_score[i] == test_y[i]:
        n_right += 1

print("\nAccuracy: %.2f%%" % ((n_right / float(len(test_y)) * 100)))

pickle.dump(
    clf,
    open(
        "saved_models/MultinomialNB_trained_oo-only_"
        + time.strftime("%Y%m%d-%H%M%S")
        + ".savedmodel",
        "wb",
    ),
)
con_mat = confusion_matrix(test_y, y_score)

from tabulate import tabulate

print(
    tabulate(
        [
            ["fail", con_mat[0][0], con_mat[0][1]],
            ["converge", con_mat[1][0], con_mat[1][1]],
        ],
        headers=["truth/model", "fail", "converge"],
    )
)

"""
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
"""
