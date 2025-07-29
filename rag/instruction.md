RAG server (port 1310) methods

- add
- show
- remove
- query
- status

- RAG
    - add
        - input: string + collection name
        - output: status (success/failure)
    - show:
        - output: all collection names
    - view
        - input: collection name
        - output: all records with id & string
    - remove
        - input: id + collection name
        - output: status (success/failure)
    - query
        - input: string + collection name
        - output: list[string]