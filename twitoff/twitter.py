from os import getenv
import basilica
import twitter_scraper
from dotenv import load_dotenv
from .db_model import db, User, Tweet








BASILICA = basilica.Connection(getenv('BASILICA_KEY'))

def add_user_twitter_scraper(username):
    """Add a user and their tweets to database."""
    try:
        # Get user profile   
        user_profile = list(get_tweets(username, pages=25))

        # add to user table (or check if existing)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        username=username,
                        followers_count=twitter_user.followers_count))
        db.session.add(db_user)

        # Get most recent tweets
        tweets = list(get_tweets(username, pages=10))
        original_tweets = [d for d in tweets if d['username']==username]

        # add newest tweet id to the user table
        if tweets:
            db_user.newest_tweet_id = tweets[0.id]

        # Get an example Basilica embedding for first tweet
        # embedding = BASILICA.embed_sentence(original_tweets[0]['text'], model='twitter')
            
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e

    return original_tweets, embedding




    from os import getenv
import basilica
import tweepy  # or twitter_scraper
from dotenv import load_dotenv
from .db_model import db, User, Tweet
load_dotenv()
TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_CONSUMER_KEY'),
                                   getenv('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(getenv('TWITTER_ACCESS_TOKEN'),
                              getenv('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(getenv('BASILICA_KEY'))
def add_user_tweepy(username):
  '''Add a user and their tweets to database'''
  try:
    # Get user info from tweepy
    twitter_user = TWITTER.get_user(username)
    # Add to User table (or check if existing)
    db_user = (User.query.get(twitter_user.id) or
               User(id=twitter_user.id,
                    username=username,
                    followers=twitter_user.followers_count))
    db.session.add(db_user)
    # Get tweets ignoring re-tweets and replies
    tweets = twitter_user.timeline(count=200,
                                   exclude_replies=True,
                                   include_rts=False,
                                   tweet_mode='extended'
                                   since_id=db_user.newest_tweet_id)
    # Add newest_tweet_id to the User table
    if tweets:
        db_user.newest_tweet_id = tweets[0].id
    # Loop over tweets, get embedding and add to Tweet table
    for tweet in tweets:
        # Get an examble basilica embedding for first tweet
        embedding = BASILICA.embed_sentence(tweets[0].full_text, model='twitter')
        # Add tweet info to Tweet table
        db_tweet = Tweet(id=tweet.id,
                         text=tweet.full_text[:300],
                         embedding=embedding)
        db_user.tweet.append(db_tweet)
        db.session.add(db_tweet)
  except Exception as e:
    print('Error processing {}: {}'.format(username, e))
    raise e
  else:
      db.session.commit()
  return tweets, embedding