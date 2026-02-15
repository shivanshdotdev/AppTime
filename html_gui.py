import webbrowser
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json


APP_DIR = Path.home()/"AppTime"
APP_DIR.mkdir(parents=True, exist_ok=True)
PERM_LOG_FILE_PATH = APP_DIR/"usage_log.json"

data = {}

def show_table():
    with open(PERM_LOG_FILE_PATH, 'r') as f:
        data = json.load(f)

    print(data)
    print(type(data))
    print(len(data))


    env = Environment(loader=FileSystemLoader(
        "C:/Users/shiva/Desktop/Projects/App Watcher"
    ))

    template = env.get_template("sample.html")

    rendered = template.render(data_dict = data)


    html_output_file = "C:/Users/shiva/Desktop/Projects/App Watcher/output.html"

    with open(html_output_file, 'w') as f:
        f.write(rendered)


    webbrowser.open_new_tab(f"file://{html_output_file}")
    