# bratviz

This is a simple python wrapper around the brat visualization tool.

It currently works for the CoNLL 2012 format and can visualize SRL and coreference links. You can subclass the `Reader` class to write your own file readers and visualize other formats as well.

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
