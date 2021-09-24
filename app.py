import streamlit as st
import pandas as pd
import yaml
import duolingo
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager
from datetime import timezone, timedelta
matplotlib.rcParams['font.family'] = ['Source Han Sans CN']

with open("duo_credentials.yaml", 'r') as stream:
    creds = yaml.safe_load(stream)

lingo  = duolingo.Duolingo(creds['username'], creds['password'])
st.write("Hello :wave: " + lingo.get_user_info()['username'])

streak = lingo.get_streak_info()
xp = lingo.get_daily_xp_progress()

st.header("Calendar")
cal = lingo.get_calendar('zs')
cal_df = pd.DataFrame.from_records(cal)
# creating new datetime-based features
# cal_df['timestamp'] = cal_df['datetime'].apply(lambda x: pytz.timezone("America/New_York").localize(pd.to_datetime(x, unit='ms'), is_dst=None))
cal_df['timestamp'] = cal_df['datetime'].apply(lambda x: pd.to_datetime(x, unit='ms') - timedelta(hours=4))
cal_df['year'] = cal_df.timestamp.dt.year
cal_df['month'] = cal_df.timestamp.dt.month
cal_df['hour'] = cal_df.timestamp.dt.hour
cal_df['weekday'] = cal_df.timestamp.dt.day_name()
cal_df['week_num'] = cal_df['timestamp'].apply(lambda x: x.isocalendar()[1] % 52)

# get weekday_num in order of MTWTFSS because we want to sort the rows of the heatmap in order
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
mapping = {k: v for k, v in zip(weekday_order, [i+1 for i in range(7)])}
cal_df['weekday_num'] = cal_df['weekday'].apply(lambda x: mapping[x])
# st.dataframe(cal_df)

df_to_pivot = cal_df[['week_num', 'weekday_num', 'improvement']]
pivoted_data = pd.pivot_table(df_to_pivot, values='improvement', index=['weekday_num'], columns=['week_num'], aggfunc=sum)
pivoted_data = pivoted_data.reindex([i+1 for i in range(max(pivoted_data.columns))], axis=1)
pivoted_data.dropna(axis=1, how='all', inplace=True)
# st.dataframe(pivoted_data)

fig = plt.figure(figsize=(6,4));
sns.heatmap(pivoted_data, linewidths=6, cmap='BuGn', cbar=True,
                 linecolor='white', square=True, yticklabels=weekday_order);
            # xticklabels=[*space, 'Jan', *space, 'Feb', *space, 'Mar', *space, 'Apr', 
                        #  *space, 'May', *space, 'Jun', *space, 'Jul']);
plt.ylabel("");
plt.xlabel("");
st.write(fig)

# cal_df.sort_values(by='datetime', ascending=False, inplace=True)
# cal_df['datetime'] = cal_df['datetime'].apply(lambda x: pd.to_datetime(x, unit='ms').date())
# fig = plt.figure(figsize=(10,6))
# ax = sns.barplot(data=cal_df, x='datetime', y='improvement', estimator=sum, ci=None)
# st.write(fig)

st.header("Language Details")
ld = lingo.get_language_details('Chinese')
lp = lingo.get_language_progress('zs')
st.write("Streak: ", ld['streak'], " :fire:")
st.write("Total points: ", ld['points'], " 📈")
st.write("Skills learned: ", lp['num_skills_learned'], " :seedling:")
st.write("Current level: ", ld['level'], " 🤓")
st.write('Progress towards next level: ', lp['level_progress'], '/', lp['level_points'])
st.progress(lp['level_percent'])

st.header('Known Topics')
st.write(', '.join(lingo.get_known_topics('zs')))

st.header('Known Words')
st.write(', '.join(lingo.get_known_words('zs')))
