import pickle
def main():
    print("Opening pickle jar...")
    pickle_in = open("qtable_init.pickle","rb")
    table = pickle.load(pickle_in)

    first_line = True
    head = ["-"]

    print("Converting to TSV...")
    with open("qtable.tsv", 'w') as file:
        for (state, actions) in table.items():
            line = [str(state)]
            for (action, value) in actions.items():
                if first_line:
                    head.append(str(action))
                line.append(str(value))

            if first_line:
                file.write("%s\n" % ("\t".join(head)))
                first_line = False
            file.write("%s\n" % ("\t".join(line)))

    print("Done!")

if __name__ == "__main__":
    main()
