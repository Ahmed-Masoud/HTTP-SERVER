import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# request input from user
request = raw_input('Enter a file request: ')
# parse input to get the port number
my_list = request.split(" ")
method = my_list[0]
fileName = my_list[1]
host = my_list[2]
if len(my_list) == 4:
    port = int(my_list[3])
else:
    port = 80
# connection to hostname on the port.
try:
    s.connect((host, port))
except:
    print("connection refused !!")
    quit()
if method == "GET":
    s.send(request)
    response_code = s.recv(512)
    print("Status Code : "+response_code+"\n")
    if response_code == "404 Not Found":
        quit()
    text_file = open(fileName, "w+")
    while True:
        serverMsg = s.recv(512)
        if not serverMsg:
            break
        print(serverMsg)
        text_file.write(serverMsg)
    text_file.close()
elif method == "POST":
    try:
        f = open(fileName, 'r')
    except:
        print("No Such File !!")
        quit()
    s.send(request)
    response_code = s.recv(512)
    print("Status Code : "+response_code+"\n")
    while True:
        data = f.readline(512)
        if not data:
            break
        s.send(data)
    f.close()