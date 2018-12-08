import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from nltk.tokenize import word_tokenize
from VoteClassifier import VoteClassifier

class pickling_training:
    
        short_pos = open("short_reviews/positive.txt", "r").read()
        short_neg = open("short_reviews/negative.txt", "r").read()

        all_words = []
        documents = []

        allowed_word_types = ["J"]
        word_features=[]

        def split(self):
            for p in self.short_pos.split('\n'):
                self.documents.append((p, "pos"))
                words = word_tokenize(p)
                pos = nltk.pos_tag(words)
                for w in pos:
                    if w[1][0] in self.allowed_word_types:
                        self.all_words.append(w[0].lower())

            for p in self.short_neg.split('\n'):
                self.documents.append((p, "neg"))
                words = word_tokenize(p)
                pos = nltk.pos_tag(words)
                for w in pos:
                    if w[1][0] in self.allowed_word_types:
                        self.all_words.append(w[0].lower())

            save_documents = open("document.pickle", "wb")
            pickle.dump(self.documents, save_documents)
            save_documents.close()

            self.all_words = nltk.FreqDist(self.all_words)
            self.word_features = list(self.all_words.keys())[:5000]

            save_word_features = open("word_features.pickle", "wb")
            pickle.dump(self.word_features, save_word_features)
            save_word_features.close()


        def find_features(self,document):
            words = word_tokenize(document)
            features = {}
            for w in self.word_features:
                features[w] = (w in words)

            return features

        def pickling(self,classifier,filename):
            save_classifier = open(filename, "wb")
            pickle.dump(classifier, save_classifier)
            save_classifier.close()

        def training(self):
            featuresets = [(self.find_features(rev), category) for (rev, category) in self.documents]

            random.shuffle(featuresets)
            print(len(featuresets))

            testing_set = featuresets[10000:]
            training_set = featuresets[:10000]

            save_featuresets = open("featuresets.pickle", "wb")
            pickle.dump(featuresets, save_featuresets)
            save_featuresets.close()

            classifier = nltk.NaiveBayesClassifier.train(training_set)
            print("Naive_Bayes_classifier accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
            self.pickling(classifier,"originalnaivebayes.pickle")


            MNB_classifier = SklearnClassifier(MultinomialNB())
            MNB_classifier.train(training_set)
            print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)
            self.pickling(classifier,"MNB_classifier.pickle")


            BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
            BernoulliNB_classifier.train(training_set)
            print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)
            self.pickling(classifier,"BernoulliNB_classifier.pickle")


            LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
            LogisticRegression_classifier.train(training_set)
            print("LogisticRegression_classifier accuracy percent:",(nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)
            self.pickling(classifier,"LogisticRegression_classifier.pickle")


            LinearSVC_classifier = SklearnClassifier(LinearSVC())
            LinearSVC_classifier.train(training_set)
            print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
            self.pickling(classifier,"LinearSVC_classifier.pickle")


            SGDC_classifier = SklearnClassifier(SGDClassifier())
            SGDC_classifier.train(training_set)
            print("SGDClassifier accuracy percent:", nltk.classify.accuracy(SGDC_classifier, testing_set) * 100)
            self.pickling(classifier,"SGDC_classifier.pickle")


            voted_classifier = VoteClassifier(classifier, MNB_classifier, BernoulliNB_classifier, LogisticRegression_classifier, SGDC_classifier, LinearSVC_classifier)
            print("voted_classifier accuracy percent:",(nltk.classify.accuracy(voted_classifier, testing_set))*100)


