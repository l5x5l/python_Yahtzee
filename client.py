import socket

SERV = "127.0.0.1"
PORT = 8888

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((SERV, PORT))
res = ""

while(True):
    n = input("input the option : ")
    _id = input("input the id : ")
    pw = input('input the password : ')
    data = ""
    data += n
    while len(_id) == 0 or len(_id) >= 11:
        _id = input("input the id : ")
    while len(pw) == 0 or len(pw) >= 11:
        pw = input("input the password : ")

    for i in range(1, 11):
        if i <= len(_id):
            data += _id[i-1]
        else:
            data += "\0"
    for i in range(11, 21):
        if i - 10 <= len(pw):
            data += pw[i-11]
        else:
            data += "\0"

    client_sock.sendall(data.encode())
    res = client_sock.recv(1024)
    res = res.decode()
    print(res, end="\n")
    if n == "2":
        new_pw = input("input new password : ")
        new_pw_temp = input("input new password again : ")
        while new_pw != new_pw_temp:
            new_pw = input("new password not matched\ninput new password : ")
            new_pw_temp = input("input new password again : ")
        new_data = ""
        for i in range(10):
            if i < len(new_pw):
                new_data += new_pw[i]
            else:
                break
        client_sock.sendall(new_data.encode())
        res = client_sock.recv(1024)
        res = res.decode()
        print(res, end="\n")