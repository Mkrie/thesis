import numpy as np
from numpy.linalg import eig
from profile_recovery import ProfileRec


if __name__ == "__main__":
    prof_recovery = ProfileRec("profile_07_05.csv", "profiles_1", "dataset_3_csv")
    rec = prof_recovery.make_data(21)
    values, v = eig(np.matmul(np.matrix(rec[1]), np.transpose(np.matrix(rec[1]))))
    print(values, v)
