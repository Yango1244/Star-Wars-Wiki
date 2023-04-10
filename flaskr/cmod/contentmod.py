def contentChecker(content):
    '''
    Feature 4, Requirement 1 
    Check the words in a comment against a list of inappropriate words
    Params: 
    content- string to be parsed through
    
    Returns True if content contains no inappropriate language
    Returns False if inappropriate language is found
    '''
    bad_words = set(set(line.strip() for line in open('flaggedwords.txt')))
    for word in content:
        if word in bad_words:
            return False
    return True
