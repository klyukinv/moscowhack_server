import numpy as np
import pandas as pd

sym_dis = np.genfromtxt('model/symptom_disease.csv', delimiter=',')
sym_title = pd.read_csv('model/sym_t.csv', index_col='syd')
dis_title = pd.read_csv('model/dia_t.csv', index_col='did')
max_weights = np.load("model/max_weights.npy")

max_valuable = 262  # chest pain. counted "by hands"
max_leaf = 18


class HealthTest:
    def __init__(self, test_id: str = None):
        if test_id is None:
            raise Exception("test id can not be None")
        self.id = test_id
        self.a = np.zeros(sym_dis.shape[0])
        self.asked = np.zeros(sym_dis.shape[0], dtype=bool)
        self.diagnosis = None
        self.last_asked = None
        self.last_positive = None
        self.last_positive_dist = 0
        self.scalars_sym = np.load("model/scalars_sym.npy")
        self.diagnosis = None
        self.last_symptom = None

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
        if best_disease >= 0.15 or np.count_nonzero(self.asked) > 6 and self.last_positive is not None:
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
                return False, max_weights.argsort()[-(np.count_nonzero(self.asked) + 1):][::-1][
                    np.count_nonzero(self.asked) - 1]

    def get_question(self) -> dict:
        try:
            if not np.any(self.asked):
                self.last_symptom = max_valuable
                return {"symptom": max_valuable}
            else:
                result = self.most_suitable()
                if result[0]:
                    self.diagnosis = result[1]
                    return {"diagnosis": self.diagnosis}
                else:
                    self.last_symptom = result[1]
                    return {"symptom": result[1]}
        except Exception as e:
            return {"error": str(e)}

    def scale(self, symptom: int, value: int) -> int:
        return value * max_weights[symptom - 1] / 5

    def get_response(self, value: int) -> dict:
        try:
            if self.last_symptom is None:
                raise Exception()
            symptom = self.last_symptom

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
    try:
        return str(sym_title.loc[sym_index][0]).replace('\u000b', '/')
    except:
        return "NaN"


def int_to_dis(dis_index: int):
    try:
        return str(dis_title.loc[dis_index][0]).replace('\u000b', '/')
    except:
        return "NaN"
