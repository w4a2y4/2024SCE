class Chapter:
    def __init__(self, title, longsummary, shortsummary, fulltext, questions, current_question=0):
        self.title = title
        self.longsummary = longsummary
        self.shortsummary = shortsummary
        self.fulltext = fulltext
        self.questions = questions
        self.current_question = current_question
    
    def GetCurrentQuestion(self):
        if (self.current_question == self.questions.length):
            ret = "That is enough questions for today"
            self.current_question = 0
        else:
            ret = self.questions[self.current_question]
            self.current_question += 1
        return ret