import os
EVAL_DIR = "eval"

def official_f1(args, mode):
    # Run the perl script
    perl_program = os.path.split(args.eval_dir)[0]
    # print(perl_program)
    # print("{0}/semeval2010_task8_scorer-v1.2.pl".format(perl_program))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)
    # folder = os.path.join(dir_path, "eval")
    # print(folder)
    # f = os.path.join(folder, "semeval2010_task8_scorer-v1.2.pl")
    # print(f)
    # print(args.eval_dir)
    # print(mode)
    try:
        # cmd = "perl {3} {1}/proposed_answers_{2}.txt " +\
        #         "{1}/answer_{2}.txt > {1}/result_{2}.txt".format(
        #     perl_program, args.eval_dir, mode, f
        # )
        cmd = "perl {0}/semeval2010_task8_scorer-v1.2.pl {1}/proposed_answers_{2}.txt {1}/answer_{2}.txt > {1}/result_{2}.txt".format(
            EVAL_DIR, args.eval_dir, mode
        )
        os.system(cmd)
    except:
        raise Exception("perl is not installed or proposed_answers.txt is missing")

    with open(os.path.join(args.eval_dir, "result_{0}.txt".format(mode)), "r", encoding="utf-8") as f:
        macro_result = list(f)[-1]
        macro_result = macro_result.split(":")[1].replace(">>>", "").strip()
        macro_result = macro_result.split("=")[1].strip().replace("%", "")
        macro_result = float(macro_result) / 100

    return macro_result


if __name__ == "__main__":
    print("macro-averaged F1 = {}%".format(official_f1() * 100))
