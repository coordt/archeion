"""A long list of stopwords to ignore when tokenizing."""
STOPWORDS = (
    "able",
    "about",
    "above",
    "abroad",
    "according",
    "accordingly",
    "across",
    "actually",
    "adj",
    "after",
    "afterwards",
    "again",
    "against",
    "ago",
    "ahead",
    "ain't",
    "all",
    "allow",
    "allows",
    "almost",
    "alone",
    "along",
    "alongside",
    "already",
    "also",
    "although",
    "always",
    "am",
    "amid",
    "amidst",
    "among",
    "amongst",
    "an",
    "and",
    "another",
    "any",
    "anybody",
    "anyhow",
    "anyone",
    "anything",
    "anyway",
    "anyways",
    "anywhere",
    "apart",
    "appear",
    "appreciate",
    "appropriate",
    "are",
    "aren't",
    "around",
    "as",
    "a's",
    "aside",
    "ask",
    "asking",
    "associated",
    "at",
    "available",
    "away",
    "awfully",
    "back",
    "backward",
    "backwards",
    "be",
    "became",
    "because",
    "become",
    "becomes",
    "becoming",
    "been",
    "before",
    "beforehand",
    "begin",
    "behind",
    "being",
    "believe",
    "below",
    "beside",
    "besides",
    "best",
    "better",
    "between",
    "beyond",
    "both",
    "brief",
    "but",
    "by",
    "came",
    "can",
    "cannot",
    "cant",
    "can't",
    "caption",
    "cause",
    "causes",
    "certain",
    "certainly",
    "changes",
    "clearly",
    "c'mon",
    "co",
    "co.",
    "com",
    "come",
    "comes",
    "concerning",
    "consequently",
    "consider",
    "considering",
    "contain",
    "containing",
    "contains",
    "corresponding",
    "could",
    "couldn't",
    "course",
    "c's",
    "currently",
    "dare",
    "daren't",
    "definitely",
    "described",
    "despite",
    "did",
    "didn't",
    "different",
    "directly",
    "do",
    "does",
    "doesn't",
    "doing",
    "done",
    "don't",
    "down",
    "downwards",
    "during",
    "each",
    "edu",
    "eg",
    "eight",
    "eighty",
    "either",
    "else",
    "elsewhere",
    "end",
    "ending",
    "enough",
    "entirely",
    "especially",
    "et",
    "etc",
    "even",
    "ever",
    "evermore",
    "every",
    "everybody",
    "everyone",
    "everything",
    "everywhere",
    "ex",
    "exactly",
    "example",
    "except",
    "fairly",
    "far",
    "farther",
    "few",
    "fewer",
    "fifth",
    "first",
    "five",
    "followed",
    "following",
    "follows",
    "for",
    "forever",
    "former",
    "formerly",
    "forth",
    "forward",
    "found",
    "four",
    "from",
    "further",
    "furthermore",
    "get",
    "gets",
    "getting",
    "given",
    "gives",
    "go",
    "goes",
    "going",
    "gone",
    "got",
    "gotten",
    "greetings",
    "had",
    "hadn't",
    "half",
    "happens",
    "hardly",
    "has",
    "hasn't",
    "have",
    "haven't",
    "having",
    "he",
    "he'd",
    "he'll",
    "hello",
    "help",
    "hence",
    "her",
    "here",
    "hereafter",
    "hereby",
    "herein",
    "here's",
    "hereupon",
    "hers",
    "herself",
    "he's",
    "hi",
    "him",
    "himself",
    "his",
    "hither",
    "hopefully",
    "how",
    "howbeit",
    "however",
    "hundred",
    "i'd",
    "ie",
    "if",
    "ignored",
    "i'll",
    "i'm",
    "immediate",
    "in",
    "inasmuch",
    "inc",
    "inc.",
    "indeed",
    "indicate",
    "indicated",
    "indicates",
    "inner",
    "inside",
    "insofar",
    "instead",
    "into",
    "inward",
    "is",
    "isn't",
    "it",
    "it'd",
    "it'll",
    "its",
    "it's",
    "itself",
    "i've",
    "just",
    "k",
    "keep",
    "keeps",
    "kept",
    "know",
    "known",
    "knows",
    "last",
    "lately",
    "later",
    "latter",
    "latterly",
    "least",
    "less",
    "lest",
    "let",
    "let's",
    "like",
    "liked",
    "likely",
    "likewise",
    "little",
    "look",
    "looking",
    "looks",
    "low",
    "lower",
    "ltd",
    "made",
    "mainly",
    "make",
    "makes",
    "many",
    "may",
    "maybe",
    "mayn't",
    "me",
    "mean",
    "meantime",
    "meanwhile",
    "merely",
    "might",
    "mightn't",
    "mine",
    "minus",
    "miss",
    "more",
    "moreover",
    "most",
    "mostly",
    "mr",
    "mrs",
    "much",
    "must",
    "mustn't",
    "my",
    "myself",
    "name",
    "namely",
    "nd",
    "near",
    "nearly",
    "necessary",
    "need",
    "needn't",
    "needs",
    "neither",
    "never",
    "neverf",
    "neverless",
    "nevertheless",
    "new",
    "next",
    "nine",
    "ninety",
    "no",
    "nobody",
    "non",
    "none",
    "nonetheless",
    "noone",
    "no-one",
    "nor",
    "normally",
    "not",
    "nothing",
    "notwithstanding",
    "novel",
    "now",
    "nowhere",
    "obviously",
    "of",
    "off",
    "often",
    "oh",
    "ok",
    "okay",
    "old",
    "on",
    "once",
    "one",
    "ones",
    "one's",
    "only",
    "onto",
    "opposite",
    "or",
    "other",
    "others",
    "otherwise",
    "ought",
    "oughtn't",
    "our",
    "ours",
    "ourselves",
    "out",
    "outside",
    "over",
    "overall",
    "own",
    "particular",
    "particularly",
    "past",
    "per",
    "perhaps",
    "placed",
    "please",
    "plus",
    "possible",
    "presumably",
    "probably",
    "provided",
    "provides",
    "que",
    "quite",
    "qv",
    "rather",
    "rd",
    "re",
    "really",
    "reasonably",
    "recent",
    "recently",
    "regarding",
    "regardless",
    "regards",
    "relatively",
    "respectively",
    "right",
    "round",
    "said",
    "same",
    "saw",
    "say",
    "saying",
    "says",
    "second",
    "secondly",
    "see",
    "seeing",
    "seem",
    "seemed",
    "seeming",
    "seems",
    "seen",
    "self",
    "selves",
    "sensible",
    "sent",
    "serious",
    "seriously",
    "seven",
    "several",
    "shall",
    "shan't",
    "she",
    "she'd",
    "she'll",
    "she's",
    "should",
    "shouldn't",
    "since",
    "six",
    "so",
    "some",
    "somebody",
    "someday",
    "somehow",
    "someone",
    "something",
    "sometime",
    "sometimes",
    "somewhat",
    "somewhere",
    "soon",
    "sorry",
    "specified",
    "specify",
    "specifying",
    "still",
    "sub",
    "such",
    "sup",
    "sure",
    "take",
    "taken",
    "taking",
    "tell",
    "tends",
    "th",
    "than",
    "thank",
    "thanks",
    "thanx",
    "that",
    "that'll",
    "thats",
    "that's",
    "that've",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "thence",
    "there",
    "thereafter",
    "thereby",
    "there'd",
    "therefore",
    "therein",
    "there'll",
    "there're",
    "theres",
    "there's",
    "thereupon",
    "there've",
    "these",
    "they",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "thing",
    "things",
    "think",
    "third",
    "thirty",
    "this",
    "thorough",
    "thoroughly",
    "those",
    "though",
    "three",
    "through",
    "throughout",
    "thru",
    "thus",
    "till",
    "to",
    "together",
    "too",
    "took",
    "toward",
    "towards",
    "tried",
    "tries",
    "truly",
    "try",
    "trying",
    "t's",
    "twice",
    "two",
    "un",
    "under",
    "underneath",
    "undoing",
    "unfortunately",
    "unless",
    "unlike",
    "unlikely",
    "until",
    "unto",
    "up",
    "upon",
    "upwards",
    "us",
    "use",
    "used",
    "useful",
    "uses",
    "using",
    "usually",
    "v",
    "value",
    "various",
    "versus",
    "very",
    "via",
    "viz",
    "vs",
    "want",
    "wants",
    "was",
    "wasn't",
    "way",
    "we",
    "we'd",
    "welcome",
    "well",
    "we'll",
    "went",
    "were",
    "we're",
    "weren't",
    "we've",
    "what",
    "whatever",
    "what'll",
    "what's",
    "what've",
    "when",
    "whence",
    "whenever",
    "where",
    "whereafter",
    "whereas",
    "whereby",
    "wherein",
    "where's",
    "whereupon",
    "wherever",
    "whether",
    "which",
    "whichever",
    "while",
    "whilst",
    "whither",
    "who",
    "who'd",
    "whoever",
    "whole",
    "who'll",
    "whom",
    "whomever",
    "who's",
    "whose",
    "why",
    "will",
    "willing",
    "wish",
    "with",
    "within",
    "without",
    "wonder",
    "won't",
    "would",
    "wouldn't",
    "yes",
    "yet",
    "you",
    "you'd",
    "you'll",
    "your",
    "you're",
    "yours",
    "yourself",
    "yourselves",
    "you've",
    "zero",
    "a",
    "how's",
    "i",
    "when's",
    "why's",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "j",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "uucp",
    "w",
    "x",
    "y",
    "z",
    "I",
    "www",
    "amount",
    "bill",
    "bottom",
    "call",
    "computer",
    "con",
    "couldnt",
    "cry",
    "de",
    "describe",
    "detail",
    "due",
    "eleven",
    "empty",
    "fifteen",
    "fifty",
    "fill",
    "find",
    "fire",
    "forty",
    "front",
    "full",
    "give",
    "hasnt",
    "herse",
    "himse",
    "interest",
    "itse”",
    "mill",
    "move",
    "myse”",
    "part",
    "put",
    "show",
    "side",
    "sincere",
    "sixty",
    "system",
    "ten",
    "thick",
    "thin",
    "top",
    "twelve",
    "twenty",
    "abst",
    "accordance",
    "act",
    "added",
    "adopted",
    "affected",
    "affecting",
    "affects",
    "ah",
    "announce",
    "anymore",
    "apparently",
    "approximately",
    "aren",
    "arent",
    "arise",
    "auth",
    "beginning",
    "beginnings",
    "begins",
    "biol",
    "briefly",
    "ca",
    "date",
    "ed",
    "effect",
    "et-al",
    "ff",
    "fix",
    "gave",
    "giving",
    "heres",
    "hes",
    "hid",
    "home",
    "id",
    "im",
    "immediately",
    "importance",
    "important",
    "index",
    "information",
    "invention",
    "itd",
    "keys",
    "kg",
    "km",
    "largely",
    "lets",
    "line",
    "'ll",
    "means",
    "mg",
    "million",
    "ml",
    "mug",
    "na",
    "nay",
    "necessarily",
    "nos",
    "noted",
    "obtain",
    "obtained",
    "omitted",
    "ord",
    "owing",
    "page",
    "pages",
    "poorly",
    "possibly",
    "potentially",
    "pp",
    "predominantly",
    "present",
    "previously",
    "primarily",
    "promptly",
    "proud",
    "quickly",
    "ran",
    "readily",
    "ref",
    "refs",
    "related",
    "research",
    "resulted",
    "resulting",
    "results",
    "run",
    "sec",
    "section",
    "shed",
    "shes",
    "showed",
    "shown",
    "showns",
    "shows",
    "significant",
    "significantly",
    "similar",
    "similarly",
    "slightly",
    "somethan",
    "specifically",
    "state",
    "states",
    "stop",
    "strongly",
    "substantially",
    "successfully",
    "sufficiently",
    "suggest",
    "thered",
    "thereof",
    "therere",
    "thereto",
    "theyd",
    "theyre",
    "thou",
    "thoughh",
    "thousand",
    "throug",
    "til",
    "tip",
    "ts",
    "ups",
    "usefully",
    "usefulness",
    "'ve",
    "vol",
    "vols",
    "wed",
    "whats",
    "wheres",
    "whim",
    "whod",
    "whos",
    "widely",
    "words",
    "world",
    "youd",
    "youre",
)
