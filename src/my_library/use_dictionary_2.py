from janome.tokenizer import Tokenizer

def load(path):
    dic = {}
    t = Tokenizer()
    with open(path, "r", encoding = "utf-8") as f:
        lines = f.read()
        for l in lines.split("\n"):
            word = l.split("\t")
            if len(word) < 2:
                continue
            #data.txtと同じ前処理を辞書に実行することにより表現の微妙な違いによる見逃しを極力減らす
            word[1] = word[1].replace(" ", "")
            word[1] = [token.base_form for token in t.tokenize(word[1])]
            value = -1 if word[0].split("（")[0] == "ネガ" else 1
            i = 0
            key = word[1][i]
            #keyが重複したら後ろの単語を足していく、前の方からkeyが全て入っている（※「耳　が　痛い」というkeyがあれば「耳」、「耳　が」というkeyも存在している）
            while key in dic and i + 1 < len(word[1]):
                i += 1
                key = key + word[1][i]
            dic[key] = value
    return dic

def count(dic, sentence):
    result = []
    for i in range(len(sentence)):
        phrase = sentence[i][1]
        if phrase in dic:
            j = i
            #i番目の単語とその後ろの単語を足していって辞書に含まれるギリギリの境界を調べる(18行目のコメントゆえ、a<bかつa個足して辞書になくb個足すと辞書にあるということはない)
            while phrase in dic and (phrase + sentence[j][1]) in dic and j < len(sentence):
                phrase = phrase + sentence[j][1]
                j += 1
            result.append(dic[phrase])
    return result