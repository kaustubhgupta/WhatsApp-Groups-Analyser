import re
import pandas as pd
import emoji
from collections import Counter
import datetime


class ExtractDataFrame:

    '''
    This module will help parsing the whatsapp chats data.
    Parameters:
        File_path (string): The path of the chats files
    Functions:
        Note: Object here refers to self

        load_file(object) -> File pointer
        is_newEntry(object, string) -> Boolean
        seperateData(object, string) -> Tuple
        process(object) -> NA
        emojis(object, string) -> List
        dataframe(object) -> Pandas DataFrame
    '''

    def __init__(self, file_path):
        '''
        Initializes the file path and data variable holding whole parsed data
        '''
        self.path = file_path
        self.data = []

    def load_file(self):
        '''
        This function loads the chat file
        '''
        file = open(self.path, 'r', encoding='utf-8')
        return file

    def is_newEntry(self, line: str) -> bool:
        '''
        This function returns if the line is a new message or continuation of the previous one
        '''
        date_time = '([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        test = re.match(date_time, line)
        if test is not None:
            return True
        else:
            return False

    def seperateData(self, line: str) -> tuple:
        '''
        This function cleans the line and seperates the author, date, time and message from the text
        '''
        entry_data = line.split(' - ')
        date, time = entry_data[0].split(', ')
        authMsg = entry_data[1].split(':')
        if len(authMsg) > 1:
            author = authMsg[0]
            message = ' '.join(authMsg[1:])
            return (date, time, author, message)
        else:
            return None

    def process(self):
        '''
        This functions aggregates all the data from different lines
        '''
        f = self.load_file()
        f.readline()
        full_message = []
        date = ''
        time = ''
        author = ''
        while True:
            line = f.readline()
            if not line:
                break

            if self.is_newEntry(line):

                if len(full_message) > 0:
                    temp = ' '.join(full_message)
                    modified_replaced = temp.replace('\n', ' ')
                    self.data.append([date, time, author, modified_replaced])

                full_message.clear()
                received = self.seperateData(line)
                if received is not None:
                    date, time, author, message = received
                    full_message.append(message)
            else:
                full_message.append(line)

        f.close()

    def emojis(self, msg: str) -> list:
        '''
        This function returns the list of emojis present in a message. 
        Note: This will recoginize some of the hindi characters as emojis.
        '''
        final_list = []
        for char in msg:
            if char in emoji.UNICODE_EMOJI:
                final_list.append(char)

        if len(final_list) == 0:
            return 0
        else:
            return final_list

    def dataframe(self) -> object:
        '''
        This function returns processed data in Pandas dataframe
        '''
        df = pd.DataFrame(self.data, columns=[
                          'Date', 'Time', 'Author', 'Message'])
        df['Date'] = pd.to_datetime(df.Date)
        df['Emojis'] = df.Message.apply(self.emojis)
        df['Emoji_num'] = df.Emojis.str.len()
        return df


class GenerateStats:

    '''
    This class of functions will be used to generate stats for any dataframe. 
    Full Group chats, any specific timeline or explicitly mentioned.
    Parameters:
        df (dataframe object): In all functions, only this needs to be passed.
    Functions:
        Note: Object here refers to self

        mediaRatio(object, dataframe) -> int
        totalEmojis(object, dataframe) -> int
        uniqueEmojis(object, dataframe) -> int
        frequentEmojis(object, dataframe) -> dataframe
        activeMembers(object, dataframe) -> dataframe
        lazyMembers(object, dataframe) -> dataframe
        activityOverDates(object, dataframe) -> dataframe
        activityOverTime(object, dataframe) -> dataframe
        holidaysDataFrame(object, dataframe) -> dict
        nightOwls_earlyBirds(object, dataframe) -> dict
        emojiCon_Emojiless(object, dataframe) -> dict
    '''

    def __init__(self):
        '''
        Here all the important initializations are done
        '''
        self.holidays_dict = {datetime.date(2020, 1, 14): 'Makar Sankranti / Pongal',
                              datetime.date(2020, 1, 26): 'Republic Day',
                              datetime.date(2020, 8, 15): 'Independence Day',
                              datetime.date(2020, 10, 2): 'Gandhi Jayanti',
                              datetime.date(2020, 12, 25): 'Christmas',
                              }

    def mediaRatio(self, df) -> int:
        '''
        This function returns the percentage of messages which are media
        '''
        return ((df[df['Message'] == ' <Media omitted> '].Message.count()) / (df.Message.count()))*100

    def totalEmojis(self, df) -> int:
        '''
        This function returns the total number of emojis in the group
        '''
        return len([i for j in df.Emojis[df.Emojis != 0] for i in j])

    def uniqueEmojis(self, df) -> int:
        '''
        This function returns the number unique emojis sent.
        '''
        return len(set([i for j in df.Emojis[df.Emojis != 0] for i in j]))

    def frequentEmojis(self, df) -> object:
        '''
        This function returns dataframe object consisting of frequent emojis of the group.
        If there are less than 10 frequent emojis then whole dataframe is returned
        '''
        emojiList = [i for j in df.Emojis[df.Emojis != 0] for i in j]
        emoji_dict = dict(Counter(emojiList))
        emoji_dict = sorted(emoji_dict.items(),
                            key=lambda x: x[1], reverse=True)
        emoji_df = pd.DataFrame(emoji_dict, columns=['Emoji', 'Count'])
        if emoji_df.shape[0] < 10:
            return emoji_df
        else:
            return emoji_df[:10]

    def activeMembers(self, df) -> object:
        '''
        This function returns dataframe object consisting of active members of the group.
        If there are less than 8 active members then whole dataframe is returned
        '''
        authors = pd.DataFrame(df.Author.value_counts())
        authors = authors.rename(columns={'Author': 'Message Count'})
        authors.index.name = 'Author'
        if authors.shape[0] < 8:
            return authors
        else:
            return authors[:8]

    def lazyMembers(self, df) -> object:
        '''
        This function returns dataframe object consisting of lazy members of the group.
        If there are less than 5 lazy members then whole dataframe is returned
        '''
        authors = pd.DataFrame(df.Author.value_counts())
        authors = authors.rename(columns={'Author': 'Message Count'})
        authors.index.name = 'Author'
        if authors.shape[0] < 5:
            return authors[::-1]
        else:
            return authors[-5:][::-1]

    def activityOverDates(self, df) -> object:
        '''
        This function returns dataframe of activity of the group over the 
        all the dates
        '''
        result = df.groupby('Date').sum()
        result = result.rename(columns={'Emoji_num': 'Number of Messages'})
        return result

    def activityOverTime(self, df) -> object:
        '''
        This function returns dataframe of activity of the group over the 
        all whole day
        '''

        result = df.groupby('Time').sum()
        result = result.rename(columns={'Emoji_num': 'Number of Messages'})
        return result

    def holidaysDataFrame(self, df) -> dict:
        '''
        Returns dict of dataframes which matches the holidays date pattern
        '''
        df_dict = {}
        for date, event in self.holidays_dict.items():
            temp = df[(df.Date.dt.day == date.day) &
                      (df.Date.dt.month == date.month)]
            df_dict[event] = temp

        return df_dict

    def nightOwls_earlyBirds(self, df) -> dict:
        '''
        This function will returns dict of two dataframes with authors who send most
        messages in night between 11 pm to 3 am and between 6 am to 9 am in the
        morning.
        If there are less than 5 members then whole dataframe is returned        
        '''
        df_dict_n = {}
        temp = pd.to_datetime(df.Time)
        morning_mask = (temp.dt.hour >= 6) & (temp.dt.hour <= 9)
        night_mask = ~((temp.dt.hour >= 3) & (temp.dt.hour <= 23))
        df_dict_n['morning'] = pd.DataFrame(
            df[morning_mask].Author.value_counts())
        df_dict_n['night'] = pd.DataFrame(df[night_mask].Author.value_counts())
        df_dict_n['morning'] = df_dict_n['morning'].rename(
            columns={'Author': 'Message Count'})
        df_dict_n['night'] = df_dict_n['night'].rename(
            columns={'Author': 'Message Count'})
        df_dict_n['night'].index.name = df_dict_n['morning'].index.name = 'Author'

        if df_dict_n['morning'].shape[0] > 5:
            df_dict_n['morning'] = df_dict_n['morning'][:5]

        if df_dict_n['night'].shape[0] > 5:
            df_dict_n['night'] = df_dict_n['night'][:5]

        return df_dict_n

    def emojiCon_Emojiless(self, df) -> dict:
        '''
        This function will returns dict of two dataframes with authors who send most
        emojis and least emojis.
        If there are less than 6 members then whole dataframe is returned        
        '''
        df_dict_n2 = {}
        temp2 = pd.DataFrame(df.groupby(
            'Author').Emoji_num.sum().sort_values(ascending=False))
        temp2 = temp2.rename(columns={'Emoji_num': 'Number of Emojis'})
        if temp2.shape[0] > 6:
            df_dict_n2['Emoji_con'] = temp2[:6]
            df_dict_n2['Emoji_less'] = temp2[-6:][::-1]
        else:
            df_dict_n2['Emoji_con'] = df_dict_n2['Emoji_less'] = temp2

        return df_dict_n2
