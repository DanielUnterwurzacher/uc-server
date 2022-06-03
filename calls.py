"""import base64
import json
import requests

hostUser = 'http://127.0.0.1:5000/user'
hostArticle = 'http://127.0.0.1:5000/article'

def encode_base64(fName):
    with open(fName, 'rb') as file:
        binary_file_data = file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        return base64_encoded_data.decode('utf-8')

def decode_Base64(fName, data):
    data_base64 = data.encode('utf-8')
    with open(fName, 'wb') as file:
        decoded_data = base64.decodebytes(data_base64)
        file.write(decoded_data)

if __name__ == '__main__':
    enc1 = encode_base64('img/Knauff.png')
    enc2 = encode_base64('img/Ribery.png')

    j1 = {'name' : 'Knauff', 'password' : 'Hallo123', 'image' : enc1}
    print(j1)

    j2 = {'name': 'Ribery', 'password': 'Hallo123', 'image': enc2}
    print(j2)
    
    response = requests.put("%s/%s" % (hostUser, "500"), json={'info' : j1})
    print(response)
    print(response.json())

    response = requests.put("%s/%s" % (hostUser, "500"), json={'info': j2})
    print(response)
    print(response.json())


    a1 = {'product_name' : 'Mehl', 'amount' : 1, 'user_id' : 2}
    print(a1)

    a2 = {'product_name': 'Eier', 'amount': 8, 'user_id': 1}
    print(a2)

    response = requests.put("%s/%s" % (hostArticle, "500"), json={'info' : a1})
    print(response)
    print(response.json())

    response = requests.put("%s/%s" % (hostArticle, "500"), json={'info': a2})
    print(response)
    print(response.json())

    response = requests.get("%s/%s" % (hostUser, "1"))
    print(response)
    print(response.json())

    response = requests.get("%s/%s" % (hostUser, "2"))
    print(response)
    print(response.json())



    j = json.dumps([{'amount': 8, 'product_id': 4, 'product_name': 'Eier', 'user_id': 1},{'amount': 8, 'product_id': 2, 'product_name': 'Eier', 'user_id': 1}])
    #ändert Artikel mit userid 1
    response = requests.patch("%s/%s" % (hostArticle, "1"),data={'info': j}).json()
    print(response)

    # liefert Artikel vom user mit user_id 1
    response = requests.patch("%s/%s" % (hostUser, "1"))
    print(response)
    print(response.json())


"""