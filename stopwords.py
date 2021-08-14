from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
import pandas as pd 
import re 

def extract_sentences(df):
    df_len=len(df.index)
    print(df_len)
    percent=int(df_len/10)
    sentences_dic={}
    j=0
    for index, row in df.iterrows():

        if (index%percent)==1:
            print(int(index/df_len*100) , "   % processed", end="\r", flush=True)
        sentences = nltk.tokenize.sent_tokenize(row["review_text"])

        for sentence in sentences:
            sentences_dic[j] = {'review_id' : row["review_id"],
                            'game_title' : row["game_title"],
                            'sentence': sentence}
            j+=1
    print("100% processed     ")
    sentences_df = pd.DataFrame.from_dict(sentences_dic,orient='index')  # Creation of the dataframe   
    sentences_df = sentences_df.sort_index()  # sorting by index

    return sentences_df


def remove_stop_prefixes(sentences_df, games_list):
    stop_words= getStopWords(games_list)
    prefixes_list= getPrefixes()




    df_len=len(sentences_df.index)
    percent=int(df_len/100)
    proc_sent_dic={}

    for index, row in sentences_df.iterrows():
        if (index%percent)==1:
            print(int(index/df_len*100) , "   % processed", end="\r", flush=True)

        proc_sent = remove_prefixes(row["sentence"],prefixes_list)
        proc_sent = proc_sent.lower()
        proc_sent = remove_stop_words(proc_sent,stop_words)

        proc_sent_dic[index] = {'review_id' : row["review_id"],
                      'game_title' : row["game_title"],
                      'sentence': row["sentence"],
                      "vader_polarity": row["vader_polarity"],
                      'processed_sentence': proc_sent}
    print("100% processed      ")
    proc_sent_df = pd.DataFrame.from_dict(proc_sent_dic,orient='index')  # Creation of the dataframe   
    proc_sent_df = proc_sent_df.sort_index()  # sorting by index
    return proc_sent_df


def getStopWords(games_list):
    
    stop_words = stopwords.words('english')

    other_stop_words="""
    blizzard game games play playing playin played
    a	hereupon six	differently
    a’s	hers	so	downed
    able	herself	some	downing
    about	hi	somebody	downs
    above	him	somehow	early
    according	himself	someone	end
    accordingly	his	something	ended
    across	hither	sometime	ending
    actually	hopefully	sometimes	ends
    after	how	somewhat	evenly
    afterwards	howbeit	somewhere	face
    again	however	soon	faces
    against	i	sorry	fact
    ain’t	i’d	specified	facts
    all	i’ll	specify	felt
    allow	i’m	specifying	find
    allows	i’ve	still	finds
    almost	ie	sub	full
    alone	if	such	fully
    along	ignored	sup	furthered
    already	immediate	sure	furthering
    also	in	t	furthers
    although	inasmuch	t’s	gave
    always	inc	take	general
    am	indeed	taken	generally
    among	indicate	tell	give
    amongst	indicated	tends
    an	indicates	th
    and	inner	than
    another	insofar	thank
    any	instead	thanks
    anybody	into	thanx	group
    anyhow	inward	that	grouped
    anyone	is	that’s	grouping
    anything	isn’t	thats	groups
    anyway	it	the
    anyways	it’d	their
    anywhere	it’ll	theirs
    apart	it’s	them
    appear	its	themselves
    appreciate	itself	then
    appropriate	j	thence
    are	just	there
    aren’t	k	there’s	kind
    around	keep	thereafter	knew
    as	keeps	thereby
    aside	kept	therefore
    ask	know	therein	latest
    asking	knows	theres	lets
    associated	known	thereupon	long
    at	l	these	longer
    available	last	they
    away	lately	they’d	made
    awfully	later	they’ll	make
    b	latter	they’re	making
    be	latterly	they’ve	man
    became	least	think
    because	less	third
    become	lest	this	men
    becomes	let	thorough	mr
    becoming	let’s	thoroughly	mrs
    been	like	those	needed
    before	liked	though	needing
    beforehand	likely	three
    behind	little	through
    being	look	throughout	number
    believe	looking	thru	numbers
    below	looks	thus
    beside	ltd	to
    besides	m	together	open	mainly	too	opened	many	took	opening
    between	may	toward	opens
    beyond	maybe	towards	order
    both	me	tried
    brief	mean	tries
    but	meanwhile	truly
    by	merely	try	part
    c	might	trying	parted
    c’mon	more	twice	parting
    c’s	moreover	two	parts
    came	most	u
    can	mostly	un
    can’t	much	under	point
    cannot	must	unfortunately	pointed
    cant	my	unless	pointing
    cause	myself	unlikely	points
    causes	n	until	present
    certain	unto	presented
    certainly	up	presenting
    changes	nd	upon	presents
    clearly	near	us
    co	nearly	use
    com	used	put
    come	useful	puts
    comes	uses	room
    concerning	neither	using	rooms
    consequently	never	usually	seconds
    consider	nevertheless	uucp	sees
    considering	v	show
    contain	next	showed
    containing	nine	various	showing
    contains	no	very	shows
    corresponding	nobody	via	side
    could	non	viz	sides
    couldn’t	none	vs
    course	noone	w
    currently	nor	want
    d	normally	wants	state
    definitely	not	was	states
    described	nothing	wasn’t	thing
    despite	novel	way	things
    did	now	we	thinks
    didn’t	nowhere	we’d	thought
    different	o	we’ll	thoughts
    do	obviously	we’re	today
    does	of	we’ve	turn
    doesn’t	off	welcome	turned
    doing	often	well	turning
    don’t	oh	went	turns
    done	ok	were	wanted
    down	okay	weren’t	wanting
    downwards	old	what	ways
    during	on	what’s	wells
    e	once	whatever
    each	one	when
    edu	ones	whence
    eg	only	whenever
    eight	onto	where	year
    either	or	where’s	years
    else	other	whereafter	young
    elsewhere	others	whereas	younger
    enough	otherwise	whereby	youngest
    entirely	ought	wherein	beings
    especially	our	whereupon	big
    et	ours	wherever	case
    etc	ourselves	whether	cases
    even	out	which	clear
    ever	outside	while	differ
    every	over	whither	hence
    everybody	overall	who	her
    everyone	own	who’s	here
    everything	p	whoever	here’s
    everywhere	particular	whole	hereafter
    ex	particularly	whom	hereby
    exactly	per	whose	herein
    example	perhaps	why	seven
    except	placed	will	several
    f	please	willing	shall
    far	plus	wish	she
    few	possible	with	should
    fifth	presumably	within	shouldn’t
    first	probably	without	since
    five	provides	won’t	haven’t
    followed	q	wonder	having
    following	que	would	he
    follows	quite	wouldn’t	he’s
    for	qv	x	hello
    former	r	y	help
    formerly	rather	yes	self
    forth	rd	yet	selves
    four	re	you	sensible
    from	really	you’d	sent
    further	reasonably	you’ll
    furthermore	regarding	you’re
    g	regardless	you’ve	asks
    get	regards	your	back
    gets	relatively	yours	backed
    getting	respectively	yourself	backing
    given	right	yourselves	backs
    gives	s	z	began
    go	said	zero
    goes	same	he’d	has
    going	saw	he’ll	hasn’t
    gone	say	how’s	have
    got	saying	mustn’t	seemed
    gotten	says	ours 	seeming
    greetings	second	shan’t	seems
    h	secondly	she’d	seen
    had	see	she’ll	why’s
    hadn’t	seeing	she’s	area
    happens	seem	when’s	asked"""

    #add other stop words
    for word in other_stop_words.split():
        stop_words.append(word)
    #     print("here1", len(stop_words))

    for game in games_list:
        for word in game.split():
            stop_words.append(word)
    #     print("here1", len(stop_words))
    return stop_words


def remove_stop_words(sentence,stop_words):
    #removes common stop words, numbers and words from game titles
    word_list = re.sub("[^\w]", " ",  sentence).split() # remove non alphanumerical characters and split 
    filtered_word_list = [word for word in word_list if word not in stop_words]
    filtered_word_list = [word for word in filtered_word_list if word.isnumeric()==False]

    sentence = " ".join(filtered_word_list)
    return sentence

def getPrefixes():
    prefixes_list=["Early Access Review"]
    return prefixes_list

def remove_prefixes(sentence,prefixes_list):
    for prefix in prefixes_list:
        sentence=sentence.replace( prefix, '')
    return sentence
