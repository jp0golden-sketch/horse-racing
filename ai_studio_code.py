import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. TECHNICAL DATA TABLES (MOZAN 1920)
# ==========================================

EGYPTIAN = {
    'A': 1, 'B': 2, 'C': 2, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 8, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 6, 'Y': 1, 'Z': 7
}

PLANETARY_ORDER = {
    1: "Sun (☀️)", 4: "Sun (☀️)", 2: "Moon (🌙)", 7: "Moon (🌙)",
    3: "Jupiter (♃)", 5: "Mercury (☿)", 6: "Venus (♀)",
    8: "Saturn (♄)", 9: "Mars (♂)"
}

# ==========================================
# 2. NUMEROLOGICAL ENGINE
# ==========================================

def reduce_teosophic(n):
    if n == 0: return 0
    res = n % 9
    return 9 if res == 0 else res

def calculate_mozan_value(name, is_horse=True):
    name = "".join(filter(str.isalpha, name.upper()))
    if not name: return 0
    
    if not is_horse:
        exclude_list = ["THE", "HIS", "HIGHNESS", "HH", "MAHARAJA", "CUP", "PLATE"]
        for word in exclude_list:
            if name.startswith(word): name = name.replace(word, "", 1)

    vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
    total = 0
    for i, char in enumerate(name):
        next_is_vowel = (i + 1 < len(name)) and (name[i+1] in vowels)
        if char == 'S': total += 3 if next_is_vowel else 6
        elif char == 'C': total += 3 if next_is_vowel else 2
        elif char in ['O', 'R']: total += 7 if char == 'O' else 2
        else: total += EGYPTIAN.get(char, 0)
    return reduce_teosophic(total)

def get_dv_value(day, month_index):
    d = day
    if month_index in [1, 3]: # Jan, Mar
        if d <= 8: return 6
        elif d == 9: return 8
        elif d == 10: return 9
        elif d <= 17: return 5
        elif d == 18: return 2
        elif d <= 26: return 4
        return 3
    elif month_index == 2: # Feb
        if d <= 8: return 6
        elif d <= 15: return 5
        elif d == 16: return 2
        elif d <= 24: return 4
        return 3
    elif month_index == 4: # Apr
        if d <= 2: return 6
        elif d <= 9: return 5
        elif d == 10: return 2
        elif d <= 18: return 4
        return 3
    elif month_index in [5, 7]: # May, Jul
        if d == 1: return 6
        elif d <= 8: return 5
        elif d <= 15: return 4
        elif d == 16: return 1
        elif d <= 24: return 3
        return 2
    elif month_index in [6, 8]: # Jun, Aug
        if d <= 7: return 5
        elif d <= 14: return 4
        elif d == 15: return 1
        elif d <= 23: return 3
        return 2
    elif month_index == 9: # Sep
        if d <= 2: return 5
        elif d <= 9: return 4
        elif d == 10: return 1
        elif d <= 18: return 3
        elif d <= 28: return 2
        return 1
    elif month_index == 10: # Oct
        if d == 1: return 5
        elif d <= 8: return 4
        elif d == 9: return 1
        elif d <= 15: return 3
        elif d == 16: return 7
        elif d <= 24: return 2
        return 1
    elif month_index == 11: # Nov
        if d <= 7: return 4
        elif d == 8: return 1
        elif d <= 14: return 3
        elif d == 15: return 9
        elif d <= 23: return 2
        return 1
    elif month_index == 12: # Dec
        if d <= 7: return 4
        elif d <= 14: return 3
        elif d <= 22: return 2
        return 1
    return 1

# ==========================================
# 3. INTERFACE (TURBO UPDATED)
# ==========================================

st.set_page_config(page_title="Mozan Professional Turbo v3.1", layout="wide")
st.title("🏇 Mozan's Racing Numerology Professional (Turbo v3.1)")
st.markdown("---")

with st.sidebar:
    st.header("📋 Race Setup")
    race_date = st.date_input("Race Date", datetime.now())
    race_name = st.text_input("Race Title (V.P.)", "Camarero Race Track")
    st.markdown("---")
    st.info("💡 Tip: If a horse is missing (e.g. #6), type 'SCRATCH' in that line to keep the numbering correct.")
    all_horses_input = st.text_area("Paste Runner List", "Horse 1\nHorse 2\nHorse 3\nHorse 4\nHorse 5\nSCRATCH\nHorse 7\nHorse 8")

# Calculation of Global Figures (Excluding Scratched Horses)
raw_horse_list = [h.strip() for h in all_horses_input.split("\n") if h.strip()]
active_runners = [h for h in raw_horse_list if "SCRATCH" not in h.upper() and "VACANT" not in h.upper()]

fnh = reduce_teosophic(len(active_runners))
dv = get_dv_value(race_date.day, race_date.month)
vp = calculate_mozan_value(race_name, is_horse=False)
id_sum = sum([EGYPTIAN.get(h[0].upper(), 0) for h in active_runners if h])
id_digit = reduce_teosophic(id_sum)

# Summary Header
st.subheader("Global Race Figures")
c1, c2, c3, c4 = st.columns(4)
c1.metric("D.V. (Day Value)", dv)
c2.metric("F.N.H. (Active Runners)", fnh)
c3.metric("I.D. (Active Group ID)", id_digit)
c4.metric("V.P. (Plate Value)", vp)

if st.button("🚀 ANALYZE ALL ACTIVE RUNNERS"):
    results = []
    
    # Process original list to maintain Saddle Numbers
    for idx, name in enumerate(raw_horse_list):
        saddle_no = idx + 1
        
        # Skip Scratched Horses for the table
        if "SCRATCH" in name.upper() or "VACANT" in name.upper():
            continue
            
        vh = calculate_mozan_value(name)
        score = 0
        verdict = "Low Probability"
        emoji = "❄️"
        
        if vh == dv: score += 60
        if vh == fnh: score += 15
        if vh == id_digit: score += 15
        if vh == reduce_teosophic(saddle_no): score += 10
        
        if score >= 60: 
            verdict = "OUTRIGHT WINNER"
            emoji = "💎"
        elif score >= 25: 
            verdict = "Strong Candidate"
            emoji = "⭐"
        elif vh == reduce_teosophic(saddle_no):
            verdict = "Unit Force (Place)"
            emoji = "📍"
        
        results.append({
            "Rank": emoji,
            "Saddle #": saddle_no,
            "Horse Name": name.upper(),
            "V.H. (Value)": vh,
            "Planet": PLANETARY_ORDER.get(vh, "-"),
            "Score": score,
            "Verdict": verdict
        })
    
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)
        st.markdown("---")
        st.subheader("Race Prediction Table")
        st.table(df)
    else:
        st.error("No active runners to analyze.")

st.markdown("---")
st.caption("Mozan's Racing Numerology v3.1 | Handles Scratch Gaps.")
