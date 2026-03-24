import socket

# Configuración básica
HOST = '127.0.0.1'  # Localhost (nuestra propia máquina)
PORT = 65432        # Puerto donde escucharemos (> 1023 para no pedir permisos de admin)

print("--- SERVIDOR TCP ---")
print(f"Iniciando servicio en {HOST}:{PORT}")

# 1. CREACIÓN DEL SOCKET
# socket.AF_INET   = Usamos IPv4
# socket.SOCK_STREAM = Usamos TCP. 
# EXPLICACIÓN: Stream significa Flujo. TCP crea un canal estable (como una tubería)
# donde los datos viajan ordenados y seguros.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    
    # 2. BIND
    # Asignamos este socket a una dirección y puerto específicos.
    server_socket.bind((HOST, PORT))
    
    # 3. LISTEN
    # Ponemos el socket en modo oreja. Empieza a escuchar peticiones.
    # TCP necesita este paso porque es orientado a conexión.
    server_socket.listen()
    print("Esperando a que alguien llame (conecte)...")
    
    # 4. ACCEPT
    # El código se PAUSA (bloquea) aquí hasta que un cliente se conecta.
    # Retorna dos cosas:
    # - conn: Un NUEVO socket exclusivo para hablar con ESE cliente específico.
    # - addr: La dirección IP y puerto del cliente.
    conn, addr = server_socket.accept()
    
    with conn:
        print(f"¡Conexión establecida con {addr}!")
        
        # Bucle para mantener la charla viva
        while True:
            # 5. RECV
            # Leemos datos de la tubería. 1024 es el tamaño del buffer (bytes).
            data = conn.recv(1024)
            
            # Si data está vacío, significa que el cliente colgó (cerró conexión).
            if not data:
                print("El cliente ha cerrado la conexión.")
                break
            
            # Decodificamos los bytes a texto legible (UTF-8)
            message = data.decode('utf-8')
            print(f"Cliente dice: {message}")
            
            # Procesamos (convertir a mayúsculas)
            response = message.upper()
            
            # 6. SENDALL
            # Enviamos la respuesta de vuelta por el MISMO tubo (conn).
            conn.sendall(response.encode('utf-8'))