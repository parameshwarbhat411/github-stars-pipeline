import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import os

FLASK_BACKEND_URL = os.getenv('FLASK_BACKEND_URL', 'http://localhost:5001')


# Helper function to plot with rolling average
def plot_with_rolling_average(df, y_col, title, ylabel, window=4):
    df['rolling_avg'] = df[y_col].rolling(window=window).mean()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='date', y='rolling_avg')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    st.pyplot(plt)


# Helper function to plot line charts with proper spacing for week-on-week growth
def plot_line_chart(df, y_col, title, ylabel):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='date', y=y_col)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def fetch_latest_repos():
    response = requests.get(f'{FLASK_BACKEND_URL}/latest_repos')
    if response.status_code == 200:
        return response.json()
    else:
        return []


# Function to fetch repo data for visualizations
def fetch_repo_data(repo_id):
    response = requests.get(f'{FLASK_BACKEND_URL}/repo_data_all?repo_id={repo_id}')
    if response.status_code == 200:
        return response.json()
    else:
        return []


# Streamlit app
st.title('GitHub Repository Viewer')

# Fetch the latest repos
latest_repos = fetch_latest_repos()

# Convert the repos to a DataFrame for easy manipulation
df_repos = pd.DataFrame(latest_repos)

# Display the selectbox for repository names
repo_name = st.selectbox(
    'Select a GitHub Repo:',
    df_repos['repo_name'] if not df_repos.empty else []
)

# Display a button to confirm selection
if st.button('Go to Dashboard'):
    # Fetch the selected repo_id
    repo_id = df_repos[df_repos['repo_name'] == repo_name]['repo_id'].values[0]

    # Fetch data for the selected repo
    repo_data = fetch_repo_data(repo_id)

    # Create DataFrames from the dictionary
    df_stars_weekly = pd.DataFrame(repo_data['stars_weekly'],
                                   columns=['date', 'repo_id', 'star_count', 'last_week_star_count', 'wow_growth'])
    df_stars_monthly = pd.DataFrame(repo_data['stars_monthly'],
                                    columns=['date', 'repo_id', 'star_count', 'last_year_star_count', 'yoy_growth'])
    df_commits_weekly = pd.DataFrame(repo_data['commits_weekly'],
                                     columns=['date', 'repo_id', 'commits_count', 'last_week_commit_count',
                                              'wow_growth'])
    df_commits_monthly = pd.DataFrame(repo_data['commits_monthly'],
                                      columns=['date', 'repo_id', 'commits_count', 'last_year_commit_count',
                                               'yoy_growth'])

    # Convert the 'date' column to datetime format
    df_commits_monthly['date'] = pd.to_datetime(df_commits_monthly['date'], format='%a, %d %b %Y %H:%M:%S %Z')
    df_commits_weekly['date'] = pd.to_datetime(df_commits_weekly['date'], format='%a, %d %b %Y %H:%M:%S %Z')
    df_stars_monthly['date'] = pd.to_datetime(df_stars_monthly['date'], format='%a, %d %b %Y %H:%M:%S %Z')
    df_stars_weekly['date'] = pd.to_datetime(df_stars_weekly['date'], format='%a, %d %b %Y %H:%M:%S %Z')

    # Plotting Monthly Data
    st.header(f'Monthly Data for {repo_name}')

    st.subheader('Stars Monthly')
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_stars_monthly, x='date', y='star_count')
    plt.title('Monthly Star Count Over Time')
    plt.xlabel('Date')
    plt.ylabel('Star Count')
    st.pyplot(plt)

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_stars_monthly, x='date', y='yoy_growth')
    plt.title('Year-on-Year Growth Over Time of Stars')
    plt.xlabel('Date')
    plt.ylabel('Year-on-Year Growth')
    st.pyplot(plt)

    st.subheader('Commits Monthly')
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_commits_monthly, x='date', y='commits_count')
    plt.title('Monthly Commit Count Over Time')
    plt.xlabel('Date')
    plt.ylabel('Commit Count')
    st.pyplot(plt)

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_commits_monthly, x='date', y='yoy_growth')
    plt.title('Year-on-Year Growth Over Time of Commits')
    plt.xlabel('Date')
    plt.ylabel('Year-on-Year Growth')
    st.pyplot(plt)


    # Plotting Weekly Data with Rolling Average
    st.header(f'Weekly Data for {repo_name}')

    st.subheader('Stars Weekly')
    plot_with_rolling_average(df_stars_weekly, 'star_count', 'Weekly Star Count Over Time (Rolling Average)',
                              'Star Count')
    plot_with_rolling_average(df_stars_weekly, 'wow_growth', 'Week-on-Week Growth Over Time of Stars', 'Week-on-Week Growth')


    st.subheader('Commits Weekly')
    plot_with_rolling_average(df_commits_weekly, 'commits_count', 'Weekly Commit Count Over Time (Rolling Average)',
                              'Commit Count')
    plot_with_rolling_average(df_commits_weekly, 'wow_growth', 'Week-on-Week Growth Over Time of Commits', 'Week-on-Week Growth')