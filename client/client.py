import socket
import json

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000


def send_message(client_socket, message):
    """Send a JSON message to the server."""
    data = json.dumps(message) + "\n"
    client_socket.sendall(data.encode("utf-8"))


def receive_message(reader):
    """Receive and decode a JSON response."""
    response = reader.readline()

    if not response:
        return None

    return json.loads(response)


def start_client():
    """Connect to the auction house server."""

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        print("Connected to Auction House Server!")
        print(f"Server: {SERVER_HOST}:{SERVER_PORT}")

        with client_socket.makefile(
            "r",
            encoding="utf-8"
        ) as reader:

            while True:
                print("\n========== AUCTION HOUSE ==========")
                print("1. Test Server Connection")
                print("2. Disconnect")
                
                choice = input("Select an option: ")

                if choice == "1":
                    message = {
                        "type": "PING"
                    }

                    send_message(client_socket, message)

                    response = receive_message(reader)

                    if response:
                        print("\n[SERVER RESPONSE]")
                        print(response)

                elif choice == "2":
                    print("Disconnecting from server...")
                    break

                else:
                    print("Invalid option. Try again.")

    except ConnectionRefusedError:
        print("Could not connect to server.")
        print("Make sure the server is running.")

    except (OSError, ConnectionError) as error:
        print(f"Connection error: {error}")

    finally:
        client_socket.close()
        print("Client disconnected.")


if __name__ == "__main__":
    start_client()
