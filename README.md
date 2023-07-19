# Archeion

An archive of URLs

## Problem

I want to bookmark web pages for reference later on. 
I want to extract all metadata from them in order to find relationships of concepts and group similar items.
I want to have a standard method for generating tags
I want to have the URL archived for offline review in several formats including (but not limited to):
    - Raw HTML
    - PDF
    - A compressed single-file HTML with all images included
I want to be able to post-process archived artifacts to
    - convert to other formats (such as HTML to Markdown)
    - summarize the content
    - generate tags and extract entities
I want an interface to browse and manage the content.
I want an interface to discover connections between the content

## Constraints

??

## Functional requirements

- Easily installable (for loose definitions of "easy")

## Non-functional requirements

- The effort for adding a new bookmark should be as low as possible

## User Stories

### Installation

- `brew install archeion`
- Maybe use the mechanism Poetry uses to bootstrap itself?
  - https://python-poetry.org/docs/#installing-with-the-official-installer
- `pipx install archeion`

?? https://help.obsidian.md/Advanced+topics/How+Obsidian+stores+data
?? https://help.obsidian.md/Advanced+topics/Using+Obsidian+URI

### Initial Setup

Pre-requisites: [Installation](#installation)

- `archeion new <name of archive directory>`

?? If multiple archives are allowed, how does archeion know which one to use


### Index a URL

Pre-requisites: [Initial setup](#initial-setup)

CLI Interface:

1. User runs `archeion add "<url>"`
2. Link is added to index
   3. File created in 
3. Options
   4. Immediately archives and post-processes
   5. Delay archiving and post-processing

- Using a custom URI
- Using a GUI
- Using a TUI

?? How do we know if an attempt failed?

### Storage Ideas

Structure the file system as the database

- 📂 Artifacts
    - 📂 <unique-filename>
        - 📄 index.yaml (a row in a "links" table)
- 📂 Queue
    - Place to store artifacts to archive
    - Maybe use a system similar to RSMQ's queue structure
- 📄 config.yaml


### Events

- Add(URL): Add a new link to the index
- Archive(link_id, format): Archive the link in the specified format
- PostProcess(link_id, format): Post-process the link in the specified format
