# spanish-word-frequency
Take a text file of a book (en español) and return a summary of how advanced the vocab is

Spanish has a lot of variations of core words. Only the core words were considered. For example:
- Adjectives. `buena`, `buenas`, and `buenos` all count as `bueno` which is frequency #115
- Verb conjugations. `tengo`, `tiene`, `tuviésemos`, etc. all count as `tener` when is frequency #18

Then, the words are categorized into groups of 1000 (the frequency list ends at 5000). A summary is created that can be used to see if the book's vocabulary would be too abstruse for your current level. The summary includes
- `unique words` :: for all the _unique_ words in the book, how many are within each group
- `total words` :: for all the words in the book (duplicates included), how many are within each group
