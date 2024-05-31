from urlextract import URLExtract
extract = URLExtract()
import pandas as pd
from collections import Counter
import regex


def fetch_stats (selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # df['message'] = df['message'].astype(str).fillna("")
    # using loc methond 
    df.loc[:, 'message'] = df['message'].astype(str).fillna("")

    # fetch the total number of message
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'].str.contains('<Media omitted>')].shape[0]

    # fetch number of links  shared
    links = []
    
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)


# helper
def most_busy_users(df):

    top_users_series = df['user'].value_counts().head(5)
    top_users_df = top_users_series.reset_index()

    # Renaming columns correctly
    top_users_df.columns = ['Candidate', 'count']

    # Calculate the percentage of total occurrences for each user
    percentages = round((df['user'].value_counts() / df.shape[0]) * 100, 2)
    percentages_df = percentages.reset_index().rename(columns={'index': 'Candidate', 'user': 'percent'})

    return top_users_df,percentages_df


def most_common_words(selected_user,df):

    f = open('backend/whatsappAnalyserFiles/stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', case=False)]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in regex.findall(r'\p{Emoji}', message) if not (c.isdigit() or c.isalpha() or c == '*')])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap