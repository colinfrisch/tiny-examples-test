import math
import re
from math import floor


def chunk_to_sentences(text_list : list[str], chunk_size : int = 100, overlap : float = 0.1)-> list[str]:
    """
    Divide a list of texts into chunks of a given size with an overlap

    Args:
        text_list (list[str]): List of texts to chunk
        chunk_size (int): Size of each chunk
        overlap (float): Overlap between chunks
    
    Returns:
        list[str]: List of chunks
    """
    chunks = []
    split_pattern = r'(?<=[.?!])'

    for text in text_list :
        sentences = re.split(split_pattern,text)
        print(len(sentences))

        new_chunk = ""
        overlap_amnt = 0
        current_sentence = 0

        while len(new_chunk) < chunk_size :

            # Ne pas dépasser la liste
            if current_sentence == len(sentences)-1:
                chunks.append(new_chunk)
                break

            # Ajouter la phrase suivante au chunk
            new_chunk+=sentences[current_sentence]
            current_sentence += 1

            print(current_sentence)

            # Lorsque le chunk dépasse la limite de caractères, on passe au chunk suivant
            if len(new_chunk) >= chunk_size :
                chunks.append(new_chunk)
                new_chunk = ""

                if len(sentences[current_sentence]) < chunk_size :
                    overlap_amnt += len(sentences[current_sentence])
                    
                    while overlap_amnt < floor(overlap*chunk_size):
                        current_sentence -= 1
                        overlap_amnt += len(sentences[current_sentence])
                        
                        
                
                    overlap_amnt = 0
                else :
                    current_sentence +=1
    return chunks


def chunk_to_words(text_list : list[str], chunk_size_in_words : int = 10, overlap : float = 0.1) -> list[str]:
    
    word_overlap = math.floor(chunk_size_in_words*overlap) # nb of character
    resulting_chunks = []
    
    for text in text_list :
        words = text.split(' ')
        
        resulting_chunks.extend(
            [
                ' '.join(words[max(0, i-word_overlap):i+chunk_size_in_words]) 
                for i 
                in range(0, len(words), chunk_size_in_words)
            ]
        )


    return resulting_chunks



if __name__ == "__main__":
    
    text_list = [
        'Hey. Im Colin. I, Colin, am an engineer ! With a deep passion for building. And designing. Software systems are both efficient and scalable.',
        'I am training for an interview. I want to join a company. It is building a product that is going to change the world. But first, do I need to build a system. It will help me prepare for the interview ?'
    ]
    
    print(chunk_to_words(text_list=text_list))

