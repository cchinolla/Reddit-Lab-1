import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='Xi9GO7ThWakVxQ',
                     client_secret='Bo980RDjTUolyKWoe1z1PblUnlg',
                     user_agent='my user agent'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


# given probability methods
def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()
    return submission.comments

# TO TEST TO SEE IF IT RECURSIVELY WENT THROUGH WHOLE THREAD
def test_process_comments(comments_list):
    # for loop to traverse through comments list
    for comments in comments_list:
        print(comments.body)
        process_comments(comments.replies)

# TO TEST IF IT APPENDED A LIST
def test_append_list(s, n_list):
    if get_text_negative_proba(s) > get_text_neutral_proba(s) and get_text_negative_proba(s) > get_text_positive_proba(s):
        # append to neg list if prob is higher than the other two methods
        n_list.append(s)




# create process_comments method that would recursively implement probability methods through whole Reddit thread
def process_comments(comments_list, negative_list, positive_list, neutral_list):
    # for loop to traverse through comments list
    for comments in comments_list:
        # if statement to compare neg prob method to other two methods
        if get_text_negative_proba(comments.body) > get_text_neutral_proba(comments.body) and get_text_negative_proba(comments.body) > get_text_positive_proba(comments.body) :
            # append to neg list if prob is higher than the other two methods
            negative_list.append(comments.body)

        # if statement to compare pos prob method to other two methods
        if get_text_positive_proba(comments.body) > get_text_neutral_proba(comments.body) and get_text_positive_proba(comments.body) > get_text_negative_proba(comments.body):
            # append to pos list if prob is higher than the other two methods
            positive_list.append(comments.body)

        # if statement to compare neu prob method to other two methods
        if get_text_neutral_proba(comments.body) > get_text_positive_proba(comments.body) and get_text_neutral_proba(comments.body) > get_text_negative_proba(comments.body):
            # append to neu list if prob is higher than the other two methods
            neutral_list.append(comments.body)

        # recursive call
        process_comments(comments.replies, negative_list, positive_list, neutral_list)



def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')

    # TEST TO SEE IF IT RECURSIVELY WENT THROUGH WHOLE THREAD
    # process_comments(comments)

    # TO TEST IF COMMENT APPENDED LIST
    # s= "i hate you"
    # n_list = []
    # test_append_list(s, n_list)
    # print(n_list)

    # create new lists to hold neg, pos, and neu comments
    negative_list = []
    positive_list = []
    neutral_list = []

    # call recursive methods
    process_comments(comments, negative_list, positive_list, neutral_list)

    # print negative list
    print("Negative list:")
    print(*negative_list, sep="\n")
    print("\n")

    # print positive list
    print("Positive list:")
    print(*positive_list, sep="\n")
    print("\n")

    # print neutral list
    print("Neutral list:")
    print(*neutral_list, sep="\n")


main()
