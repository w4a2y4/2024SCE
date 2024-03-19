from ch1 import *
from ch2 import *

# Phase1: Greetings
FIRST_GREETING = ("1st greeting", "Hi, I am Nick! I heard that you love reading and I am here to help you with that. Today we will start with a beautiful book called 'The Wonderful Wizard of OZ'")
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
DEFAULT_ANSWER = ("default", "Hmmmm.... I don't know. Let's ask Markus next time!")
CH1_FULL_TEXT = ("ch1 full text", ch1.fulltext)
CH2_FULL_TEXT = ("ch2 full text", ch2.fulltext)

# Phase3: Feed back & farewell
END_SESSION = ("end session", "Alright! That's all for today!")
FEEDBACK_PAGE = ("feedback page", "Next time should we read more or less pages?")
FEEDBACK_QUESTIONS = ("feedback questions", "Do you want me to ask more or less questions next time?")
FAREWELL = ("farewell", "It's been so fun reading together! See you next time, bye bye!")

# for GPT
SYS_PROMPT = f"You are a reading companion agent named Nick. You are here to read with a dimentia patient.\
     Today, you are reading the book 'The Wonderful Wizard of OZ' together. The patient may ask you about the \
     plot of the story. Please read the following content and anser accordingly: {ch1.fulltext} {ch2.fulltext}"