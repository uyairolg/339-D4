import os
import csv
import requests
from bs4 import BeautifulSoup
import re

def scrape_teams(base_path):
    teams = ['mens_team', 'womens_team']
    all_athletes_data = []

    for team in teams:
        team_path = os.path.join(base_path, team)
        if not os.path.exists(team_path):
            print(f"The path {team_path} does not exist.")
            continue

        for filename in os.listdir(team_path):
            if filename.endswith('.html'):
                file_path = os.path.join(team_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    athlete_data = extract_athlete_data(soup)
                    # Clean the athlete name to remove numbers at the end
                    athlete_data['name'] = re.sub(r'\d+$', '', athlete_data['name']).strip()
                    all_athletes_data.append((team, athlete_data))

    save_athletes_data(all_athletes_data)

def extract_athlete_data(soup):
    name = soup.find('h1').text.strip() if soup.find('h1') else "Unknown"
    records_table = soup.find('table')
    records = []

    if records_table:
        rows = records_table.find_all('tr')[1:]  # Skipping the header row
        for row in rows:
            cells = row.find_all('td')
            year = cells[0].text.strip() if len(cells) > 0 else ""
            record = cells[1].text.strip() if len(cells) > 1 else ""
            records.append((year, record))

    return {
        'name': name,
        'records': records
    }

def save_athletes_data(all_athletes_data):
    output_file = os.path.join('xc_data-main', 'athletes_data.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Team', 'Name', 'Year', 'Record'])
        for team, athlete in all_athletes_data:
            for year, record in athlete['records']:
                writer.writerow([team, athlete['name'], year, record])

def generate_homepage(directory='xc_data-main'):
    teams = ['mens_team', 'womens_team']
    mens_files = []
    womens_files = []

    for team in teams:
        team_path = os.path.join(directory, team)
        if os.path.exists(team_path):
            if team == 'mens_team':
                mens_files += [os.path.join(team, f) for f in os.listdir(team_path) if f.endswith('.html')]
            elif team == 'womens_team':
                womens_files += [os.path.join(team, f) for f in os.listdir(team_path) if f.endswith('.html')]

    # Create the content for the home page HTML file (index.html)
    index_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cross Country Teams</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html">Home Page</a></li>
            <li><a href="mens.html">Men's Team</a></li>
            <li><a href="womens.html">Women's Team</a></li>
        </ul>
    </nav>
    <h1>Cross Country Teams</h1>

    <h2>Mens Team</h2>
    <table>
        <tr><th>Athlete Name</th></tr>'''

    for html_file in mens_files:
        file_name = os.path.basename(html_file)
        cleaned_name = re.sub(r'\d+\.html$', '', file_name).strip()
        index_content += f'\n        <tr><td><a href="mens_team/{file_name}">{cleaned_name}</a></td></tr>'

    index_content += '''
    </table>

    <h2>Womens Team</h2>
    <table>
        <tr><th>Athlete Name</th></tr>'''

    for html_file in womens_files:
        file_name = os.path.basename(html_file)
        cleaned_name = re.sub(r'\d+\.html$', '', file_name).strip()
        index_content += f'\n        <tr><td><a href="womens_team/{file_name}">{cleaned_name}</a></td></tr>'

    index_content += '''
    </table>
</body>
</html>'''

    # Write the content to the index.html file for the home page
    with open(os.path.join(directory, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_content)

    # Create the content for the mens.html page
    mens_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mens Team</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html">Home Page</a></li>
            <li><a href="mens.html">Men's Team</a></li>
            <li><a href="womens.html">Women's Team</a></li>
        </ul>
    </nav>
    <h1>Mens Team</h1>
    <table>
        <tr><th>Athlete Name</th></tr>'''

    for html_file in mens_files:
        file_name = os.path.basename(html_file)
        cleaned_name = re.sub(r'\d+\.html$', '', file_name).strip()
        mens_content += f'\n        <tr><td><a href="mens_team/{file_name}">{cleaned_name}</a></td></tr>'

    mens_content += '''
    </table>
</body>
</html>'''

    # Create the content for the womens.html page
    womens_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Womens Team</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html">Home Page</a></li>
            <li><a href="mens.html">Men's Team</a></li>
            <li><a href="womens.html">Women's Team</a></li>
        </ul>
    </nav>
    <h1>Womens Team</h1>
    <table>
        <tr><th>Athlete Name</th></tr>'''

    for html_file in womens_files:
        file_name = os.path.basename(html_file)
        cleaned_name = re.sub(r'\d+\.html$', '', file_name).strip()
        womens_content += f'\n        <tr><td><a href="womens_team/{file_name}">{cleaned_name}</a></td></tr>'

    womens_content += '''
    </table>
</body>
</html>'''

    # Write the content to the mens.html and womens.html files
    with open(os.path.join(directory, 'mens.html'), 'w', encoding='utf-8') as f:
        f.write(mens_content)

    with open(os.path.join(directory, 'womens.html'), 'w', encoding='utf-8') as f:
        f.write(womens_content)

if __name__ == "__main__":
    base_path = 'xc_data-main'
    scrape_teams(base_path)
    generate_homepage()
