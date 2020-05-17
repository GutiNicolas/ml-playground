import pandas as pd
import sklearn.model_selection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import ml_utils as MLUtils

pd.set_option('display.max_columns', 5)
data_set = pd.read_csv("data/spam_data/data.csv", sep=";")
data_set['category'] = data_set['category'].apply(MLUtils.map_bool)

filtered_bow = CountVectorizer(analyzer=MLUtils.filter_and_transform).fit_transform(data_set['text'])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(filtered_bow, data_set['category'], test_size=0.2)

classifier = MultinomialNB()
classifier.fit(x_train, y_train)

print(classifier.predict(x_train))
print(y_train.values)
pred = classifier.predict(x_train)
print(classification_report(y_train, pred))
print('\nAccuracy: ', accuracy_score(y_train, pred))
print('\n Loading Predictions...\n')

actual = classifier.predict(x_test)
expected = y_test.values
for i in range(3, 10):
    print('Predicted value: {} ({}) \n Expected: {} ({})\n'.format(MLUtils.easy_read(actual[i]), actual[i], MLUtils.easy_read(expected[i]), expected[i]))

total = 0
for i in range(0, len(y_test.values)):
    if actual[i] != expected[i]:
        total= total+1

print('Found {} mismatchs on a total of {} with {}% accuracy'.format(total, len(y_test.values), accuracy_score(y_train, pred)))







