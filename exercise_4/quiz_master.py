"""
INTERACTIVE QUIZ MASTER.
"""
import time
import random
import os
import ast

DATA_FILE = os.path.join(os.path.dirname(__file__), "quiz_highscores.py")


QUESTIONS = {
    "Science": {
        "easy": [
            {"question": "What planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": 1},
            {"question": "What gas do plants breathe in?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": 1},
            {"question": "How many legs does an insect have?", "options": ["4", "6", "8", "10"], "answer": 1},
            {"question": "What is H2O?", "options": ["Salt", "Water", "Oxygen", "Hydrogen"], "answer": 1},
            {"question": "What organ pumps blood?", "options": ["Liver", "Heart", "Lung", "Brain"], "answer": 1},
        ],
        "hard": [
            {"question": "What is the atomic number of Carbon?", "options": ["4", "6", "8", "12"], "answer": 1},
            {"question": "What is the speed of light in km/s?", "options": ["300,000", "150,000", "30,000", "3,000"], "answer": 0},
            {"question": "What is the chemical symbol for gold?", "options": ["Au", "Ag", "Gd", "Go"], "answer": 0},
            {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"], "answer": 1},
            {"question": "What is the largest planet?", "options": ["Earth", "Jupiter", "Saturn", "Neptune"], "answer": 1},
        ]
    },
    "History": {
        "easy": [
            {"question": "Who was the first US president?", "options": ["Lincoln", "Washington", "Jefferson", "Adams"], "answer": 1},
            {"question": "What year did WW2 end?", "options": ["1945", "1939", "1918", "1963"], "answer": 0},
            {"question": "Where were the pyramids built?", "options": ["Greece", "Egypt", "Rome", "China"], "answer": 1},
            {"question": "Who discovered America?", "options": ["Columbus", "Magellan", "Cook", "Vespucci"], "answer": 0},
            {"question": "What wall fell in 1989?", "options": ["Berlin", "China", "Hadrian's", "Wailing"], "answer": 0},
        ],
        "hard": [
            {"question": "Who wrote the Iliad?", "options": ["Homer", "Virgil", "Plato", "Socrates"], "answer": 0},
            {"question": "Who was the first Roman emperor?", "options": ["Julius Caesar", "Augustus", "Nero", "Tiberius"], "answer": 1},
            {"question": "What year did the French Revolution start?", "options": ["1789", "1776", "1812", "1804"], "answer": 0},
            {"question": "Who was known as the Maid of Orléans?", "options": ["Cleopatra", "Joan of Arc", "Elizabeth I", "Catherine"], "answer": 1},
            {"question": "What empire built Machu Picchu?", "options": ["Aztec", "Inca", "Maya", "Olmec"], "answer": 1},
        ]
    },
    "Sports": {
        "easy": [
            {"question": "How many players in a soccer team?", "options": ["9", "10", "11", "12"], "answer": 2},
            {"question": "What sport uses a bat and ball?", "options": ["Soccer", "Tennis", "Cricket", "Basketball"], "answer": 2},
            {"question": "What color are tennis balls?", "options": ["Red", "Yellow", "Blue", "Green"], "answer": 1},
            {"question": "What is the NBA?", "options": ["Baseball", "Basketball", "Football", "Hockey"], "answer": 1},
            {"question": "What sport is Serena Williams famous for?", "options": ["Golf", "Tennis", "Soccer", "Swimming"], "answer": 1},
        ],
        "hard": [
            {"question": "How many Olympic rings?", "options": ["4", "5", "6", "7"], "answer": 1},
            {"question": "Who has most Grand Slam tennis titles (men)?", "options": ["Nadal", "Federer", "Djokovic", "Sampras"], "answer": 2},
            {"question": "What country won the 2018 FIFA World Cup?", "options": ["Brazil", "France", "Germany", "Spain"], "answer": 1},
            {"question": "What is a perfect score in bowling?", "options": ["200", "250", "300", "350"], "answer": 2},
            {"question": "What is the national sport of Japan?", "options": ["Karate", "Sumo", "Judo", "Kendo"], "answer": 1},
        ]
    }
}

def load_highscores():
    highscores = {}
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    cat, score = line.split(':', 1)
                    try:
                        highscores[cat] = int(score)
                    except Exception:
                        pass
    except Exception:
        pass
    return highscores

def save_highscores(highscores):
    with open(DATA_FILE, "w") as f:
        f.write("# High scores by category\n")
        for cat, score in highscores.items():
            f.write(f"{cat}:{score}\n")

def progress_bar(current, total, width=20):
    done = int(width * current / total)
    return '[' + '█' * done + '░' * (width - done) + f'] {int(100*current/total)}% Complete'

def quiz():
    highscores = load_highscores()
    print("=== QUIZ MASTER ===")
    categories = list(QUESTIONS.keys())
    print("Categories:", ', '.join(categories))
    cat = input("Select category: ").strip().title()
    if cat not in QUESTIONS:
        print("Invalid category.")
        return
    diff = input("Select difficulty (easy/hard): ").strip().lower()
    if diff not in QUESTIONS[cat]:
        print("Invalid difficulty.")
        return
    questions = QUESTIONS[cat][diff][:]
    random.shuffle(questions)
    score = 0
    correct = 0
    results = []
    start_time = time.time()
    for idx, q in enumerate(questions, 1):
        print(f"\nQuestion {idx}/{len(questions)}: {q['question']}")
        print(progress_bar(idx, len(questions)))
        for i, opt in enumerate(q['options']):
            print(f"{chr(65+i)}) {opt}", end='    ')
        print()
        ans = input("Your answer: ").strip().upper()
        try:
            ans_idx = ord(ans) - 65
            if ans_idx == q['answer']:
                print("\n✅ Correct! (+10 points)")
                score += 10
                correct += 1
                results.append((q['question'], True, q['options'][q['answer']]))
            else:
                print(f"\n❌ Incorrect. Correct answer: {q['options'][q['answer']]}")
                results.append((q['question'], False, q['options'][q['answer']]))
        except Exception:
            print("Invalid answer. Skipped.")
            results.append((q['question'], False, q['options'][q['answer']]))
        print(f"Time: {time.time() - start_time:.1f} seconds")
    print(f"\nFINAL SCORE: {score}/{len(questions)*10} ({correct}/{len(questions)} correct)")
    if cat not in highscores or score > highscores[cat]:
        highscores[cat] = score
        save_highscores(highscores)
        print(f"New personal best in {cat}!")
    print("\nDetailed Results:")
    for q, was_correct, correct_ans in results:
        if not was_correct:
            print(f"- {q} | Correct: {correct_ans}")

def main():
    quiz()

if __name__ == "__main__":
    main()
