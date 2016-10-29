import socket

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"

port = 8888

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))
    clientMsg = clientsocket.recv(512)
    print(clientMsg+"\n")
    webClient = False
    if '/' in clientMsg:
        webClient = True
        webRequest = clientMsg.split('\n')
        temp = webRequest[0].split(' ')
        method = 'GET'
        fileName = temp[1][1:]
    else:
        mylist = clientMsg.split(" ")
        method = mylist[0]
        fileName = mylist[1]
    if method == "GET":
        try:
            f = open(fileName, 'r')
        except:
            clientsocket.send("404 Not Found")
            clientsocket.close()
            continue
        if not webClient:
            clientsocket.send("200 OK")
        while True:
            data = f.readline(512)
            if not data:
                break
            clientsocket.send(data)
        f.close()
    elif method == "POST":
        text_file = open(fileName, "w+")
        clientsocket.send("receiving")
        while True:
            msg = clientsocket.recv(512)
            if not msg:
                break
            print(msg)
            text_file.write(msg)
        text_file.close()
    else:
        clientsocket.send("unknown command")
    clientsocket.close()