import pickle
import requests
from instascrape import *
filename = 'comment_classifier.sav'

# https://www.youtube.com/watch?v=yebUIymZJm0
with open(filename, 'rb') as file:
    loaded_pickle = pickle.load(file)
    print(loaded_pickle)

import tweepy
import csv

# Twitter API credentials
consumer_key = "###########"
consumer_secret = "################"
access_key = "#################"
access_secret = "#####################"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
user_name = "@nameofuser"

replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name),
                                since_id=tweet_id, tweet_mode='extended').items()
while True:
    try:
        reply = replies.next()
        if not hasattr(reply, 'in_reply_to_status_id_str'):
            continue
        if reply.in_reply_to_status_id == tweet_id:
           logging.info("reply of tweet:{}".format(reply.full_text))

    except tweepy.RateLimitError as e:
        logging.error("Twitter api rate limit reached".format(e))
        time.sleep(60)
        continue

    except tweepy.TweepError as e:
        logging.error("Tweepy error occured:{}".format(e))
        break

    except StopIteration:
        break

    except Exception as e:
        logger.error("Failed while fetching replies {}".format(e))
        break
def main():
    get_all_tweets("tartecosmetics")


if __name__ == '__main__':
    main()

