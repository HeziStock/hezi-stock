# How to run HEZI STOCK portal

## Option 1: Double-click
Double-click **`Open Portal.bat`**.  
A window will open; after a few seconds the browser will open the dashboard. **Leave that window open** – closing it stops the site.

## Option 2: Terminal (if Bat doesn’t work)
1. Open **PowerShell** or **CMD**.
2. Run:
   ```bash
   cd c:\Users\hezima\stock-tracker
   python app.py
   ```
3. In the browser go to: **http://127.0.0.1:5000/app**

## If you see an error
- **"Python not found"** → Install Python and add it to PATH, or run from **Anaconda Prompt** if you use Anaconda.
- **"Address already in use"** → Something is already using port 5000. Close that program or run: `python app.py` and the app will show the real error.
- **Module not found (e.g. flask, yfinance)** → In the project folder run: `pip install flask pandas yfinance plyer`

## Direct link once it’s running
- Dashboard: http://127.0.0.1:5000/app  
- Home: http://127.0.0.1:5000
