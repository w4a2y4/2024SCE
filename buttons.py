from ch1 import *
from ch2 import *

BUTTONS = [
    ("greetings", "Good morning I am Nick."),
    ("ch1 start", "Let's start from chapter 1 today"),
    ("ch1 summary", "Once upn a time in a far far away galaxy..."),
    ("ch1 question", "Who is Toto?"),
    ("bye","See you next time, bye bye!")
]

# Phase1: Greetings
FIRST_GREETING = ("1st greeting", "Hi, I am Nick! I heard that you love reading and I am here to help you with that. Today we will start with a beautiful book called 'The Wixard of OZ'")
SECOND_GREETING = ("ask for summary", "Good to see you again! I somewhat forget what we read last time. Can you help me out?")
__explain_before_summary = "Now I remember! Last time we read that"
CH1_SHORT_SUMMARY = ("ch1 short summary", f"{__explain_before_summary} {ch1.shortsummary}")
CH2_SHORT_SUMMARY = ("ch2 short summary", f"{__explain_before_summary} {ch2.shortsummary}")
CH1_LONG_SUMMARY = ("ch1 long summary", f"{__explain_before_summary} {ch1.longsummary}")
CH2_LONG_SUMMARY = ("ch2 long summary", f"{__explain_before_summary} {ch2.longsummary}")
__explain_before_read = "You can ask me any questions while you read. Also, when you don't feel like reading yourself, just flip the tablet and I will continue reading for you."
START_READ = ("start read", f"Let's start reading! {__explain_before_read}")
CONTINUE_READ = ("start read", f"Let's continue reading! {__explain_before_read}")

# Phase2: Reading

# Phase3: Feed back & farewell