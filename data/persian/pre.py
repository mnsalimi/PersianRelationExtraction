import re
import numpy as np
import pandas as pd

file_type = "train"
file_txt = file_type + ".txt" 
file_tsv = file_type + ".tsv" 
train_size = 0.70
test_size = 1 - float((1-train_size)/2)

swapped = True
queries = True

with open(file_txt, "r", encoding="utf-8") as f:
    lines = f.readlines()
    r1 = []
    r1s = []
    r2 = []
    r2s = []
    r_sw = []
    r_sw1 = []
    for i in range(0, len(lines), 1):
        if lines[i].count("<e2>")>1:
            r2.append((lines[i], lines[i+1]))
        elif lines[i].count("</e2>")>1:
            r2s.append((lines[i], lines[i+1]))
        elif lines[i].count("<e1>")>1:
            r1.append((lines[i], lines[i+1]))
        elif lines[i].count("</e1>")>1:
            r1s.append((lines[i], lines[i+1]))
        if "<e2></e1>" in lines[i]:
            r_sw.append((lines[i], lines[i+1]))
        elif "<e1></e2>" in lines[i]:
            r_sw1.append((lines[i], lines[i+1]))
print("num of <e1> > 1: " + str(len(r1)))
print("num of </e1> > 1: " + str(len(r1s)))
print("num of <e2> > 1: " + str(len(r2)))
print("num of </e2> > 1: " + str(len(r2s)))
print("num of <e2></e1>: " + str(len(r_sw)))
print("num of <e1></e2>: " + str(len(r_sw1)))
with open("issues1_in_train.txt", "w", encoding="utf-8") as ff:
    [ff.write(line[0]+"\n"+line[1]+"\n") for line in r1]
    [ff.write(line[0]+"\n"+line[1]+"\n") for line in r2]
with open("issues2_in_train.txt", "w", encoding="utf-8") as ff:
    [ff.write(line[0]+"\n"+line[1]+"\n") for line in r_sw]
    [ff.write(line[0]+"\n"+line[1]+"\n") for line in r_sw1]


with open(file_txt, "r", encoding="utf-8") as f:
    lines = f.readlines()
    lines = [line.replace("\n", "").replace("\"", "") for line in lines if line!="\n" and not line.startswith("Comment:")]
    results = []
    for i in range(0, len(lines)):
        if i%2==0:
            results.append(
                [
                    lines[i+1].replace("\n", ""),
                    lines[i].replace("\n", "").replace("\"", "").split("\t")[1],
                ]
            )
    # print(len(results))
    # print(results[:10])
    if swapped:
        for i in range(len(results)):
            if "<e2></e1>" in results[i][1]:
                results[i][1] = results[i][1].replace("<e2></e1>", "</e1><e2>")
            if "<e1></e2>" in results[i][1]:
                results[i][1] = results[i][1].replace("<e1></e2>", "</e2><e1>")


def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString

results_final = []
for i in range(0, len(results), 1):
    if queries:

        if results[i][1].count("<e2>")==1 and results[i][1].count("</e2>")==1 and\
        results[i][1].count("<e1>")==1 and results[i][1].count("</e1>")==1:
            results_final.append(results[i])
    else:
        if results[i][1].count("<e2>")>1:
            count = results[i][1].count("<e2>")
            for j in range(count-1):
                results[i][1] = replacenth(results[i][1], "<e2>", "", 2)   
                results[i][1] = replacenth(results[i][1], "</e2>", "", 2)

        if lines[i][1].count("</e1>")>1:
            count = lines[i][1].count("<e1>")
            for j in range(count-1):
                results[i][1] = replacenth(results[i][1], "<e1>", "", 2)   
                results[i][1] = replacenth(results[i][1], "</e1>", "", 2)
        if results[i][1].count("<e1>")<=1 and results[i][1].count("</e1>")<=1 and\
        "<e2></e1>" not in results[i][1] and "<e1></e2>" not in results[i][1]:
            results_final.append(lines[i])

# print(results[:5])
df = pd.DataFrame(results_final, columns =['relation', 'sentence'])
train, validate, test = \
              np.split(df.sample(frac=1, random_state=42), 
                       [int(train_size*len(df)), int(test_size*len(df))])
# print(train)
# print(test)
# print(validate)
train.to_csv("train.tsv", sep="\t", index=False, header=False)
test.to_csv("test.tsv", sep="\t", index=False, header=False)
validate.to_csv("dev.tsv", sep="\t", index=False, header=False)

i = 1
with open("answer_test.txt", "w", encoding="utf-8") as f:
    for index, row in test.iterrows():
        f.write(str(len(train)+i) + "\t" + row['relation'] + "\n")
        i += 1

i = 1
with open("answer_dev.txt", "w", encoding="utf-8") as f:
    for index, row in test.iterrows():
        f.write(str(len(train)+i) + "\t" + row['relation'] + "\n")
        i += 1