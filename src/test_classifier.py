from google import genai
from src.agents.intent_classifier_agent import IntentClassifierAgent

clf = IntentClassifierAgent()
res = clf.classify("I am new to finance explain stocks")
print("\nRAW MODEL OUTPUT:\n", res)
