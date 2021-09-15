import streamlit as st
import pandas as pd
import yaml
import duolingo
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager
matplotlib.font_manager._rebuild()
matplotlib.rcParams['font.family'] = ['Heiti TC']

with open("duo_credentials.yaml", 'r') as stream:
    creds = yaml.safe_load(stream)

lingo  = duolingo.Duolingo(creds['username'], creds['password'])
st.write("Hello :wave: " + lingo.get_user_info()['username'])

st.header("Streak Info")
streak = lingo.get_streak_info()
xp = lingo.get_daily_xp_progress()
st.write(str(streak['site_streak']) + " days")
streak_pct = xp['xp_today'] / xp['xp_goal']
streak_pct = streak_pct if streak_pct < 1 else 1.00
st.write('Daily Streak Progress')
st.progress(streak_pct)

st.header("Calendar")
cal = lingo.get_calendar('zs')
calendar_df = pd.DataFrame.from_records(cal)
calendar_df.sort_values(by='datetime', ascending=False, inplace=True)
calendar_df['datetime'] = calendar_df['datetime'].apply(lambda x: pd.to_datetime(x, unit='ms').date())
fig = plt.figure(figsize=(10,6))
ax = sns.barplot(data=calendar_df, x='datetime', y='improvement', estimator=sum, ci=None)
st.write(fig)

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

vocab = lingo.get_vocabulary()
vocab_data = []
for word in vocab['vocab_overview']:
    vocab_data.append([word['normalized_string'].strip(), word['word_string'], word['strength'], word['skill_url_title']])
vocab_df = pd.DataFrame(vocab_data, columns=['word', 'character', 'strength', 'skill'])
vocab_df.sort_values(by='strength', inplace=True)
fig = plt.figure(figsize=(15,20))
ax = sns.barplot(x="strength", y="character", data=vocab_df.iloc[:20],
                 hue='skill', ci=None)
plt.xticks(fontsize=20);
plt.yticks(fontsize=20);
plt.xlabel('character', fontsize=20);
plt.ylabel('strength', fontsize=20);
plt.legend(fontsize=16);
st.write(fig)