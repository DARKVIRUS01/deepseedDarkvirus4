"""
PASSWORD SECURITY ANALYZER
A CLI tool to analyze password strength and suggest improvements.
"""
import re

COMMON_PASSWORDS = [
    'password', '123456', '123456789', 'qwerty', 'abc123', 'password1', '111111', '123123',
    'letmein', 'welcome', 'monkey', 'dragon', 'football', 'iloveyou', 'admin', 'login',
    'princess', 'sunshine', 'master', 'hello', 'freedom', 'whatever', 'qazwsx', 'trustno1'
]

CRITERIA = [
    (lambda pw: len(pw) >= 8, 'Length (minimum 8 characters)'),
    (lambda pw: re.search(r'[A-Z]', pw), 'Contains uppercase letters'),
    (lambda pw: re.search(r'[a-z]', pw), 'Contains lowercase letters'),
    (lambda pw: re.search(r'\d', pw), 'Contains numbers'),
    (lambda pw: re.search(r'[!@#$%^&*]', pw), 'Contains special characters (!@#$%^&*)'),
    (lambda pw: pw.lower() not in COMMON_PASSWORDS, 'Not a common password')
]

LEVELS = [
    (101, 120, 'Excellent'),
    (81, 100, 'Strong'),
    (61, 80, 'Good'),
    (41, 60, 'Fair'),
    (0, 40, 'Weak')
]

def analyze_password(pw):
    score = 0
    results = []
    suggestions = []
    for i, (check, desc) in enumerate(CRITERIA):
        passed = bool(check(pw))
        results.append((desc, passed))
        if passed:
            score += 20
        else:
            if i == 0:
                suggestions.append('- Use at least 8 characters')
            elif i == 1:
                suggestions.append('- Add uppercase letters')
            elif i == 2:
                suggestions.append('- Add lowercase letters')
            elif i == 3:
                suggestions.append('- Add numbers')
            elif i == 4:
                suggestions.append('- Add special characters (!@#$%^&*)')
            elif i == 5:
                suggestions.append('- Avoid common password patterns')
    for minv, maxv, label in LEVELS:
        if minv <= score <= maxv:
            level = label
            break
    return score, level, results, suggestions

def main():
    print("=== PASSWORD SECURITY ANALYZER ===")
    pw = input("Enter password to analyze: ")
    print("\n🔒 SECURITY ANALYSIS RESULTS")
    print(f"Password: {pw}")
    score, level, results, suggestions = analyze_password(pw)
    print(f"Score: {score}/120 ({level})\n")
    for desc, passed in results:
        print(f"{'✅' if passed else '❌'} {desc}")
    if suggestions:
        print("\n💡 SUGGESTIONS:")
        for s in suggestions:
            print(s)
    else:
        print("\nYour password is excellent!")

if __name__ == "__main__":
    main()
