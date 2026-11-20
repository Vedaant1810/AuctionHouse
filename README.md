# AuctionHouse
## Setup Instructions

### Requirements
- Python 3 installed.
- No additional Python packages are required.

### Running the Server
1. Open a terminal in the main project directory.
2. Run the following command:

   ```bash
   python3 server/server.py
   ```
3. The server will start listening on port `5000`.
4. Keep the server terminal running while clients connect.

### Running the Client
1. Open a separate terminal in the main project directory.
2. Run:

   ```bash
   python3 client/client.py
   ```
3. The client will connect to the server.
4. Select option `1` to test the server connection or option `2` to disconnect.

### Running Multiple Clients
Open additional terminals and run the client command again. Multiple clients can connect to the same server simultaneously.

### Network Configuration
The server listens on port `5000` using `0.0.0.0`. For connections from other computers, update `SERVER_HOST` in `client/client.py` to the server computer's IP address. Ensure port `5000` is allowed through the server's firewall.