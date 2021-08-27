import os
import re
import random
import numpy as np
import pandas as pd

from googletrans import Translator
translator = Translator()

random.seed(200)
file_name = "dataset"
file_txt = file_name + ".txt" 
file_tsv = file_name + ".tsv" 
train_size = 0.70
test_size = 1 - float((1-train_size)/2)
swapped = True
queries = False

add_noisy_data = []
deleted_tokens = 2
folder_name = "swapped_queries_" + str(train_size) +  "_" +\
    str(round(1-test_size,2)) + "_" + str(round(1-test_size,2))
if add_noisy_data:
    folder_name += "_" + "_".join(add_noisy_data)
if "del" in add_noisy_data or "swap_del" in add_noisy_data:
    folder_name += str(deleted_tokens)
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def do_transalte(txt, lang):
    result = translator.translate(txt, dest=lang).text
    return result

def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString

def back_translate(mylist2):
    f2 = []
    for i in range(len(mylist2)):
        if i%10 == 0:
            print(i)
        # i = 22
        # [print(r) for r in mylist2[i][1].split(" ")]
        e1b_index = mylist2[i][1].index("<e1>")
        e2b_index = mylist2[i][1].index("<e2>")
        if e1b_index < e2b_index:

            old_text = mylist2[i].copy()[1]
            be1 = re.findall(r"[^\n]*<e1>", mylist2[i][1])[0].replace("<e1>", " ").lstrip().rstrip().strip()
            e1 = re.findall(r"<e1>[^\n]*</e1>", mylist2[i][1])[0].replace("<e1>", " ").replace("</e1>", " ").lstrip().rstrip().strip()
            ae1_be2 = re.findall(r"</e1>[^\n]*<e2>", mylist2[i][1])[0].replace("</e1>", " ").replace("<e2>", " ").lstrip().rstrip().strip()
            e2 = re.findall(r"<e2>[^\n]*</e2>", mylist2[i][1])[0].replace("<e2>", " ").replace("</e2>", " ").lstrip().rstrip().strip()
            ae2 = re.findall(r"</e2>[^\n]*", mylist2[i][1])[0].replace("</e2>", " ").lstrip().rstrip().strip()
            persian_texts = [be1, e1, ae1_be2, e2, ae2]
            english_texts = [] 
            for item in persian_texts:
                if item == "":
                    english_texts.append("")
                else:
                    while 1==1:
                        try:
                            english_texts.append(do_transalte(item, "en"))
                            break
                        except:
                            pass
                
            final_texts = [] 
            
            for item in english_texts:
                if item == "":
                    final_texts.append("")
                else:
                    while 1==1:
                        try:
                            final_texts.append(do_transalte(item, "fa"))
                            break
                        except:
                            pass
            result = final_texts[0] + " <e1> " + final_texts[1] + " </e1> " + final_texts[2] +\
                " <e2> " + final_texts[3] + " </e2> " + final_texts[4]
            f2.append(
                [mylist2[i][0], old_text]
                )
            f2.append(
                [mylist2[i][0], result]
                )
            # break
        elif e2b_index < e1b_index:
            old_text = mylist2[i].copy()[1]
            be2 = re.findall(r"[^\n]*<e2>", mylist2[i][1])[0].replace("<e2>", " ").lstrip().rstrip().strip()
            e2 = re.findall(r"<e2>[^\n]*</e2>", mylist2[i][1])[0].replace("<e2>", " ").replace("</e2>", " ").lstrip().rstrip().strip()
            ae2_be1 = re.findall(r"</e2>[^\n]*<e1>", mylist2[i][1])[0].replace("</e2>", " ").replace("<e1>", " ").lstrip().rstrip().strip()
            e1 = re.findall(r"<e1>[^\n]*</e1>", mylist2[i][1])[0].replace("<e1>", " ").replace("</e1>", " ").lstrip().rstrip().strip()
            ae1 = re.findall(r"</e1>[^\n]*", mylist2[i][1])[0].replace("</e1>", " ").lstrip().rstrip().strip()
            persian_texts = [be2, e2, ae2_be1, e1, ae1]
            english_texts = [] 
            for item in persian_texts:
                if item == "":
                    english_texts.append("")
                else:
                    while 1==1:
                        try:
                            english_texts.append(do_transalte(item, "en"))
                            break
                        except:
                            pass
                
            final_texts = [] 
            
            for item in english_texts:
                if item == "":
                    final_texts.append("")
                else:
                    while 1==1:
                        try:
                            final_texts.append(do_transalte(item, "fa"))
                            break
                        except:
                            pass
            result = final_texts[0] + " <e2> " + final_texts[1] + " </e2> " + final_texts[2] +\
                " <e1> " + final_texts[3] + " </e1> " + final_texts[4]
            f2.append(
                [mylist2[i][0], old_text]
                )
            f2.append(
                [mylist2[i][0], result]
                )
            # break
    # print(txt.text)
    return f2

def del_token(mylist1, delete_count):
    ff = []
    for i in range(len(mylist1)):
        # print(i)
        # i = 324
        qr = [tkn for tkn in mylist1[i][1].split(" ") if tkn]
        e1b = qr.index("<e1>")
        e1e = qr.index("</e1>")
        e2b = qr.index("<e2>")
        e2e = qr.index("</e2>")
        nums = []
        for j in range(delete_count):
            if j == 0:
                nums.append(
                    random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e ])
                )
            try:
                if j == 1:
                    nums.append(
                        random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=nums[0] ])
                    )
            except:
                continue
            try:
                if j == 2:
                    nums.append(
                        random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=nums[0] and ele!=nums[1] ])
                    )
            except:
                continue
            try:
                if j == 3:
                    nums.append(
                        random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=nums[0] and ele!=nums[1] and ele!=nums[2]])
                    )
            except:
                continue
        qr_new = qr.copy()
        # print(nums)
        # print(len(qr_new))
        qr_new = [qr_new[i] for i in range(len(qr_new)) if i not in nums]
        # print(len(qr_new))
        ff.append([mylist1[i][0], " ".join(qr)])
        ff.append([mylist1[i][0], " ".join(qr_new)])
        # print(ff)
        # exit()
    return ff

def del_swap_tokens(mylist3, delete_count):
    ff2 = []
    for i in range(len(mylist3)):
        # print(i)
        # i = 324
        qr = [tkn for tkn in mylist3[i][1].split(" ") if tkn]
        e1b = qr.index("<e1>")
        e1e = qr.index("</e1>")
        e2b = qr.index("<e2>")
        e2e = qr.index("</e2>")
        nums = []
        for i in range(delete_count):
            if i == 0:
                nums.append(
                    random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e ])
                )
            try:
                if i == 1:
                    nums.append(
                        random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=nums[0] ])
                    )
            except:
                continue
            try:
                if i == 2:
                    nums.append(
                        random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=nums[0] and ele!=nums[1] ])
                    )
            except:
                continue
            try:
                if i == 3:
                    nums.append(
                        random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=nums[0] and ele!=nums[1] and ele!=nums[2]])
                    )
            except:
                continue
        qr_new = qr.copy()
        # print(nums)
        # print(len(qr_new))
        qr_new = [qr_new[i] for i in range(len(qr_new)) if i not in nums]
        e1b = qr_new.index("<e1>")
        e1e = qr_new.index("</e1>")
        e2b = qr_new.index("<e2>")
        e2e = qr_new.index("</e2>")
        try:
            num1 = random.choice([ele for ele in list(range(0, len(qr_new))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e ])
            num2 = random.choice([ele for ele in list(range(0, len(qr_new))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=num1 ])
            qr_new1 = qr_new.copy()
            qr_new1[num1], qr_new1[num2] = qr_new1[num2], qr_new1[num1]
        
            ff2.append([mylist3[i][0], " ".join(qr)])
            ff2.append([mylist3[i][0], " ".join(qr_new1)])
        except:
            ff2.append([mylist3[i][0], " ".join(qr)])
            ff2.append([mylist3[i][0], " ".join(qr_new)])
        
        # print(ff2)
        # exit()
    return ff2

def swap_tokens(mylist):
    fff = []
    for i in range(len(mylist)):
        qr = [tkn for tkn in mylist[i][1].split(" ") if tkn]
        e1b = qr.index("<e1>")
        e1e = qr.index("</e1>")
        e2b = qr.index("<e2>")
        e2e = qr.index("</e2>")
        num1 = random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e ])
        num2 = random.choice([ele for ele in list(range(0, len(qr))) if not e1b <= ele <= e1e and not e2b <= ele <= e2e and ele!=num1 ])
        qr_new = qr.copy()
        qr_new[num1], qr_new[num2] = qr_new[num2], qr_new[num1]
        fff.append(
            [
                mylist[i][0],
                ' '.join(qr)
            ]
        )
        fff.append(
            [
                mylist[i][0],
                ' '.join(qr_new)
            ]
        )
        # print(fff)
        # break
        
    # print(f_results[:5])
    return fff

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

with open(os.path.join(folder_name, "issues1_in_train.txt"), "w", encoding="utf-8") as ff:
    [ff.write(line[0]+"\n"+line[1]+"\n") for line in r1]
    [ff.write(line[0]+"\n"+line[1]+"\n") for line in r2]

with open(os.path.join(folder_name, "issues2_in_train.txt"), "w", encoding="utf-8") as ff:
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
    f= 0
    if swapped:
        for i in range(len(results)):
            if "دی بانک اوگاندا نشان می دهد که ب" in results[i][1]:
                # print("yes")
                # [print(r) for r in results[i][1].split(" ")]
                f = 1
            # print(results[i])
            if "<e2></e1>" in results[i][1]:
                results[i][1] = results[i][1].replace("<e2></e1>", "</e1><e2>")
            if "<e1></e2>" in results[i][1]:
                results[i][1] = results[i][1].replace("<e1></e2>", "</e2><e1>")
            results[i][1] = results[i][1].replace("<e1>", " <e1> ")
            results[i][1] = results[i][1].replace("</e1>", " </e1> ")
            results[i][1] = results[i][1].replace("<e2>", " <e2> ")
            results[i][1] = results[i][1].replace("</e2>", " </e2> ")
            if f == 1:
            #     print(":no")
            #     [print(r) for r in results[i][1].split(" ")]
                f = 0
# exit()
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

        if results[i][1].count("</e1>")>1:
            count = results[i][1].count("<e1>")
            for j in range(count-1):
                results[i][1] = replacenth(results[i][1], "<e1>", "", 2)   
                results[i][1] = replacenth(results[i][1], "</e1>", "", 2)
        if results[i][1].count("<e1>")<=1 and results[i][1].count("</e1>")<=1 and\
        "<e2></e1>" not in results[i][1] and "<e1></e2>" not in results[i][1]:
            results_final.append(results[i])
df = pd.DataFrame(results_final, columns =['relation', 'sentence'])
print(len(df))
train, validate, test = \
              np.split(df.sample(frac=1, random_state=42), 
                       [int(train_size*len(df)), int(test_size*len(df))])

if add_noisy_data:
    if "swap" in add_noisy_data or "del" in add_noisy_data or "translate" in\
        add_noisy_data or "swap_del" in add_noisy_data:
        train = train.values.tolist()
        if "swap_del" in add_noisy_data:
            print(1)
            train = del_swap_tokens(train, deleted_tokens)
        if "swap" in add_noisy_data:
            print(2)
            train = swap_tokens(train)
        if "del" in add_noisy_data:
            print(3)
            train = del_token(train, deleted_tokens)
        if "translate" in add_noisy_data:
            print(4)
            train = back_translate(train)
        train = pd.DataFrame(train, columns =['relation', 'sentence'])
        train = train.sample(frac=1).reset_index(drop=True)
print(len(train))
print(len(test))
print(len(validate))

# print(train)
# print(test)
# print(validate)
train.to_csv(os.path.join(folder_name, "train.tsv"), sep="\t", index=False, header=False)
test.to_csv(os.path.join(folder_name, "test.tsv"), sep="\t", index=False, header=False)
validate.to_csv(os.path.join(folder_name, "dev.tsv"), sep="\t", index=False, header=False)

i = 1
with open(os.path.join(folder_name, "answer_test.txt"), "w", encoding="utf-8") as f:
    for index, row in test.iterrows():
        f.write(str(len(train)+i) + "\t" + row['relation'] + "\n")
        i += 1

i = 1
with open(os.path.join(folder_name, "answer_dev.txt"), "w", encoding="utf-8") as f:
    for index, row in validate.iterrows():
        f.write(str(len(train)+i) + "\t" + row['relation'] + "\n")
        i += 1
labels = [
    "Other",
    "Cause-Effect(e1,e2)",
    "Cause-Effect(e2,e1)",
    "Instrument-Agency(e1,e2)",
    "Instrument-Agency(e2,e1)",
    "Product-Producer(e1,e2)",
    "Product-Producer(e2,e1)",
    "Content-Container(e1,e2)",
    "Content-Container(e2,e1)",
    "Entity-Origin(e1,e2)",
    "Entity-Origin(e2,e1)",
    "Entity-Destination(e1,e2)",
    "Entity-Destination(e2,e1)",
    "Component-Whole(e1,e2)",
    "Component-Whole(e2,e1)",
    "Member-Collection(e1,e2)",
    "Member-Collection(e2,e1)",
    "Message-Topic(e1,e2)",
    "Message-Topic(e2,e1)",
]
with open(os.path.join(folder_name, "labels.txt"), "w", encoding="utf-8") as f:
    for label in labels:
        f.write(label + "\n")
