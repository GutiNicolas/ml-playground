from itertools import islice


def take_and_transform(read_files, outpu_file, top_labels, over_write=False, sep=";"):
    write_t = "x" if over_write else "w"
    save = open(outpu_file, write_t)
    if over_write:
        top_labels[len(top_labels) - 1] = "".join([top_labels[len(top_labels) - 1], "\n"])
        labels = sep.join(top_labels)
        save.write(labels)

    for r, i, s in read_files:
        file = open(r, "r")
        if '.csv' in r:
            for line in islice(file, 1, None):
                spltd = line.split(s, 1)
                data_clear = '"{}";"{}"\n'.format(spltd[1 if i else 0].replace("\n", "").replace('"', ""),
                                                  spltd[0 if i else 1].replace("\n", "").replace('"', ""))
                save.write(data_clear)
        else:
            for line in file:
                spltd = line.split(None, 1)
                data_clear = '"{}";"{}"\n'.format(spltd[1 if i else 0].replace("\n", "").replace('"', ""),
                                                  spltd[0 if i else 1].replace("\n", "").replace('"', ""))
                save.write(data_clear)
        file.close()
    save.close()


if __name__ == '__main__':
   sources = [("SMSSpamCollection", False, None), ("emails.csv", True, '",')]
   take_and_transform(sources, "data/spam_data/data.csv", ["category", "text"], True)