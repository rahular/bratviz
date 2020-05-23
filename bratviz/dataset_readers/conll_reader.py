import spacy

from collections import defaultdict
from allennlp.data.dataset_readers.dataset_utils import Ontonotes

from bratviz.dataset_readers import Reader

# load spacy as soon as imported
nlp = spacy.load("en")


class ConllReader(Reader):
    def __init__(self):
        self.onto_reader = Ontonotes()

    def get_srl_ents(self, srl_frame):
        ents, rels = [], []
        begin = False
        arg = None
        start, end = -1, -1
        for idx, tag in enumerate(srl_frame):
            if tag.startswith("B") and not begin:
                begin = True
                start = idx
                arg = tag[2:]
            elif begin and tag.startswith("I"):
                assert arg == tag[2:], (arg, tag[2:])
                continue
            elif begin:
                if tag == "O":
                    begin = False
                    end = idx
                    ents.append((start, end))
                    rels.append((arg, (start, end)))
                    start = end = -1
                elif tag.startswith("B"):
                    end = idx
                    ents.append((start, end))
                    rels.append((arg, (start, end)))
                    start = idx
                    end = -1
                    arg = tag[2:]
        if len(rels) <= 1:
            return ents, []

        final_rels, verb_span = [], None
        for tag, mention in rels:
            if tag == "V":
                verb_span = mention
                break
        if not verb_span:
            # we did not find a verb
            return ents, final_rels
        for tag, mention in rels:
            if tag != "V":
                final_rels.append((tag, ("head", verb_span), ("dep", mention)))
        return ents, final_rels

    def get_coref_ents(self, cc):
        ents, clusters, rels = [], defaultdict(list), []
        for idx, mention in cc:
            mention = (
                mention[0],
                mention[1] + 1,
            )  # we add one to maintain python slicing
            ents.append(mention)
            clusters[idx].append(mention)
        for cluster in clusters.values():
            if len(cluster) <= 1:
                continue
            ant = cluster[0]
            for mention in cluster[1:]:
                rels.append(("COREF", ("head", ant), ("dep", mention)))
        return ents, rels

    def w2c(self, text, ents):
        doc = nlp(text)
        w2c = dict()
        for word in doc:
            w2c[word.i] = (word.idx, word.idx + len(word))
        cents = {ent: (w2c[ent[0]][0], w2c[ent[1] - 1][1]) for ent in ents}
        return w2c, cents

    def make_ter(self, sent):
        text = " ".join(sent.words)
        # one sentence can have multiple srl annotations
        # depending on how many verbs it has
        to_return = []
        for _, frame in sent.srl_frames:
            ents, rels = [], []
            e_srl, r_srl = self.get_srl_ents(frame)
            e_coref, r_coref = self.get_coref_ents(sent.coref_spans)
            ents.extend(e_srl + e_coref)
            rels.extend(r_srl + r_coref)
            _, cents = self.w2c(text, set(ents))
            ent_dict = {
                k: {"id": "E" + str(n), "cid": v}
                for n, (k, v) in enumerate(cents.items())
            }
            ents = [["E" + str(n), "", [list(v)]] for n, (_, v) in enumerate(cents.items())]
            for idx, rel in enumerate(rels):
                (tag, (head, e1), (dep, e2)) = rel
                rels[idx] = [
                    "R" + str(idx),
                    tag,
                    [[head, ent_dict[e1]["id"]], [dep, ent_dict[e2]["id"]]],
                ]
            to_return.append([text, ents, rels])
        return to_return

    def read(self, fpath: str):
        for doc in self.onto_reader.dataset_document_iterator(fpath):
            for sent in doc:
                to_return = self.make_ter(sent)
                for text, ents, rels in to_return:
                    yield text, ents, rels
