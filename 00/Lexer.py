import re

# Defining our RE language Grammer ----------------------------------------------------------
identifier = re.compile(r"[\_A-Za-z][A-Za-z0-9_]*", re.UNICODE)  # id can start with _ or alpha and then any rep
keywords = ['auto','break','case','char','const','continue','default','do','double','else','enum','extern','float',
            'for','goto','if','int','long','register','return','short','signed','sizeof','static','switch','typedef'
            'union','unsigned','void','volatile','while']
delimiters = ":;()[]{}#,"+'"'
operators = "+,-,*,/,%,++,--,=,+=,-=,*=,/=,%=,==,>,<,!=,>=,<=,&&,||,!,&,|,^,-,<<,>>,sizeof,?"


# --------------------------------------------------------------------------------------------
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------------------------------
def open_file(file_name):
    # read the lines , line by line striped from \n
    lines_file = [line.rstrip('\n') for line in open(file_name)]
    if len(lines_file) < 0:
        print("File is empty please enter a valid file")
    return lines_file


# --------------------------------------------------------------------------------------------
def parse_lines(lines):
    # split line using white space
    split_line = []
    # chars in any number of repetitions or not chars (special chars)
    pattern = r"[\w]+|[^\s]"			# \w means any rep of words or numbers [a-z , 0-9] ^\s anything but whitespaces
    for index in range(len(lines)):
        temp = re.findall(pattern, lines[index])   # return what matches the pattern into array
        split_line.append(temp)						# if found more than one Array[Tuples]
    return split_line


# --------------------------------------------------------------------------------------------
def lexer(tokens):
    # result arrays
    identifier_result = []
    keywords_result = []
    delimiters_result = []
    operators_result = []
    numbers_result = []
    unknown_result = []

    results = {}

    # iterate over lines
    for i in tokens:
        tok = 0

        # iterate over tokens in line
        while tok < len(i):

            # token is keyword
            if i[tok] in keywords:
                keywords_result.append(i[tok])
                print(i[tok],": Keyword")

            # token is operator
            elif i[tok] in operators:
                # the blow if conditions are for handling ++ , == , != or such operator that contains
                # of two operators not one only one such as +
                # SIMPLE LOOKAHEAD CREATION
                # check if the next token is operator too
                if i[tok+1] in operators:
                    # if the next token is operator too get temp token that take the two tokens
                    temp_operator = i[tok]+i[tok+1]

                    # if temp token is operator
                    if temp_operator in operators:
                        # skip the next loop iteration
                        tok += 1
                        # the operator is the temp one

                        operators_result.append(temp_operator)
                        print(temp_operator, ": Operator")
                    else:
                        # skip the next loop iteration
                        tok += 1

                        # the operator is the temp one
                        invalid_operator = temp_operator

                        unknown_result.append(invalid_operator)
                        print(invalid_operator, ": Invalid Operator")

                else:
                    operator = i[tok]
                    operators_result.append(operator)
                    print(operator,": Operator")

            # token is delimiter
            elif i[tok] in delimiters:
                delimiters_result.append(i[tok])
                print(i[tok], ": Delimiter")
            # token is identifier
            elif re.match(identifier, i[tok]) is not None:
                identifier_result.append(i[tok])
                print(i[tok], ": Identifier")
            elif is_number(i[tok]):
                numbers_result.append(i[tok])
                print(i[tok], ": Number")
            else:
                unknown_result.append(i[tok])
                print(i[tok], ": Unknown Result")

            tok += 1
    results = {"identifier": identifier_result, "keyword": keywords_result, "delimiter": delimiters_result,
                "operator": operators_result, "number": numbers_result, "unknown": unknown_result}
    return results


# --------------------------------------------------------------------------------------------
def format_output(results_input):
    file = open("result.txt", 'w')
    with file as the_file:
        for key, value in results_input.items():
            the_file.write("Type: " + str(key) + '\n')
            the_file.write("Number Of Tokens: " + str(len(value)) + '\n')
            the_file.write("List Of Tokens: \n")

            for token in range(len(value)):
                the_file.write(str(token) + ". " + value[token] + "\n")

            the_file.write("------------------------------------------------------------------------\n")

    file.close()


# --------------------------------------------------------------------------------------------
def main(filename):
    lines = open_file(filename)
    tokens = parse_lines(lines)
    results = lexer(tokens)
    format_output(results)


main("mostafa.txt")
