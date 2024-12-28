import random

class PoemGenerationEnv:
    def __init__(self, df, num_verses, syllables_per_verse, rhyme_data):
        """
        Initialize the environment.

        Args:
            vocab: List of all possible words.
            syllable_data: Dictionary {word: syllable_count}.
            rhyme_data: Dictionary {word: rhyme_ending}.
            num_verses: Number of verses in the poem.
            syllables_per_verse: Number of syllables per verse.
        """
        df = df.sort_values(by=['syllables'], key= lambda col : col.str.len())
        df = df[df['joint_syllables'] != 'not-found']
        self.vocab = df['word'].tolist()
        self.syllable_data = self.compute_syllables()
        self.rhyme_data = {x: x[-rhyme_data:] for x in self.vocab}
        self.num_verses = num_verses
        self.syllables_per_verse = syllables_per_verse

        self.reset()

    def compute_syllables(self):
        d = {}
        for index, row in self.df.iterrows():
            word = row['word']
            syl = eval(row['syllables'])
            d[word] = len(syl)


    def reset(self):
        """
        Reset the environment to its initial state.
        """
        self.current_poem = []
        self.current_verse = []
        self.current_verse_syllables = 0
        self.verse_index = 0
        self.done = False
        return self.get_state()

    def get_state(self):
        """
        Return the current state.
        The state includes:
        - Current poem (as a list of verses)
        - Current verse (as a list of words)
        - Current syllable count for the verse
        """
        return {
            "poem": self.current_poem,
            "verse": self.current_verse,
            "syllables_left": self.syllables_per_verse - self.current_verse_syllables,
            "verse_index": self.verse_index
        }

    def step(self, action):
        """
        Perform an action in the environment.
        The action is the index of the word selected from the vocabulary.

        Args:
            action: Index of the word in the vocabulary.

        Returns:
            state: The new state after taking the action.
            reward: Reward for the action.
            done: Whether the poem is complete.
        """
        word = self.vocab[action]
        syllables = self.syllable_data[word]
        rhyme_ending = self.rhyme_data[word]

        # Update the current verse and syllable count
        self.current_verse.append(word)
        self.current_verse_syllables += syllables

        reward = 0

        # Check if the verse is complete
        if self.current_verse_syllables == self.syllables_per_verse:
            # Add the verse to the poem
            self.current_poem.append(" ".join(self.current_verse))

            # Check for rhyme pattern
            if len(self.current_poem) > 1:
                previous_rhyme = self.rhyme_data[self.current_poem[-2].split()[-1]]
                if rhyme_ending == previous_rhyme:
                    reward += 10  # Bonus for rhyming

            # Move to the next verse
            self.current_verse = []
            self.current_verse_syllables = 0
            self.verse_index += 1

            # Check if the poem is complete
            if self.verse_index == self.num_verses:
                self.done = True
                reward += 50  # Bonus for completing the poem

        elif self.current_verse_syllables > self.syllables_per_verse:
            # Penalty for exceeding syllable count
            reward -= 15
            self.done = True  # End the episode early
        else:
            # Small reward for valid progress
            reward += 1

        return self.get_state(), reward, self.done

    def sample_action(self):
        """
        Sample a random action (word index) from the vocabulary.
        """
        return random.randint(0, len(self.vocab) - 1)
