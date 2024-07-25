import socket
import json 
import os

def request_data(client_socket):
    while True:
        pilihan = input('Enter choice (1. All countries, 2. One country): ')

        if pilihan == '1':
            while True:
                tipe_data = input('Enter the type of data to be received (1. General, 2. Details): ')
                if tipe_data in ['1', '2']:
                    break
                else:
                    print('Invalid data type input. Please enter 1 for General or 2 for Details.')
            negara_diminta = ''
            request = f'{pilihan}|{tipe_data}|{negara_diminta}'
        elif pilihan == '2':
            while True:
                tipe_data = input('Enter the type of data to be received (1. General, 2. Details): ')
                if tipe_data in ['1', '2']:
                    break
                else:
                    print('Invalid data type input. Please enter 1 for General or 2 for Details.')
            negara_diminta = input('Enter the name of the country: ')
            request = f'{pilihan}|{tipe_data}|{negara_diminta}'
        else:
            print('Invalid input. Please enter 1 or 2.')
            continue

        client_socket.send(request.encode())

        data = b''
        while True:
            part = client_socket.recv(4096)
            if b"END_OF_DATA" in part:
                data += part.replace(b"END_OF_DATA", b"")
                break
            data += part

        data_entry = json.loads(data.decode())

        if pilihan == '1':
            folder_name = 'all_countries_data'
            os.makedirs(folder_name, exist_ok=True)

            for country, country_data in data_entry.items():
                file_path = os.path.join(folder_name, f'{country}.txt')
                with open(file_path, 'w') as file:
                    for key, value in country_data.items():
                        file.write(f"{key}: {value}\n")
            print(f'All country data has been saved in the "{folder_name}" folder.')
        elif pilihan == '2':
            if data_entry != "Data not found" and data_entry != "Invalid data type":
                with open(f'data_{negara_diminta}.txt', 'w') as file:
                    for key, value in data_entry.items():
                        file.write(f"{key}: {value}\n")
                print(f'Data for {negara_diminta} has been saved in the file "data_{negara_diminta}.txt".')
            else:
                print(data_entry)

        more_requests = input('Do you have any more requests? (yes/no): ')
        if more_requests.lower() != 'yes':
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.10.184.169', 8080)) 

request_data(client_socket)

client_socket.close()