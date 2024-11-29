from graphviz import Digraph

class DFA:
    def __init__(self, K, Q, F, S, Z):
        self.K = K  # 状态集合
        self.Q = Q  # 输入符号集
        self.F = F  # 转移函数
        self.S = S  # 初始状态
        self.Z = Z  # 接受状态集

    def minimize(self):
        P = [set(self.Z), set(self.K) - set(self.Z)]
        W = [set(self.Z)]

        while W:
            A = W.pop()
            for c in self.Q:
                X = {s for s in self.K if self.F.get(s, {}).get(c) in A}
                for Y in P[:]:
                    intersection = X & Y
                    difference = Y - X
                    if intersection and difference:
                        P.remove(Y)
                        P.append(intersection)
                        P.append(difference)
                        if Y in W:
                            W.remove(Y)
                            W.append(intersection)
                            W.append(difference)
                        else:
                            if len(intersection) <= len(difference):
                                W.append(intersection)
                            else:
                                W.append(difference)

        new_states = sorted({frozenset(s) for s in P}, key=lambda x: min(self.K.index(state) for state in x))
        state_map = {state: str(i) for i, state in enumerate(new_states)}
        new_start_state = state_map[next(s for s in new_states if self.S[0] in s)]
        new_accept_states = [state_map[s] for s in new_states if s & set(self.Z)]
        new_transition_function = {}
        for s in new_states:
            for c in self.Q:
                target = self.F.get(next(iter(s)), {}).get(c)
                if target:
                    new_target = next(ns for ns in new_states if target in ns)
                    new_transition_function[state_map[s], c] = state_map[new_target]

        new_K = tuple(state_map.values())
        new_F = {state: {c: new_transition_function[state, c] for c in self.Q if (state, c) in new_transition_function} for state in new_K}
        new_S = (new_start_state,)
        new_Z = tuple(new_accept_states)

        return DFA(new_K, self.Q, new_F, new_S, new_Z)

    def show(self):
        print(f"K: {self.K}")
        print(f"Q: {self.Q}")
        print(f"F: {self.F}")
        print(f"S: {self.S}")
        print(f"Z: {self.Z}")

    def Draw(self, filename):
        dot = Digraph(comment='DFA State')
        dot.attr(rankdir='LR')

        for state in self.K:
            shape = 'doublecircle' if state in self.Z else 'circle'
            dot.node(state, shape=shape)

        dot.node('start', shape='none')
        dot.edge('start', self.S[0])

        for from_state, transitions in self.F.items():
            for input_symbol, to_state in transitions.items():
                dot.edge(from_state, to_state, label=input_symbol)

        dot.render(filename, view=True, format='pdf')

def test():
    K = ('0', '1', '2', '3')
    Q = ('0', '1')
    F = {
        '0': {'0': '1', '1': '2'},
        '1': {'0': '1', '1': '3'},
        '2': {'0': '3', '1': '1'},
        '3': {'0': '3', '1': '3'},
    }
    S = ('0',)
    Z = ('3',)
    D1 = DFA(K, Q, F, S, Z)
    D2 = D1.minimize()
    D1.Draw('original_dfa_state')
    D2.Draw('minimized_dfa_state')

if __name__ == "__main__":
    test()