#coding: utf-8
import numpy as np

def get_distance(v1, v2):
    return 1 - np.dot(v1, v2) / np.sqrt(np.dot(v1, v1) * np.dot(v2, v2))

if __name__ == "__main__":
    filename = "embeddings.txt"
    word2embedding = {}
    for line in open(filename):
        word, raw_embedding = line.strip().split()
        embedding = [float(num) for num in raw_embedding.split(",")]
        word2embedding[word] = embedding
    min_distance = 1
    min_word = ""
    fix_word = "裸体"
    fix_embedding = word2embedding[fix_word]
    for word in word2embedding:
        if word == fix_word:
            continue
        embedding = word2embedding[word]
        distance = get_distance(fix_embedding, embedding)
        if distance < min_distance:
            min_distance = distance
            min_word = word
    print (min_word, min_distance)
