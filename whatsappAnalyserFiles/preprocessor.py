import re
import pandas as pd


def preprocess(data):
    # Define the pattern to extract date/time and the entire message
    pattern = r'(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} *[ap]m) - (.+)'

    # Find all occurrences of the pattern in the data
    matches = re.findall(pattern, data)

    # Create a DataFrame from the extracted information
    df = pd.DataFrame(matches, columns=['Date', 'Message'])

    # Convert the "Date" column to the desired format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %I:%M %p')

    # Display the DataFrame with columns in the desired order
    df = df[['Message', 'Date']]

    users = []
    messages = []

    for message in df['Message']:
        entry = re.split('([\\w\\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['only_date'] = df['Date'].dt.date
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['Message'], inplace=True)
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df