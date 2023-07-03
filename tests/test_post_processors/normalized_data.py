"""Compilation of normalized data for use in tests."""

import dateutil.parser

csstricks_html = {
    "type": "https://schema.org/CreativeWork",
    "headline": "Words To Avoid in Educational Writing | CSS-Tricks",
    "description": (
        "I'm no English major, but as a writer and consumer of loads of educational (mostly tech) writing, I've come "
        "to notice a number of words and phrases that"
    ),
    "author": None,
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
csstricks_jsonld = {
    "type": "https://schema.org/CreativeWork",
    "headline": None,
    "description": (
        "I'm no English major, but as a writer and consumer of loads of educational (mostly tech) writing, I've come "
        "to notice a number of words and phrases that"
    ),
    "author": None,
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
github_html = {
    "type": "https://schema.org/CreativeWork",
    "headline": (
        "archivy/archivy: Archivy is a self-hosted knowledge repository that allows you to safely preserve useful\n"
        "    content that contributes to your own personal, searchable and extendable wiki."
    ),
    "description": (
        "Archivy is a self-hosted knowledge repository that allows you to safely preserve useful content "
        "that contributes to your own personal, searchable and extendable wiki. - archivy/archivy"
    ),
    "author": None,
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
github_jsonld = {
    "type": "https://schema.org/CreativeWork",
    "headline": None,
    "description": None,
    "author": None,
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}

medium_html = {
    "type": "https://schema.org/CreativeWork",
    "headline": (
        "Fetching Better Beer Recommendations with Collie (Part 1) " "| by Nathan Cooper Jones | ShopRunner | Medium"
    ),
    "description": (
        "TL;DR \u2014 I talk about ShopRunner\u2019s latest open source library, Collie [GitHub, PyPI, "
        "Docs], for training and evaluating deep learning recommendations systems. We use Collie to train "
        "a model to\u2026"
    ),
    "author": [
        {
            "type": "https://schema.org/Person",
            "name": "Nathan Cooper Jones",
        }
    ],
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
medium_jsonld = {
    "type": "https://schema.org/NewsArticle",
    "headline": "Fetching Better Beer Recommendations with Collie (Part 1)",
    "description": (
        "TL;DR \u2014 I talk about ShopRunner\u2019s latest open source library, Collie [GitHub, PyPI, "
        "Docs], for training and evaluating deep learning recommendations systems. We use Collie to train "
        "a model to\u2026"
    ),
    "author": [
        {
            "type": "https://schema.org/Person",
            "name": "Nathan Cooper Jones",
            "url": "https://medium.com/@nathancooperjones",
        }
    ],
    "publisher": [
        {
            "type": "https://schema.org/Organization",
            "name": "ShopRunner",
            "url": "https://medium.com/shoprunner",
            "logo": {
                "type": "ImageObject",
                "width": 273,
                "height": 60,
                "url": "https://miro.medium.com/max/546/1*cAawW8I5BpAOGBqk-Y8OQg.png",
            },
        }
    ],
    "keywords": set(),
    "datePublished": dateutil.parser.isoparse("2021-05-04T19:11:02.311Z"),
    "source": (
        "https://medium.com/shoprunner/fetching-better-beer-recommendations-" "with-collie-part-1-18c73ab30fbd"
    ),
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}

missing_data_html = {
    "type": "https://schema.org/CreativeWork",
    "headline": None,
    "description": None,
    "author": None,
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
missing_data_jsonld = {
    "type": "https://schema.org/CreativeWork",
    "headline": None,
    "description": None,
    "author": None,
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
uxcollective_html = {
    "type": "https://schema.org/CreativeWork",
    "headline": (
        "How to design data visualizations that are actually valuable | by Angelica Gutierrez "
        "| Jul, 2021 | UX Collective"
    ),
    "description": (
        "Great visualizations help people quickly and accurately make sense of the data so they can make "
        "appropriate decisions. These types of visualizations optimize for the human visual system "
        "making\u2026"
    ),
    "author": [
        {
            "type": "https://schema.org/Person",
            "name": "Angelica Gutierrez",
        }
    ],
    "publisher": None,
    "keywords": set(),
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
youtube_html = {
    "type": "https://schema.org/CreativeWork",
    "headline": "Pascal (Not Just Nickel & Dime) - Computerphile",
    "description": (
        "Pascal evolved from Algol 60. Professor Brailsford discusses the rift in the Algol committee "
        "that led to its creation.Brian Kernighan's Bell Labs Memo: http:..."
    ),
    "author": None,
    "publisher": None,
    "keywords": {"computers", "computerphile", "computer", "science"},
    "datePublished": None,
    "source": None,
    "encodingFormat": "text/html",
    "sourceEncodingFormat": "text/html",
}
yoast_jsonld = {
    "author": [
        {
            "id": "https://a16z.com/#/schema/person/919c5e090d740be0076090817db58591",
            "image": {
                "caption": "dharris",
                "contentUrl": (
                    "https://secure.gravatar.com/avatar/37b22968271038e7833f6768c3ce09cd?s=96&d=identicon&r=g"
                ),
                "id": "https://a16z.com/#/schema/person/image/6c0183d836b70fb6abbca31a12615882",
                "inLanguage": "en-US",
                "type": "ImageObject",
                "url": "https://secure.gravatar.com/avatar/37b22968271038e7833f6768c3ce09cd?s=96&d=identicon&r=g",
            },
            "name": "dharris",
            "type": "https://schema.org/Person",
            "url": "https://a16z.com/author/dharris/",
        }
    ],
    "dateArchived": None,
    "datePublished": dateutil.parser.isoparse("2023-06-20T19:23:48+00:00"),
    "description": (
        "A reference architecture for the LLM app stack. It shows the most common systems, tools, and design patterns "
        "used by AI startups and tech companies."
    ),
    "encodingFormat": "text/html",
    "headline": "Emerging Architectures for LLM Applications | Andreessen Horowitz",
    "keywords": set(),
    "publisher": None,
    "source": [
        "https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications/",
        "https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications/",
    ],
    "sourceEncodingFormat": "text/html",
    "type": "https://schema.org/WebPage",
}
yoast2_jsonld = {
    "author": [
        {
            "id": "https://trishagee.com/#/schema/person/4737d3294c02a8c1b44e08946d0c6081",
            "image": {
                "caption": "Trisha Gee",
                "contentUrl": "https://trishagee.com/wp-content/uploads/2022/09/cropped-TRISHA-GEE-NEGATIVE-transparent-1.png",  # NOQA: E501
                "height": 250,
                "id": "https://trishagee.com/#/schema/person/image/be51a6d663f3c07c984f3a770818f583",
                "inLanguage": "en-US",
                "type": "ImageObject",
                "url": "https://trishagee.com/wp-content/uploads/2022/09/cropped-TRISHA-GEE-NEGATIVE-transparent-1.png",  # NOQA: E501
                "width": 565,
            },
            "logo": "https://trishagee.com/#/schema/person/image/be51a6d663f3c07c984f3a770818f583",
            "name": "Trisha Gee",
            "type": "https://schema.org/Person",
        }
    ],
    "datePublished": dateutil.parser.isoparse("2023-05-29T15:31:36+00:00"),
    "description": None,
    "encodingFormat": "text/html",
    "headline": "Why I prefer trunk-based development",
    "keywords": {"vcs", "ci", "git", "cd"},
    "publisher": [
        {
            "id": "https://trishagee.com/#/schema/person/4737d3294c02a8c1b44e08946d0c6081",
            "image": {
                "caption": "Trisha Gee",
                "contentUrl": "https://trishagee.com/wp-content/uploads/2022/09/cropped-TRISHA-GEE-NEGATIVE-transparent-1.png",  # NOQA: E501
                "height": 250,
                "id": "https://trishagee.com/#/schema/person/image/be51a6d663f3c07c984f3a770818f583",
                "inLanguage": "en-US",
                "type": "ImageObject",
                "url": "https://trishagee.com/wp-content/uploads/2022/09/cropped-TRISHA-GEE-NEGATIVE-transparent-1.png",  # NOQA: E501
                "width": 565,
            },
            "logo": "https://trishagee.com/#/schema/person/image/be51a6d663f3c07c984f3a770818f583",
            "name": "Trisha Gee",
            "type": "https://schema.org/Person",
        }
    ],
    "source": "https://trishagee.com/2023/05/29/why-i-prefer-trunk-based-development/#article",
    "sourceEncodingFormat": "text/html",
    "type": "https://schema.org/Article",
}
