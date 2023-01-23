import re
import pandas as pd

def preprocess (data):

    time_pattern = '\[\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}:\d{1,2}\s\w{2}\]\s'

    messages = re.split(time_pattern, data)[1:]

    pattern1 = r':'
    pattern2 = r'created this group'
    pattern3 = r"joined using this group's invite link"
    pattern4 = r"changed this group's icon"
    pattern5 = r"added"
    pattern6 = r"left"

    person = []
    text = []

    patterns_to_delete = ['\u200e\u202a', '\xa0', '\u202c', '\u200e', '\u202a']

    for i in range(len(messages)):
        for letter in patterns_to_delete:
            messages[i] = messages[i].replace(letter, '')

        pattern = (re.split(r'{}|{}|{}|{}|{}|{}'.format(pattern1, pattern2, pattern3, pattern4, pattern5, pattern6), messages[i]))
        person.append(pattern[0])
        text.append(pattern[1:])

    time_stamp = re.findall(r'\[\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}:\d{1,2}\s\w{2}\]\s', data)
    df = pd.DataFrame({"User": person, "Message": text, "Date": time_stamp})

    df['Message'] = df['Message'].apply(lambda x: ' '.join(x))
    df['Date'] = df['Date'].str.extract(r'\[(.*?)\]', expand=False)
    df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%y, %I:%M:%S %p")

    df['User'] = df['User'].replace('You', '~anika()')

    df['User'] = df['User'].str.strip()
    df['Message'] = df['Message'].str.strip()

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Month_num'] = df['Date'].dt.month
    df['Only_Date'] = df['Date'].dt.date
    df['DayOfTheWeek'] = df['Date'].dt.day_name()
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period = []
    for hour in df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['Period'] = period

    return df