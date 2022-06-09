"""
written on a snowy day
inputs:
- txt file of book
- txt file of word frequencies
- csv of verbs
"""

from collections import Counter 
import csv

def main():
    """haga la mierda"""
    book_file = '/home/jasper/Documents/cincomil/El-Tunel.txt'
    print (book_file.split('/')[-1][:-4])
    text = read_book(book_file)
    verbos = verbing('/home/jasper/Documents/cincomil/jehle_verb_database.csv')
    freq = get_freeky('/home/jasper/Documents/cincomil/5k_palabras.txt', verbos)
    counts, aires, entero = count_words_fast(text)
    unique, total = find_freq(counts, freq, aires)
    group(unique, total, entero)


def read_book(title_path):
    """convert txt file into string"""
    with open(title_path, "r", encoding ="utf8") as current_file:
        text = current_file.read()
        text = text.replace("\n", " ").replace("\r", " ").replace("—", " ")
    return text.lower()
    

def verbing(verbs_file):
    """obtain root for all possible verb endings"""
    # create a dict for possible pairings
    posi = {}
    
    # read the file
    with open(verbs_file, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
        
            # do the indicatives
            if row[1] == 'Indicativo':
                if row[2] in ('Presente'):
                    posi[row[0]] = agregar(row, (3, 4, 5, 6, 7, 8, 9, 10), posi)
                
                if row[2] in ('Futuro', 'Imperfecto', 'Pretérito', 'Condicional'):
                    posi[row[0]] = agregar(row, (3, 4, 5, 6, 7, 8), posi)
                    
            # do subjunctives
            if row[1] == 'Subjuntivo':
                if row[2] in ('Presente', 'Imperfecto', 'Futuro'):
                    posi[row[0]] = agregar(row, (3, 4, 5, 6, 7, 8), posi)
                
            # do commands
            if row[1] == 'Imperativo Afirmativo':
                posi[row[0]] = agregar(row, (4, 5, 7, 8), posi)
                
            if row[1] == 'Imperativo Negativo':
                already = posi.get(row[0], [])
                already.append(row[4].replace('no ', ''))
                posi[row[0]] = already
                
    return posi


def agregar(row, numeros, posibilidades):
    """add items to dict"""
    already = posibilidades.get(row[0], [])
    for num in numeros:
        already.append(row[num])
    return already
    
    
def get_freeky(master, verbs):
    """convert text file into frequency dict"""
    # dict of words with their frequency rank
    the_dict = {}
    
    # iterate through file
    with open(master) as the_list:
        for line in the_list:
            chunks = line.split(',')
            
            # add to dict
            if len(chunks) > 1:
                word = chunks[1]
                freq = int(chunks[0])
                the_dict[word] = freq
                
                # add entries for adjectives
                if word[-1] == 'o':
                    the_dict[word[:-1] + 'a'] = freq
                    the_dict[word[:-1] + 'os'] = freq
                    the_dict[word[:-1] + 'as'] = freq
                    
                # add entries for verb forms
                if verbs.get(word):
                    for forma in verbs.get(word):
                        the_dict[forma] = freq

    return the_dict


def count_words_fast(text):     
    """get a list of all the words in the text"""    
    # cleanse the text
    skips = [".", ", ", ":", ";", "'", '"',
             "-", "¡", "!", "¿", "?", ","
             "»", "«", "(", ")"]    
    for ch in skips: 
        text = text.replace(ch, " ") 
        
    # return a list of all unique words
    word_counts = dict(Counter(text.split(" ")) )
    return list(word_counts.keys()), word_counts, sum(list(word_counts.values()))
    
    
def find_freq(words, freq, counts):
    """obtain frequencies"""    
    # create a dict of {unique_word: [frequency, count]}
    freeky = {}
    for w in words:
        # cleanse endings
        if w[-2:] in ('me', 'te', 'se', 'os'):
            rank = category(freq.get(w[:-2], 6666))
            
        elif w[-3:] in ('los', 'las', 'nos'):
            rank = category(freq.get(w[:-3], 6666))
            
        else:
            rank = category(freq.get(w, 6666))
        
        # optional QA
        #if rank == 9:
        #   print (w)
        
        try:
            int(w)
        except:
            #if len(w) > 1:
            freeky[w] = [rank, counts.get(w)]
        
    # return a list of all the frequencies
    listed = list(freeky.values())
    return (listed, len(listed))
        

def category(num):
    """simplify rankings into groups"""    
    if num < 1000:
        return 1
    elif 2000 > num >= 1000:
        return 2
    elif 3000 > num >= 2000:
        return 3
    elif 4000 > num >= 3000:
        return 4
    elif 5000 > num >= 4000:
        return 5
    else:
        return 9


def group(unique, total, entero):
    """aggregate results for all words"""    
    acabar = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 9: 0}
    conjunto = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 9: 0}
    
    # add to running totals
    for r in unique:
        index = r[0]
        aires = r[1]
        acabar[index] = acabar.get(index) + 1
        conjunto[index] = conjunto.get(index) + aires
    
    # show final summary
    print ('unique words')
    for n in (1, 2, 3, 4, 5, 9):
        pct = round(100*acabar.get(n)/total)
        print (str(n) + ': ' + str(pct) + '%')
        
    print ('\ntotal words')
    for n in (1, 2, 3, 4, 5, 9):
        pct = round(100*conjunto.get(n)/entero)
        print (str(n) + ': ' + str(pct) + '%')
    
    print ()


main()

