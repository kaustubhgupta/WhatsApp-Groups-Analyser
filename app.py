from WhatsApp.functions import ExtractDataFrame, GenerateStats

chats = ExtractDataFrame('WhatsApp Chat with I-7_8.txt')
chats.process()
df = chats.dataframe()

stats = GenerateStats()
print(stats.frequentEmojis(df))