import numpy as np
import pandas as pd

sym_dis = np.genfromtxt('symptom_disease.csv', delimiter=',')
sym_title = pd.read_csv('sym_t.csv')
dis_title = pd.read_csv('dia_t.csv', index_col='did')
max_weights = np.load("max_weights.npy")

max_valuable = 262  # chest pain. counted "by hands"
max_leaf = 18


class HealthTest:
    def __init__(self):
        self.a = np.zeros(sym_dis.shape[0])
        self.asked = np.zeros(sym_dis.shape[0], dtype=bool)
        self.diagnosis = None
        self.last_asked = None
        self.last_positive = None
        self.last_positive_dist = 0
        self.scalars_sym = np.load("scalars_sym.npy")

    def top_disease_cos(self):
        best_dis = -1
        best_dis_index = -1
        for i in range(sym_dis.shape[1]):
            b = sym_dis[:, i]
            der = (np.linalg.norm(self.a) * np.linalg.norm(b))
            if der != 0:
                dist = (self.a @ b) / der
                if dist > best_dis:
                    best_dis = dist
                    best_dis_index = i
        return best_dis, best_dis_index

    def most_suitable(self) -> (bool, int):
        sym_i = -1
        best_disease, bd_index = self.top_disease_cos()
        if best_disease >= 0.15 or np.count_nonzero(self.asked) > 6:
            return True, bd_index
        if self.a[self.last_asked] > 0:
            row = self.scalars_sym[:, self.last_asked + 1]
            index = np.unravel_index(row.argmax(), row.shape)[0]
            self.scalars_sym[self.last_asked + 1, :] = np.zeros(self.scalars_sym[self.last_asked + 1, :].shape)
            self.scalars_sym[:, self.last_asked + 1] = np.zeros(self.scalars_sym[:, self.last_asked + 1].shape)
            return False, index
        else:
            if self.last_positive is not None:
                return False, self.scalars_sym[self.last_positive, :].argsort()[-(self.last_positive_dist + 1):][::-1][
                    self.last_positive_dist - 1]
            else:
                nz = np.count_nonzero(self.asked)
                return False, max_weights.argsort()[-(nz + 1):][::-1][nz - 1]

    def get_question(self) -> dict:
        try:
            if not np.any(self.asked):
                return {"symptom": max_valuable}
            else:
                result = self.most_suitable()
                if result[0]:
                    self.diagnosis = result[1]
                    return {"diagnosis": self.diagnosis}
                else:
                    return {"symptom": result[1]}
        except Exception as e:
            return {"error": str(e)}

    def scale(self, symptom: int, value: int) -> int:
        return value * max_weights[symptom - 1] / 5

    def get_response(self, symptom: int, value: int) -> dict:
        try:
            if self.diagnosis is not None:
                return {"diagnosis": dis_title.loc[self.diagnosis]['diagnose'],
                        "doctor": dis_title.loc[self.diagnosis]['doctor']}
            else:
                self.last_asked = symptom - 1
                self.a[symptom - 1] = self.scale(symptom, value)
                if value > 0:
                    self.last_positive = symptom - 1
                    self.last_positive_dist = 0
                else:
                    self.last_positive_dist += 1
                self.asked[symptom - 1] = True
                return {"vector": self.a}
        except Exception as e:
            return {"error": str(e)}

    def top_popular_symptoms(self):
        n = np.count_nonzero(self.asked)
        return max_weights.argsort()[-n + 1][::-1][n]


def int_to_sym(sym_index: int):
    return sym_title.loc[sym_index]
