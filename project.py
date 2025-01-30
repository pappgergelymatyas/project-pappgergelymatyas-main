"""A "Counter" a szavak megszámlálásához kell."""
from collections import Counter
"""A szavak szótővé való redukálásához kell az nltk (natural language toolkit) library."""
import nltk
from nltk.stem import WordNetLemmatizer

def read_file(file_path):
    ''' 
    Megnyitjuk a fájlt olvasási módben (ez az 'r'), és megadjuk neki, hogy UTF-8 formátum kell. 
    Erre azért van szükség, mert ez a formátum tartalmazza az angol abc összes betűjét.
    A "with" pedig egy kontextuskezelő, amivel a fájl automatikusan bezáródik miután a művelet véget ért.
    '''
    with open(file_path, "r", encoding="utf-8") as file:
        '''A fájl teljes tartalmát beolvassuk egyetlen text nevű változóba, mint egy hosszú stringet.'''
        text = file.read()
        '''
        A "split" a szöveget szóközök mentén bontja szavakra, majd egy listát ad vissza.
        Itt minden elem egy-egy szó a szövegből, és vesszőkkel vannak elválasztva.
        '''
    words = text.split()
    '''Eltávolítjuk a szavak végén lévő esetleges írásjeleket, és kisbetűssé alakítjuk az összes szót.'''
    words = [word.strip('.,!?;:"()').lower() for word in words]
    '''A függvény visszaadja az összes szót egy listában, amely most már csak tisztított, kisbetűs szavakat tartalmaz.'''
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    """
    A lemitizer szótőre vágja szét a szavakat, és azokat hasonlítja össze.
    Csak értelmes szavakat ad vissza a halmazba - ezért kicsit lassab."""

    return words


def read_stopwords(file_path):
    """Beolvassuk a stopwordok listáját a fájlból, majd ez a szavak halmazaként lesz visszaadva."""
    with open(file_path, "r", encoding="utf-8") as file:
        stopwords = file.read().splitlines()
    return set(word.strip().lower() for word in stopwords)

def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords]

def compare_texts(bible_path, user_text_path, stopword_path):
    '''Stopwords lista (gyakori szavak, amelyeket figyelmen kívül hagyunk).'''
    stopwords = stopwords = read_stopwords(stopword_path)
    
    '''A szavakat beolvassuk a két fájlból.'''
    bible_words = read_file(bible_path)
    user_words = read_file(user_text_path)

    '''Stopword szavakat eltávolítjuk.'''
    bible_words = remove_stopwords(bible_words, stopwords)
    user_words = remove_stopwords(user_words, stopwords)

    '''Az egyes szavak előfordulását megszámoljuk mindkét szövegben.'''
    bible_word_count = Counter(bible_words)
    user_word_count = Counter(user_words)

    '''
    Közös szavak és azok számlálása
    Létrehounk egy üres listát, amelybe a közös szavakat gyűjtjük.
    '''
    common_words = []
    '''Végigmegyünk a bible_word_count.keys() szavain.'''
    for word in bible_word_count.keys():
        '''Ellenőrizzük, hogy a szó benne van-e a user_word_count.keys()-ben, és ha igen, hozzáadjuk a szót a common_words listához.'''
        if word in user_word_count.keys():
            common_words.append(word)

    '''
    Az összes közös szavak számát úgy számoljuk ki, hogy először létrehozunk total_common_words egy változót, 
    amely a közös szavak összesített számát tárolja. Kezdetben ez nulla lesz.
    '''
    total_common_words = 0
    """A "for word in common_words" végigmegy a common_words listán, amely a két szöveg közös szavait tartalmazza."""
    for word in common_words:
        """
        Ha a szó mindkét szótárban (bible_word_count és user_word_count) szerepel, meghatározzuk a szó min. előfordulási számát a két szövegben.
        Majd hozzáadjuk ezt a számot a total_common_words változóhoz.
        """
        if word in bible_word_count and word in user_word_count:
            total_common_words += min(bible_word_count[word], user_word_count[word])

    """
    A szövegek közötti hasonlóság százalékos aránya: A százalékos hasonlóság számítása a következőképpen történik:
    1. Kiszámítjuk a közös szavak számát, vagyis ez az érték az összes olyan szót tartalmazza, ami közös a két szövegben.
    2. Kiszámítjuk a felhasználói szöveg összes szavának számát, azonban a stopwords szavakat kiszedjük.
    3. Százalékos arányt pedig úgy számítjuk ki, hogy a közös szavak számát elosztjuk a felhasználói szöveg összes szavának számával, majd megszorozzuk 100-zal.
    """
    total_words_user = len(user_words)
    similarity_percentage = (
        (total_common_words / total_words_user * 100) if total_words_user > 0 else 0
    )

    """A 10 leggyakoribb közös szó meghatározása a felhasználói szövegben"""
    top_common_words = Counter(
        {word: user_word_count[word] for word in common_words}
    ).most_common(10)

    """Eredmények kiírása"""
    print(f"Közös szavak száma: {total_common_words}")
    print(f"A szövegek közötti hasonlóság: {similarity_percentage}%")
    print("A 10 leggyakoribb közös szó a két szövegben:")
    for word, count in top_common_words:
        print(f"{word}: {count}")

if __name__ == "__main__":
    '''Fájl elérési utak megadása''' 
    base_path = "C:\\Users\\Lenovo X390\\Desktop\\Rajk\\II\\II. Prog1\\project-pappgergelymatyas-main\\project-pappgergelymatyas-main\\"
    default_bible_file = base_path + "bible.txt"
    default_user_file = base_path + "user_file.txt"
    default_stopword_file = base_path + "stopwords_file.txt"
    
    use_default = input("Használod az alapértelmezett fájlútvonalakat? (igen/nem): ").strip().lower()
    
    if use_default == "igen":
        bible_file = default_bible_file
        user_file = default_user_file
        stopword_file = default_stopword_file
    else:
        bible_file = input("Add meg a Biblia fájl elérési útját: ").strip()
        user_file = input("Add meg a felhasználói fájl elérési útját: ").strip()
        stopword_file = input("Add meg a stopword fájl elérési útját: ").strip()
    
    compare_texts(bible_file, user_file, stopword_file)
