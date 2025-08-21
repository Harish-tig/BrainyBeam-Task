import re
import wikipedia

#steps
#input by word
#suggest word
#user picks a word
#feeds to wikidpedia
#create summary
#write to txt
#save to cwd

def input_result():
    try:
        user_input = input("Enter a search word: ")
        results = wikipedia.search(user_input, results=3)

        if not results:
            print("No results found.")
            return -1
        else:
            return results

    except Exception:
        return -1


def get_search_word(options: list):
        try:
            results = options
            print("0 to exit.")
            for i, title in enumerate(results, start=1):
                print(f"{i} for {title}")
            print("4 for re search")
            while True:
                try:
                    result_num = int(input("Enter number (0-4): "))
                    if result_num == 4:
                        return -2 #signal to re-search
                    elif result_num == 0:
                        print("Closing Program")
                        return -1
                    elif 1 <= result_num <= 3:
                        return results[result_num - 1]
                    else:
                        print("Invalid option. Please enter a number between 0 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            return -1


def get_summary(search_word):
    try:
        print(f"\nYou selected: {search_word}")
        page = wikipedia.page(search_word,auto_suggest=False)
        return page.summary
    except wikipedia.exceptions.DisambiguationError as e:
        option = e.options
        print("0 to exit.")
        num_options = min(3, len(option))
        for i, title in enumerate(option[:num_options], start=1):
            print(f"{i} for {title}")
        while True:
            try:
                result_num = int(input("Enter number (0-3): "))
                if result_num == 0:
                    print("Closing Program")
                    return -1
                elif 1 <= result_num <= 3:
                    print(f"\nYou selected: {option[result_num-1]}")
                    page = wikipedia.page(option[result_num-1], auto_suggest=False)
                    return page.summary
            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(e)
                return -1

def write_summary_to_txt(summary: str, filename: str):
    try:
        with open(f"{filename}.txt", "w", encoding="utf-8") as file:
            file.write(summary + "\n\n")
    except Exception as e:
        print(e)

def clean_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)
def main():
    while True:
        try:
            result = input_result()
            if result == -1:
                print("No result for this search query. exiting")
                exit(-1)
            search_word = get_search_word(result)
            if search_word == -2:
                continue
            elif search_word != -1:
                print(f"getting explanation for the following search_word -> {search_word}")
                content = get_summary(search_word = search_word)
                write_summary_to_txt(summary=content,filename=clean_filename(search_word))
                print("file saved to current working directory")
                exit(0)
        except Exception as e:
            print(e)
            exit(-1)

if __name__ == '__main__':
    main()