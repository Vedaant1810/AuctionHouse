import socket
import threading
import json

# Server configuration
HOST = "0.0.0.0"
PORT = 5000

# Keep track of connected clients
connected_clients = set()
clients_lock = threading.Lock()


def send_message(client_socket, message):
    """Send a JSON message followed by a newline."""
    try:
        data = json.dumps(message) + "\n"
        client_socket.sendall(data.encode("utf-8"))
    except OSError:
        print("Failed to send message to client.")


def handle_client(client_socket, client_address):
    """Handle communication with an individual client."""

    print(f"[NEW CONNECTION] {client_address} connected.")

    with clients_lock:
        connected_clients.add(client_socket)

    try:
        # Read newline-delimited messages
        with client_socket.makefile("r", encoding="utf-8") as reader:
            for line in reader:
                line = line.strip()

                if not line:
                    continue

                try:
                    message = json.loads(line)
                    message_type = message.get("type")

                    print(f"[RECEIVED] {client_address}: {message}")

                    # Handle test communication
                    if message_type == "PING":
                        response = {
                            "type": "PONG",
                            "message": "Server received your message."
                        }

                    else:
                        response = {
                            "type": "ERROR",
                            "error_code": 400,
                            "message": "Unknown message type."
                        }

                    send_message(client_socket, response)

                except json.JSONDecodeError:
                    send_message(client_socket, {
                        "type": "ERROR",
                        "error_code": 400,
                        "message": "Invalid JSON message."
                    })

    except (OSError, ConnectionError) as error:
        print(f"[CONNECTION ERROR] {client_address}: {error}")

    finally:
        with clients_lock:
            connected_clients.discard(client_socket)

        client_socket.close()
        print(f"[DISCONNECTED] {client_address} disconnected.")


def start_server():
    """Start the auction house TCP server."""

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Allow the server to reuse its port
    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("================================")
    print("       AUCTION HOUSE SERVER     ")
    print("================================")
    print(f"Server listening on {HOST}:{PORT}")
    print("Waiting for client connections...\n")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            # Create a separate thread for each client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )

            client_thread.start()

    except KeyboardInterrupt:
        print("\nShutting down server...")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
