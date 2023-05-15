# Values retrieved from https://en.wikipedia.org/wiki/Letter_frequency
# I took the "texts" values which are all percents
# I just made up numbers for the numbers and the space
alpha_frequency = {
    "a": .082, "b": .015, "c": .028, "d": .043, "e": .130, "f": .022, "g": .020, "h": .061,
    "i": .070, "j": .002, "k": .008, "l": .040, "m": .024, "n": .067, "o": .075, "p": .019,
    "q": .001, "r": .060, "s": .063, "t": .091, "u": .028, "v": .010, "w": .024, "x": .002,
    "y": .020, "z": .001, "0": .001, "1": .001, "2": .001, "3": .001, "4": .001, "5": .001,
    "6": .001, "7": .001, "8": .001, "9": .001, " ": .010
}


class Frequencer:
    def __init__(self):
        self.counts = {
            "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0,
            "i": 0, "j": 0, "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0,
            "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0,
            "y": 0, "z": 0, "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
            "6": 0, "7": 0, "8": 0, "9": 0, " ": 0
        }
        self.parsed = 0

    def parse_text(self, ciphertext):
        for char in ciphertext:
            self.counts[char] += 1
            self.parsed += 1

    def attack(self, ciphertext):
        self.percents = {
            "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0,
            "i": 0, "j": 0, "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0,
            "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0,
            "y": 0, "z": 0, "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
            "6": 0, "7": 0, "8": 0, "9": 0, " ": 0
        }

        for c in self.percents.keys():
            self.percents[c] = self.counts[c] / self.parsed

        self.trial = {
            "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0,
            "i": 0, "j": 0, "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0,
            "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0,
            "y": 0, "z": 0, "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
            "6": 0, "7": 0, "8": 0, "9": 0, " ": 0
        }

        # Initialize self.trial with the mapping of cipher characters to plain text approximate frequencies
        self.trial = {}

        # Create a copy of alpha_frequency and sort it based on frequency in descending order
        sorted_alpha_frequency = dict(sorted(alpha_frequency.items(), key=lambda x: x[1], reverse=True))
        sorted_attack_frequency = dict(sorted(self.percents.items(), key=lambda x: x[1], reverse=True))
        sorted_alpha_chars = list(sorted_alpha_frequency.keys())
        sorted_attack_chars = list(sorted_attack_frequency.keys())
        print("Sorted: " + str(sorted_alpha_chars))

        # Initialize self.trial with the mapping of cipher characters to plain text approximate frequencies
        for i in range(len(sorted_alpha_chars)):
            self.trial.update({sorted_attack_chars[i]: sorted_alpha_chars[i]})

        print(self.trial)

        trial_text = ""

        for c in ciphertext:
            trial_text += str(self.trial[c])

        return trial_text

freq = Frequencer()
freq.parse_text("EZ9YLPNLFDAABEL9AILMNL7Z1FL17V96LMPLD423FL17V96LMQLYZ1Z9YL749LMLEBK".lower())
print(freq.attack("EZ9YLPNLFDAABEL9AILMNL7Z1FL17V96LMPLD423FL17V96LMQLYZ1Z9YL749LMLEBK".lower()))
print(freq.trial)
