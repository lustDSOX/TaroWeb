def create_balance_prompt(user_query, cards):
    prompt = f"""[INST]Question: {user_query}

Cards (use all 4, name each):
1. DEVELOP: {cards[0]['name']} - {cards[0]['meaning_rev'] if cards[0].get('reversed') else cards[0]['meaning_up']}
2. RELEASE: {cards[1]['name']} - {cards[1]['meaning_rev'] if cards[1].get('reversed') else cards[1]['meaning_up']}
3. RESOURCES: {cards[2]['name']} - {cards[2]['meaning_rev'] if cards[2].get('reversed') else cards[2]['meaning_up']}
4. OUTCOME: {cards[3]['name']} - {cards[3]['meaning_rev'] if cards[3].get('reversed') else cards[3]['meaning_up']}

Give detailed practical answer:
- For each card: specific action (1-2 sentences with card name in brackets)
- Final advice section: synthesis and concrete next steps (3-4 sentences)

Start:[/INST]
To address your question, here's what the cards reveal:

**What to Develop ({cards[0]['name']})**:"""
    return prompt


def create_advice_prompt(user_query, cards):
    prompt = f"""[INST]Question: {user_query}

Cards (use both, name each):
1. SITUATION: {cards[0]['name']} - {cards[0]['meaning_rev'] if cards[0].get('reversed') else cards[0]['meaning_up']}
2. GUIDANCE: {cards[1]['name']} - {cards[1]['meaning_rev'] if cards[1].get('reversed') else cards[1]['meaning_up']}

Give detailed practical answer:
- Current situation analysis with {cards[0]['name']} (2-3 sentences)
- Specific actions based on {cards[1]['name']} (2-3 concrete steps)
- Final recommendation (2 sentences)

Start:[/INST]
**Current Situation ({cards[0]['name']})**:"""
    return prompt


def create_linear_prompt(user_query, cards):
    prompt = f"""[INST]Question: {user_query}

Cards (use all 3, name each):
1. PAST: {cards[0]['name']} - {cards[0]['meaning_rev'] if cards[0].get('reversed') else cards[0]['meaning_up']}
2. PRESENT: {cards[1]['name']} - {cards[1]['meaning_rev'] if cards[1].get('reversed') else cards[1]['meaning_up']}
3. FUTURE: {cards[2]['name']} - {cards[2]['meaning_rev'] if cards[2].get('reversed') else cards[2]['meaning_up']}

Give detailed practical answer:
- What led here ({cards[0]['name']}): 2 sentences
- Current state ({cards[1]['name']}): what's happening now, 2 sentences  
- Where it leads ({cards[2]['name']}): likely outcome, 2 sentences
- Action plan: 3 concrete steps to improve the situation

Start:[/INST]
**Past Influences ({cards[0]['name']})**:"""
    return prompt
