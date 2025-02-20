
import math


def norm(vec):
    sum_of_squares = 0.0  
    
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot_product = 0.0
    for i in vec1:
        if i in vec2:
            dot_product += vec1[i] * vec2[i]
    norm_product = norm(vec1) * norm(vec2)
    if norm_product == 0:
        return -1
    return dot_product / norm_product

    
    


def build_semantic_descriptors(sentences):
    semantic_descriptors = {}
    
    for sentence in sentences:
        unique_words_in_sen = set(sentence)
        for word in unique_words_in_sen:
            if word not in semantic_descriptors:
                semantic_descriptors[word] = {}
    
        for word in unique_words_in_sen:
            for unique_word in unique_words_in_sen:
                if unique_word != word:
                    if unique_word not in semantic_descriptors[word]:
                        semantic_descriptors[word][unique_word] = 1
                    else:
                        semantic_descriptors[word][unique_word] += 1
    
    return semantic_descriptors
                

import re

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as f:
            text = f.read().lower()

        text = re.sub(r'[.!?]+', '.', text)
        text = re.sub(r'[\-–—]', ' ', text)
        text = re.sub(r'[,"\'():;]', ' ', text)
        text = text.replace('\n', ' ')

        split_text = text.split('.')
        for sentence in split_text:
            words = sentence.strip().split()
            if words:
                sentences.append(words)
    return build_semantic_descriptors(sentences)




def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity = float('-inf')
    best_choice = choices[0]
    for choice in choices:
        if word in semantic_descriptors and choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
        else:
            similarity = -1
        if similarity > max_similarity or (similarity == max_similarity and choices.index(choice) < choices.index(best_choice)):
            max_similarity = similarity
            best_choice = choice
    return best_choice



def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    total = 0
    
    with open(filename, "r", encoding="latin1") as f:
        for line in f:
            if not line.strip():
                continue
                
            words = line.strip().split()
            if len(words) >= 2:
                word = words[0]
                real_answer = words[1]
                choices = words[1:]
                
                answer = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
                
                if answer == real_answer:
                    correct += 1
                total += 1
    if total == 0:
        return 0.0
    return float((correct / total) * 100)
                

if __name__ == '__main__':
    semantic_descriptors = build_semantic_descriptors_from_files(['novel1.txt', 'novel2.txt'])
    print(run_similarity_test('simtest.txt', semantic_descriptors, cosine_similarity))
