#coding: utf-8

import tensorflow as tf
import numpy as np
import subprocess

try:
    import jieba
except:
    subprocess.call(["pip3", "install", "jieba"])
    import jieba

def get_raw_data(filename):
    raw_data = ""
    for line in open(filename):
        raw_data += line
    return raw_data

def get_stop_words(filename):
    stop_words = []
    for line in open(filename):
        word = line.strip()
        stop_words.append(word)
    return stop_words

def get_raw_sentences(raw_data, stop_words):
    raw_data = raw_data.replace("\n", "")
    raw_sentences = raw_data.strip().split()
    sentences = []
    cnt = 0
    for sentence in raw_sentences:
        sentence = sentence.replace("，", " ")
        sentence = sentence.replace("。", " ")
        sentence = sentence.replace("、", " ")
        sentence = sentence.replace("「", " ")
        sentence = sentence.replace("」", " ")
        sentence = sentence.replace("！", " ")
        sentence = sentence.replace("？", " ")
        sentence = sentence.replace("：", " ")
        sentence = sentence.replace("…", " ")
        sentence = sentence.replace("～", " ")
        sentence = sentence.replace("＊", " ")
        sentences += sentence.split()
        cnt += 1
    return sentences

def get_sentences(sentences):
    splited_sentences = []
    cnt = 0
    for sentence in sentences:
        tokens = jieba.cut(sentence, cut_all=True)
        words = [token.strip() for token in tokens if token.strip()]
        splited_sentences.append(words)
    return splited_sentences

def get_word2int(sentences):
    word_set = set()
    word2int = {}
    int2word = {}
    for sentence in sentences:
        for token in sentence:
            word_set.add(token)
    for i, word in enumerate(word_set):
        word2int[word] = i
        int2word[i] = word
    return word2int, int2word

def get_data(sentences, window_size):
    data = []
    for sentence in sentences:
        for word_index, word in enumerate(sentence):
            for nb_word in sentence[max(word_index - window_size, 0): min(word_index + window_size, len(sentence))]:
                if nb_word != word:
                    data.append([word, nb_word])   
    return data

def to_one_hot(data_point_index, vocab_size):
    temp = np.zeros(vocab_size)
    temp[data_point_index] = 1
    return temp

if __name__ == "__main__":
    stop_file = "data/stop_words.txt"
    example_file = "data/zh_example.txt"
    fp = open("embeddings.txt", "w")

    stop_words = get_stop_words(stop_file)
    raw_data = get_raw_data(example_file)
    raw_sentences = get_raw_sentences(raw_data, stop_words)
    sentences = get_sentences(raw_sentences)

    # first 5000 sentences
    sentences = sentences[:5000]
    print ("sentences: ", len(sentences))
    word2int, int2word = get_word2int(sentences)
    data = get_data(sentences, 2)

    vocab_size = len(word2int)
    print ("vocab_size:", vocab_size)
    x_train = []
    y_train = []
    for data_word in data:
        x_train.append(to_one_hot(word2int[data_word[0]], vocab_size))
        y_train.append(to_one_hot(word2int[data_word[1]], vocab_size))
    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)

    print (x_train.shape, y_train.shape)
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(30, activation='relu'),
        tf.keras.layers.Dense(vocab_size, activation='softmax')])
  
    model.compile(optimizer='adam',
                loss=tf.keras.losses.categorical_crossentropy,
                metrics=['accuracy'])
     
    model.fit(x_train, y_train, epochs=50)
    layer =model.layers[0]
    weights = layer.get_weights()[0]

    for i, word in int2word.items():
        embedding = weights[i]
        fp.write("%s\t%s\n" % (word, ",".join(map(str, embedding))))
    fp.close()
