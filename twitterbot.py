import tweepy
import logging

logger = logging.getLogger()

ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

def create_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True, compression=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
        logger.info("API created")
    return api

def fav_retweet(api):
    logger.info("Retrieving tweets...")
    mentions = api.mentions_timeline(tweet_mode = 'extended')
    for mention in reversed(mentions):
        if mention.in_reply_to_status_id is not None or mention.user.id == api.me().id:
            return
        if not mention.favorited:
            try:
                mention.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not mention.retweeted:
            try:
                mention.retweet()
            except Exception as e:
                logger.error("Error on retweets", exc_info=True)

def fav_retweet_user(api):
    search_query = f"{user_handle} -filter:retweets"
    logger.info("Retrieving tweets...")
    tweets = api.search(q=search_query, lang="en")
    for tweet in tweets:
        if tweet.in_reply_to_status_id is not None or tweet.user.id == api.me().id:
            return
        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on retweets", exc_info=True)
        while True:
            fav_retweet(api, "@StevenLeQuang7")
            time.sleep(30)
