from collections import defaultdict


class Stats:
    # A list of stats that are unaffected by global multipliers
    statics = ['speed cap', 'enchantment modifier', 'ability damage', 'gear score']

    def __init__(self, args=None):
        if args is None:
            args = {}
        self._dict = args
        self.multiplier = 1
        self.modifiers = defaultdict(list)
        self.children = []
        self.base_children = []

    def __getitem__(self, key):
        if isinstance(key, str):
            base = self._dict.get(key, 0) + sum(c[key] for t, c in self.children)
            for f in self.modifiers[key]:
                base = f(base)
            return base if key in Stats.statics else base * self.multiplier
        else:
            raise TypeError

    def __iadd__(self, other, value=None):
        if isinstance(other, Stats) and not value:
            for k, v in other:
                self[k] += v
        elif isinstance(other, str) and isinstance(value, (int, float)):
            if other in self._dict:
                self._dict[other] += value
            else:
                self._dict[other] = value
        else:
            raise TypeError
        return self

    def __setitem__(self, key, value):
        if isinstance(value, (int, float)):
            self._dict[key] = value
        else:
            raise ValueError

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return str(self._dict)

    def __len__(self):
        return len(self._dict)

    def get_stats_with_base(self, key):
        if isinstance(key, str):
            base = self._dict.get(key, 0) + sum(
                self.children[i][1].multiplier * c[key] for i, (t, c) in enumerate(self.base_children))
            for f in self.modifiers[key]:
                base = f(base)
            return base if key in Stats.statics else base * self.multiplier
        else:
            raise TypeError

    def get_raw_base_stats(self, key):
        if isinstance(key, str):
            return self._dict.get(key, 0) + sum(
                self.children[i][1].multiplier * c[key] for i, (t, c) in enumerate(self.base_children))
        else:
            raise TypeError

    @staticmethod
    def _gen(cls):
        for k in cls._dict.keys():
            yield k, cls[k]

    def __iter__(self):
        return Stats._gen(self)
