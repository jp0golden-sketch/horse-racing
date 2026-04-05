import streamlit as st
from datetime import datetime

# ==========================================
# 1. TECHNICAL DATA TABLES (MOZAN 1920)
# ==========================================

# Base Egyptian Alphabet Table (Page 9)
EGYPTIAN = {
    'A': 1, 'B': 2, 'C': 2, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 8, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 6, 'Y': 1, 'Z': 7
}

# Planetary Influences (Chapter VIII)
PLANETARY_ORDER = {
    1: "Sun (☀️) - Vitality and Success",
    4: "Sun (☀️) - Strength and Ambition",
    2: "Moon (🌙) - Intuition and Change",
    7: "Moon (🌙) - Adaptability",
    3: "Jupiter (♃) - Fortune and Expansion",
    5: "Mercury (☿) - Speed and Intelligence",
    6: "Venus (♀) - Harmony and Luck",
    8: "Saturn (♄) - Discipline and Endurance",
    9: "Mars (♂) - Energy and Courage"
}

# ==========================================
# 2. NUMEROLOGICAL CALCULATION ENGINE
# ==========================================

def reduce_teosophic(n):
    """Theosophical Reduction to a single digit 1-9 (Mozan's Rule of Zero)."""
    if n == 0: return 0
    # Rule Page 11: Zero does not count (60 = 6, 20 = 2)
    res = n % 9
    return 9 if res == 0 else res

def calculate_mozan_value(name, is_horse=True):
    """
    Calculates the name value using Mozan's exception rules (Page 10):
    - Conditional 'S' and 'C' values based on the following letter.
    - Invariant 'O' and 'R' rules.
    - Title exclusion for Plate Values (V.P.).
    """
    name = "".join(filter(str.isalpha, name.upper()))
    if not name: return 0
    
    # Cleaning titles for V.P. (Page 12)
    if not is_horse:
        exclude_list = ["THE", "HIS", "HIGHNESS", "HH", "MAHARAJA", "CUP", "PLATE"]
        for word in exclude_list:
            if name.startswith(word): name = name.replace(word, "", 1)

    vowels = ['A', 'E', 'I', 'O', 'U', 'Y'] # 'Y' is treated as a vowel per Mozan
    total = 0
    
    for i, char in enumerate(name):
        # Determine if the next letter exists and is a vowel
        next_is_vowel = (i + 1 < len(name)) and (name[i+1] in vowels)
        
        # SPECIFIC MOZAN RULES (Pages 10-11)
        if char == 'S':
            # S followed by vowel = 3 / S followed by consonant = 6
            total += 3 if next_is_vowel else 6
        elif char == 'C':
            # C followed by vowel = 3 / C followed by consonant = 2
            total += 3 if next_is_vowel else 2
        elif char in ['O', 'R']:
            # O and R are always 7 and 2 respectively
            total += 7 if char == 'O' else 2
        else:
            total += EGYPTIAN.get(char, 0)
            
    return reduce_teosophic(total)

def get_dv_value(day, month_index):
    """Table 'Ruling Figure of the Day' (Pages 14-15)."""
    d = day
    if month_index in [1, 3]: # Jan, Mar
        if d <= 8: return 6
        if d == 9: return 8
        if d == 10: return 9
        if d <= 17: return 5
        if d == 18: return 2
        if d <= 26: return 4
        return 3
    elif month_index == 2: # Feb
        if d <= 8: return 6
        if d <= 15: return 5
        if d == 16: return 2
        if d <= 24: return 4
        return 3
    elif month_index == 4: # Apr
        if d <= 2: return 6
        if d <= 9: return 5
        if d == 10: return 2
        if d <= 18: return 4
        return 3
    elif month_index in [5, 7]: # May, Jul
        if d == 1: return 6
        if d <= 8: return 5
        if d <= 15: return 4
        if d == 16: return 1
        if d <= 24: return 3
        return 2
    elif month_index in [6, 8]: # Jun, Aug
        if d <= 7: return 5
        if d <= 14: return 4
        if d == 15: return 1
        if d <= 23: return 3
        return 2
    elif month_index == 9: # Sep
        if d <= 2: return 5
        if d <= 9: return 4
        if d == 10: return 1
        if d <= 18: return 3
        if d <= 28: return 2
        return 1
    elif month_index == 10: # Oct
        if d == 1: return 5
        if d <= 8: return 4
        if d == 9: return 1
        if d <= 15: return 3
        if d == 16: return 7
        if d <= 24: return 2
        return 1
    elif month_index == 11: # Nov
        if d <= 7: return 4
        if d == 8: return 1
        if d <= 14: return 3
        if d == 15: return 9
        if d <= 23: return 2
        return 1
    elif month_index == 12: # Dec
        if d <= 7: return 4
        if d <= 14: return 3
        if d <= 22: return 2
        return 1
    return 1

# ==========================================
# 3. USER INTERFACE (STREAMLIT)
# ==========================================

st.set_page_config(page_title="Mozan's Expert System", layout="wide")

# Header
st.title("🏇 Mozan's Racing Numerology Professional")
st.markdown("---")

# Column Layout
col_side, col_main = st.columns([1, 2])

with col_side:
    st.header("📋 Race Data")
    race_date = st.date_input("Race Date", datetime.now())
    race_name = st.text_input("Race Title (V.P.)", "Arlington Handicap")
    st.subheader("👥 All Entries")
    all_horses_input = st.text_area("Paste names of all runners (one per line)", "Shadow\nThunderbolt\nGold Star\nWinner")
    
    # Real-time Calculations
    horse_list = [h.strip() for h in all_horses_input.split("\n") if h.strip()]
    fnh = reduce_teosophic(len(horse_list))
    dv = get_dv_value(race_date.day, race_date.month)
    vp = calculate_mozan_value(race_name, is_horse=False)
    # I.D. Calculation (Initials of all entries using Egyptian table)
    id_sum = sum([EGYPTIAN.get(h[0].upper(), 0) for h in horse_list if h])
    id_digit = reduce_teosophic(id_sum)

with col_main:
    st.header("🔍 Horse Analysis")
    target_name = st.text_input("Horse Name to Evaluate", "SHADOW")
    target_no = st.number_input("Saddle Number (#)", min_value=1, value=1)
    
    st.markdown("### Ruling Figures Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("D.V. (Day Value)", dv)
    c2.metric("F.N.H. (Structure)", fnh)
    c3.metric("I.D. (Group ID)", id_digit)
    c4.metric("V.P. (Plate Value)", vp)

    if st.button("CALCULATE PROBABILITY"):
        vh = calculate_mozan_value(target_name)
        planet_desc = PLANETARY_ORDER.get(vh, "Unknown")
        
        st.markdown("---")
        st.subheader(f"Analysis Report: {target_name}")
        
        score = 0
        matches = []
        
        # Scoring Logic based on the Book's Hierarchy
        if vh == dv:
            score += 60
            matches.append(f"🌟 **Direct Day Connection:** The horse vibrates with the ruling day force {dv}.")
        if vh == fnh:
            score += 15
            matches.append(f"📊 **F.N.H. Affinity:** Matches the structural count of participants.")
        if vh == id_digit:
            score += 15
            matches.append(f"🆔 **I.D. Affinity:** Synchronized with the group's initials.")
        if vh == target_no:
            score += 10
            matches.append(f"⚡ **Unit Force:** The name value matches the saddle number.")

        # Visual Verdicts
        if score >= 60:
            st.success(f"💎 **OUTRIGHT WINNER** - Score: {score}")
            st.balloons()
        elif score >= 25:
            st.warning(f"⭐ **STRONG CANDIDATE** - Score: {score}")
        elif vh == target_no:
            st.info(f"📍 **UNIT FORCE** - Recommended for Podiums (Place)")
        else:
            st.error(f"❌ **LOW PROBABILITY** - Score: {score}")

        st.markdown(f"**Influence:** {planet_desc}")
        
        with st.expander("Technical Details (Mozan's Rules)"):
            st.write(f"- Horse Value (V.H.): {vh}")
            st.write(f"- Initial rules applied: Yes")
            st.write(f"- S/C/O/R exceptions processed: Yes")
            if matches:
                for m in matches: st.write(m)
            else:
                st.write("No significant numerical matches detected.")

st.markdown("---")
st.caption("Mozan's Racing Numerology v2.1 | Algorithmic Implementation of the 1920 Original Manual.")