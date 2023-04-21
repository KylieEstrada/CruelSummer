import pandas as pd

pd.options.display.width = 0
pd.options.display.max_rows = 10000
pd.options.display.max_info_columns = 10000

hot100_df = pd.read_csv('hot_100.csv')
ts_df = pd.read_csv('taylor_swift_songs.csv')

hot100_df["chart_date"] = pd.to_datetime(hot100_df["chart_date"])
hot100_df = hot100_df[hot100_df['performer'].str.contains('Taylor Swift')]
hot100_df = hot100_df.groupby('song').last().sort_values('peak_position', ascending = True)
hot100_df = hot100_df.drop(['performer', 'song_id', 'chart_url', 'chart_date', 'instance', 'previous_week', 'chart_position'], axis=1)
hot100_df = hot100_df.fillna(0)

pd.merge(ts_df, hot100_df, on='business_id', how='outer')

print(result.head(10))