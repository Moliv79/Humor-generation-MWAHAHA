import ollama


MODEL = "qwen2.5:3b"


def generate_candidates(prompt, number=3):

    candidates = []

    for _ in range(number):

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.9
            }
        )
        joke = response["message"]["content"].strip()

        candidates.append(joke)

    return candidates


def select_best_joke(candidates, language):

    jokes = "\n\n".join(
        f"JOKE {i + 1}:\n{joke}"
        for i, joke in enumerate(candidates)
    )

    if language == "Hindi":

        evaluation_prompt = f"""
आप एक अनुभवी हिंदी कॉमेडी एडिटर हैं।

नीचे तीन संभावित चुटकुले हैं:

{jokes}

इनमें से सबसे अच्छा और सबसे मजेदार चुटकुला चुनें।

इन बातों को ध्यान में रखें:

- चुटकुले का अर्थ स्पष्ट हो।
- setup और punchline का संबंध हो।
- punchline unexpected और मजेदार हो।
- भाषा स्वाभाविक हो।
- चुटकुला random या meaningless न हो।
- चुटकुला वास्तव में funny होना चाहिए।

बहुत महत्वपूर्ण:

आपको केवल एक NUMBER लिखना है।

अगर पहला चुटकुला सबसे अच्छा है तो लिखें:
1

अगर दूसरा चुटकुला सबसे अच्छा है तो लिखें:
2

अगर तीसरा चुटकुला सबसे अच्छा है तो लिखें:
3

कोई दूसरा शब्द न लिखें।
"""

    else:

        evaluation_prompt = f"""
You are an experienced comedy editor.

Here are three candidate jokes:

{jokes}

Choose the funniest and most original joke.

Consider:

- Clear meaning
- Natural setup
- Strong punchline
- Surprise
- Originality
- Relevance
- Actual comedic value

Reject jokes that are random, confusing, meaningless, or forced.

IMPORTANT:

You must return ONLY ONE NUMBER.

Return:

1

if JOKE 1 is the funniest.

Return:

2

if JOKE 2 is the funniest.

Return:

3

if JOKE 3 is the funniest.

Do not write anything else.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        options={
            "temperature": 0.1
        }
    )

    result = response["message"]["content"].strip()

    # Find which joke was selected
    if "1" in result:
        return candidates[0]

    elif "2" in result:
        return candidates[1]

    elif "3" in result:
        return candidates[2]

    # Fallback
    return candidates[0]


def generate_best_joke(prompt, language):

    candidates = generate_candidates(prompt, 3)

    best_joke = select_best_joke(
        candidates,
        language
    )

    return best_joke