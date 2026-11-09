#!/usr/bin/env python3
"""
Itihaas Rank Quiz - Indian History GK Rank Game
------------------------------------------------
- 10 random questions per game, 20 seconds each
- Points: 10 for a correct answer + speed bonus (0-5) + streak bonus (+3 from 3rd correct in a row)
- One 50-50 lifeline per game (costs 3 points)
- Your score decides your RANK TITLE (Praja -> Chakravarti)
- Leaderboard is saved in leaderboard.json next to this script

Run:  python indian_history_quiz.py
"""

import json
import os
import random
import time
from datetime import datetime

# ----------------------------- Settings -----------------------------
QUESTIONS_PER_GAME = 10
QUESTION_TIME = 20          # seconds
BASE_POINTS = 10
MAX_SPEED_BONUS = 5
STREAK_BONUS = 3            # given when streak >= 3
LIFELINE_COST = 3
LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")

# Rank titles: (minimum % of max score, title)
RANKS = [
    (0,  "Praja (Commoner)"),
    (20, "Sipahi (Soldier)"),
    (40, "Sardar (Chieftain)"),
    (55, "Mansabdar (Noble)"),
    (70, "Diwan (Minister)"),
    (85, "Peshwa (Prime Minister)"),
    (95, "Chakravarti (Emperor)"),
]

# ----------------------------- Question bank -----------------------------
# (question, [options], index of correct option)
QUESTIONS = [
    ("Who founded the Maurya Empire?",
     ["Ashoka", "Chandragupta Maurya", "Bindusara", "Brihadratha"], 1),
    ("Ashoka embraced Buddhism after which war?",
     ["Battle of Hydaspes", "Battle of Kalinga", "Battle of Tarain", "Battle of Chausa"], 1),
    ("Who wrote the Arthashastra?",
     ["Kalidasa", "Banabhatta", "Kautilya (Chanakya)", "Vishakhadatta"], 2),
    ("Which Chinese traveller visited India during the reign of Chandragupta II (Gupta period)?",
     ["Hiuen Tsang", "Fa-Hien", "I-tsing", "Marco Polo"], 1),
    ("Who wrote the Harshacharita, the biography of Harshavardhana?",
     ["Banabhatta", "Kalhana", "Bilhana", "Dandin"], 0),
    ("Alexander fought King Porus on the banks of which river?",
     ["Indus", "Ravi", "Jhelum (Hydaspes)", "Sutlej"], 2),
    ("Which Indus Valley site is famous for the 'Great Bath'?",
     ["Harappa", "Mohenjo-daro", "Lothal", "Kalibangan"], 1),
    ("Which is the oldest of the four Vedas?",
     ["Yajurveda", "Samaveda", "Atharvaveda", "Rigveda"], 3),
    ("Where was Gautama Buddha born?",
     ["Bodh Gaya", "Sarnath", "Lumbini", "Kushinagar"], 2),
    ("Which Chola king built the Brihadeshwara Temple at Thanjavur?",
     ["Rajendra I", "Rajaraja I", "Aditya I", "Kulottunga I"], 1),
    ("Who founded the Slave (Mamluk) dynasty of the Delhi Sultanate?",
     ["Iltutmish", "Balban", "Qutb ud-Din Aibak", "Razia Sultan"], 2),
    ("Nalanda University was destroyed by which invader?",
     ["Mahmud of Ghazni", "Muhammad Ghori", "Bakhtiyar Khalji", "Timur"], 2),
    ("Vasco da Gama reached Calicut in which year?",
     ["1453", "1498", "1526", "1600"], 1),
    ("The First Battle of Panipat (1526) was fought between Babur and whom?",
     ["Rana Sanga", "Ibrahim Lodi", "Hemu", "Sher Shah Suri"], 1),
    ("Who defeated Humayun at the Battle of Chausa in 1539?",
     ["Sher Shah Suri", "Rana Pratap", "Hemu", "Bairam Khan"], 0),
    ("Which Mughal emperor founded the religious path called Din-i-Ilahi?",
     ["Humayun", "Jahangir", "Akbar", "Aurangzeb"], 2),
    ("Which Mughal emperor built the Taj Mahal?",
     ["Akbar", "Jahangir", "Shah Jahan", "Aurangzeb"], 2),
    ("Sher Shah Suri is credited with rebuilding which major highway?",
     ["Silk Road", "Grand Trunk Road", "Royal Road", "Deccan Highway"], 1),
    ("Who was the founder of the Maratha Empire?",
     ["Shahu", "Sambhaji", "Shivaji", "Baji Rao I"], 2),
    ("The Third Battle of Panipat (1761) was fought between the Marathas and whom?",
     ["Nadir Shah", "Ahmad Shah Abdali", "Hyder Ali", "The British"], 1),
    ("Who founded the Sikh Empire in Punjab?",
     ["Guru Gobind Singh", "Banda Singh Bahadur", "Maharaja Ranjit Singh", "Guru Nanak"], 2),
    ("The Battle of Plassey was fought in which year?",
     ["1757", "1764", "1799", "1857"], 0),
    ("Who was the last Mughal emperor?",
     ["Muhammad Shah", "Shah Alam II", "Bahadur Shah Zafar", "Akbar II"], 2),
    ("The Revolt of 1857 began at which place?",
     ["Delhi", "Kanpur", "Lucknow", "Meerut"], 3),
    ("The 'Doctrine of Lapse' was introduced by which Governor-General?",
     ["Lord Wellesley", "Lord Dalhousie", "Lord Cornwallis", "Lord Canning"], 1),
    ("In which year was the Indian National Congress founded?",
     ["1857", "1885", "1905", "1919"], 1),
    ("The Partition of Bengal (1905) was carried out by which Viceroy?",
     ["Lord Curzon", "Lord Minto", "Lord Ripon", "Lord Hardinge"], 0),
    ("The capital of British India was shifted from Calcutta to Delhi in which year?",
     ["1905", "1911", "1919", "1931"], 1),
    ("Gandhi's first satyagraha in India (1917) was in which place?",
     ["Kheda", "Bardoli", "Champaran", "Ahmedabad"], 2),
    ("The Jallianwala Bagh massacre took place in which year?",
     ["1915", "1919", "1922", "1930"], 1),
    ("The Dandi March (Salt Satyagraha) took place in which year?",
     ["1920", "1927", "1930", "1942"], 2),
    ("The Quit India Movement was launched in which year?",
     ["1930", "1940", "1942", "1946"], 2),
    ("Which leader is associated with the slogan 'Delhi Chalo'?",
     ["Bhagat Singh", "Subhas Chandra Bose", "Lala Lajpat Rai", "Bal Gangadhar Tilak"], 1),
    ("Who was the last Viceroy of India and first Governor-General of independent India?",
     ["Lord Wavell", "Lord Mountbatten", "C. Rajagopalachari", "Lord Linlithgow"], 1),
    ("The Constitution of India came into effect on which date?",
     ["15 August 1947", "26 November 1949", "26 January 1950", "2 October 1950"], 2),
]

# ----------------------------- Helpers -----------------------------

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def max_possible_score():
    """Theoretical max: every answer correct, instant, with streak bonuses, no lifeline."""
    streak_bonuses = max(0, QUESTIONS_PER_GAME - 2) * STREAK_BONUS
    return QUESTIONS_PER_GAME * (BASE_POINTS + MAX_SPEED_BONUS) + streak_bonuses


def get_rank(score):
    pct = max(0, score) / max_possible_score() * 100
    title = RANKS[0][1]
    for min_pct, name in RANKS:
        if pct >= min_pct:
            title = name
    return title


def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save_leaderboard(entries):
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    except OSError:
        print("(Could not save leaderboard.)")


def sorted_board(entries):
    return sorted(entries, key=lambda e: (-e.get("score", 0), e.get("time", 9999)))


def show_leaderboard(highlight=None, top=10):
    board = sorted_board(load_leaderboard())
    print("\n" + "=" * 66)
    print(f"{'🏆  LEADERBOARD':^66}")
    print("=" * 66)
    if not board:
        print("No games played yet. Be the first!")
        return
    print(f"{'#':<4}{'Player':<16}{'Score':<8}{'Correct':<10}{'Rank Title':<28}")
    print("-" * 66)
    for i, e in enumerate(board[:top], 1):
        mark = " <-- you" if highlight is not None and e is highlight else ""
        print(f"{i:<4}{e['name'][:15]:<16}{e['score']:<8}"
              f"{str(e['correct']) + '/' + str(e['total']):<10}{e['rank'][:27]:<28}{mark}")


def ask_question(number, total, q, state):
    """Ask one question. Returns True if correct, False if wrong/timeout, None if quit."""
    text, options, correct_idx = q
    # shuffle options but remember the correct one
    order = list(range(4))
    random.shuffle(order)
    shown = [options[i] for i in order]
    correct_pos = order.index(correct_idx)
    removed = set()

    print("\n" + "-" * 66)
    print(f"Question {number}/{total}   |   Score: {state['score']}   |   Streak: {state['streak']}")
    print("-" * 66)
    print(text + "\n")

    def draw():
        for i, opt in enumerate(shown):
            if i not in removed:
                print(f"  {i + 1}. {opt}")
        extras = "  [h] 50-50 lifeline" if not state["lifeline_used"] else ""
        print(f"\n  [q] quit game{extras}")

    draw()
    start = time.time()

    while True:
        ans = input(f"\nYour answer (you have {QUESTION_TIME}s): ").strip().lower()
        elapsed = time.time() - start

        if ans == "q":
            return None
        if ans == "h":
            if state["lifeline_used"]:
                print("Lifeline already used!")
                continue
            state["lifeline_used"] = True
            state["score"] -= LIFELINE_COST
            wrong = [i for i in range(4) if i != correct_pos]
            removed.update(random.sample(wrong, 2))
            print(f"50-50 used! (-{LIFELINE_COST} points)\n")
            draw()
            continue
        if ans in {"1", "2", "3", "4"}:
            choice = int(ans) - 1
            if choice in removed:
                print("That option was removed. Choose another.")
                continue
            break
        print("Enter 1-4, h for lifeline, or q to quit.")

    state["time_taken"] += elapsed

    if elapsed > QUESTION_TIME:
        print(f"\n⏰ Time's up! ({elapsed:.1f}s) The answer was: {shown[correct_pos]}")
        state["streak"] = 0
        return False

    if choice == correct_pos:
        speed_bonus = round(MAX_SPEED_BONUS * (1 - elapsed / QUESTION_TIME))
        state["streak"] += 1
        streak_bonus = STREAK_BONUS if state["streak"] >= 3 else 0
        gained = BASE_POINTS + speed_bonus + streak_bonus
        state["score"] += gained
        print(f"\n✅ Correct!  +{BASE_POINTS} base  +{speed_bonus} speed"
              + (f"  +{streak_bonus} streak 🔥" if streak_bonus else "")
              + f"   = +{gained}  ({elapsed:.1f}s)")
        return True

    print(f"\n❌ Wrong! The answer was: {shown[correct_pos]}")
    state["streak"] = 0
    return False


def play_game(name):
    questions = random.sample(QUESTIONS, QUESTIONS_PER_GAME)
    state = {"score": 0, "streak": 0, "lifeline_used": False, "time_taken": 0.0}
    correct = 0
    answered = 0

    for i, q in enumerate(questions, 1):
        result = ask_question(i, QUESTIONS_PER_GAME, q, state)
        if result is None:
            print("\nGame abandoned. Score not saved.")
            return
        answered += 1
        if result:
            correct += 1

    final_score = max(0, state["score"])
    rank_title = get_rank(final_score)

    entry = {
        "name": name,
        "score": final_score,
        "correct": correct,
        "total": QUESTIONS_PER_GAME,
        "rank": rank_title,
        "time": round(state["time_taken"], 1),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    entries = load_leaderboard()
    entries.append(entry)
    save_leaderboard(entries)

    board = sorted_board(entries)
    position = next(i for i, e in enumerate(board, 1) if e is entry or e == entry)

    print("\n" + "=" * 66)
    print(f"{'GAME OVER':^66}")
    print("=" * 66)
    print(f"Player        : {name}")
    print(f"Correct       : {correct}/{QUESTIONS_PER_GAME}")
    print(f"Final score   : {final_score} / {max_possible_score()}")
    print(f"Rank title    : 👑 {rank_title}")
    print(f"Leaderboard # : {position} of {len(board)}")

    show_leaderboard(highlight=next((e for e in board if e == entry), None))


def show_rank_guide():
    mx = max_possible_score()
    print("\n" + "=" * 66)
    print(f"{'RANK TITLES':^66}")
    print("=" * 66)
    for pct, title in RANKS:
        print(f"  {title:<28} needs {round(mx * pct / 100):>3}+ points")
    print(f"\n  Max possible score: {mx}")
    print(f"  Scoring: {BASE_POINTS} per correct + up to {MAX_SPEED_BONUS} speed bonus "
          f"+ {STREAK_BONUS} streak bonus (3+ in a row)")
    print(f"  Time limit: {QUESTION_TIME}s per question. 50-50 lifeline costs {LIFELINE_COST} points.")


def main():
    clear_screen()
    print("=" * 66)
    print(f"{'🇮🇳  ITIHAAS RANK QUIZ  🇮🇳':^66}")
    print(f"{'Test your Indian History GK & climb the ranks!':^66}")
    print("=" * 66)

    name = ""
    while not name:
        name = input("\nEnter your name: ").strip()

    while True:
        print(f"\n--- Menu (Player: {name}) ---")
        print("1. Play quiz")
        print("2. View leaderboard")
        print("3. Rank titles & scoring")
        print("4. Change player")
        print("5. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            play_game(name)
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            show_rank_guide()
        elif choice == "4":
            new = input("New player name: ").strip()
            if new:
                name = new
        elif choice == "5":
            print("Jai Hind! 🙏")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nGoodbye! Jai Hind! 🙏")
