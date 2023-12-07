import math
from typing import Any, Union
from dataclasses import dataclass

import numpy as np
from numpy import dtype, floating, ndarray

from src.direct_measurements import DirectMeasurements
from src.profile_recovery import ProfileRec


@dataclass(frozen=True)
class Bayesian(object):
    """Class for solving inverse problems using the optimal statistical estimation method"""

    profile: str
    profile_path: str
    dataset_name: str = "dataset_2_csv"

    @staticmethod
    def correlation_function(
        f_0: ndarray[Any, dtype],
        h: ndarray[Any, dtype[floating]],
        h_0: int,
        n: int,
    ) -> ndarray[Any, dtype[floating]]:
        """Сorrelation function calculation."""
        return np.array(
            [
                [
                    0.25
                    * f_0[j]
                    * f_0[i]
                    * (math.e ** (-((h[i] - h[j]) ** 2) / h_0))
                    for j in range(n)
                ]
                for i in range(n)
            ],
        )

    @staticmethod
    def priori_profile(n: int, factor: float) -> ndarray[Any, dtype]:
        """Priori profile calculation."""
        return np.array(n * [factor])

    def assessment(
        self,
        sigma_1: float,
        n: int,
        sigma_2: float,
        factor: float,
        h_0: int = 200,
    ) -> tuple[
        ndarray[Any, dtype[floating]],
        tuple[Union[ndarray[Any, dtype[floating]], Any]],
    ]:
        """Calculation of the optimal statistical estimate."""
        # get data: xi == \xi, M == M(matrix(21x21)), h == heights
        gotten_data: (
            tuple[
                ndarray[Any, dtype[floating]],
                ndarray[Any, dtype[floating]],
                ndarray[Any, dtype[floating]],
            ]
        ) = self.get_data(sigma_1=sigma_1, n=n)
        xi: ndarray[Any, dtype[floating]] = gotten_data[0]
        m: ndarray[Any, dtype[floating]] = gotten_data[1]
        f_0: ndarray[Any, dtype] = Bayesian.priori_profile(n=n, factor=factor)
        f = Bayesian.correlation_function(
            f_0=f_0, h=gotten_data[2], h_0=h_0, n=n
        )
        return gotten_data[2], (
            f
            @ m.T
            @ np.linalg.inv(
                m @ f @ m.T + (sigma_2 * 10**15) ** 2 * np.eye(n)
            )
            @ (xi - m @ f_0)
            + f_0,
        )

    def get_data(
        self, sigma_1: float, n: int = 21
    ) -> tuple[
        ndarray[Any, dtype[floating]],
        ndarray[Any, dtype[floating]],
        ndarray[Any, dtype[floating]],
    ]:
        """Get data: xi == \\xi, M == M(matrix(21x21)), h == heights."""
        dir_meas: DirectMeasurements = DirectMeasurements(
            profile=self.profile,
            sigma=sigma_1,
            dataset_name=self.dataset_name,
            dir_profiles_name=self.profile_path,
        )
        prof_recovery: ProfileRec = ProfileRec(
            profile=self.profile,
            profile_path=self.profile_path,
            dataset_name=self.dataset_name,
        )
        data: tuple[
            Union[tuple, tuple[Union[float, Any], ...]], list[tuple]
        ] = prof_recovery.make_data(n=n)
        return (
            np.array(
                [x[1] for x in dir_meas.direct_measurements_for_profile()]
            ),
            np.array(data[1]),
            np.array(data[0]),
        )


if __name__ == "__main__":
    e = Bayesian(
        profile="threemod_1.csv",
        profile_path="profiles_2",
        dataset_name="dataset_2_csv",
    )
    h_out, out = e.assessment(sigma_1=1, n=21, sigma_2=0.1, factor=10**13)
    print(h_out, out)
    h_out, out = e.assessment(sigma_1=1, n=21, sigma_2=0.1, factor=10 ** 13)
    print(h_out, out)
