import pandas as pd

# IDK if this is pertinent
pd.options.display.width = 0
pd.options.display.max_rows = 10000
pd.options.display.max_info_columns = 10000

# Importing our Hot 100 charted song data as well as Taylor Swift spotify data
hot100_df = pd.read_csv('hot_100.csv')
songs_df = pd.read_csv('taylor_swift_songs.csv')

# Cleaning up Hot 100
hot100_df["chart_date"] = pd.to_datetime(hot100_df["chart_date"])
hot100_df = hot100_df[hot100_df['performer'].str.contains('Taylor Swift')]
hot100_df = hot100_df.groupby('song').last().sort_values('peak_position', ascending=True)
hot100_df = hot100_df.drop(['performer', 'song_id', 'chart_url', 'chart_date', 'instance', 'previous_week', 'chart_position'], axis=1)

# Selecting only studio albums
albums = ['Taylor Swift', 'Fearless', 'Speak Now', 'Red', '1989', 'reputation', 'Lover', 'evermore', 'folklore', 'Midnights']

# Merging Hot 100 and Taylor Swift Spotify data
ts_df = pd.merge(songs_df, hot100_df, how='outer', on='song')
ts_df = ts_df[ts_df['album'].isin(albums)]
ts_df = ts_df.sort_values('popularity', ascending=False).drop_duplicates('song').sort_index()
ts_df = ts_df.fillna(0)

# Export completed dataframe to csv
ts_df.to_csv('taylor_swift.csv')




