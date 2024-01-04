class Symbol:
    """Grammatical unit"""

    def __init__(self, is_terminal: bool, name: str):
        self.is_terminal = is_terminal
        self.name = name

    def __repr__(self):
        if self.is_terminal:
            return f"Terminal : {self.name}"
        return f"Non terminal : {self.name}"
    
    def __hash__(self):
        """Symbols are used as keys in rules, but generated separately by the lexer.
        Different instances of a same token need to hash to the same value"""
        return hash((self.name,self.is_terminal))
    
    def __eq__(self,other):
        return self.is_terminal == other.is_terminal and self.name == other.name


class SimpleLexer:
    def __init__(self, phrase, end_symbol, split_spaces=False):
        self.phrase = phrase
        if split_spaces:
            self.symbols = [
                Symbol(is_terminal=True, name=word) for word in phrase.split()
            ]
        else:
            self.symbols = [Symbol(is_terminal=True, name=word) for word in phrase]

        self.symbols.append(end_symbol)


class Rule:
    """Representation of a grammatical rule for lr parsers"""

    def __init__(self, key: Symbol, items: list, dot_pos: int = 0, lookahead=None):
        self.key = key
        self.items = items
        self.dot_pos = dot_pos

    def __repr__(self):
        """for debugging (not proper usage of __repr__)"""
        name_list = [item.name for item in self.items]
        if self.dot_pos == len(self.items):
            name_list.append("¤")
        else:
            name_list.insert(self.dot_pos, "¤")
        return f"""Rule [{self.key.name} : {" ".join(name_list)}]"""

    def __hash__(self):
        """Rules are generated by different loops during the generation process
        However, we want states (frozen sets of rules) to be keys in the states dict,
        so identical rules should hash to the same number"""
        return hash(tuple([self.key, self.dot_pos] + self.items))

    def __eq__(self, other):
        """Same for eq"""
        return (
            self.key == other.key
            and self.items == other.items
            and self.dot_pos == other.dot_pos
        )

    def shift_dot(self):
        if self.dot_pos > len(self.items):
            return None
        return Rule(self.key, self.items, self.dot_pos + 1)

    def get_active_symbol(self):
        """returns symbol after dot"""
        try:
            return self.items[self.dot_pos]
        except IndexError:
            return None


class GrammaticalNode:
    """Node in the parse tree"""

    def __init__(self, name: Symbol, children=[]):
        """
        Args:
            name (Symbol): grammatical element (symbol) represented by the node
            children (list, optional): children nodes. Defaults to [].
        """
        self.name = name
        self.children = children

    def get_dict_children(self):
        return {self.name: [child.get_dict_children() for child in self.children]}

    def __repr__(self):
        return self.get_dict_children().__repr__()


class ParseTree:
    """Abstract syntax tree generated by the parser"""

    def __init__(self):
        self.node_stack = []
        self.active_node = None

    def shift(self, shift_name):
        """Called when the parser shifts on a terminal
        (on a non terminal, it always happens after a reduce,
        so self.reduce() does everything):
        Active node is pushed to stack and changed to the a new node
        """
        if self.active_node is not None:
            self.node_stack.append(self.active_node)
        self.active_node = GrammaticalNode(name=shift_name)

    def reduce(self, name: Symbol, n_nodes_reduced: int):
        """Called when the parser reduces state(s)
        Pops as many nodes as necessary from the stack,
        and set the new active node as their parent"""
        if n_nodes_reduced > 1:
            children = self.node_stack[-(n_nodes_reduced - 1) :] + [self.active_node]
            self.node_stack = self.node_stack[: -(n_nodes_reduced - 1)]

        else:
            children = [self.active_node]
        self.active_node = GrammaticalNode(name=name, children=children)
