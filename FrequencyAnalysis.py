# Find pairs and count the number of times they appear
def findPairs(text):
    i = 0
    pairDict = {}

    # Remove German Umlaute
    if "\u00DF" in text:
       text =  text.replace("\u00DF", "S") # ß
    if "\u00C4" in text:
       text = text.replace("\u00C4", "A") # Ä
    if "\u00D6" in text:
       text = text.replace("\u00D6","O") # Ö
    if "\u00DC" in text:
        text = text.replace("\u00DC","U") # Ü

    # Go through each letter in text
    for i in range(0, len(text)-1):
        pair = []
        
        # Remove special characters
        if text[i].isalpha():
          pair.append(text[i])
          if text[i+1].isalpha():
            pair.append(text[i+1])
            pairStr = ''.join(pair)

            # Add new pair or increment existing pair
            if pairStr in pairDict:
              pairDict[pairStr] += 1
            else:
              pairDict[pairStr] = 1
        
        i += 1
    
    # Sort in descending order
    sortedPair = sorted(pairDict.items(), key=lambda x: x[1], reverse=True)
    i= 0
    for k in sortedPair:
        if i == 20:
            break
        print(k[0], k[1])
        i += 1
    
    return "Finished"

def main():
    with open('./English Text.txt', encoding="utf8") as file:
        english = file.read().replace('\n', '')

    print("English Text")
    findPairs(english.upper())

    print("")
    print("================")
    print("")

    with open('./German Text.txt', encoding="utf8") as file:
        german = file.read().replace('\n', '')
    
    print("German Text")
    findPairs(german.upper())

if __name__ == "__main__":
    main()