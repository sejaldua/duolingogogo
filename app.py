import streamlit as st
import pandas as pd
import yaml
import duolingo
import seaborn as sns
import matplotlib.pyplot as plt

with open("duo_credentials.yaml", 'r') as stream:
    creds = yaml.safe_load(stream)

lingo  = duolingo.Duolingo(creds['username'], creds['password'])
st.write(lingo.get_user_info()['username'])
