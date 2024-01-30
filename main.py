from typing import List
import itertools


class PartyResult:
    vote_rate = 0.
    name = "<party-name>"

    def __init__(self, name, vote_rate, possible_partners):
        self.name = name
        self.vote_rate = vote_rate
        self.possible_partners = possible_partners

    def __str__(self):
        return f"{self.name}:{self.vote_rate}"


class CoalitionCandidate:
    total_vote_rate = 0.
    party_results: List[PartyResult]

    def __init__(self, _party_results):
        self.party_results = _party_results
        self.total_vote_rate = sum([_pr.vote_rate for _pr in _party_results])

    def __str__(self):
        return f'[{self.total_vote_rate}] - {", ".join([str(_pr) for _pr in self.party_results])}'


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s) + 1))


# SORTIERE 1. NACH ANZAHL PARTEIEN (WENIGER -> HÖHER), 2. NACH TOTALPROZENT (MEHR -> HÖHER)
def sort_func(i):
    return -(len(i.party_results) * 1000) + i.total_vote_rate * 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    party_results = [
        PartyResult("Union", 29, ["SPD", "Grünen", "FDP", "FW"]),
        PartyResult("AfD", 20, ["Union", "SPD", "FDP", "FW", "BSW"]),
        PartyResult("SPD", 14, ["Union", "Grünen", "FDP", "BSW", "Linke", "FW"]),
        PartyResult("Grünen", 12, ["Union", "SPD", "FDP", "BSW", "Linke", "FW"]),
        PartyResult("BSW", 5, ["Union", "SPD", "Grünen", "FDP", "Linke", "FW"]),
        PartyResult("FDP", 5, ["Union", "SPD", "Grünen", "BSW", "FW"]),
        PartyResult("FW", 5, ["Union", "SPD", "Grünen", "FDP", "BSW", "AfD"]),
        PartyResult("Linke", 5, ["SPD", "Grünen", "FDP", "BSW"]),
        PartyResult("DAVA", 5, ["Union", "SPD", "Grünen", "FDP", "BSW", "Linke", "FW", "AfD"]),
    ]

    ccs = []
    for idx_outer, i in enumerate(powerset(party_results)):
        i = list(i)
        cc = CoalitionCandidate(i)
        # ZEIGE NUR KOMBINATIONEN MIT GRÖSSER GLEICH 50 PROZENT
        if cc.total_vote_rate >= 50:
            # PRÜFE, OB KOMBINATION MÖGLICH IST (ANHAND VON MÖGLICHER PARTNER-LISTE ALLER BETEILIGTER)
            possible_combination = True
            for pr in cc.party_results:  # Grüne -> [Linke, SPD, CDU, ...]
                all_possible_partners = pr.possible_partners.copy()
                all_possible_partners.append(pr.name)
                all_combination_partners = [_pr.name for _pr in cc.party_results]
                for acp in all_combination_partners:
                    if acp not in all_possible_partners:
                        possible_combination = False
                        break
            if possible_combination:
                ccs.append(cc)

    # FILTER KOMBINATIONEN DESSEN TEILMENGE BEREITS ENTHALTEN IST (BEREITS [CDU, SPD] DA? -> VERWERFE [CDU, SPD, GRÜNEN])
    ccs_new = []
    for idx_outer, cc_outer in enumerate(ccs):
        is_no_superset = True
        for idx_inner, cc_inner in enumerate(ccs):
            if idx_inner != idx_outer:
                outer_set = set([i.name for i in cc_outer.party_results])
                inner_set = set([i.name for i in cc_inner.party_results])
                outer_is_superset = inner_set.issubset(outer_set)
                if outer_is_superset:
                    is_no_superset = False
        if is_no_superset:
            ccs_new.append(cc_outer)

    ccs = ccs_new
    ccs.sort(key=sort_func, reverse=True)
    for cc in ccs:
        print(cc)

