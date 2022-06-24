import spot
import json


class Automaton:
    """
    Extracts data from spot automaton format.
    """
    def __init__(self):
        self.acc_name = None
        self.num_sets = -1
        self.num_states = -1
        self.init_state = -1
        self.atoms = list()
        self.name = None
        self.is_deterministic = None
        self.is_unambiguous = None
        self.is_state_based_acc = None
        self.is_terminal = None
        self.is_weak = None
        self.is_inherently_weak = None
        self.is_stutter_invariant = None
        self.state2edges = {}

    def toJSON(self):
        return {
            "acceptance": self.acc_name,
            "num_sets": self.num_sets,
            "num_states": self.num_states,
            "init_state": self.init_state,
            "atoms": self.atoms,
            "name": self.name,
            "is_deterministic": self.is_deterministic,
            "is_unambiguous": self.is_unambiguous,
            "is_state_based_acc": self.is_state_based_acc,
            "is_terminal": self.is_terminal,
            "is_weak": self.is_weak,
            "is_inherently_weak": self.is_inherently_weak,
            "is_stutter_invariant": self.is_stutter_invariant,
            "state2edges": self.state2edges
        }


def translate(formula, options=None):
    if options is None or options == []:
        options = ["BA", "High", "SBAcc", "Complete"]

    spot_aut = spot.translate(formula, *options)
    bdd_dict = spot_aut.get_dict()

    aut = Automaton()

    aut.acc_name = spot_aut.acc().name()
    aut.acc_cond = str(spot_aut.get_acceptance())
    aut.num_sets = spot_aut.num_sets()
    aut.num_states = spot_aut.num_states()
    aut.init_state = spot_aut.get_init_state_number()
    aut.atoms = {str(ap): bdd_dict.varnum(ap) for ap in spot_aut.ap()}
    aut.name = formula if spot_aut.get_name() is None else spot_aut.get_name()
    aut.is_deterministic = bool(spot_aut.prop_universal() and spot_aut.is_existential())
    aut.is_unambiguous = bool(spot_aut.prop_unambiguous())
    aut.is_state_based_acc = bool(spot_aut.prop_state_acc())
    aut.is_terminal = bool(spot_aut.prop_terminal())
    aut.is_weak = bool(spot_aut.prop_weak())
    aut.is_inherently_weak = bool(spot_aut.prop_inherently_weak())
    aut.is_stutter_invariant = bool(spot_aut.prop_stutter_invariant())

    for s in range(0, spot_aut.num_states()):
        aut.state2edges[s] = dict()
        for t in spot_aut.out(s):
            aut.state2edges[s][t.dst] = [spot.bdd_format_formula(bdd_dict, t.cond), list(t.acc.sets())]
        # aut.state2edges[s]["acc_sets"] = list(aut.state2edges[s]["acc_sets"])
    return aut


if __name__ == '__main__':
    print(translate("GFa & GFb").toJSON())
    json.dumps(translate("GFa & GFb").toJSON())