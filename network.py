# reads from socket until "\r\n"
def read_from_socket(s):
    result = ""
    while True:
        data = s.recv(256)
        data = data.decode()
        if data[-2:] == "\r\n":
            result += data[:-2]
            break
        result += data
        # if result != "":
        #     print("read : %s") % result
    return result


# sends all on socket, adding "\r\n"
def send_to_socket(s, msg):
    # print("respond : %s")% msg
    s.sendall((str(msg) + "\r\n").encode())
