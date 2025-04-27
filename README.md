# gamesReader

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

Project to fetch the latest news from major gaming websites.

## About This Project

I used to be a Google Reader user, which was a very popular RSS feed aggregator. Google Reader shut down its services in July 2013. Recently, I had the idea to create my own feed reader, starting with gaming websites as the initial focus.

## How to Use

1. Clone the repository:

```bash
git clone https://github.com/JoeReis1983/gamesReader.git
cd gamesReader
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

4. Install the dependencies:

```bash
pip install -r requirements
```

5. Run the project:

```bash
python main.py
```

6. Output:

- A file named `news.json` will be generated containing the latest collected news.

## Project Structure

- `main.py` → Main script to fetch news.
- `requirements` → List of required libraries.
- `sites.txt` → List of gaming websites to scrape.
- `news.json` → Output file with the collected news.

## Notes

- Make sure you have Python 3.8 or higher installed.
- Each time you run the script, it will overwrite the `news.json` file.
- This project is for educational purposes.

---

## License

This project is licensed under the [MIT License](LICENSE).
