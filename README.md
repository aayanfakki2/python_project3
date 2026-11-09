# Itihaas Rank Quiz

Indian History GK quiz with rank titles (Praja to Chakravarti) and a leaderboard.

## Files
- index.html: the mobile-style web app (all HTML, CSS and JS in one file)
- indian_history_quiz.py: the original terminal version

## Run the web app
Option 1 (easiest): double-click index.html. It opens in your browser.

Option 2 (local server, from this folder):
    python -m http.server 8000
Then open http://localhost:8000 in your browser.
On the same Wi-Fi you can open http://<your-computer-IP>:8000 on your phone.

Scores and your name are saved in the browser (localStorage).
The Nunito font loads from Google Fonts when online; offline it falls back to a system font.

## Run the terminal version
Needs Python 3.8+ (no extra packages):
    python indian_history_quiz.py
The leaderboard is saved to leaderboard.json next to the script.
