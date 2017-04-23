#!/usr/bin/env python3


class studentHelper:
    def __init__(self, sid="NA", fName="NA", lName="NA"):
        self.sid = sid;
        self.fName = fName;
        self.lName = lName;


if __name__ == "__main__":
    print("Running self test...")
    c = studentHelper()
    attrs = vars(c)
    print('\n'.join("%s: %s" % item for item in attrs.items()))
    print("Done")
