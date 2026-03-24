import socket
import threading

HOST = "127.0.0.1" 
PORT = 65432        

def manejar_cliente(conn, addr):
    """
    Esta función corre en su propio hilo. 
    Se encarga de la charla con UN cliente específico.
    """
    print(f"[NUEVA CONEXIÓN] ¡Conexión establecida con {addr}!")
    
    with conn:
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"[DESCONEXIÓN] {addr} ha cerrado la conexión.")
                    break

                message = data.decode('utf-8')
                print(f"[{addr}] dice: {message}")

                response = message.upper()
                conn.sendall(response.encode('utf-8'))
        except ConnectionResetError:
            print(f"[ERROR] Conexión perdida forzosamente con {addr}")

def iniciar_servidor():
    print("--- SERVIDOR TCP MULTI-HILO ---")
    print(f"Iniciando servicio en {HOST}:{PORT}")

    # 1. CREACIÓN DEL SOCKET
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        
        # 2. BIND
        server_socket.bind((HOST, PORT))

        # 3. LISTEN
        # El número 100 indica el 'backlog' (cola de espera)
        server_socket.listen(100)
        print("Esperando conexiones entrantes...")

        while True:
            # 4. ACCEPT
            # El hilo principal se queda aquí esperando. 
            # En cuanto alguien conecta, despierta, acepta y sigue.
            conn, addr = server_socket.accept()

            # 5. CREAR HILO
            # Creamos un hilo para que 'manejar_cliente' se ejecute en paralelo
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            
            # 6. INICIAR HILO
            # Al hacer .start(), el hilo principal vuelve inmediatamente al 'accept'
            hilo.start()
            
            print(f"[ESTADO] Conexiones totales activas: {threading.active_count() - 1}")

if __name__ == "__main__":
    iniciar_servidor()
