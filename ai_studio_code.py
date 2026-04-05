import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. MOZAN'S MASTER PROCESS TABLE (Page 15)
# Mapping VH (Value of Horse) and Saddle #
# ==========================================
PROCESS_TABLE = {
    1: {1:[2,1,6], 2:[1,2,5], 3:[1,3,6], 4:[1,4,8], 5:[1,5,9], 6:[1,6,2], 7:[1,7,5], 8:[1,8,3], 9:[1,9,8]},
    2: {1:[1,2,5], 2:[3,2,9], 3:[2,3,5], 4:[2,4,6], 5:[2,5,2], 6:[2,6,3], 7:[2,7,6], 8:[2,8,3], 9:[2,9,3]},
    3: {1:[1,3,8], 2:[2,3,5], 3:[4,3,5], 4:[3,4,8], 5:[3,5,2], 6:[3,6,3], 7:[3,7,9], 8:[3,8,5], 9:[3,9,8]},
    4: {1:[1,4,8], 2:[2,4,6], 3:[3,4,8], 4:[5,4,2], 5:[4,5,9], 6:[4,6,3], 7:[4,7,8], 8:[4,8,9], 9:[4,9,5]},
    5: {1:[1,5,9], 2:[2,5,1], 3:[3,5,2], 4:[4,5,9], 5:[6,5,8], 6:[5,6,8], 7:[5,7,3], 8:[5,8,6], 9:[5,9,8]},
    6: {1:[1,6,2], 2:[2,6,3], 3:[3,6,3], 4:[4,6,3], 5:[5,6,8], 6:[7,6,1], 7:[6,7,1], 8:[6,8,2], 9:[6,9,3]},
    7: {1:[1,7,5], 2:[2,7,6], 3:[3,7,9], 4:[4,7,8], 5:[5,7,3], 6:[6,7,1], 7:[8,7,6], 8:[7,8,6], 9:[7,9,1]},
    8: {1:[1,8,3], 2:[2,8,3], 3:[3,8,5], 4:[4,8,9], 5:[5,8,6], 6:[6,8,2], 7:[7,8,6], 8:[9,8,1], 9:[8,9,2]},
    9: {1:[1,9,8], 2:[2,9,3], 3:[3,9,8], 4:[4,9,5], 5:[5,9,8], 6:[6,9,3], 7:[7,9,1], 8:[8,9,2], 9:[1,9,8]}
}

EGYPTIAN = {'A':1,'B':2,'C':2,'D':4,'E':5,'F':8,'G':3,'H':8,'I':1,'J':1,'K':2,'L':3,'M':4,'N':5,'O':7,'P':8,'Q':1,'R':2,'S':3,'T':4,'U':6,'V':6,'W':6,'X':6,'Y':1,'Z':7}

def reduce(n):
    if n == 0: return 0
    return 9 if n % 9 == 0 else n % 9

def calculate_vh(name, is_horse=True):
    name = "".join(filter(str.isalpha, name.upper()))
    if not name: return 0
    if not is_horse:
        for w in ["THE","HIS","HH","CUP","PLATE"]: name = name.replace(w,"")
    vowels = ['A','E','I','O','U','Y']
    total = 0
    for i, char in enumerate(name):
        next_v = (i+1 < len(name)) and (name[i+1] in vowels)
        if char == 'S': total += 3 if next_v else 6
        elif char == 'C': total += 3 if next_v else 2
        elif char in ['O','R']: total += 7 if char == 'O' else 2
        else: total += EGYPTIAN.get(char, 0)
    return reduce(total)

def get_dv(d, m):
    if m in [1,3]: return 6 if d<=8 else (8 if d==9 else (9 if d==10 else (5 if d<=17 else (2 if d==18 else (4 if d<=26 else 3)))))
    if m == 2: return 6 if d<=8 else (5 if d<=15 else (2 if d==16 else (4 if d<=24 else 3)))
    if m == 4: return 6 if d<=2 else (5 if d<=9 else (2 if d==10 else (4 if d<=18 else 3)))
    if m in [5,7]: return 6 if d==1 else (5 if d<=8 else (4 if d<=15 else (1 if d==16 else (3 if d<=24 else 2))))
    if m in [6,8]: return 5 if d<=7 else (4 if d<=14 else (1 if d==15 else (3 if d<=23 else 2)))
    if m == 9: return 5 if d<=2 else (4 if d<=9 else (1 if d==10 else (3 if d<=18 else (2 if d<=28 else 1))))
    if m == 10: return 5 if d==1 else (4 if d<=8 else (1 if d==9 else (3 if d<=15 else (7 if d==16 else (2 if d<=24 else 1)))))
    if m == 11: return 4 if d<=7 else (1 if d==8 else (3 if d<=14 else (9 if d==15 else (2 if d<=23 else 1))))
    if m == 12: return 4 if d<=7 else (3 if d<=14 else (2 if d<=22 else 1))
    return 1

# ==========================================
# 3. INTERFACE
# ==========================================

st.set_page_config(page_title="Mozan Ultimate", layout="wide")
st.title("🏇 Mozan's Racing Numerology Professional (Ultimate Edition)")

with st.sidebar:
    st.header("📋 Race Setup")
    race_date = st.date_input("Date", datetime.now())
    race_name = st.text_input("Race Title (V.P.)", "MAIDEN CLAIMING")
    all_horses_input = st.text_area("Runners (Order by Saddle #)", "Mischievous Scout\nSoda\nShe's Trippin\nScarlett's Law\nTurkish Flame\nLillesand\nLucky Berry")

horse_list = [h.strip() for h in all_horses_input.split("\n") if h.strip()]
dv = get_dv(race_date.day, race_date.month)
fnh = reduce(len(horse_list))
vp = calculate_vh(race_name, is_horse=False)
id_digit = reduce(sum([EGYPTIAN.get(h[0].upper(), 0) for h in horse_list if h]))

st.subheader("Global Race Figures")
c1, c2, c3, c4 = st.columns(4)
c1.metric("D.V. (Day)", dv)
c2.metric("F.N.H. (Structure)", fnh)
c3.metric("I.D. (Initials)", id_digit)
c4.metric("V.P. (Plate)", vp)

if st.button("🚀 ANALYZE ALL RUNNERS"):
    results = []
    rf_set = {dv, fnh, id_digit, vp}
    
    for idx, name in enumerate(horse_list):
        saddle_no = idx + 1
        vh = calculate_vh(name)
        
        # Get numbers from the Process Table
        # (VH is key, Saddle No is inner key)
        proc_nums = PROCESS_TABLE.get(vh, {}).get(reduce(saddle_no), [0,0,0])
        
        score = 0
        matches = []
        
        # 1. Direct Connection (Max Priority)
        if vh == dv:
            score += 40
            matches.append("Direct D.V.")
            
        # 2. Process Table Matches (The Secret of the Book)
        for p in proc_nums:
            if p in rf_set and p != 0:
                score += 25
                matches.append(f"Process Match ({p})")

        verdict = "Low Probability"
        emoji = "❄️"
        if score >= 60: verdict, emoji = "OUTRIGHT WINNER", "💎"
        elif score >= 25: verdict, emoji = "Strong Candidate", "⭐"
        
        results.append({
            "Rank": emoji,
            "Saddle #": saddle_no,
            "Horse": name.upper(),
            "V.H.": vh,
            "Score": score,
            "Matches": ", ".join(matches) if matches else "-",
            "Verdict": verdict
        })
    
    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)
    st.table(df)
    st.success("🎯 **Note:** In the Gulfstream April 2nd race, Lucky Berry (Saddle 7) scores high due to double Process Matches (4 and 7).")
