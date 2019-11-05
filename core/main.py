import os
import numpy as np
import jieba

def get_stop_words():
    stop_file = "data/stop_words.txt"
    stop_words = []
    for line in open(stop_file):
        word = line.strip()
        stop_words.append(word)
    return stop_words

stop_words = get_stop_words()

def parse_txt(filename):
    with open(filename, "rb") as fp:
        text = fp.read()
        data = str(text, encoding="utf-8") 
        keyword_count = {}
        keyword_score = {}
        seg_list = jieba.cut(data, cut_all=True)
        for keyword in seg_list:
            keyword = keyword.strip()
            if keyword and len(keyword) > 1 and keyword not in stop_words:
                keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        total = 0
        for k, v in keyword_count.items():
            total += v * v
        total = max(1, total)
        for k, v in keyword_count.items():
            keyword_score[k] = v * 1.0 / np.sqrt(total)
    return keyword_score
                
def similar_score(keyword2score_a, keyword2score_b):
    score = 0
    for keyword, s_a in keyword2score_a.items():
        if keyword in keyword2score_b:
            s_b = keyword2score_b[keyword]
            score += s_a * s_b
    return score

if __name__ == "__main__":
    root = "data/20191105"
    text_file_list = os.listdir("%s/clean" % root)[:5]
    text_file2keyword_score = {}
    for text_file in text_file_list:
        text_file_full_path = os.path.join(root, "clean", text_file)
        keyword_score = parse_txt(text_file_full_path)
        text_file2keyword_score[text_file] = keyword_score

    score_info = []
    for text_file_1 in text_file_list:
        for text_file_2 in text_file_list:
            if text_file_1 == text_file_2:
                continue
            keyword_score_1 = text_file2keyword_score[text_file_1]
            keyword_score_2 = text_file2keyword_score[text_file_2]
            score = similar_score(keyword_score_1, keyword_score_2)
            score_info.append([text_file_1, text_file_2, score])
    score_info.sort(key=lambda item: item[2], reverse=True)
    print (score_info[:5])


        
