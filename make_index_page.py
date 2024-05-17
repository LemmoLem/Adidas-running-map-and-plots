"""
this script adds all the image files in this folder to a webpage
the image files are whats saved by the saveplots script
"""


import os

def generate_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"/>
        <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"/>
        <style>
            img {
              width: 50%;
              margin: auto;
              display: block;
            }
        </style>
    </head>
    <body>
        <div class = "navbar">
        <a href="foliumMap.html">MAP</a>
        <a href="index.html">PLOTS</a>
        </div>
        <div id="image-container">
    """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_directory):
        if filename.lower().endswith('.png'):
            img_tag = f'<img src="./{filename}" alt="{filename} class="center"">\n'
            html_content += img_tag

    html_content += """
        </div>
    </body>
    </html>
    """

    with open('index.html', 'w') as file:
        file.write(html_content)