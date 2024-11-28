import requests
from nicegui import ui, app
import pandas as pd

# VARIABLES INITIALIZATION
ip = ""


# API
BASE_URL_JAVA = "https://api.mcsrvstat.us/3/"

def get_response(ip):
    response = requests.get(BASE_URL_JAVA + ip)
    print("Response: ", response.json())
    return response

# GUI-TABLE
server_table = pd.DataFrame(columns=['IP', 'Version', 'Hostname', 'Port', 'Players', 'Max Players', 'Online'])

def add_server_data(data):
    global server_table, version

    if data['ip'] not in server_table['IP'].values:
        new_data = {
            'IP': data.get('ip', ''),
            'Hostname': data.get('hostname', ''),
            'Port': data.get('port', ''),
            'Players': data.get('players', {}).get('online', 0),
            'Max Players': data.get('players', {}).get('max', 0),
            'Online': data.get('online', False),
        }

        table.add_row(new_data)
        table.run_method('scrollTo', len(table.rows) - 1)

        print(new_data)
        temp_table = pd.DataFrame([new_data])
        server_table = server_table.reset_index(drop=True)
        server_table = pd.concat([server_table, temp_table], ignore_index=True)
        print(server_table)

# GUI
app.native.window_args['resizable'] = True
app.native.start_args['debug'] = False
app.native.settings['ALLOW_DOWNLOADS'] = True

ui.input('Server IP:', on_change=lambda e: globals().update(ip=e.value))
ui.button('Get server data', on_click=lambda: add_server_data(get_response(ip).json()))

table = ui.table.from_pandas(server_table)
table.style('text-align: center')

add_server_data(get_response('mc.hypixel.net').json())
ui.run(native=True, window_size=(800, 600), fullscreen=False, dark=True)