from socket import*
import base64
import time
#from bs4 import BeautifulSoup


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_HOST,SERVER_PORT))

USER_NAME = 'bilkentstu'
PASSWORD = 'cs421s2021'
target_host = "localhost:8000/"


def part_A(client_socket):
    # send http get request
    print("Part A--------------------")
    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
    client_socket.send(request.encode())  

    #receive
    response = client_socket.recv(4096)
    content = repr(response)
    print("Response for part A\n"+ content)
    with open('index2.html', 'w') as f:
        f.write(content)
    #parsing html file and getting link
    #with open("index2.html") as fp:
    #    soup = BeautifulSoup(fp, "html.parser")
    #for a in soup.findAll('a', href =True):
    #    parsed_link = a['href']
    parsed_link = parseFile(0)
    print("Ths is link parsed from index2.html: "+ parsed_link)
    return parsed_link

def part_B_fail(client_socket, link_b):
    # send http get request
    print("PART B--------------------")
    request = "GET /"  + link_b + " HTTP/1.1\r\nHost:%s\r\n\r\n" %target_host
    client_socket.send(request.encode())  

    #receive
    response = client_socket.recv(4096)
    content = repr(response)
    print(content)

def part_B_auth(client_socket,link_b):
    # send http get request with auth
    auth_creds = USER_NAME + ':' + PASSWORD
    auth_creds = auth_creds.encode()
    auth_creds = base64.b64encode(auth_creds)
    auth_creds = auth_creds.decode("utf-8")
    encoded_auth = auth_creds.encode()
    print("Authentication key is "+ auth_creds)

    request =  "GET /" + link_b + " HTTP/1.1\r\nAuthorization: Basic " + auth_creds + "\r\nHost: localhost:8000/\r\n\r\n"
    client_socket.sendall(request.encode())

    # receive
    response = client_socket.recv(4096)
    content = repr(response)
    print("This is response to the request that uses authorization\n" + content)
    with open('protected2.html', 'w') as f:
        f.write(content)
    #parsing html file and getting link
   # with open("protected2.html") as fp:
    #    soup = BeautifulSoup(fp, "html.parser")
    #for a in soup.findAll('a', href =True):
     #   parsed_link = a['href']
    parsed_link = parseFile(1)
    print("Entity name for part C is " + parsed_link)
    return parsed_link


def part_C(client_socket, entity_txt,link_b):
    print("Part C*********************")
    # send http head request for big.txt
    request = "HEAD /" + entity_txt + " HTTP/1.1\r\nHost: localhost:8000/\r\n\r\n" 
    client_socket.send(request.encode())  

    #receive
    response = client_socket.recv(1024)
    content = repr(response)
    print("This is head request response for entity big.txt \n"+ content)

     #send http head request for index2.html
    request = "HEAD /index.html HTTP/1.1\r\nHost: localhost:8000/\r\n\r\n" 
    client_socket.send(request.encode())  

    #receive
    response = client_socket.recv(4096)
    content = repr(response)
    print("This is head request response for entity index2.html \n"+ content)
    txt_length = 6488394
    ranges = [100,1000,10000,15000]
    times = []
    for i in ranges:
        #start = time.time()
        t = time.process_time()
        download_range(i,entity_txt,txt_length)
        #end = time.time()
        elapsed_time = time.process_time()-t
        times.append(elapsed_time)
    print(ranges)
    print("*********ExecTime********")
    print(times)
    

    

def download_range(range1,entity_txt,txt_length):
    for start in range(0,txt_length,range1):
        nextNum = start+range1
        str1 =  str(start) 
        str2 = str(nextNum)
        request = "GET /" + entity_txt + " HTTP/1.1\r\nHost: localhost:8000/\r\nRange: bytes=" +str1 + "-" + str2 + "\r\n\r\n" 
        client_socket.sendall(request.encode())
        #receive
        response = client_socket.recv(16000)
        content = repr(response)
        #write obtained files to big<range>.txt
        txt_name = "big" + str(range1) + ".txt"
        with open(txt_name, 'a') as f:
            f.write(content)

def parseFile(part):
    if(part== 0):
        with open('index2.html') as f:
            datafile = f.readlines()
        
        for line in datafile:
            if "protected.html" in line:
                return "protected.html"
    else:
        with open('protected2.html') as f:
            datafile = f.readlines()
        
        for line in datafile:
            if "big.txt" in line:
                return "big.txt"



parsed_link_A = part_A(client_socket)
part_B_fail(client_socket, parsed_link_A)
parsed_entity_B = part_B_auth(client_socket, parsed_link_A)
part_C(client_socket,parsed_entity_B,parsed_link_A)
##Send exit request
print("Sending exit request")
request = "EXIT / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
client_socket.send(request.encode())  
 #receive
response = client_socket.recv(4096)
content = repr(response)

