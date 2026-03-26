import socket
import urllib.parse

HOST = '127.0.0.1'
PORT = 80

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        
        print(f"--- Servidor Avanzado corriendo en http://{HOST}:{PORT} ---")

        while True:
            client_socket, addr = server_socket.accept()
            
            with client_socket:
                # 1. Recibir la petición entera (Aumentamos a 4096 bytes por si el POST es grande)
                request_data = client_socket.recv(4096).decode('utf-8')
                if not request_data:
                    continue

                # 2. PARSEO: Separar Encabezados del Body
                # HTTP usa \r\n\r\n para separar la metadata de los datos reales
                partes = request_data.split('\r\n\r\n', 1)
                headers = partes[0]
                body = partes[1] if len(partes) > 1 else ""

                # 3. PARSEO: Leer la primera línea para saber qué quiere el navegador
                lineas = headers.split('\r\n')
                primera_linea = lineas[0].split()
                
                if len(primera_linea) >= 2:
                    metodo = primera_linea[0]  # GET o POST
                    ruta = primera_linea[1]    # / o /enviar
                else:
                    continue

                print(f"[{addr[0]}] Solicitud: {metodo} a la ruta '{ruta}'")

                # 4. LÓGICA DE ENRUTAMIENTO (Nuestra "API")
                
                if metodo == 'GET' and ruta == '/':
                    # Página principal con un formulario HTML
                    respuesta_body = """
                    <!DOCTYPE html>
                    <html>
                    <body style="font-family: sans-serif; padding: 20px;">
                        <h2>Taller HTTP: Prueba de POST</h2>
                        <form action="/enviar" method="POST">
                            <label>Escribe un mensaje secreto:</label><br><br>
                            <input type="text" name="mensaje_secreto" size="40"><br><br>
                            <input type="submit" value="Enviar al Servidor por POST">
                        </form>
                    </body>
                    </html>
                    """
                    codigo_estado = "200 OK"

                elif metodo == 'POST' and ruta == '/enviar':
                    # 1. Limpiamos la codificación URL (+ a espacio, %3E a >, etc.)
                    body_limpio = urllib.parse.unquote_plus(body)
                    
                    if body_limpio.startswith("mensaje_secreto="):
                        mensaje_final = body_limpio.replace("mensaje_secreto=", "")
                    else:
                        mensaje_final = body_limpio

                    print(f"--> DATOS CRUDOS: {body}")
                    print(f"--> DATOS LIMPIOS: {mensaje_final}") 
                    
                    respuesta_body = f"""
                    <!DOCTYPE html>
                    <html>
                    <body style="background-color: #e0ffe0; font-family: sans-serif; padding: 20px;">
                        <h2>¡POST Recibido Exitosamente!</h2>
                        <p>El servidor entendió perfectamente tu mensaje:</p>
                        <h3>{mensaje_final}</h3>
                        <br><br>
                        <a href="/">Volver a intentar</a>
                    </body>
                    </html>
                    """
                    codigo_estado = "200 OK"

                else:
                    # Si piden una URL que no existe
                    respuesta_body = "<h1>Error 404</h1><p>Esa ruta no existe en este servidor.</p>"
                    codigo_estado = "404 Not Found"

                # 5. CONSTRUIR Y ENVIAR RESPUESTA FINAL
                headers_resp = f"HTTP/1.1 {codigo_estado}\r\n"
                headers_resp += "Content-Type: text/html; charset=utf-8\r\n"
                headers_resp += "Connection: close\r\n\r\n"
                
                http_response = headers_resp + respuesta_body
                client_socket.sendall(http_response.encode('utf-8'))

if __name__ == '__main__':
    iniciar_servidor()