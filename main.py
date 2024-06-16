import http.server
import socketserver
import json
import requests
import pandas as pd
import sqlite3
import time
import random
import os
import hashlib
import pprint

class ServiceHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()

            url = "https://restcountries.com/v3.1/all"
            urlXregion= "https://restcountries.com/v3.1/region/{region}"
            
            region = []
            languages=[]
            hash_languages = []
            countries = []
            times = []

            data = json.loads(requests.get(url).text)
            
            for country in data:
                if 'languages' in country and country['languages']:
                    start_time = time.time()
                    country_name = country.get('name', {}).get('common', 'Unknown')
                    language = list(country['languages'].values())[0]
                    hash_language = hashlib.sha1(language.encode()).hexdigest()
                    process_time = time.time() - start_time

                    countries.append(country_name)
                    languages.append(language)
                    hash_languages.append(hash_language)
                    times.append(process_time)
            
            df = pd.DataFrame({
                "Country": countries,
                "Language": languages,
                "Encrypted Language": hash_languages,
                "Time": times
            })

            conn = sqlite3.connect('countries.db')
            df.to_sql('countries', conn, if_exists='replace', index=False)
            conn.close()

            df.to_json('data.json', orient='records', lines=True)

            total_time = df['Time'].sum()
            average_time = df['Time'].mean()
            min_time = df['Time'].min()
            max_time = df['Time'].max()

        

            result = {
                "total_time": total_time,
                "average_time": average_time,
                "min_time": min_time,
                "max_time": max_time,
                "data": df.to_dict(orient='records')
            }

            self.wfile.write(json.dumps(result).encode())

class ReuseAddrTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

PORT= 8000
myserver  = ReuseAddrTCPServer(("",PORT),ServiceHandler)
myserver.deamon_threads = True
print(f"Server started at http://127.0.0.1:{PORT}/")
try:
        myserver.serve_forever()
except:
        print("Closing the server.")
        myserver.server_close()


   
    