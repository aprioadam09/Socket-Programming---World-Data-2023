import socket
import csv
import json

def baca_data_negara():
    data = {}
    with open('world-data-2023-new.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data[row['Country']] = row
    return data

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

print('The server is running and waiting for a connection...')

data_negara = baca_data_negara()

while True:
    client_socket, client_address = server_socket.accept()
    print('Connection accepted from:', client_address)

    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break
        
        pilihan, tipe_data, negara_diminta = request.split('|')

        pilihan_str = 'All countries' if pilihan == '1' else 'One country'
        tipe_data_str = 'General' if tipe_data == '1' else 'Details'

        print(f'Selected country data: {pilihan_str}')
        print(f'Type of data requested: {tipe_data_str}')
        if pilihan != '1':
            print(f'Requested country: {negara_diminta}')

        if pilihan == '1':
            all_data = {}
            for country, data in data_negara.items():
                if tipe_data == '1':
                    data_umum = {
                        'Country': data['Country'],
                        'Capital/Major City': data['Capital/Major City'],
                        'Region': data['Region'],
                        'Sub-region': data['Sub-region'],
                        'Official language': data['Official language'],
                        'Population': data['Population'],
                        'Density (P/Km2)': data['Density (P/Km2)'],
                        'Land Area(Km2)': data['Land Area(Km2)'],
                        'Calling Code': data['Calling Code'],
                        'Currency-Code': data['Currency-Code'],
                        'Latitude': data['Latitude'],
                        'Longitude': data['Longitude']
                    }
                    all_data[country] = data_umum
                elif tipe_data == '2':
                    all_data[country] = data
            data = all_data
        elif pilihan == '2':
            data = data_negara.get(negara_diminta, "Data not found")
            if data != "Data not found":
                if tipe_data == '1':
                    data_umum = {
                        'Country': data['Country'],
                        'Capital/Major City': data['Capital/Major City'],
                        'Region': data['Region'],
                        'Sub-region': data['Sub-region'],
                        'Official language': data['Official language'],
                        'Population': data['Population'],
                        'Density (P/Km2)': data['Density (P/Km2)'],
                        'Land Area(Km2)': data['Land Area(Km2)'],
                        'Calling Code': data['Calling Code'],
                        'Currency-Code': data['Currency-Code'],
                        'Latitude': data['Latitude'],
                        'Longitude': data['Longitude']
                    }
                    data = data_umum
                elif tipe_data != '2':
                    data = "Invalid data type"

        data_str = json.dumps(data)
        client_socket.sendall(data_str.encode())
        client_socket.sendall(b"END_OF_DATA")

    client_socket.close()  