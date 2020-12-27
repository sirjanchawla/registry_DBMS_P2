import re

def ExtractOutput(line):
    match = re.search(r"output *= *[a-z]+", line)
    subquery = []

    if not match is None:
        values = match.group().split("=")
        subquery.append(["output", "=", values[1].strip()])

    return subquery
    

def ExtractDate(line):
    matches = re.findall(r"date *[:><=]+ *[0-9]{4}/[0-9]{2}/[0-9]{2}", line)
    subqueries = []

    for match in matches:
        symbol = re.search(r"[:><=]+", match).group()
        term = re.search(r"[0-9]{4}/[0-9]{2}/[0-9]{2}", match).group()
        subqueries.append(["date", symbol, term])

    return subqueries

        
def ExtractFromAndTo(line):
    matches = re.findall(r"from *: *[a-z.]+@[a-z.]+", line)
    matches += re.findall(r"to *: *[a-z.]+@[a-z.]+", line)
    subqueries = []

    for match in matches:
        values = match.split(":")
        subqueries.append([values[0].strip(), ":", values[1].strip()])

    return subqueries


def ExtractBCCAndCC(line):
    matches = re.findall(r"bcc *: *[a-z.]+@[a-z.]+", line)
    line = re.sub(r"bcc *: *[a-z.]+@[a-z.]+", "", line)
    matches += re.findall(r"cc *: *[a-z.]+@[a-z.]+", line)
    subqueries = []

    for match in matches:
        values = match.split(":")
        subqueries.append([values[0].strip(), ":", values[1].strip()])

    return subqueries


def ExtractSubject(line):
    '''
    The first element of subquery will be "subject", never "subj".
    '''
    
    matches = re.findall(r"subject *: *[a-z0-9_-]+", line)
    line = re.sub(r"subject *: *[a-z0-9_-]+", "", line)
    matches += re.findall(r"subj *: *[a-z0-9_-]+", line)
    subqueries = []

    for match in matches:
        values = match.split(":")
        subqueries.append(["subject", ":", values[1].strip()])

    return subqueries


def ExtractBody(line):
    keywords = ["output", "date", "from", "to", "bcc", "subj", "body"]
    match = re.search(r"body *: *[a-z0-9 _-]+", line)
    subqueries = []

    if not match is None:
        match = match.group()
        match = re.sub(r"body *: *", "", match)
        match = re.sub(r" +", " ", match)
        terms = match.split(" ")

        for term in terms:
            if not term in keywords:
                subqueries.append(["body", ":", term])

    return subqueries


def ExtractWildCard(line):
    '''
    The first element of subquery will be empty string.
    '''
    
    matches = re.findall(r"[a-z0-9_-]+%", line)
    subqueries = []

    for match in matches:
        subqueries.append(["", "%", match[: len(match) - 1]])

    return subqueries


def Interpret(line):
    '''
    Converts line to a two dimensional array.
    Each subarray contains three elements.
    The first element is a keyword (i.e. "output", "date", "from", "to", "bcc", "subject" or "body").
    The second element is a symbol (i.e. "=", ":", ">", "<", ">=", "<=" or "%").
    The third element is a term.
    '''
    
    line = line.lower()
    query = []
    query += ExtractOutput(line)
    query += ExtractDate(line)
    query += ExtractFromAndTo(line)
    query += ExtractBCCAndCC(line)
    query += ExtractSubject(line)
    query += ExtractBody(line)
    query += ExtractWildCard(line)
    
    return query
#ine = input("enter quey")
#print(Interpret(line))
    