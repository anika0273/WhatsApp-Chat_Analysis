from urlextract import URLExtract
from wordcloud import WordCloud
import nltk
import emojis
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd

extractor = URLExtract()


def fetch(selected_user, df):
    urls = []
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    num_msgs = df.shape[0]
    words = []
    for msg in df['Message']:
        words.extend(msg.split())

    image = df[df['Message'] == "image omitted"].shape[0]
    for message in df['Message']:
        urls.extend(extractor.find_urls(message))

    return num_msgs, len(words), image, len(urls)


def fetch_most_busy(df):
    x = df['User'].value_counts().head(20)
    prcnt_df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    return x, prcnt_df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    column = ' '.join(df["Message"])
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(column)
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    df1 = df[df['User'] != 'MIT Data Science']
    temp = df1[df1['Message'] != 'This message was deleted']
    temp = temp[temp['Message'] != 'image omitted']
    temp = temp[temp['Message'] != '']

    nltk_stop_words = set(stopwords.words('english'))
    nltk_stop_words = list(nltk_stop_words)
    nltk_stop_words

    stop_words = ['A', 'ABOUT', 'ACTUALLY', 'ALMOST', 'ALSO', 'ALTHOUGH', 'ALWAYS', 'AM', 'AN', 'AND', 'ANY',
                  'ARE', 'AS', 'AT', 'BE', 'BECAME', 'BECOME', 'BUT', 'BY', 'CAN', 'COULD', 'DID', 'DO', 'DOES', 'EACH',
                  'EITHER',
                  'ELSE', 'FOR', 'FROM', 'HAD', 'HAS', 'HAVE', 'HENCE', 'HOW', 'I', 'ID', 'IF', 'IM', 'I’M', 'IN', 'IS',
                  'IT', 'ITS', "IT'S", 'IT’S', 'JUST',
                  'MAY', 'MAYBE', 'ME', 'MIGHT', 'MINE', 'MUST', 'MY', 'MINE', 'MUST', 'MY', 'NEITHER', 'NOR',
                  'NOT', 'OF', 'OH', 'OK', 'ON', 'OR', 'SO', 'THE', 'THERE', 'THEIR', 'THIS', 'THAT', 'TO', 'TOO', 'U',
                  'US', 'WHAT', 'WAS',
                  'WE', 'WHEN', 'WHERE', 'WHEREAS', 'WHEREVER', 'WHENEVER', 'WHETHER',
                  'WHICH', 'WHILE', 'WHO', 'WHOM', 'WHOEVER', 'WHOSE', 'WHY', 'WILL', 'WITH', 'WITHIN',
                  'WITHOUT', 'WOULD', 'YES', 'YET', 'YOU', 'YOUR', '1', '2']
    stop_words_lower = []
    for stop in stop_words:
        stop_words_lower.append(stop.lower())


    stop_word = stop_words_lower + nltk_stop_words
    stop_word = list(set(stop_word))
    stop_word

    words = []

    for message in temp['Message']:
        message = message.replace("?", "")
        message = message.replace("..", "")
        message = message.replace(",", "")
        message = message.replace("=", "")
        message = message.replace("-", "")
        for word in message.lower().split():
            # print(word)
            if word not in stop_word:
                words.append(word)

    most_used_words = pd.DataFrame(Counter(words).most_common(500), columns=['Words', 'Frequency'])
    return most_used_words


def emoji_helper(selected_user, df):
    emoji_list = []
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    for msg in df['Message']:
        emoji_list.append(emojis.get(msg))

    list_of_strings = [", ".join(s) for s in emoji_list]
    # print(list_of_strings)
    separator = ","
    list_of_characters = [c for s in list_of_strings for c in s.split(separator)]
    to_remove = ['']

    list_of_characters = [x for x in list_of_characters if x not in to_remove]
    emoji_df = pd.DataFrame(Counter(list_of_characters).most_common(len(Counter(list_of_characters))),
                            columns=['Emoji', 'Frequency'])
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline["Time"] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    dt = df.groupby('Only_Date').count()['Message'].reset_index()
    return dt


def wk_day(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    dt = df.groupby('DayOfTheWeek').count()['Message'].reset_index()
    dt = dt.sort_values(by=['Message'])
    return dt


def monthly_activity(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    value_counts = df['Month'].value_counts()
    value_counts_df = value_counts.to_frame()
    value_counts_df = value_counts.reset_index()
    value_counts_df.columns = ['Month', 'Count']
    value_counts_df = value_counts_df.sort_values(by=['Month'])

    return value_counts_df


def heat_plot(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    activity_hm = df.pivot_table(index='DayOfTheWeek', columns='Period', values='Message', aggfunc='count').fillna(0)

    return activity_hm



