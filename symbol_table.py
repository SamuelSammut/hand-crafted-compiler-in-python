class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes, each scope is a dictionary

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def add(self, identifier, attributes):
        # Check if the variable already exists in the current scope
        if identifier in self.scopes[-1]:
            self.update(identifier, attributes)
        else:
            self.scopes[-1][identifier] = attributes

    def get_variables_in_current_scope(self):
        current_scope_vars = []
        current_scope = self.scopes[-1]
        for identifier, attributes in current_scope.items():
            current_scope_vars.append({
                'identifier': identifier,
                'type': attributes['type'],
                'level': attributes['level'],
                'index': attributes['index']
            })
        return current_scope_vars

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Variable or function '{name}' not declared")

    def lookup_in_current_scope(self, name):
        return name in self.scopes[-1]

    def get_all_variables(self):
        all_vars = []
        for level, scope in enumerate(self.scopes):
            for identifier, attributes in scope.items():
                all_vars.append({
                    'identifier': identifier,
                    'type': attributes['type'],
                    'level': attributes['level'],
                    'index': attributes['index']
                })
        return all_vars

    def update(self, identifier, attributes):
        for scope in reversed(self.scopes):
            if identifier in scope:
                scope[identifier].update(attributes)
                return True
        return False