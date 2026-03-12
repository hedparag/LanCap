# LanCap Messenger

LanCap is a local network (LAN) messenger built with Python and PySide6. It features a classic, clean instant messenger interface that runs natively on your desktop. It automatically discovers other users on the same local network using UDP broadcasts, eliminating the need to connect to an external server.

## Features

- **Classic UI:** A vertical, clean interface reminiscent of classic chat applications.
- **Auto-Discovery:** Automatically finds other peers on your local network and displays them under the general chats list.
- **Dynamic Names:** Picks up your exact system name automatically so you never have to register.
- **Zero Configuration:** Operates completely peer-to-peer on the local network (LAN). Just run it without adjusting firewall routing.

## Prerequisites

- **Python 3.8+** installed on your system.
- Make sure `pip` (the Python package installer) is available.

## Installation and Setup

1. **Get the Source Code**
   Make sure you have all the source files in a local directory (e.g., your `LanCap` folder).

2. **Open your Terminal (or Command Prompt / PowerShell)**
   Navigate to the project root directory where the `requirements.txt` file is located:
   ```bash
   cd path\to\LanCap
   ```

3. **(Optional) Create a Virtual Environment**
   It is recommended to use a virtual environment to manage dependencies separately from your global Python installation.
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install Dependencies**
   Install the required libraries listed in `requirements.txt`, which includes `PySide6` for the user interface.
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To launch the messenger, make sure you are in the project's root folder and run the `main.py` script:

```bash
python src/main.py
```

> **Note:** Depending on your operating system, Windows Firewall (or your respective firewall software) may display a popup asking to allow the application to communicate on Private networks upon first launch. This is necessary for the auto-discovery broadcast to work.

## Testing LAN Discovery

To see the dynamic discovery feature in action:
1. Ensure the application is set up on **two computers** on the exact same Wi-Fi connection or local area network.
2. Run `python src/main.py` on both computers.
3. The computers will automatically discover each other via UDP broadcasts (default Port 37020) in the background. If successful, the second computer's operating system name will appear dynamically under your `General` group list, and vice-versa!

## Technologies Used

- **Python**
- **PySide6 (Qt for Python)** - for the robust GUI framework.
- Built-in **socket** & **threading** packages - for managing the local background peer discovery.
