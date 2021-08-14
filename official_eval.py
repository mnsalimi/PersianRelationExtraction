import os

def official_f1(args, mode):
    # Run the perl script
    # print(args.eval_dir)
    # print(os.path.split(args.eval_dir))
    # print(os.path.split(args.eval_dir))
    perl_program = os.path.split(args.eval_dir)[0]
    try:
        cmd = "perl {0}/semeval2010_task8_scorer-v1.2.pl {1}/proposed_answers_{2}.txt " +\
                "{1}/answer_{2}.txt > {1}/result_{2}_lr_{3}_btchSize_{4}_" +\
                "maxSeqLen_{5}_drpRate_{6}_epoch_{7}.txt".format(
            perl_program, args.eval_dir, mode,
            args.learning_rate, args.train_batch_size,
            args.max_seq_len, args.dropout_rate, args.num_train_epochs

        )
        os.system(cmd)
    except:
        raise Exception("perl is not installed or proposed_answers.txt is missing")

    with open(os.path.join(args.eval_dir, "result_{0}.txt".format(mode)), "r", encoding="utf-8") as f:
        # print(list(f))
        # print(list(f))
        macro_result = list(f)[-1]
        macro_result = macro_result.split(":")[1].replace(">>>", "").strip()
        macro_result = macro_result.split("=")[1].strip().replace("%", "")
        macro_result = float(macro_result) / 100

    return macro_result


if __name__ == "__main__":
    print("macro-averaged F1 = {}%".format(official_f1() * 100))
