class Stats:
    """
    Base stats class.
    """

    # List of stat that isn't affected by multiplier/modifier/dungeon bonus
    _static_stats = ['speed cap', 'ability damage', 'gear score']

    def __init__(self, stats_dict):
        if not stats_dict:
            # so it wont be empty
            stats_dict = {'speed cap': 0}
        self._stats = stats_dict
        self.multiplier = 1
        self.modifiers = {}
        self.dungeon_bonus = 1

        self.profile = None
        self.type = None

    def __str__(self):
        return str(self._stats)

    def __repr__(self):
        return str(self._stats)

    def __len__(self):
        return len(self._stats)

    def get_stat(self, key):
        raise NotImplementedError

    def add_stat(self, key, value):
        """
        Default add stat is add to non dungeon base stat
        """
        if isinstance(key, str) and isinstance(value, (int, float)):
            if key in self._stats:
                self._stats[key] += value
            else:
                self.set_stat(key, value)
        else:
            raise TypeError

    def set_stat(self, key, value):
        """
        Default set stat is set stat to non dungeon base stat
        """
        if isinstance(key, str) and isinstance(value, (int, float)):
            self._stats[key] = value
        else:
            raise TypeError

    def add_modifier(self, key, modifier):
        """
        Add a modifier to the modifiers dict
        """
        if isinstance(key, str) and callable(modifier):
            if key in self._static_stats:
                raise KeyError
            if key not in self.modifiers.keys():
                self.modifiers[key] = []
            self.modifiers[key].append(modifier)
        else:
            raise TypeError

    def __iadd__(self, other):
        if isinstance(other, (dict, Stats)):
            for key, value in other:
                self.add_stat(key, value)
        else:
            raise TypeError
        return self

    @staticmethod
    def _gen(self):
        for key in self._stats.keys():
            yield key, self.get_stat(key)

    def __iter__(self):
        return Stats._gen(self)


class ProfileStats(Stats):
    """
    Profile stats class, extends from Stats class and has extra children attribute that contains all profile item stats.
    """

    def __init__(self, stats_dict=None, profile=None):
        super().__init__(stats_dict)
        self.profile = profile
        self.childrens = []
        self.combat_bonus = 0
        self.archery_bonus = 0

    def get_stat(self, key, *, base=False, raw=False, dungeon=False, ignore=None):
        """
        Default get stat is get all stat + multiplier + modifiers
        Base stat is profile stat without profile multiplier + children base stat
        Raw stat is profile stat without modifiers + children base stat
        """
        if ignore is None:
            ignore = []
        if isinstance(key, str):
            childrens_stat = self.get_all_children_stat(key, base=(base or raw), dungeon=dungeon, ignore=ignore)
            stat = self._stats.get(key, 0) + childrens_stat
            if not base:
                stat = stat if key in self._static_stats else stat * self.multiplier
            if not raw:
                if key in self.modifiers:
                    for func in self.modifiers[key]:
                        stat = func(stat)
            return stat
        else:
            raise TypeError

    def get_all_children_stat(self, key, *, base=False, dungeon=False, ignore=None):
        if isinstance(key, str):
            total = 0
            for child in self.childrens:
                if isinstance(child, PetStats):
                    total += child.get_stat(key)
                elif isinstance(child, ItemStats):
                    total += child.get_stat(key, base=base, dungeon=dungeon)
            return total
        else:
            raise TypeError


class ItemStats(Stats):
    """
    Item stats class, extends from Stats class and has extra reforge stat attribute.
    So getting a base stat from item stat will be: item stat - reforge stat
    """

    def __init__(self, stats_dict=None, item=None):
        super().__init__(stats_dict)
        self.item = item
        self.type = item.type
        self.profile = item.profile
        self.reforge_stat = {}

    def get_stat(self, key, *, base=False, dungeon=False):
        """
        Default get stat is get all stat + multiplier + modifiers.
        Base stat is stat without reforge stat.
        Stat returns is always with multiplier and modifiers
        """
        if isinstance(key, str):
            stat = self._stats.get(key, 0)
            if base and key in self.reforge_stat:
                stat = stat - self.reforge_stat.get(key, 0)
            if key in self.modifiers:  # this wont affect static stat due to add_modifier never accept static stat
                for func in self.modifiers[key]:
                    stat = func(stat)
            return stat if key in self._static_stats else stat * self.multiplier
        else:
            raise TypeError


class PetStats(Stats):
    """
    Pet stats class, extends from Stats class
    """

    def __init__(self, stats_dict=None, pet=None):
        super().__init__(stats_dict)
        self.pet = pet
        self.type = pet.type
        self.profile = pet.profile

    def get_stat(self, key):
        if isinstance(key, str):
            return self._stats.get(key, 0)
        else:
            raise TypeError
