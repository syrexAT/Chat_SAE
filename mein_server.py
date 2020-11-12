import socket #socket modul importieren
import sockettools
import threading
# Family: AF_INET = IPv4, AF_INET6 = IPv6 (UNIX hier nicht relevant)
# Type: STREAM/DGRAM, SOCK_STREAM = "TCP" (im kontext von ipv4/6)
# SOCK_DGRAM = "UDP" (im kontext von ipv4/6)

# Socket erstellen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #protokoll erkennt eh automatisch TCP

#Socket Options
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #REUSEADDR Soll auf 1 gesetzt werden, 

#Bind, bindet den socket auf den port
addr = ('', 5555) #hostname, port --> hostname empty string hört er auf alle interfaces (127.0.0.1, 10.0.0.1, 192.168.0.1 usw.) #weil wir ein server sind
s.bind(addr) #größer als 1024 weil das sind die common known ones
#würde auch so gehen s.bind(('', 5555)) --> TUPLE!

#Listen, weisst den kernel an auf dem port zu horchen
s.listen() #nichts übergeben nimmt er ein default value

#Accept
#auf dem socket object, keine parameter, braucht nur ein bind und listen davor, return value ist tuple
print("socket:", s)

def handle_connection(conn, address):
    # der erste socket existiert weiterhin und da ruft man wieder accept auf, server socket ist nur dafür da neue connections entgegenzunehmen
    hostname, port = address
    print("got connection:", hostname, "with port:", port)
    #print(s)


    while True:
        line = sockettools.read_line_from_socket(conn) 
        if line is None:
            print('CONNECTION CLOSED')
            break
        if line == 'quit':
            conn.close()
            break
        print('got line:', line)
        #conn.send(f'ok -> {line}\r\n'.encode('utf-8')) #ist ein interpolated string, magic string?
        #response = f'ok -> {line}\r\n'
        response = f'ok -> {line}\r\n'
        conn.send(response.encode('utf-8'))

while True:
    print("vor accept") #da bleibt er hängen weil noch keine connection da ist
    accept_result = s.accept()
    conn, address = accept_result #conn ist ein neuer socket, der die client -> server verbindung darstellt
    thread = threading.Thread(target=handle_connection, args=[conn, address])
    thread.start()
    print("nach accept")
    #print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#while True:
  #  ch = conn.recv(1) #wir lesen 1 byte ein, es wäre effizienter wenn man ihn einen bytearray geben würde, recv ist blocking, es wartet auf den 1 byte
  #  print(ch)
 #   conn.send(b'ok\r\n') #b für byte! oder man macht 'ok\r\n'.encode('utf-8') #hier in puttytel ausprobieren