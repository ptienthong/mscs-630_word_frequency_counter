import threading
from collections import Counter
import re

# Global counter and lock
word_counter = Counter()
lock = threading.Lock()

def count_words(text_segment):
    local_counter = Counter()
    words = re.findall(r'\b\w+\b', text_segment.lower())
    local_counter.update(words)
    print(f"Intermediate count for segment: {local_counter}")
    with lock:
        word_counter.update(local_counter)

def main():
    file_name = 'sample.txt'
    try:
        with open(file_name, 'r') as file:
            text = file.read()
            print("Contents of text file:\n")
            print(text)
            print('\n')
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
        return

    # Count words in the text
    num_threads = 4
    words = re.findall(r'\b\w+\b', text)
    total_words = len(words)
    chunk_size = (total_words + num_threads - 1) // num_threads

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = min(start + chunk_size, total_words)
        text_segment = ' '.join(words[start:end])
        thread = threading.Thread(target=count_words, args=(text_segment,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Display final word counts
    print("Combined Word counts:")
    for word, count in word_counter.items():
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()