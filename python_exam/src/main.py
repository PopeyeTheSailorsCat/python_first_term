from src import file_reader as fr
from src import research
from src import directory_reader as dir_read


# The format of the data
# ID	Name	Hour(hour)	Machine	Seq
# 0	Petr Mazeev	16	IDSSA1	GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
def most_busy_hour(researches):
    all_machine = []  # To record the names of all machines
    for res in researches:  # We collect names for all studies
        if res.machine not in all_machine:
            all_machine.append(res.machine)

    max_research_hour_for_machine = []  # To record the result
    for mach in all_machine:  # For all cars
        how_many_research_hour = {}  # Creating a dictionary for counting
        for res in researches:  # For all studies
            if res.machine == mach:  # on this machine
                old = how_many_research_hour.get(res.hour, 0)  # We get how many have already counted this hour
                how_many_research_hour[res.hour] = old + 1  # Increase by 1
        max_key = max(how_many_research_hour,
                      key=lambda k: how_many_research_hour[
                          k])  # From the dictionary, we get the hour that is the busiest
        max_research_hour_for_machine.append([mach, max_key])
        how_many_research_hour.clear()  # Clearing the dictionary

    with open("result.txt", "w") as file_output:  # Open the file to display information about the machines
        for elem in max_research_hour_for_machine:
            file_output.write("Name:" + elem[0] + " Hours:" + elem[1] + "\n")


def info_about_researcher(researches):
    all_researchers = []
    for res in researches:  # We collect the names of all researchers
        if res.machine not in all_researchers:
            all_researchers.append(res.full_name)

    for person in all_researchers:  # For all researchers, we create a file and write all the information about their
        # research into it
        with open("researcher_data" + "\\" + person + ".txt", "w") as file_output:
            for res in researches:
                if res.full_name == person:
                    file_output.write(res.machine + " " + res.hour + " " + res.seq + "\n")


path = input()  # Getting our way

researches = []  # To record studies that satisfy us
dir_reader = dir_read.DirReader(path)
for file_name in dir_reader:  # We get the canonical file name that matches our conditions
    with fr.FileReader(
            file_name) as record_reader:  # With the help of our generator, which will give us the correct lines
        for record in record_reader:  # Getting the correct string
            researches.append(research.Research(
                record))  # We write the string of this study to our class and it to the list of studies
most_busy_hour(researches)
info_about_researcher(researches)