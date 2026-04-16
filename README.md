# chatLLM - Chat with your codebase

![doctests](https://github.com/ryankim8/llmLabv1/actions/workflows/doctests.yaml/badge.svg)
![integration-tests](https://github.com/ryankim8/llmLabv1/actions/workflows/integration-tests.yaml/badge.svg)
![flake8](https://github.com/ryankim8/llmLabv1/workflows/flake8/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-ryankim)](https://pypi.org/project/cmc-csci040-ryankim/)
[![codecov](https://codecov.io/gh/ryankim8/llmLabv1/branch/main/graph/badge.svg)](https://codecov.io/gh/ryankim8/llmLabv1)

An AI-powered terminal chat agent that lets you explore and query local files using natural language, powered by Groq.

## Examples

<!-- everytime you have a figure/codeblock/etc, you need sometext beforehand telling the reader why they should care -->

![demo](demo.gif)

<!-- everyone who uses github knows how to install a pypi project;
you don't want to waste their attention telling them -->

This example shows how the agent can look at other files in the directory

```
$ cd testProjects/ryankim8.github.io
$ chat
chat> /ls
./README.md ./animals ./images ./index.html ./styles.css
chat> tell me about these files
This is a simple web page for a zoo. It has a navigation menu with links to different animal pages, a table listing the animals in the zoo, and a footer with links to the author's work and a Creative Commons license. The page also includes some basic CSS styling to make it look a bit nicer.
```

This example shows how the agent cant read the content of files in a folder (ex: README.md) and return a summary

```
$ cd testProjects/markdown-compiler
$ chat
chat> /cat README.md
chat> tell me about this project
This be a Markdown to HTML compiler, a simple project that converts Markdown files to HTML. It seems to have a basic usage where ye can just run it on a Markdown file, and it'll spit out the HTML version. But if ye want some fancy CSS formatting, ye can use the `--add_css` flag.
```

This example shows how the agent can read and output specific details about the project, such as Python libraries

```
$ cd testProjects/ebayWebscraper
$ chat
chat> /cat ebay-dl.py
chat> what python imports does this project use
The project uses the following Python imports:

- `argparse`
- `json`
- `csv`
- `playwright.sync_api`
- `bs4`
- `undetected_playwright`
```
<!-- it would be nice to have some examples that are automatically calling the tools and not manually doing it -->


