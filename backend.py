from flask import Flask, jsonify, request
import duckdb
import os

app = Flask(__name__)
db_path = os.getenv('DB_PATH', 'file.db')


def fetch_data(query, params=()):
    """Helper function to fetch data from the database."""
    conn = duckdb.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data


def get_repo_data_all(repo_id):
    """Fetch all relevant data for a specific repo."""
    queries = {
        'stars_monthly': "SELECT * FROM file.main.fact_stars_monthly WHERE repo_id = ?",
        'stars_weekly': "SELECT * FROM file.main.fact_stars_weekly WHERE repo_id = ?",
        'commits_monthly': "SELECT * FROM file.main.fact_commits_monthly WHERE repo_id = ?",
        'commits_weekly': "SELECT * FROM file.main.fact_commits_weekly WHERE repo_id = ?"
    }

    data = {}
    for key, query in queries.items():
        data[key] = fetch_data(query, (repo_id,))

    return data


@app.route('/repo_data_all', methods=['GET'])
def repo_data_all():
    repo_id = request.args.get('repo_id')
    data = get_repo_data_all(repo_id)
    return jsonify(data)


@app.route('/latest_repos', methods=['GET'])
def latest_repos():
    repos = get_latest_repos()
    return jsonify(repos)


def get_latest_repos():
    """Fetch the latest named repos."""
    query = """
    SELECT repo_id, repo_name
    FROM file.main.dim_repos
    WHERE end_date IS NULL
    """
    repos = fetch_data(query)
    return [{'repo_id': row[0], 'repo_name': row[1]} for row in repos]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)