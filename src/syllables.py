class SyllableRules:
    def __init__(self):
        self.vowels="aeiouăîâ"
        self.example_words = self.readFromFile("data/example_words.txt")

    def readFromFile(self, filename):
        with open(filename, 'r') as file:
            return file.readlines()

    def RegulaHiatului(self, word):
        """
        Regula hiatului - doua vocale succesive se despart in silabe diferite
        """
        syllables = []
        st = 0
        for dr in range(len(word)-1):
            if word[dr] in self.vowels and word[dr+1] in self.vowels:
                print(dr, word[dr], word[dr+1])
                syllables.append(word[st:dr+1])
                st = min(dr + 1, len(word)-1)
        syllables.append(word[st:])
        return syllables

def splitToSyllables(word):
    """
    Splits a word into syllables.
    """

    return [word]

sr = SyllableRules()
for i in sr.example_words:
    print(i)
    print(sr.RegulaHiatului(i))