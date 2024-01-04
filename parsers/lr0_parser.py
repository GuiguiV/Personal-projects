from itertools import count
from lr_parsers_utils import Symbol, ParseTree, Rule, SimpleLexer


class LR0TableGenerator:
    def __init__(self, rules: list, start_symbol):
        """

        :param rules: grammar in the form of a list of dicts with key, value for production rules.
        It is converted into a list of Rule objects.
        """
        self.rules = []
        self.start_symbol = start_symbol
        for rule in rules:
            key, items = list(rule.items())[0]
            self.rules.append(Rule(key, items))

        self.sparse_shift_table = {}
        self.sparse_reduce_table = {}
        self.state_id_counter = count()
        self.states = dict()
        start_symbol_closure = frozenset(self.get_closure(start_symbol))
        start_closure_id = next(self.state_id_counter)
        self.states[start_symbol_closure] = start_closure_id
        self.get_all_states(start_symbol_closure, start_closure_id)

    def get_all_states(self, starting_state, starting_id):
        next_symbols = set()
        for rule in starting_state:
            symbol = rule.get_active_symbol()
            if symbol is not None:
                next_symbols.add(symbol)

        for symbol in next_symbols:
            new_state = self.shift_from_state(starting_state, symbol)
            if len(new_state) == 0:  # no new state here
                continue

            if new_state not in self.states:  # no duplicate states
                # store new state (key is tuple of Rules)
                new_state_id = next(self.state_id_counter)
                self.states[new_state] = new_state_id

                reduction_rule = self.check_reduction(new_state)

                if reduction_rule is None:  # recursion
                    self.get_all_states(new_state, new_state_id)  # recursion

                else:  # reducible state : no need for recursion, we mark it as reduce immediately
                    # this makes reduction the priority operation, even if other rules indicated to shift

                    self.sparse_reduce_table[new_state_id] = {
                        symbol: (reduction_rule.key, len(reduction_rule.items))
                    }

            else:
                new_state_id = self.states[new_state]

            if starting_id in self.sparse_shift_table:  # dict of dict (sparse matrix)
                self.sparse_shift_table[starting_id][symbol] = new_state_id
            else:
                self.sparse_shift_table[starting_id] = {symbol: new_state_id}

    def display_states(self):
        for state, id in self.states.items():
            print(f"State number {id}")
            print(state)

    def check_reduction(self, state):
        """Check if the current state has a rule that needs to be reduced"""
        for rule in state:
            if rule.get_active_symbol() is None:
                return rule

        return None

    def get_closure(self, symbol: Symbol, already_processed=[]):
        """
        Returns all the rules, with properly set dots, that the symbol can produce (recursive).
        :param symbol: The symbol involved
        :param already_processed: protects against infinite recursion
        :return:
        """
        if symbol.is_terminal:
            return []

        closure = set()
        for rule in self.rules:
            if rule.key == symbol:
                closure.add(rule)
                sub_symbol = rule.items[0]
                processed = already_processed + [symbol]

                if sub_symbol not in processed:
                    sub_closure = self.get_closure(
                        sub_symbol, already_processed=processed
                    )
                    closure.update(sub_closure)

        return closure

    def get_possible_terminals_from_state(self, state: set):
        terminals = set()
        for rule in state:
            symbol = rule.get_active_symbol()
            if symbol.is_terminal:
                terminals.add(symbol)
        return terminals

    def shift_from_state(self, state, symbol) -> frozenset:
        new_state = set()
        for rule in state:
            if rule.get_active_symbol() == symbol:
                shifted_rule = rule.shift_dot()
                if shifted_rule is not None:
                    new_state.add(shifted_rule)
                    new_active_symbol = shifted_rule.get_active_symbol()
                    if new_active_symbol is not None:
                        new_state.update(self.get_closure(new_active_symbol))

        return frozenset(new_state)


class LR0Parser:
    def __init__(self, grammar, start_symbol):
        self.generator = LR0TableGenerator(grammar, start_symbol=start_symbol)
        self.reduce_table = self.generator.sparse_reduce_table
        self.shift_table = self.generator.sparse_shift_table
        self.tree = ParseTree()

    def parse(self, phrase: list):
        """Phrase is a list of symbols """
        self.state_stack = [0]
        phrase = phrase[::]
        self.current_symbol = phrase.pop(0)
        self.tree = ParseTree()

        while self._shift():
            if not self._reduce():
                if len(phrase) == 0:
                    break
                self.current_symbol = phrase.pop(0)

        return self.tree.active_node.get_dict_children()

    def _shift(self):
        """Shift if possible"""

        current_state = self.state_stack[-1]
        symbol = self.current_symbol

        if current_state == 0 and symbol == self.generator.start_symbol:
            return False

        if (
            current_state in self.shift_table
            and symbol in self.shift_table[current_state]
        ):
            new_state = self.shift_table[current_state][symbol]
            self.state_stack.append(new_state)

            if symbol.is_terminal:
                self.tree.shift(symbol)

            return True

        raise NameError(f"Unexpected symbol : {symbol}")

    def _reduce(self):
        """Reduce if possible"""

        current_state = self.state_stack[-1]
        symbol = self.current_symbol

        if (
            current_state in self.reduce_table
            and symbol in self.reduce_table[current_state]
        ):
            reduce_to, n_symbol_reduced = self.reduce_table[current_state][symbol]
            self.state_stack = self.state_stack[:-n_symbol_reduced]
            self.current_symbol = reduce_to
            self.tree.reduce(reduce_to, n_nodes_reduced=n_symbol_reduced)
            return True

        return False


# symbols for playing around, and a grammar
S = Symbol(False, "S")
A = Symbol(False, "A")
B = Symbol(False, "B")
V = Symbol(False,"V")
x = Symbol(True, "x")
y = Symbol(True, "y")
plus = Symbol(True, "+")
times = Symbol(True, "*")

eof = Symbol(True, "eof")

gram = [{S: [B, eof]}, {B: [B, A]}, {A: [y]}, {B: [x]}]


if __name__ == "__main__":

    parser = LR0Parser(gram, start_symbol=S)
    print(f"Grammar : {gram}")
    
    while True:
        phrase = input("Try it : ")
        symbols_phrase = SimpleLexer(phrase=phrase,end_symbol=eof,split_spaces=False).symbols
        print(symbols_phrase)
        print(parser.parse(symbols_phrase))
