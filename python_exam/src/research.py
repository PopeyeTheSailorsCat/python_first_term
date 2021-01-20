class Research:
    def __init__(self, line):  # Got the string
        data = line.split()  # smashed it
        self.full_name = data[1] + " " + data[2]  # Collected last name first name in full name
        # self.second_name=data[2]
        self.hour = data[3]
        self.machine = data[4]
        self.seq = data[5]
