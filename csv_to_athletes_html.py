import re
import csv
import os
import glob

def process_athlete_data(file_path):
    # Extracting athlete stats by year
    records = []

    # Extracting athlete races
    races = []

    athlete_name = ""
    athlete_id = ""
    comments = ""

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

        athlete_name = data[0][0]
        athlete_id = data[1][0]
      #   print(f"The athlete id for {athlete_name} is {athlete_id}")

        for row in data[5:-1]:
            if row[2]:
                # Remove non-numeric strings from the record (e.g., "PR")
                cleaned_record = re.sub(r'[^\d.:]', '', row[3])
                records.append({"year": row[2], "sr": cleaned_record})
            else:
                # Remove non-numeric strings from the race time (e.g., "PR")
                cleaned_time = re.sub(r'[^\d.:]', '', row[3])
                races.append({
                    "finish": row[1],
                    "time": cleaned_time,
                    "meet": row[5],
                    "url": row[6],
                    "comments": row[7]
                })

    return {
        "name": athlete_name,
        "athlete_id": athlete_id,
        "season_records": records,
        "race_results": races,
        "comments": comments
    }

def gen_athlete_page(data, outfile):
    # Find the best record (fastest time)
    best_record = None
    for record in data["season_records"]:
        try:
            record_time = list(map(float, record["sr"].replace(':', '.').split('.')))
            record_seconds = record_time[0] * 60 + record_time[1] + (record_time[2] if len(record_time) > 2 else 0) / 100
            if best_record is None or record_seconds < best_record["seconds"]:
                best_record = {
                    "record": record,
                    "seconds": record_seconds
                }
        except ValueError:
            continue

    athlete_image_filename = f"{data['athlete_id']}.jpg"
    # print(athlete_image_filename)
    athlete_image_path = os.path.join("/Users/gloriayu/Desktop/339 D3/xc_data-main/images/profiles", athlete_image_filename)

    # Debugging: Print the path being checked
    # print(f"Checking if athlete image exists at: {athlete_image_path}")
    # print(f"Current working directory: {os.getcwd()}")

    # Check if the athlete-specific image file exists in the images/profiles folder
    if os.path.exists(athlete_image_path):
        # The athlete image exists, so use it
        athlete_image_path = f"../images/profiles/{athlete_image_filename}"
        # print("found")
    else:
        # The athlete image does not exist, use the default image
        athlete_image_path = "../images/profiles/default_image.jpg"
        # print ("defalut")
    # Return the value of athlete_image_path if you want to use it elsewhere
 

    html_content = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link rel="stylesheet" href="../css/reset.css">
        <link rel="stylesheet" href="../dist/css/lightbox.css">
        <link rel="stylesheet" href="../css/style.css">
        

        <title>{data["name"]}</title>
    </head>
    <body>
    <a href="#main" class="skiplink">Skip to Main Content</a>

    <nav>
        <ul>
            <li><a href="../index.html">Home Page</a></li>
            <li><a href="../mens.html">Men's Team</a></li>
            <li><a href="../womens.html">Women's Team</a></li>
        </ul>
    </nav>
    <header>
        <h1>{data["name"]}</h1>
    <a href="{athlete_image_path}" id = "lightbox-image" data-lightbox="{athlete_image_filename}" data-title="Athlete Headshot" data-alt = "Image of Athlete in Race" target = "_blank">
        <img src="{athlete_image_path}" alt="Athlete headshot" width="200">
    </a>




    </header>
    <main id="main">
    <p id="dateTime"></p>
        <section id="athlete-sr-table">
            <h2>Athlete's Seasonal Records (SR) per Year</h2>
            <table tabindex="0">
                <thead>
                    <tr>
                        <th> Year </th>
                        <th> Season Record (SR) </th>
                    </tr>
                </thead>
                <tbody>
    '''

    for sr in data["season_records"]:
        record_class = ' class="best-record"' if best_record and sr == best_record["record"] else ""
        html_content += f'''
                    <tr>
                        <td>{sr["year"]}</td>
                        <td{record_class}>{sr["sr"]}</td>
                    </tr>
        '''

    html_content += '''
                </tbody>
            </table>
        </section>

        <h2>Race Results</h2>
        <section id="athlete-result-table">
            <table id="athlete-table">
                <thead>
                    <tr>
                        <th>Race</th>
                        <th>Athlete Time</th>
                        <th>Athlete Place</th>
                        <th>Race Comments</th>
                    </tr>
                </thead>
                <tbody>
    '''

    for race in data["race_results"]:
        html_content += f'''
                    <tr class="result-row">
                        <td><a href="{race["url"]}">{race["meet"]}</a></td>
                        <td>{race["time"]}</td>
                        <td>{race["finish"]}</td>
                        <td>{race["comments"]}</td>
                    </tr>
        '''

    html_content += '''
                </tbody>
            </table>
        </section>
    </main>
    <footer>
        <p>
            Skyline High School<br>
            <address>
                2552 North Maple Road<br>
                Ann Arbor, MI 48103<br><br>
            </address>
            <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
            Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/"><i class="fa-brands fa-instagram" aria-label="Instagram"></i>Here</a>
        </p>
    </footer>
    <button id="topBtn" onclick="scrollToTop()">Go Back to Top</button>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script> 
    <script>
        document.querySelectorAll('img').forEach(img => {
            img.onerror = function() {
                this.onerror = null; // Prevents infinite loop if default image missing
                this.src = '../images/profiles/default_image.jpg';
                this.alt = "";
            };
        });
    </script>   
    <script src="../js/script.js"></script>
    <script src="../dist/js/lightbox-plus-jquery.js"></script>

  
    
    </body> 
    </html>
    '''

    with open(outfile, 'w') as output:
        output.write(html_content)

def main():
    # Ensure xc_data-main/mens_team and xc_data-main/womens_team directories exist
    mens_team_path = '../xc_data-main/mens_team'
    womens_team_path = '../xc_data-main/womens_team'

    if not os.path.exists(mens_team_path):
        os.makedirs(mens_team_path)
    if not os.path.exists(womens_team_path):
        os.makedirs(womens_team_path)

    # Process men's team files
    folder_path = mens_team_path
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    csv_file_names = [os.path.basename(file) for file in csv_files]
   #  (csv_file_names)print
    for file in csv_file_names:
        athlete_data = process_athlete_data(os.path.join(folder_path, file))
        gen_athlete_page(athlete_data, os.path.join(folder_path, file.replace(".csv", ".html")))

    # Process women's team files
    folder_path = womens_team_path
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    csv_file_names = [os.path.basename(file) for file in csv_files]
   #  print(csv_file_names)
    for file in csv_file_names:
        athlete_data = process_athlete_data(os.path.join(folder_path, file))
        gen_athlete_page(athlete_data, os.path.join(folder_path, file.replace(".csv", ".html")))

if __name__ == '__main__':
    main()

