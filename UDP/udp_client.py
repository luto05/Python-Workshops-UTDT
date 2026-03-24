import socket

HOST = '127.0.0.1'
PORT = 65432

print("--- CLIENTE UDP ---")

# 1. CREACIÓN DEL SOCKET (IPv4 + Datagram/UDP)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    
    # No usamos connect().
    # No necesitamos llamar al servidor antes de hablar. Solo enviamos.
    
    while True:
        message = input("Tú: ")
        
        if message.lower() == 'salir':
            break
            
        # 2. SENDTO
        # Empaquetamos el mensaje en un datagrama y se lo lanzamos a la IP/Puerto destino.
        client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
        
        # 3. RECVFROM
        # Esperamos respuesta.
        # Nota: Si el paquete se pierde en el camino, esta línea podría quedarse esperando para siempre.
        data, server_addr = client_socket.recvfrom(1024)
        
        print(f"Servidor responde: {data.decode('utf-8')}")