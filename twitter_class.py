from tweepy import Stream
from tweepy import OAuthHandler
from class_listener import listener


class twitter:
#consumer key, consumer secret, access token, access secret.
    def  __init__(self):
        self.ckey=""
        self.csecret=""
        self.atoken=""
        self.asecret=""



    def get_tweets(self):
        auth = OAuthHandler(self.ckey, self.csecret)
        auth.set_access_token(self.atoken, self.asecret)

        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["Facebook","facebook"], languages = ["en"], stall_warnings = True)
