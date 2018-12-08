
import csv
import pickle
from nltk.tokenize import word_tokenize
from VoteClassifier import VoteClassifier

class get_sentiment:
    def __init__(self):

        self.word_features=self.load_pickle("word_features.pickle")
        self.classifier=self.load_pickle("originalnaivebayes.pickle")
        self.MNB_classifier=self.load_pickle("MNB_classifier.pickle")
        self.BernoulliNB_classifier=self.load_pickle("BernoulliNB_classifier.pickle")
        self.LogisticRegression_classifier=self.load_pickle("LogisticRegression_classifier.pickle")
        self.LinearSVC_classifier=self.load_pickle("LinearSVC_classifier.pickle")
        self.SGDC_classifier=self.load_pickle("SGDC_classifier.pickle")

    def find_features(self,document):
        word = word_tokenize(document)
        features = {}
        for w in self.word_features:
            features[w] = (w in word)

        return features

    def load_pickle(self,filename):
        open_file = open(filename,"rb")
        classifier = pickle.load(open_file)
        open_file.close()
        return classifier

      
    def sentiment(self,text):
        feats = self.find_features(text)
        voted_classifier = VoteClassifier(self.classifier, self.MNB_classifier, self.BernoulliNB_classifier, self.LogisticRegression_classifier, self.SGDC_classifier, self.LinearSVC_classifier)
        csv_add=[]
        csv_add=voted_classifier.classify_v(feats)
        csv_add.append(voted_classifier.classify(feats))
        csv_add.append(voted_classifier.confidence(feats)*100)
        print(csv_add)
       
        csv_add.append(text.encode("utf-8"))
        csv_add.append("Facebook")
        print(csv_add)
        with open("twitter_1.csv", "a",newline='') as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(csv_add)
        return voted_classifier.classify(feats),voted_classifier.confidence(feats)
