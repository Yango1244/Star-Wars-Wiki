def contentChecker(content):
    '''
    Feature 4, Requirement 1 
    Check the words in a comment against a list of inappropriate words
    Params: 
    content- string to be parsed through
    
    Returns True if content contains no inappropriate language
    Returns False if inappropriate language is found
    '''
    bad_words = {
        'masokist', 'schlong', 'qweerz', 'Ekrem*', 'porn', 'knob', 'h00r',
        'son-of-a-bitch', 'Shity', 'knulle', 'ahole', 'pecker', 'sluts', 'muie',
        'pr1ck', 'mouliewop', 'skribz', 'bi+ch', 'skurwysyn', 'futkretzn',
        'shi+', 'dildos', 'retard', 'Fukken', 'dilld0', 'feces', 'schaffer',
        'boobs', 'recktum', 'Felcher', 'enculer', 'gays', 'screw', 'dild0s',
        'lesbian', 'ficken', 'Lezzian', 'testicle*', 'butt-pirate', 'mofo',
        'cazzo', 'pusse', 'azzhole', 'packie', 'skank', 'skankey', 'guiena',
        'smut', 'vulva', 'cunt', 'pussee', 'qahbeh', 'jism', 'faen', '*dyke',
        'boffing', 'sharmute', 'fart', 'shemale', 'h0ar', 'knobz', 'amcik',
        'puuker', 'fag1t', 'screwing', 'schlampe', 'b00bs', 'pule', 'dild0',
        'titt', 'Skanky', 'gayboy', 'cnts', 'dick', 'pizda', 'nastt', 'nigga',
        'kuntz', 'fuk*', 'b!+ch', 'spic', 'Clit', 'chraa', 'Kurac', 'fucking',
        'ejackulate', 'fagg1t', 'niigr;', 'fag*', 'mother-fucker', 'knobs',
        'penus', 'bastardz', 'cock', 'zabourah', 'masterbat3', 'nazi', 'fucks',
        '*damn', 'Fotze', 'pakie', 'basterdz', 'sh1t', 'bitch', 'teets',
        'peeenusss', 'titt*', 'blowjob', 'nutsack', 'queerz', 'cawks', 'l3itch',
        'Phuc', 'shiz', 'Shitty', 'Huevon', 'chuj', 'p0rn', 'cockhead',
        'fuckin', 'nigger*', 'pen1s', 'masterbates', 'shit', 'buttwipe', 'feg',
        'dyke', 'dirsa', 'Fukin', 'andskota', 'assh0le', 'bitch*', 'pr1c',
        'Shyt', 'c0cks', 'dego', 'cock-sucker', 'anus', 'pr1k', 'pimpis',
        'whore', 'sharmuta', 'twat', 'dilld0s', 'vajina', 'sh!+', 'kraut',
        'puta', 'dildo', 'splooge', 'jap', 'fanny', 'nazis', 'shitz', 'ash0les',
        'puto', 'skanck', 'Poonani', 'pula', 'jizm', 'cuntz', 'fux0r',
        'scrotum', 'Fudge Packer', 'gayz', 'Fuken', 'paky', 'peeenus', 'cntz',
        'mulkku', 'bastard', 'fanculo', 'jerk-off', 'buceta', 'wh00r', 'Shytty',
        'va1jina', 'Fukker', 'Lesbian', 'kanker*', 'xxx', 'basterds',
        'butthole', 'pr0n', 'jiss', 'b!tch', 'kurwa', 'Mother Fuker',
        'masstrbait', 'cunts', 'gaygirl', 'chink', 'sex', 'Phuck', 'h0re',
        'orgasum', 'queers', 'hore', 'Cock*', 'Mutha Fuker', 'Lipshitz', 'hoor',
        'honkey', 'polac', 'Fukkin', 'klootzak', 'scank', 'Mutha Fucker',
        'testical', 'tit', 'piss*', 'mamhoon', 'assh0lez', 'yed', 'bi7ch',
        'daygo', 'masturbate', 'kunt', 'shitter', 'puuke', 'h0r', 'packy',
        'sexy', 'Shyty', 'vittu', 'Lipshits', 'asswipe', 'pussy', 'vag1na',
        'nigur;', 'fitt*', 'semen', 's.o.b.', 'masterbaiter', 'ass', 'polak',
        'kusi*', 'fatass', 'scheiss*', 'bitches', 'pimmel', 'ejakulate',
        'asholes', 'boiolas', 'penuus', 'faget', 'arse*', 'assrammer', 'hoer*',
        'sadist', 'kunts', 'dominatricks', 'kuksuger', 'hui', 'poop', 'sh1tter',
        'assholz', 'Biatch', 'testicle', 'wichser', 'orifiss', 'wank', '*shit*',
        'asshole', 'fags', 'kuk', 'faggot', 'kyrpa*', 'helvete', 'turd',
        'faigs', 'qweir', 'cawk', 'orafis', 'b17ch', 'nigger', 'perse',
        'Motha Fukker', 'gook', 'dupa', 'cock-head', 'orgasim;', 'masochist',
        'fuck', 'peenus', 'enema', 'hoore', '@$$', 'hoar', 'b1tch', 'muschi',
        'vullva', 'masterbat*', 'queef*', 'Mutha Fukker', 'Phukker', 'teez',
        'suka', 'faig', 'Motha Fuker', 'poontsee', 'Shyte', 'sh!t', 'h4x0r',
        'masturbat*', 'clit', 'cocks', 'cabron', 'crap', 'monkleigh', 'niiger;',
        'kawk', 'tits', 'lesbo', 'cum', 'Ekto', 'fucker', 'hell', 'slut',
        'japs', 'whoar', 'cipa', 'dike*', 'Flikker', 'pierdol*', 'w00se',
        '*fuck*', 'packi', 'dick*', 'merd*', 'assholes', 'slutz',
        'Carpet Muncher', 'dziwka', 'nepesaurio', 'bassterds', 'f u c k e r',
        'sh1ter', 'skankee', 'sh!t*', 'bollock*', 'n1gr', 'oriface', 'Assface',
        'Fukk', 'breasts', 'vagiina', 'masstrbate', 'fuker', 'cunt*', 'Sh!t',
        'bastards', 'fagz', 'phuck', 'qweers', 'Phuk', 'arschloch', 'c0ck',
        'ayir', 'schmuck', 'sh1tz', 'fagit', 'sh1ts', 'massterbait', 'hoer',
        'foreskin', 'paska*', 'hells', 'vagina', 'jisim', 'fag', 'Fu(*',
        'Motha Fucker', 'fcuk', 'xrated', 'b00b*', 'jizz', 'fuk', 'gay',
        'wank*', 'queer', 'rectum', 'preteen', 'orospu', 'picka', 'paki',
        'skanks', 'penas', 'l3i+ch', 'pillu*', 'polack', 'd4mn', 'f u c k',
        'Phuker', 'Mother Fukkah', 'orgasm', 'penis', 'CockSucker', 'wetback*',
        'Mother Fukker', 'wh0re', 'flipping the bird', 'Fukah', 'dominatrics',
        'ash0le', 'injun', 'motherfucker', 'masterbate', 'peinus', 'Slutty',
        'Fukkah', 'God-damned', 'penis-breath', 'shits', 'kike', 'Ass Monkey',
        'g00k', 'jackoff', 'spierdalaj', 'rautenberg', 'Blow Job', 'vaj1na',
        'dominatrix', 'Mutha Fukah', 'shipal', 'mibun', 'wop*', 'orifice',
        'w0p', 'clits', 'c0k', 'faggit', 'sphencter', 'nigger;'
    }
    words = content.split()
    for word in words:
        if word in bad_words:
            return False
    return True
