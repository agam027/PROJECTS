class text_analyzer:
    def __init__(self):
        self.path = ""
        self.count_lines = 0
        self.count_words = 0
        self.comm_words = 0
        self.res = 0


    def read_file(self):
        contents = []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    li = ""
                    for ch in line:
                        if ch.isalpha() or ch.isspace():
                            li += ch.lower()
                    contents.append(li)
        except(FileNotFoundError):
            print("Error Opening the file")
            return
        
        self.count_lines = len(contents)
        return contents

    def tokenize(self, text):
        # return list of cleaned, lowercase words
        words = []

        for line in text:
            word = ""
            for ch in line:
                if ch in [" ", "\n"]:
                    words.append(word.replace(" ", ""))
                    word = ""

                word += ch

        self.count_words = len(words)
        return words
    

    def word_frequencies(self, words):
        # return dict: word -> count
        from collections import Counter
        self.comm_words = Counter(w for w in words if w).most_common()

        return


    def stats(self, N = 1):
        self.res = {"lines": self.count_lines, "Words": self.count_words, "top_words": self.comm_words[:N]}
        
        return


    def print_stats(self):
        print(f"Lines: {self.count_lines}")    
        print(f"Words: {self.count_words}")
        print(f"Average Words Per Line: {round(self.count_words/self.count_lines, 2) if self.count_lines > 0 else 'N/A'}")
        print("|--------------|")
        print("Top 10 Words:", end= "\n\n")

        for word, count in self.res["top_words"]:
            label = word.capitalize()
            dash_count = max(1, 12 - len(label))  # 12 = padding width
            print(f"{label} " + "-" * dash_count + f" {count}")
    
    
    def __str__(self):
        return (
            f"TextAnalyzer("
            f"lines={len(self.lines)}, "
            f"words={len(self.words)}, "
            f"unique_words={len(self.freqs)})"
        )