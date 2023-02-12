"""
--------------------------------------------------------------------------------
"Morse-Code" - Morse encoding and decoding text
https://en.wikipedia.org/wiki/Morse_code
Copyright (c) FEB 2023 Oleksii Hurov
--------------------------------------------------------------------------------
"""


from enum import Enum, auto


# --- MorseCode ----------------------------------------------------------------

class MorseCode:

    class STRING_TYPE(Enum):
        """Types of strings as parameters for encoding/decoding."""
        TEXT = auto()
        MORSE_CODE = auto()
        MORSE_SIGNAL = auto()

    def __init__(
            self,
            # dot: str = '·',
            dot: str = '.',
            dash: str = '-',
            bit_gap: str = '',
            character_gap: str = ' ',
            word_gap: str = '   ',
            signal_on: str = '█',
            signal_off: str = '_',
            dot_timing: int = 1,
            dash_timing: int = 3,
            bit_timing: int = 1,
            character_timing: int = 3,
            word_timing: int = 7
    ):
        """
        Morse encoding and decoding strings.
        Also, signal-representation of the Morse code.

        (https://en.wikipedia.org/wiki/Morse_code)

        :param dot: dot-symbol for morse code input/output.
        :param dash: dash-symbol for morse code input/output.
        :param bit_gap:
            space -symbol or -string between dots and dashes within a character
            for morse code input/output.
        :param character_gap:
            space -symbol or -string between letters/characters
            for morse code input/output.
        :param word_gap:
            space -symbol or -string between words
            for morse code input/output.

        :param signal_on: symbol ON for morse signal input/output.
        :param signal_off: symbol OFF for morse signal input/output.
        :param dot_timing:
            duration in ticks for dot
            for morse signal input/output.
        :param dash_timing:
            duration in ticks for dash
            for morse signal input/output.
        :param bit_timing:
            duration in ticks between dots and dashes within a character
            for morse signal input/output.
        :param character_timing:
            duration in ticks between letters/characters
            for morse signal input/output.
        :param word_timing:
            duration in ticks between words
            for morse signal input/output.
        """

        # symbols and gaps for morse line string compiling
        self.dot = self._assertion_dot(dot)
        self.dash = self._assertion_dash(dash)
        self.bit_gap = self._assertion_bit_gap(bit_gap)
        self.character_gap = self._assertion_character_gap(character_gap)
        self.word_gap = self._assertion_word_gap(word_gap)
        self.morse_code_bits = {self.dot, self.dash}

        # symbols and timings for morse signal
        self.signal_on = self._assertion_signal_on(signal_on)
        self.signal_off = self._assertion_signal_off(signal_off)
        self.dot_timing = self._assertion_dot_timing(dot_timing)
        self.dash_timing = self._assertion_dash_timing(dash_timing)
        self.bit_timing = self._assertion_bit_timing(bit_timing)
        self.character_timing = self._assertion_character_timing(character_timing)
        self.word_timing = self._assertion_word_timing(word_timing)
        self.morse_signal_bits = {self.signal_on, self.signal_off}

        # code tables
        self._table_of_letters = {
            'A': '.-',
            'B': '-...',
            'C': '-.-.',
            'D': '-..',
            'E': '.',
            'F': '..-.',
            'G': '--.',
            'H': '....',
            'I': '..',
            'J': '.---',
            'K': '-.-',
            'L': '.-..',
            'M': '--',
            'N': '-.',
            'O': '---',
            'P': '.--.',
            'Q': '--.-',
            'R': '.-.',
            'S': '...',
            'T': '-',
            'U': '..-',
            'V': '...-',
            'W': '.--',
            'X': '-..-',
            'Y': '-.--',
            'Z': '--..'
        }
        self._table_of_numbers = {
            '1': '.----',
            '2': '..---',
            '3': '...--',
            '4': '....-',
            '5': '.....',
            '6': '-....',
            '7': '--...',
            '8': '---..',
            '9': '----.',
            '0': '-----'
        }
        self._table_of_punctuation = {
            '.': '.-.-.-',
            ',': '--..--',
            '?': '..--..',
            '`': '.----.',
            '!': '-.-.--',
            '/': '-..-.',
            '(': '-.--.',
            ')': '-.--.-',
            '&': '.-...',
            ':': '---...',
            ';': '-.-.-.',
            '=': '-...-',
            '+': '.-.-.',
            '-': '-....-',
            '_': '..--.-',
            '"': '.-..-.',
            '$': '...-..-',
            '@': '.--.-.'
        }
        self._table_of_non_latin = {
            'À': '.--.-',
            'Ä': '.-.-',
            'Å': '.--.-',
            'Ą': '.-.-',
            'Æ': '.-.-',
            'Ć': '-.-..',
            'Ĉ': '-.-..',
            'Ç': '-.-..',
            'CH': '----',
            'Đ': '..-..',
            'Ð': '..--.',
            'É': '..-..',
            'È': '.-..-',
            'Ę': '..-..',
            'Ĝ': '--.-.',
            'Ĥ': '----',
            'Ĵ': '.---.',
            'Ł': '.-..-',
            'Ń': '--.--',
            'Ñ': '--.--',
            'Ó': '---.',
            'Ö': '---.',
            'Ø': '---.',
            'Ś': '...-...',
            'Ŝ': '...-.',
            'Š': '----',
            'Þ': '.--..',
            'Ü': '..--',
            'Ŭ': '..--',
            'Ź': '--..-.',
            'Ż': '--..-'
        }
        self._table_of_prosigns = {
            '[End of work]': '...-.-',
            '[Error]': '........',
            '[General invitation to transmit]': '-.-',
            '[Starting signal]': '-.-.-',
            '[New message follows]': '.-.-.',
            '[Verified]': '...-.',
            '[Wait]': '.-...'
        }

        # constants and rules
        self.UNKNOWN_CHARACTER = '�'  # '\ufffd' - print instead of unrecognized morse code
        self.PARAGRAPHS_IN_MORSE_CODE = True
        self.INCLUDE_PUNCTUATION = True
        self.INCLUDE_NON_LATIN = True
        self.INCLUDE_PROSIGNS = True
        self.BEEP_FREQUENCY = 880  # in Hz
        self.BEEP_DURATION = 200  # tick in milliseconds

        # Morse code tables
        self.encoding = self._init_encoding()
        self.decoding = self._init_decoding()

    # --- Assertion methods ----------------------------------------------------

    @staticmethod
    def _assertion_dot(dot: str) -> str:
        """Assertion before assigning dot."""
        assert type(dot) == str, \
            "Provided dot-parameter expected to be a string"
        assert len(dot) == 1, \
            "Provided dot-parameter expected to be a single character"
        return dot

    def _assertion_dash(self, dash: str) -> str:
        """Assertion before assigning dash."""
        assert type(dash) == str, \
            "Provided dash-parameter expected to be a string"
        assert len(dash) == 1, \
            "Provided dash-parameter expected to be a single character"
        assert self.dot != dash, \
            "Provided dot- and dash-parameters expected to be different"
        return dash

    @staticmethod
    def _assertion_bit_gap(bit_gap: str) -> str:
        """Assertion before assigning bit_gap."""
        assert type(bit_gap) == str, \
            "Provided bit_gap-parameter expected to be a string"
        return bit_gap

    def _assertion_character_gap(self, character_gap: str) -> str:
        """Assertion before assigning character_gap."""
        assert type(character_gap) == str, \
            "Provided character_gap-parameter expected to be a string"
        assert character_gap not in self.bit_gap, \
            "Provided character_gap-parameter can not be part of bit_gap-string"
        return character_gap

    def _assertion_word_gap(self, word_gap: str) -> str:
        """Assertion before assigning word_gap."""
        assert type(word_gap) == str, \
            "Provided word_gap-parameter expected to be a string"
        assert word_gap not in self.bit_gap, \
            "Provided word_gap-parameter can not be part of bit_gap-string"
        assert word_gap not in self.character_gap, \
            "Provided word_gap-parameter can not be part of character_gap-string"
        return word_gap

    @staticmethod
    def _assertion_signal_on(signal_on: str) -> str:
        """Assertion before assigning signal_on."""
        assert type(signal_on) == str, \
            "Provided signal_on-parameter expected to be a string"
        assert len(signal_on) == 1, \
            "Provided signal_on-parameter expected to be a single character"
        return signal_on

    def _assertion_signal_off(self, signal_off: str) -> str:
        """Assertion before assigning signal_off."""
        assert type(signal_off) == str, \
            "Provided signal_off-parameter expected to be a string"
        assert len(signal_off) == 1, \
            "Provided signal_off-parameter expected to be a single character"
        assert self.signal_on != signal_off, \
            "Provided signal_on- and signal_off-parameters expected to be different"
        return signal_off

    @staticmethod
    def _assertion_dot_timing(dot_timing: int) -> int:
        """Assertion before assigning dot_timing."""
        assert type(dot_timing) == int, \
            "Provided dot_timing-parameter expected to be an integer number"
        assert dot_timing > 0, \
            "Provided dot_timing-parameter expected to be a positive number"
        return dot_timing

    def _assertion_dash_timing(self, dash_timing: int) -> int:
        """Assertion before assigning dash_timing."""
        assert type(dash_timing) == int, \
            "Provided dash_timing-parameter expected to be an integer number"
        assert dash_timing > self.dot_timing, \
            "Provided dash_timing-parameter expected to be longer than dot_timing"
        return dash_timing

    @staticmethod
    def _assertion_bit_timing(bit_timing: int) -> int:
        """Assertion before assigning bit_timing."""
        assert type(bit_timing) == int, \
            "Provided bit_timing-parameter expected to be an integer number"
        assert bit_timing > 0, \
            "Provided bit_timing-parameter expected to be a positive number"
        return bit_timing

    def _assertion_character_timing(self, character_timing: int) -> int:
        """Assertion before assigning character_timing."""
        assert type(character_timing) == int, \
            "Provided character_timing-parameter expected to be an integer number"
        assert character_timing > self.bit_timing, \
            "Provided character_timing-parameter expected to be longer than bit_timing"
        return character_timing

    def _assertion_word_timing(self, word_timing: int) -> int:
        """Assertion before assigning word_timing."""
        assert type(word_timing) == int, \
            "Provided word_timing-parameter expected to be an integer number"
        assert word_timing > self.character_timing, \
            "Provided word_timing-parameter expected to be longer than character_timing"
        return word_timing

    @staticmethod
    def _assertion_unknown_character(unknown_character: str) -> str:
        """Assertion before assigning unknown_character."""
        assert type(unknown_character) == str, \
            "Provided unknown_character-parameter expected to be a string"
        return unknown_character

    @staticmethod
    def _assertion_paragraphs_in_morse_code(paragraphs_in_morse_code: bool) -> bool:
        """Assertion before assigning paragraphs_in_morse_code."""
        assert type(paragraphs_in_morse_code) == bool, \
            "Provided paragraphs_in_morse_code-parameter expected to be boolean"
        return paragraphs_in_morse_code

    @staticmethod
    def _assertion_include_punctuation(include_punctuation: bool) -> bool:
        """Assertion before assigning include_punctuation."""
        assert type(include_punctuation) == bool, \
            "Provided include_punctuation-parameter expected to be boolean"
        return include_punctuation

    @staticmethod
    def _assertion_include_non_latin(include_non_latin: bool) -> bool:
        """Assertion before assigning include_non_latin."""
        assert type(include_non_latin) == bool, \
            "Provided include_non_latin-parameter expected to be boolean"
        return include_non_latin

    @staticmethod
    def _assertion_include_prosigns(include_prosigns: bool) -> bool:
        """Assertion before assigning include_prosigns."""
        assert type(include_prosigns) == bool, \
            "Provided include_prosigns-parameter expected to be boolean"
        return include_prosigns

    # --- Initialization methods -----------------------------------------------

    def _init_encoding(self) -> dict[str, str]:
        """Initialization morse encoding."""

        codes: dict[str, str] = dict(
            **(self._table_of_non_latin if self.INCLUDE_NON_LATIN else {}),
            **(self._table_of_punctuation if self.INCLUDE_PUNCTUATION else {}),
            **self._table_of_numbers,
            **self._table_of_letters
        )

        codes = self._replace_dots_and_dashes(codes)

        return codes

    def _init_decoding(self) -> dict[str, str]:
        """Initialization morse decoding."""

        inverted_codes: dict[str, str] = {v: k for k, v in self.encoding.items()}

        if self.INCLUDE_PROSIGNS:
            prosigns = self._replace_dots_and_dashes(self._table_of_prosigns)
            inverted_prosigns = {v: k for k, v in prosigns.items()}
            inverted_prosigns.update(inverted_codes)
            inverted_codes = inverted_prosigns

        return inverted_codes

    def _replace_dots_and_dashes(self, table: dict[str, str]) -> dict[str, str]:
        """Replacing predefined symbols in tables to actual dots and dashes."""

        codes = table.copy()

        if self.dot != '-':
            codes = {k: v.replace('.', self.dot) for k, v in codes.items()}
            codes = {k: v.replace('-', self.dash) for k, v in codes.items()}
        elif self.dash != '.':
            codes = {k: v.replace('-', self.dash) for k, v in codes.items()}
            codes = {k: v.replace('.', self.dot) for k, v in codes.items()}
        else:  # case when dots and dashes should be swapped
            codes = {k: v.replace('.', '*') for k, v in codes.items()}
            codes = {k: v.replace('-', self.dash) for k, v in codes.items()}
            codes = {k: v.replace('*', self.dot) for k, v in codes.items()}

        return codes

    # --- Getter and Setter methods --------------------------------------------

    def get_unknown_character(self) -> str:
        """
        Retrieves current printing symbol for unknown character
        during decoding process.
        """
        return self.UNKNOWN_CHARACTER

    def set_unknown_character(self, unknown_character: str):
        """
        Defines printing symbol for unknown character
        during decoding process.
        Returns assertion error feedback if provided parameter doesn't satisfy.
        """
        try:
            self.UNKNOWN_CHARACTER = \
                self._assertion_unknown_character(unknown_character)
        except AssertionError as feedback:
            return feedback

    def get_paragraphs_in_morse_code(self) -> bool:
        """
        Retrieves current state of PARAGRAPHS_IN_MORSE_CODE rule,
        which is used during encode and decode processes.
        """
        return self.PARAGRAPHS_IN_MORSE_CODE

    def set_paragraphs_in_morse_code(self, paragraphs_in_morse_code: bool):
        """
        Defines current state of PARAGRAPHS_IN_MORSE_CODE rule,
        which is used during encode and decode processes.
        Returns assertion error feedback if provided parameter doesn't satisfy.
        """
        try:
            self.PARAGRAPHS_IN_MORSE_CODE = \
                self._assertion_paragraphs_in_morse_code(paragraphs_in_morse_code)
        except AssertionError as feedback:
            return feedback

    def get_include_punctuation(self) -> bool:
        """
        Retrieves current state of INCLUDE_PUNCTUATION rule,
        which is used in building encoding and decoding tables.
        """
        return self.INCLUDE_PUNCTUATION

    def set_include_punctuation(self, include_punctuation: bool):
        """
        Defines current state of INCLUDE_PUNCTUATION rule,
        which is used in building encoding and decoding tables.
        Returns assertion error feedback if provided parameter doesn't satisfy.
        """
        try:
            self.INCLUDE_PUNCTUATION = \
                self._assertion_include_punctuation(include_punctuation)
            self.encoding = self._init_encoding()
            self.decoding = self._init_decoding()
        except AssertionError as feedback:
            return feedback

    def get_include_non_latin(self) -> bool:
        """
        Retrieves current state of INCLUDE_NON_LATIN rule,
        which is used in building encoding and decoding tables.
        """
        return self.INCLUDE_NON_LATIN

    def set_include_non_latin(self, include_non_latin: bool):
        """
        Defines current state of INCLUDE_NON_LATIN rule,
        which is used in building encoding and decoding tables.
        Returns assertion error feedback if provided parameter doesn't satisfy.
        """
        try:
            self.INCLUDE_NON_LATIN = \
                self._assertion_include_non_latin(include_non_latin)
            self.encoding = self._init_encoding()
            self.decoding = self._init_decoding()
        except AssertionError as feedback:
            return feedback

    def get_include_prosigns(self) -> bool:
        """
        Retrieves current state of INCLUDE_PROSIGNS rule,
        which is used in building decoding table.
        """
        return self.INCLUDE_PROSIGNS

    def set_include_prosigns(self, include_prosigns: bool):
        """
        Defines current state of INCLUDE_PROSIGNS rule,
        which is used in building decoding table.
        Returns assertion error feedback if provided parameter doesn't satisfy.
        """
        try:
            self.INCLUDE_PROSIGNS = \
                self._assertion_include_prosigns(include_prosigns)
            self.decoding = self._init_decoding()
        except AssertionError as feedback:
            return feedback

    # --- Information methods --------------------------------------------------

    def get_encoding_table(self):
        """
        Retrieves dictionary of current morse encoding table
        in format {from: to}
        """
        return self.encoding

    def get_decoding_table(self):
        """
        Retrieves dictionary of current morse decoding table
        in format {from: to}
        """
        return self.decoding

    def identify_string_type(self, string: str) -> STRING_TYPE:
        """
        Identifies type of provided string, which may be one of three cases:
            - human-readable text
            - morse code (dots and dashes)
            - morse signal (ON/OFF signals)
        """

        string_bits = set(''.join(string.split()))
        if string_bits == self.morse_code_bits:
            return MorseCode.STRING_TYPE.MORSE_CODE
        if string_bits == self.morse_signal_bits:
            return MorseCode.STRING_TYPE.MORSE_SIGNAL
        return MorseCode.STRING_TYPE.TEXT

    # --- Operational methods --------------------------------------------------

    def encode(self, string: str) -> str:
        """
        Returns Morse code as dots and dashes
        from provided string.

        :param string: may be provided as human-readable text,
                       or as morse-signal string.
        """

        # Step 1: leading string to a text type string to work with
        string_type = self.identify_string_type(string)
        if string_type == MorseCode.STRING_TYPE.MORSE_SIGNAL:
            return self.from_signal(string)
        elif string_type == MorseCode.STRING_TYPE.MORSE_CODE:
            return string
        # else:  # string_type == MorseCode.STRING_TYPE.TEXT
        #     pass

        # Step 2: building line of morse-code
        line = []

        for paragraph in string.strip().splitlines():
            words = [word for word in paragraph.upper().split() if word]
            for word in words:
                for character in word:
                    if character in self.encoding.keys():
                        if self.bit_gap:
                            for ch in self.encoding[character]:
                                line.append(ch)
                                line.append(self.bit_gap)
                            if line:
                                line.pop()
                        else:
                            line.append(self.encoding[character])
                        line.append(self.character_gap)
                if line:
                    line.pop()
                line.append(self.word_gap)
            if line:
                line.pop()
            if self.PARAGRAPHS_IN_MORSE_CODE:
                line.append('\n')
            else:
                line.append(self.word_gap)
        if line:
            line.pop()

        # Step 3: compiling morse-code string from built line and return
        line = ''.join(line)
        return line

    def signal(self, string: str) -> str:
        """
        Provides Morse signal as ON/OFF timing-representation
        from provided string.

        :param string: may be provided as human-readable text
                       or as morse-code string.
        """

        # Step 1: leading string to a morse-code type string to work with
        string_type = self.identify_string_type(string)
        if string_type == MorseCode.STRING_TYPE.TEXT:
            string = self.encode(string)
        elif string_type == MorseCode.STRING_TYPE.MORSE_SIGNAL:
            return string
        # else:  # string_type == MorseCode.STRING_TYPE.MORSE_CODE
        #     pass

        # eliminating paragraphs before compiling signal
        string = string.replace('\n', self.word_gap)

        # Step 2: building line of signals
        line = []

        words = [word for word in string.split(self.word_gap) if word]
        for word in words:
            characters = [char for char in word.split(self.character_gap) if char]
            for character in characters:
                if self.bit_gap:
                    character = character.replace(self.bit_gap, '')
                for ch in character:
                    if ch == self.dot:
                        line.append(self.signal_on * self.dot_timing)
                    else:  # ch == self.dash
                        line.append(self.signal_on * self.dash_timing)
                    line.append(self.signal_off * self.bit_timing)
                if line:
                    line.pop()
                line.append(self.signal_off * self.character_timing)
            if line:
                line.pop()
            line.append(self.signal_off * self.word_timing)
        if line:
            line.pop()

        # Step 3: compiling morse-signal string from built line and return
        line = ''.join(line)
        return line

    def from_signal(self, string: str) -> str:
        """
        Returns Morse code as dots and dashes
        from provided Morse signal string.

        :param string: ON/OFF timing-representation signal string.
        """

        # Step 1: assertion input-string of morse-signal type
        string_type = self.identify_string_type(string)
        assert string_type == MorseCode.STRING_TYPE.MORSE_SIGNAL, \
            "Provided morse_signal-parameter expected to be only a signal string-type"

        # Step 2: building line of morse-code
        line = []
        word_space = self.signal_off * self.word_timing
        char_space = self.signal_off * self.character_timing
        bit_space = self.signal_off * self.bit_timing
        dot = self.signal_on * self.dot_timing
        # dash = self.signal_on * self.dash_timing

        words = [word for word in string.split(word_space) if word]
        for word in words:
            characters = [char for char in word.split(char_space) if char]
            for character in characters:
                bits = [bit for bit in character.split(bit_space) if bit]
                for bit in bits:
                    if bit == dot:
                        line.append(self.dot)
                    else:  # bit == dash
                        line.append(self.dash)
                    line.append(self.bit_gap)
                if line:
                    line.pop()
                line.append(self.character_gap)
            if line:
                line.pop()
            line.append(self.word_gap)
        if line:
            line.pop()

        # Step 3: compiling morse-code string from built line and return
        line = ''.join(line)
        return line

    def decode(self, string: str) -> str:
        """
        Returns human-readable text from provided string.

        :param string: may be provided as morse-code,
                       or as morse-signal string.
        """

        # Step 1: leading string to a morse-code type string to work with
        string_type = self.identify_string_type(string)
        if string_type == MorseCode.STRING_TYPE.MORSE_SIGNAL:
            string = self.from_signal(string)
        elif string_type == MorseCode.STRING_TYPE.TEXT:
            return string
        # else:  # string_type == MorseCode.STRING_TYPE.MORSE_CODE
        #     pass

        # Step 2: building line of text
        line = []

        for paragraph in string.strip().splitlines():
            words = [word for word in paragraph.split(self.word_gap) if word]
            for word in words:
                characters = [char for char in word.split(self.character_gap) if char]
                for character in characters:
                    if self.bit_gap:
                        character = character.replace(self.bit_gap, '')
                    line.append(self.decoding.get(character, self.UNKNOWN_CHARACTER))
                line.append(' ')
            if line:
                line.pop()
            line.append('\n')
        if line:
            line.pop()

        # Step 3: compiling text string from built line and return
        line = ''.join(line)
        line = line.capitalize()
        return line

    def convert_to_list(self, string: str) -> list[list[str]]:
        """
        Converts provided string to Morse code as dots and dashes,
        presented as list of words, subdivided by list of encoded characters.

        :param string: may be provided as human-readable text,
                       or as morse-code string,
                       or as morse-signal string.
        """

        # getting morse-code
        string = self.encode(string)

        # eliminating paragraphs before compiling signal
        string = string.replace('\n', self.word_gap)

        # building list of lists of encoded characters
        line = []

        words = [word for word in string.split(self.word_gap) if word]
        for word in words:
            characters = [char for char in word.split(self.character_gap) if char]
            line.append(characters)

        return line

    # TODO WIP. Current implementation with builtin winsound library works bad
    def beep(self, string: str):
        """Play Morse signal to the PC speaker."""

        # getting morse-code
        string = self.signal(string)

        # eliminating paragraphs before compiling signal
        string = string.replace('\n', self.word_gap)

        from winsound import Beep as beep
        from time import sleep

        word_space = self.signal_off * self.word_timing
        char_space = self.signal_off * self.character_timing
        bit_space = self.signal_off * self.bit_timing
        dot = self.signal_on * self.dot_timing
        # dash = self.signal_on * self.dash_timing

        frequency = self.BEEP_FREQUENCY
        dot_duration = self.BEEP_DURATION * self.dot_timing
        dash_duration = self.BEEP_DURATION * self.dash_timing
        bit_duration = self.BEEP_DURATION * self.bit_timing * 0.001
        char_duration = self.BEEP_DURATION * self.character_timing * 0.001
        word_duration = self.BEEP_DURATION * self.word_timing * 0.001

        # going through the signal beeping and sleeping
        words = [word for word in string.split(word_space) if word]
        for index_word, word in enumerate(words, start=1):
            characters = [char for char in word.split(char_space) if char]
            for index_char, character in enumerate(characters, start=1):
                bits = [bit for bit in character.split(bit_space) if bit]
                for index_bit, bit in enumerate(bits, start=1):
                    if bit == dot:
                        beep(frequency, dot_duration)
                    else:  # bit == dash
                        beep(frequency, dash_duration)
                    if index_bit != len(bits):
                        sleep(bit_duration)
                if index_char != len(characters):
                    sleep(char_duration)
            if index_word != len(words):
                sleep(word_duration)
