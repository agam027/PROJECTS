from helpers import *

def main():
    fname = "testt.txt"
    top_N = 10

    ta = text_analyzer()
    ta.path = fname
    ta.word_frequencies(ta.tokenize(ta.read_file()))
    stats = ta.stats(top_N)
    ta.print_stats()
    
    return


if __name__ == "__main__":
    main()

