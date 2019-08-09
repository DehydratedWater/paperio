from server.socket_threads import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
MAX_NUM_OF_PLAYERS = 4

free_ports = set()
taken_ports = set()
dict_of_clients = {}

for i in range(1, MAX_NUM_OF_PLAYERS+1):
    free_ports.add(PORT+i)

main_thread = threading.Thread(target=start_main_socket, args=(dict_of_clients, HOST, PORT, free_ports, taken_ports))
main_thread.start()

