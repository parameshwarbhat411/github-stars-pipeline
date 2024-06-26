# GitHub Open Source ETL Pipeline

## Overview
**GitHub Open Source ETL Pipeline**

This ETL (Extract, Transform, Load) project provides an insightful analysis of GitHub open-source repositories. Designed for investors and companies considering open-source investments, it offers a detailed view of project dynamics, community engagement, and technological innovation. Data sourced daily from GH Archive is processed and presented in a SQL database format, enabling straightforward querying and advanced analysis.

## Key Metrics Targeted
The ETL pipeline targets an array of metrics to provide a multidimensional understanding of open-source repositories:

- **Popularity Metrics:** Tracks the growth rate of repositories based on stars and forks to gauge overall popularity.
- **Contribution Metrics:** Assesses contributions through commit activities and pull request rates to understand developer involvement.

## Future work 
- **Influence Score:** A composite metric that integrates various signals such as stars, forks, and issues to evaluate the project's influence.
- **Developer Engagement Index:** Measures the frequency and recency of contributions, indicating active development and project health.
- **Issue Resolution Efficiency:** Analyzes how quickly issues are resolved, offering insights into the project's operational efficiency.
- **Dependency Risk Analysis:** Examines the number and reliability of project dependencies to assess stability risks.
- **Innovation Rate:** Monitors the introduction of new features and technologies, identifying projects that are at the forefront of innovation.
- **Funding and Sponsorship Activity:** Tracks sponsorship activities to gauge financial support and commercial interest in the project.

## Data Update Frequency
- **Daily Updates:** The data warehouse is updated on a daily basis to ensure the most current data is available for analysis. This frequent refresh rate allows for up-to-date insights and trend monitoring.

## Models Provided
- **SQL Database Access:** Data is delivered in a SQL database format, facilitating easy access and custom query capabilities for detailed analysis.
- **Custom Analysis Capability:** Future enhancements will include the ability to perform ad-hoc custom analyses, allowing users to tailor insights to specific requirements.

## Models

### Introduction
We use Kimball dimensional models to structure our data warehouse. This approach ensures efficient querying and analysis.

### Fact and Dimension Models

#### Fact Tables
- **fact_stars**
  - `event_id` (Primary Key)
  - `repo_id` (Foreign Key to `dim_repositories`)
  - `user_id` (Foreign Key to `dim_users`)
  - `event_date` (Date)

- **fact_commits**
  - `event_id` (Primary Key)
  - `repo_id` (Foreign Key to `dim_repositories`)
  - `user_id` (Foreign Key to `dim_users`)
  - `event_date` (Date)

#### Aggregate Fact Tables
- **fact_stars_weekly**
  - `event_id` (Primary Key)
  - `repo_id` (Foreign Key to `dim_repositories`)
  - `user_id` (Foreign Key to `dim_users`)
  - `week` (Date)

- **fact_stars_monthly**
  - `event_id` (Primary Key)
  - `repo_id` (Foreign Key to `dim_repositories`)
  - `user_id` (Foreign Key to `dim_users`)
  - `month` (Date)

- **fact_commits_weekly**
  - `event_id` (Primary Key)
  - `repo_id` (Foreign Key to `dim_repositories`)
  - `user_id` (Foreign Key to `dim_users`)
  - `week` (Date)

- **fact_commits_monthly**
  - `event_id` (Primary Key)
  - `repo_id` (Foreign Key to `dim_repositories`)
  - `user_id` (Foreign Key to `dim_users`)
  - `month` (Date)

#### Dimension Tables
- **dim_repositories**
  - `repo_id` (Primary Key)
  - `repo_name`
  - `owner_login`

- **dim_users**
  - `user_id` (Primary Key)
  - `login`

### Sample SQL Queries

#### Types of SQL Queries You Can Perform

- **Calculate Growth Rate of Stars**: Aggregate and analyze the growth rate of stars for a particular repository over a specified period.
- **Year-on-Year Growth Analysis**: Evaluate the year-on-year growth in stars or commits for specific repositories to understand their performance over time.

These are the types of aggregation and analysis queries you can perform using the data provided by our ETL pipeline. These queries facilitate in-depth insights into the dynamics of GitHub repositories, supporting data-driven decision-making.

## Getting Started

To get started with the work, follow these steps (click on the
links for guides):

### Set up your IDE

> ℹ️ Skip some steps if you're already set!
>
> If you already have git, VSCode, and/or Python installed, just skip the corresponding step(s).

1. If you don't already use git, [install it here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

2. If you don't have a coding editor installed, [install VSCode](https://code.visualstudio.com/download). After that, [install the Python and Python extension](https://code.visualstudio.com/docs/languages/python#_install-python-and-the-python-extension).

3. Make sure you have Python 3 installed (or [install it here](https://www.python.org/downloads/)).

### Create your personal repo

1. [Create a new repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) in your Github account and name it `github-stars-pipeline`.

2. Clone this repo.

```bash
git clone https://github.com/parameshwarbhat411/github-stars-pipeline.git
```


3. Point your local clone to your own remote (so that you can modify your copy of the repo, not the template). Make sure you repalce `{your_github_username}` with the corresponding value.

```bash
cd github-stars-pipeline
git remote set-url origin https://github.com/{your_github_username}/github-stars-pipeline.git
```

4. Push to your new github repo.

```bash
git push origin master
```

### Set up your python environment and DuckDB

1. Create a python virtual environment for your repo:

```bash
python -m venv venv
source venv/bin/activate
```

2. [Install DuckDB](https://duckdb.org/docs/installation/?version=stable&environment=python) (make sure you select the Python option), your first python dependency.

> ℹ️ You might have to install additional dependencies if you're on Windows.

3. [Install DBeaver](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to explore DuckDB.

4. Create a new git branch:
```bash
git checkout -b add_duck_db
```

