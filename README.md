# bratviz

This is a simple python wrapper around the brat visualization tool.

It currently works for the CoNLL 2012 format and can visualize SRL and coreference links. You can subclass the `Reader` class to write your own file readers and visualize other formats as well.

## Usage

To see all options
```
$ python run.py --help
usage: run.py [-h] -f FILE_PATH [-n NUM_SENT]

Create brat visualizations from file

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file_path FILE_PATH
                        Path to the file to visualize.
  -n NUM_SENT, --num_sent NUM_SENT
                        Number of sentences to parse
```

To visualize the first 100 sentences from a `.conll` file

```
python run.py -f dev.english.v4_gold_conll -n 100
```

## Parsing files

Every `Reader` class is expected to have a `read` method which returns 3 things:
- `text`: text to visualie (usually a sentence). 
- `ents`: a list of constituents/mentions. It should have the following format
```
[
  ['ent_id', '', [[start_char_idx, end_char_idx]]], 
  ...
]
```
- `rels`: a list of relation links between 2 `ents`. It should have the following format
```
[
  ['rel_id', 'rel_tag', [['head', 'ent_id_1'], ['dep', 'ent_id_2']]], 
  ...
]
```

The brat download script and HTML templates are taken from [https://github.com/gabrielStanovsky/brat-visualizer](https://github.com/gabrielStanovsky/brat-visualizer)
