import numpy as np
from gekko import GEKKO
from scipy.stats import chi2


class DR:
    """
        - Data Reconciliation
        - Gross Error Detection
        - Gross Error Identification
        - Return reconciliation of x

        * Example
            dr = DR()
            x_recon = mydr.reconciliate(jacobian, measured_x, sigma_from_data)
    """

    def __init__(self):
        self.show_result = True

    def _initialize_x(self, m, text, lb_=0, ub_=10000):
        for i in range(self.xnum):
            globals()[text + '{}'.format(i + 1)] = m.Var(lb=lb_, ub=ub_)
            globals()[text + '{}'.format(i + 1)].value = self.measured_x[i]

    def _set_consts(self, m, text, eq):
        for eqs in range(self.eqnum):
            m.Equation(sum([globals()[text + '{}'.format(i + 1)] *
                            self.jacobian[eqs][0 + i] for i in range(self.xnum)]) == eq)

    def _copy_x(self, text):
        copied_x = []
        for i in range(self.xnum):
            copied_x.append(globals()[text + '{}'.format(i + 1)])
        copied_x = np.array(copied_x)
        return copied_x

    def _solve(self, m, obj_func, show=True):
        m.Obj(obj_func)
        m.options.IMODE = 3  # steady state optimization
        if show:
            m.solve(disp=self.show_result)
        else:
            m.solve(disp=show)

    def _calculate_gamma(self, xs1, xs2):
        gamma = 0
        for i in range(self.xnum):
            gamma += ((xs1[i] - xs2[i]) / self.sigma_from_data[i]) ** 2
        gamma = float(gamma)
        return gamma

    def reconciliate(self, jacobian, measured_x, sigma_from_data):
        """
        :parameter
            jacobian: list
            measured_x: list
            sigma_from_data: Numpy Array
        :return:
            reconcil_x = Numpy Array
        """
        self.xnum = len(measured_x)
        self.eqnum = len(jacobian)

        self.jacobian = jacobian
        self.measured_x = measured_x
        # 예제를 위한 값으로 설정값으로 지정
        self.sigma_from_data = np.array(sigma_from_data)
        self.chi_square_1 = chi2.ppf(0.95, self.xnum - 1)
        self.chi_square_2 = chi2.ppf(0.95, self.xnum - 2)

        # Initialize Model
        m = GEKKO()
        text1 = 'x'

        # define parameter
        eq = m.Param(value=0)

        # initialize variables, initial values
        self._initialize_x(m, text1)

        # Equations
        self._set_consts(m, text1, eq)

        # Define the objective function
        obj_func = sum(
            [((globals()['x{}'.format(i + 1)] - self.measured_x[i]) / self.sigma_from_data[i]) ** 2 for i in
             range(self.xnum)])

        # Optimize
        self._solve(m, obj_func)
        reconcil_x = self._copy_x(text1)

        if self.show_result:
            print('Results of Fault Detect')
            for i in range(self.xnum):
                print(f'x{i + 1}:\t{round(float(reconcil_x[i]),3)}')

        # Detection
        gamma = self._calculate_gamma(reconcil_x, self.measured_x)
        if gamma > self.chi_square_1:
            print(
                f"Gross Error 검정치({round(gamma, 2)}) > 카이제곱 기준치({round(self.chi_square_1, 2)}): Gross Error 존재.")
            self.identify()
            reconcil_x = self.reconil_x2

        return reconcil_x

    def identify(self):
        text2 = 'id'
        for k in range(self.xnum):
            # Initialize Model
            m2 = GEKKO()
            eq2 = m2.Param(value=0)

            # initialize variables, initial values
            self._initialize_x(m2, text2)

            # Equations
            self._set_consts(m2, text2, eq2)

            # Define the objective function
            obj_func2 = sum(
                [((globals()['id{}'.format(i + 1)] - self.measured_x[i]) / self.sigma_from_data[i]) ** 2 for i in
                 range(self.xnum)])
            term = ((globals()['id{}'.format(k + 1)] - self.measured_x[k]) / self.sigma_from_data[k]) ** 2

            # Optimize
            self._solve(m2, obj_func2 - term, show=False)
            reconcil_x2 = self._copy_x(text2)

            # Identification
            term_value = (
                                 (reconcil_x2[k] - self.measured_x[k]) / self.sigma_from_data[k]) ** 2
            gamma_id = self._calculate_gamma(reconcil_x2, self.measured_x)
            gamma_id = float(gamma_id - term_value)
            print(f"[{k + 1}번째 변수 식별 중] 검정치:\t{gamma_id}")

            if gamma_id < self.chi_square_2:
                print(f"x{k + 1}번째가 Gross Error를 갖고 있음")

                if self.show_result:
                    print('Results of Fault Identification')
                    for i in range(self.xnum):
                        print(f'x{i + 1}:\t{round(float(reconcil_x2[i]),3)}')
                    print(reconcil_x2)
                    self.reconil_x2 = reconcil_x2
                    break





if __name__ == "__main__":
    # 참고자료: DR_Example_v1.xlsm
    dr = DR()
    # 참고자료 내 Jacobian 행렬
    jacobian = [[1, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, -1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, -1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, -1]]
    # 참고자료 내 계측값(현재값)
    measured_x = [100, 150, 80, 250, 330.0, 250, 110, 100, 80, 60, 40, 40, 50, 60, 90, 150]
    # 참고자료 내 표준편차
    sigma = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    # Data Reconciliation 결과:
    # Fault Detection > Identify 까지 진행된 결과가 출력됨.
    x_recon = dr.reconciliate(jacobian, measured_x, sigma_from_data=sigma)