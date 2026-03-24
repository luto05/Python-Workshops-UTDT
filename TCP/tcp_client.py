import socket

HOST = '127.0.0.1'
PORT = 65432

print("--- CLIENTE TCP ---")

# 1. CREACIÓN DEL SOCKET
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
    print(f"Intentando conectar a {HOST}:{PORT}...")
    
    # 2. CONNECT
    # Esto inicia el handshake.
    # Si el servidor no está escuchando, esto dará error.
    client_socket.connect((HOST, PORT))
    print("¡Conectado! Escribe 'salir' para cerrar.")

    while True:
        # Pedimos al usuario que escriba
        message = input("Tú: ")
        
        if message.lower() == 'salir':
            print("Cerrando la llamada...")
            break
            
        # 3. SENDALL
        # Como ya estamos conectados, solo empujamos los datos por el tubo.
        client_socket.sendall(message.encode('utf-8'))
        
        # 4. RECV
        # Esperamos a que el servidor responda.
        data = client_socket.recv(1024)
        print(f"Servidor responde: {data.decode('utf-8')}")