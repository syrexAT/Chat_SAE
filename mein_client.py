import socket
import sockettools

address = ('localhost', 5555)
conn = socket.create_connection(address)
print(conn)
while True:
    text = input('> ')
    #conn.send(b'hallo welt!\r\n')
    conn.send(f'{text}\r\n'.encode('utf-8'))
    #if text == 'quit':
    #   break
    response = sockettools.read_line_from_socket(conn)
    if response is None:
        print('Server closed the connection(?)')
        break
    print('got from server:', response)
#conn.send(b'quit\r\n')
conn.close()
