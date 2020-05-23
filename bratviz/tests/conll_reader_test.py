import unittest

from bratviz.dataset_readers import ConllReader


class ConllReaderTestMethods(unittest.TestCase):
    def test_get_srl_ents(self):
        reader = ConllReader()
        # fmt:off
        srl_tags = [
            ["O", "O", "O"],
            ["O","O","O","O","O","O","O","O","O","O","O","O","B-V","O","O","O","O","O","O","O","O","O","O","O","O","O","O"],
            ["B-ARGM-TMP","I-ARGM-TMP","I-ARGM-TMP","I-ARGM-TMP","I-ARGM-TMP","O","B-ARG1","I-ARG1","I-ARG1","I-ARG1","I-ARG1",
            "I-ARG1","I-ARG1","I-ARG1","I-ARG1","I-ARG1","B-V","B-ARG1","I-ARG1","I-ARG1","I-ARG1","I-ARG1","I-ARG1","I-ARG1",
            "I-ARG1","I-ARG1","O"],
        ]
        ents = [[], [(12, 13)], [(0, 5), (6, 16), (16, 17), (17, 26)]]
        rels = [[], [], [
                ("ARGM-TMP", ("head", (16, 17)), ("dep", (0, 5))),
                ("ARG1", ("head", (16, 17)), ("dep", (6, 16))),
                ("ARG1", ("head", (16, 17)), ("dep", (17, 26))),
            ],
        ]
        # fmt:on

        for idx, st in enumerate(srl_tags):
            e, r = reader.get_srl_ents(st)
            ents[idx] = sorted(ents[idx], key=lambda x: (x[0], x[1]))
            e = sorted(e, key=lambda x: (x[0], x[1]))
            self.assertListEqual(ents[idx], e)
            self.assertListEqual(rels[idx], r)

    def test_get_coref_ents(self):
        reader = ConllReader()
        coref_spans = [
            {},
            {(19, (9, 10)), (19, (24, 25))},
            {(1, (1, 7)), (9, (10, 12)), (9, (6, 7))},
        ]
        ents = [[], [(9, 11), (24, 26)], [(1, 8), (6, 8), (10, 13)]]
        rels = [
            [],
            [("COREF", ("head", (9, 11)), ("dep", (24, 26)))],
            [("COREF", ("head", (10, 13)), ("dep", (6, 8)))],
        ]
        for idx, cs in enumerate(coref_spans):
            e, r = reader.get_coref_ents(cs)
            ents[idx] = sorted(ents[idx], key=lambda x: (x[0], x[1]))
            e = sorted(e, key=lambda x: (x[0], x[1]))
            self.assertListEqual(ents[idx], e)
            self.assertListEqual(rels[idx], r)

    def test_w2c(self):
        text = "This is a tokenized sentence . Let 's put some more text here ."
        ents = ((0, 1), (2, 5), (6, 8), (8, 9), (9, 12), (12, 13))
        # fmt:off
        w2c_gold = {0: (0, 4), 1: (5, 7), 2: (8, 9), 3: (10, 19), 4: (20, 28), 5: (29, 30), 6: (31, 34), 7: (35, 37), 
               8: (38, 41), 9: (42, 46), 10: (47, 51), 11: (52, 56), 12: (57, 61), 13: (62, 63)}
        cents_gold = {(0, 1): (0, 4), (2, 5): (8, 28), (6, 8): (31, 37), (8, 9): (38, 41), 
                      (9, 12): (42, 56), (12, 13): (57, 61)}
        # fmt:on
        reader = ConllReader()
        w2c, cents = reader.w2c(text, ents)
        self.assertDictEqual(w2c_gold, w2c)
        self.assertDictEqual(cents_gold, cents)


if __name__ == "__main__":
    unittest.main()
