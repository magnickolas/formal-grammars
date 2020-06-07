# Formal grammars

![][cyk_example]

Some tools to run algorithms on context-free grammars (CFG).
Requires Python 3.7.

## Usage

- `git clone https://github.com/magnickolas/formal_grammars && cd formal_grammars`
- `python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt`
- Put the CFG's rules inside [grammar file][grammar_file], see an example there
- Use one of the following algorithms:
    - **LL(1)-parser builder**: print LL(1)-parser table
        ```
        python -m formal_grammars ll1
        ```
    - **LR(1)-parser builder**: print LR(1)-parser table
        ```
        python -m formal_grammars lr1
        ```
    - **Cocke — Younger — Kasami table builder**: checks if a word is accepted by the grammar (the implementation accepts an arbitrary CFG).
        ```
        python -m formal_grammars cyk <word:str>
        ```
    - **Grammar words generator**: generate words from the grammar in alphabetical order (uses CYK algorithm)
        ```
        python -m formal_grammars gen [-n <num:int, 20>]
        ```

For educational purposes only.

[grammar_file]: grammar.yaml
[cyk_example]: imgs/cyk_example.jpg
