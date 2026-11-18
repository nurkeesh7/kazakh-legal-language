from pathlib import Path
from search import load_search_system, search_documents

PROJECT_DIR = Path(__file__).resolve().parent.parent


def main():
    models, lemma_map = load_search_system(PROJECT_DIR)

    while True:
        print("\nKAZAKH LEGAL DOCUMENT SEARCH")
        print("1. Baseline TF-IDF")
        print("2. Lemma-based TF-IDF")
        print("3. Compare both models")
        print("4. Exit")

        choice = input("Choose option (1-4): ").strip()

        if choice == "4":
            print("Goodbye!")
            break

        if choice not in ("1", "2", "3"):
            print("Invalid option")
            continue

        query = input("Enter legal search query: ").strip()

        if not query:
            print("Query cannot be empty")
            continue

        try:
            value = input("Top K (1-20, default 5): ").strip()
            top_k = int(value) if value else 5

            if not 1 <= top_k <= 20:
                raise ValueError("Top K out of range")

            names = (
                ["Baseline", "Lemma-based"]
                if choice == "3"
                else ["Baseline" if choice == "1" else "Lemma-based"]
            )

            for name in names:
                result = search_documents(
                    query, models, lemma_map, name, top_k
                )

                print(f"\n{name} RESULTS")
                print(result.to_string(index=False)
                      if not result.empty else "No matches")

        except ValueError as exc:
            print("Input error:", exc)

        except (OSError, FileNotFoundError) as exc:
            print("File access error:", exc)


if __name__ == "__main__":
    main()
