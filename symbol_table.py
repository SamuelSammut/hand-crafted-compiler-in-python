class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes, each scope is a dictionary

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def add(self, name, info):
        if name in self.scopes[-1]:
            raise Exception(f"Variable or function '{name}' already declared in this scope")
        self.scopes[-1][name] = info

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Variable or function '{name}' not declared")

    def lookup_in_current_scope(self, name):
        return name in self.scopes[-1]
