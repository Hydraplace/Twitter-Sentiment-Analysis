from nltk.classify import ClassifierI

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []        
        for c in self._classifiers:
            v = c.classify(features)
            
            votes.append(v)
        return max(set(votes), key = votes.count)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)


        choice_votes = votes.count(max(set(votes), key = votes.count))
        conf = choice_votes / len(votes)
        return conf
    def classify_v(self,features):
        csv_add=[]
        for c in self._classifiers:
            v=c.classify(features)
            csv_add.append(v)

        return csv_add
