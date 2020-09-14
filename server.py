import sqlite3
import socket

ERROR_MSG = "ERROR : "
dbconn = sqlite3.connect("database.db")
cur = dbconn.cursor()

HOST = "127.0.0.1"
PORT = 8888

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))

server_sock.listen(5)

client_sock, addr = server_sock.accept()

# 이건 한번만!
# cur.execute("CREATE TABLE user (id TEXT, pw TEXT, win INTEGER, lose INTEGER);")


def check_id_pw(_data):
    _id = ""
    _pw = ""
    for i in range(1, 11):
        if _data[i] == "\0":
            break
        else:
            _id += _data[i]
    for i in range(11, 21):
        if _data[i] == "\0":
            break
        else:
            _pw += _data[i]
    return _id, _pw

while True:
    data = client_sock.recv(1024)
    data = data.decode()
    if not data:
        break

    # data 의 첫 바이트는 기능 식별용도로 사용된다.
    # 0이면 새 아이디 생성으로, 아이디는 1부터, 비밀번호는 11부터 시작된다.
    # 1이면 로그인으로, 아이디, 비밀번호의 위치인덱스는 0옵션과 같다.
    # 2이면 회원 정보 수정으로, 비밀번호만을 입력받는다.
    # 3이면 전적 갱신으로, 승리시 '+'를, 패배시 '-'를 입력받는다
    # 4이면 회원 탈퇴기능으로, 탈퇴할 아이디와 비밀번호를 입력받는다.
    if data[0] == "0":
        id, pw = check_id_pw(data)
        if id == "" or pw == "":
            error_empty = ERROR_MSG + " empty msg recv"
            client_sock.sendall(error_empty.encode())
            # 잘못된 입력입을 전송
        cur.execute("INSERT INTO user VALUES('" + id + "','" + pw + "','" + str(0) + "','" + str(0) + "');")
        dbconn.commit()
        client_sock.sendall(b"success!")
    elif data[0] == "1":
        id, pw = check_id_pw(data)
        if id == "" or pw == "":
            error_empty = ERROR_MSG + " empty msg recv"
            client_sock.sendall(error_empty.encode())
            # 잘못된 입력입을 전송
        cur.execute("SELECT pw FROM user WHERE id='" + id + "';")
        temp = cur.fetchall()
        if len(temp) == 0:
            client_sock.sendall(b"can't find user!")
        elif temp[0][0] == pw:
            client_sock.sendall(b"login success!")
        else:
            client_sock.sendall(b"password is not matched!")
    elif data[0] == "2":
        id, pw = check_id_pw(data)
        if id == "" or pw == "":
            error_empty = ERROR_MSG + " empty msg recv"
            client_sock.sendall(error_empty.encode())
        cur.execute("SELECT pw FROM user WHERE id='" + id + "';")
        temp = cur.fetchall()
        if len(temp) == 0:
            client_sock.sendall(b"can't find user!")
        elif temp[0][0] == pw:
            client_sock.sendall(b"login success!")
            new_data = client_sock.recv(1024)
            new_data = new_data.decode()
            cur.execute("UPDATE user SET pw = '" + new_data + "' WHERE id == '" + id + "';")
            dbconn.commit()
            client_sock.sendall(b"password change success!")
        else:
            client_sock.sendall(b"password is not matched!")
    elif data[0] == "4":
        id, pw = check_id_pw(data)
        if id == "" or pw == "":
            error_empty = ERROR_MSG + " empty msg recv"
            client_sock.sendall(error_empty.encode())
        cur.execute("SELECT pw FROM user WHERE id='" + id + "';")
        temp = cur.fetchall()
        if len(temp) == 0:
            client_sock.sendall(b"can't find user!")
        elif temp[0][0] == pw:
            cur.execute("DELETE FROM user WHERE id = '" + id + "';")
            client_sock.sendall(b"delete account")
            dbconn.commit()
        else:
            client_sock.sendall(b"password is not matched!")
    else:
        client_sock.sendall(b"can't find option!")

dbconn.close()
client_sock.close()
server_sock.close()
