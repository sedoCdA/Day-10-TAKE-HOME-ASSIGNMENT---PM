# AI-Augmented Task — Text Analysis Function

---

## 1. Prompt Used

"Write a Python module with a function called analyze_text(text: str, **options)
that accepts any text and keyword arguments for options (count_words=True,
count_sentences=True, find_longest_word=True, sentiment_simple=True). Each
option enables a different analysis. Use *args and **kwargs, add type hints
and Google-style docstrings. Return a dict with all requested analyses."

---

## 2. AI-Generated Output
```python
def analyze_text(text: str, **options) -> dict:
    """Analyzes text based on provided options."""
    results = {}

    if options.get("count_words", True):
        results["word_count"] = len(text.split())

    if options.get("count_sentences", True):
        results["sentence_count"] = text.count('.') + text.count('!') + text.count('?')

    if options.get("find_longest_word", True):
        words = text.split()
        results["longest_word"] = max(words, key=len)

    if options.get("sentiment_simple", True):
        positive = ["good", "great", "excellent", "happy", "love"]
        negative = ["bad", "terrible", "hate", "sad", "awful"]
        words = text.lower().split()
        pos = sum(1 for w in words if w in positive)
        neg = sum(1 for w in words if w in negative)
        if pos > neg:
            results["sentiment"] = "positive"
        elif neg > pos:
            results["sentiment"] = "negative"
        else:
            results["sentiment"] = "neutral"

    return results
```

---

## 3. Critical Evaluation of AI Code

### Does it properly use **kwargs?
Partially. It uses `**options` and `.get()` correctly to check flags.
However the function does everything inside one block — no separation
of concerns. Each analysis should be its own function.

### Are type hints correct?
The return type `-> dict` is too vague. It should be `-> dict[str, any]`
and each sub-function should have its own specific return type hint.

### Does it handle edge cases?
No. The following all cause crashes:
- Empty string: `max(words, key=len)` raises `ValueError` on empty list
- Text with no sentences: returns 0 which may be misleading
- No options passed: all analyses run by default with no way to opt out
- Whitespace-only string: `split()` returns empty list, crashes on longest word

### Is the docstring useful?
No. "Analyzes text based on provided options." tells the reader nothing.
There is no Args section, no Returns section, no Example, and no mention
of what happens on edge cases.

### Does it follow Single Responsibility Principle?
No. One function is doing four completely different jobs. If any single
analysis fails, the whole function fails. Each analysis should be its
own function that can be tested and maintained independently.

---

## 4. Improved Version
```python
# text_analysis.py
# Day 10 PM - Improved text analysis module

import re


# -----------------------------------------
# Individual analysis functions
# -----------------------------------------

def count_words(text: str) -> int:
    """
    Counts the number of words in a string.

    Args:
        text: Input string to analyse.

    Returns:
        Integer word count. Returns 0 for empty or whitespace-only input.

    Example:
        >>> count_words("Hello world")
        2
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


def count_sentences(text: str) -> int:
    """
    Counts sentences by detecting terminal punctuation (. ! ?).

    Args:
        text: Input string to analyse.

    Returns:
        Integer sentence count. Returns 0 for empty input.

    Example:
        >>> count_sentences("Hello! How are you? I am fine.")
        3
    """
    if not text or not text.strip():
        return 0
    return len(re.findall(r'[.!?]', text))


def find_longest_word(text: str) -> str:
    """
    Finds the longest word in a string.

    Args:
        text: Input string to analyse.

    Returns:
        The longest word as a string.
        Returns empty string if text is empty.

    Example:
        >>> find_longest_word("I love programming")
        'programming'
    """
    if not text or not text.strip():
        return ""
    words = re.findall(r"[a-zA-Z']+", text)
    if not words:
        return ""
    return max(words, key=len)


def simple_sentiment(text: str) -> str:
    """
    Returns a basic sentiment label based on keyword matching.

    Args:
        text: Input string to analyse.

    Returns:
        One of 'positive', 'negative', or 'neutral'.
        Returns 'neutral' for empty input.

    Example:
        >>> simple_sentiment("This is a great day")
        'positive'
    """
    if not text or not text.strip():
        return "neutral"

    positive_words = {
        "good", "great", "excellent", "happy", "love",
        "wonderful", "amazing", "fantastic", "brilliant", "joy"
    }
    negative_words = {
        "bad", "terrible", "hate", "sad", "awful",
        "horrible", "dreadful", "poor", "disappointing", "angry"
    }

    words = re.findall(r"[a-zA-Z]+", text.lower())
    pos = sum(1 for w in words if w in positive_words)
    neg = sum(1 for w in words if w in negative_words)

    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


# -----------------------------------------
# Main orchestrator function
# -----------------------------------------

def analyze_text(text: str, **options) -> dict[str, any]:
    """
    Analyses text using the options provided as keyword arguments.

    Each option flag enables a specific analysis. If no options are
    passed, all analyses are run by default.

    Args:
        text: The input string to analyse.
        **options: Keyword flags to control which analyses to run.
            count_words (bool): Count total words. Defaults to True.
            count_sentences (bool): Count sentences. Defaults to True.
            find_longest_word (bool): Find longest word. Defaults to True.
            sentiment_simple (bool): Basic sentiment label. Defaults to True.

    Returns:
        A dict containing results for each enabled analysis.
        Returns {'error': 'Empty text provided.'} if text is empty.

    Example:
        >>> analyze_text("I love Python!", sentiment_simple=True,
        ...              count_words=True, count_sentences=False,
        ...              find_longest_word=False)
        {'word_count': 3, 'sentiment': 'positive'}
    """
    if not text or not text.strip():
        return {"error": "Empty text provided."}

    results = {}

    if options.get("count_words", True):
        results["word_count"] = count_words(text)

    if options.get("count_sentences", True):
        results["sentence_count"] = count_sentences(text)

    if options.get("find_longest_word", True):
        results["longest_word"] = find_longest_word(text)

    if options.get("sentiment_simple", True):
        results["sentiment"] = simple_sentiment(text)

    return results


# -----------------------------------------
# Tests
# -----------------------------------------
if __name__ == "__main__":

    sample = "I love Python! It is a great language. Programming is wonderful."

    print("Full analysis:")
    print(analyze_text(sample))

    print("\nWords and sentiment only:")
    print(analyze_text(sample, count_words=True, sentiment_simple=True,
                       count_sentences=False, find_longest_word=False))

    print("\nEdge case - empty string:")
    print(analyze_text(""))

    print("\nEdge case - whitespace only:")
    print(analyze_text("     "))

    print("\nEdge case - no punctuation:")
    print(analyze_text("hello world this has no punctuation"))
```

---

## 5. Improvements Summary

| Issue | AI Code | Improved Version |
|-------|---------|-----------------|
| Single Responsibility | One monolithic function | Five focused functions |
| Empty text crash | ValueError on max() | Guard clause returns error dict |
| Whitespace crash | split() on empty string | Explicit empty check in each function |
| Vague type hint | -> dict | -> dict[str, any] |
| Weak docstring | One line, no Args/Returns | Full Google-style with examples |
| Sentence detection | Counts raw characters | Uses re.findall for accuracy |
| Word detection | text.split() only | re.findall strips punctuation cleanly |
| Sentiment word list | 5 words each | 10 words each, stored as sets (O(1) lookup) |
```

---

### Step 3 — Commit Message
```
feat(day10-pm): Part D - AI text analysis evaluation and improved solution
