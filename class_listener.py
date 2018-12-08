from tweepy.streaming import StreamListener

from class_preprocessing import preprocessing
from get_sentiment import get_sentiment

class listener(StreamListener):
    def __init__(self, api=None):
        self.ob=preprocessing()
        self.ob1=get_sentiment()
        super(listener, self).__init__()
        self.num_tweets = 0
    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
                try:
                        self.tweet = status.retweeted_status.extended_tweet["full_text"]
                except:
                        self.tweet = status.retweeted_status.text
        else:
                try:
                        self.tweet = status.extended_tweet["full_text"]
                except AttributeError:
                        self.tweet = status.text
        if status.coordinates:
            print ('coords:', status.coordinates)
        if status.place:
            print ('place:', status.place.full_name)
        self.tweet=self.ob.BMP(self.tweet)
        self.tweet=self.ob.processTweet2(self.tweet)
        user_location = status.user.location
        print("Name",status.user.screen_name)
        print("Location",user_location)
        print("Followers ",status.user.followers_count)
        print("Retweet Count",status.retweet_count)


        sentiment_value, confidence = self.ob1.sentiment(self.tweet)
        print(self.tweet, sentiment_value, confidence)

        if (confidence*100>=80):
            output = open("twitter-out.txt","a")
            output.write(sentiment_value)
            output.write("\n")
            output.close()

        
        
        print("\n\n")
        self.num_tweets += 1
        if self.num_tweets < 10:
            return True
        else:
            return False
        
    def on_error(self, status):
        print(status)
