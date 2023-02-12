"""
--------------------------------------------------------------------------------
"Morse-Code" - Morse encoding and decoding text
https://en.wikipedia.org/wiki/Morse_code
Copyright (c) FEB 2023 Oleksii Hurov
--------------------------------------------------------------------------------
"""


from morse_code import MorseCode


def example():

    morse = MorseCode()

    text = """
        Morse code is named after Samuel Morse,
        one of the inventors of the telegraph.
    """

    print("\nTEXT:")
    print(text)
    print("\nENCODE:")
    print(code := morse.encode(text))
    print("\nSIGNAL:")
    print(signal := morse.signal(code))
    print("\nFROM SIGNAL:")
    print(morse.from_signal(signal))
    print("\nDECODE:")
    print(morse.decode(code))
    print("\nCONVERT TO LIST:")
    print(morse.convert_to_list(text))
    print()


if __name__ == "__main__":
    example()
