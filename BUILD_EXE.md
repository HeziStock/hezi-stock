# Building a single EXE (HEZI STOCK)

You can build a standalone executable so others can run HEZI STOCK **without installing Python**.

## Prerequisites

- Python 3.8+ with the project dependencies installed:
  ```bash
  pip install -r requirements.txt
  pip install pyinstaller
  ```

## One-line build

From the **project folder** (where `app.py` is):

```bash
pyinstaller --name "HEZI STOCK" --onefile --add-data "templates;templates" --add-data "static;static" --hidden-import=flask --hidden-import=yfinance --hidden-import=pandas --hidden-import=plyer --collect-all yfinance app.py
```

- **Windows:** use semicolons in `--add-data` as above (`templates;templates`).
- **macOS/Linux:** use colons: `--add-data "templates:templates"` and `--add-data "static:static"`.

The `.exe` (or binary) will be in the `dist/` folder.

## What the EXE does

- Running the EXE starts the **Flask server** (same as `python app.py`).
- It listens on `http://0.0.0.0:5000`.
- The user must open a browser and go to **http://127.0.0.1:5000** (or use a batch file that starts the EXE and then runs `start http://127.0.0.1:5000` after a short delay).

## Notes

- **config.json** and **reports** folder: the EXE will create/use them in the **current working directory** when you run it. So place the EXE in a folder where you want config and reports, or run it from that folder.
- For a friend: give them the EXE + a copy of **config.json** (and optionally a **reports** folder). They run the EXE and open the browser.
- Antivirus may flag PyInstaller EXEs; this is common. You can add an exception or build on the target PC.

## Using the spec file (optional)

For more control, use the provided spec file:

```bash
pyinstaller build_hezi_stock.spec
```

Edit `build_hezi_stock.spec` to add more `--add-data` or `hiddenimports` if needed.
