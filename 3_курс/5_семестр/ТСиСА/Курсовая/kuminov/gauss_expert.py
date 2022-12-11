import math

class GaussExpert:
    __crits = 2
    __alts = 2
    grades = [[], []]
    gauss_parametrs = [{'dominant_value': [0.0] * 3,
                        'bound_neighb': [0.0] * 2,
                        'membership_deg': [0.0] * 2,
                        'ds_sigma': [0.0] * 4,
                        'y': [0.0] * 4},
                       {'dominant_value': [0.0] * 3,
                        'bound_neighb': [0.0] * 2,
                        'membership_deg': [0.0] * 2,
                        'ds_sigma': [0.0] * 4,
                        'y': [0.0] * 4}
                       ]

    def __init__(self):
        self.__alts = 5

        self.grades = [[0] * self.__alts for i in range(2)]
        print(self.grades)

        for i in range(self.__crits):
            for j in range(3):
                self.gauss_parametrs[i]['dominant_value'][j] = float(input(f'crit#{i} dv{j}: '))
            for j in range(2):
                self.gauss_parametrs[i]['bound_neighb'][j] = float(input(f'crit#{i} bn{j}: '))
            for j in range(2):
                self.gauss_parametrs[i]['membership_deg'][j] = float(input(f'crit#{i} md{j}: '))


        for j in range(self.__crits):
            for i in range(self.__alts):
                self.grades[j][i] = int(input(f'Введите альт#{j} крит#{i}: '))

        print(self.grades)


    #GaussExpert(int alts_amount, int, crit_amount,
    #                     gauss_parametrs *params_, double **grades_) { // АРГУМЕНТ ДОЛЖЕН БЫТЬ КОНСТАНТНЫМ!!!
    #             crits = crit_amount;
    #             alts = alts_amount;
    #             params = std::move(params_);
    #             grades = std::move(grades_);
    #
    #             calculateParams();
    #
    #             for (int i = 0; i < crits; i++) {
    #                 for (int j = 0; j < 4; j++) {
    #                     std::cout << "Sigma: " << params[i].ds_sigma[j] << std::endl;
    #                 }
    #                 for (int j = 0; j < 4; j++) {
    #                     std::cout << "Y: " << params[i].y[j] << std::endl;
    #                 }
    #             }
    #         }

    def calculateParams(self):
        for i in range(self.__crits):
            dv_ind, bn_ind, md_ind = 0, 0, 0
            for j in range(4):
                match j:
                    case 1:
                        dv_ind = 1
                    case 2:
                        bn_ind = 1
                        md_ind = 1
                    case 3:
                        dv_ind = 2
                self.gauss_parametrs[i]['ds_sigma'][j] = ((self.gauss_parametrs[i]['bound_neighb'][bn_ind] -
                                                          self.gauss_parametrs[i]['dominant_value'][dv_ind]) ** 2) \
                                                          / (-math.log(self.gauss_parametrs[i]['membership_deg'][md_ind]))

                self.gauss_parametrs[i]['y'][j] = self.gauss_parametrs[i]['dominant_value'][dv_ind] + (-1) ** j * \
                                                  math.fabs((-self.gauss_parametrs[i]['ds_sigma'][j] * math.log(0.05)) ** 0.5)

                if self.gauss_parametrs[i]['y'][j] > self.gauss_parametrs[i]['dominant_value'][2]:
                    self.gauss_parametrs[i]['y'][j] = self.gauss_parametrs[i]['dominant_value'][2]

                if self.gauss_parametrs[i]['y'][j] < self.gauss_parametrs[i]['dominant_value'][0]:
                    self.gauss_parametrs[i]['y'][j] = self.gauss_parametrs[i]['dominant_value'][0]

    def gaussEstimate(self, crit, alt, membership):
        if membership == 0:
            if self.grades[crit][alt] < self.gauss_parametrs[crit]['dominant_value'][0]:
                return 1

            if self.grades[crit][alt] > self.gauss_parametrs[crit]['y'][0]:
                return 0

            return math.exp(-((self.grades[crit][alt] - self.gauss_parametrs[crit]['dominant_value'][0]) ** 2)
                            / self.gauss_parametrs[crit]['ds_sigma'][0])

        if membership == 1:
            if (self.gauss_parametrs[crit]['y'][1] <= self.grades[crit][alt]) and \
               (self.grades[crit][alt] >= self.gauss_parametrs[crit]['y'][2]):
                return 0;

            if (self.grades[crit][alt] > self.gauss_parametrs[crit]['y'][1]) and \
                (self.grades[crit][alt] < self.gauss_parametrs[crit]['dominant_value'][1]):
                return math.exp(-((self.grades[crit][alt]
                                    - self.gauss_parametrs[crit]['dominant_value'][1]) ** 2)
                                / self.gauss_parametrs[crit]['ds_sigma'][1])

            return math.exp(-((self.grades[crit][alt]
                                - self.gauss_parametrs[crit]['dominant_value'][1]) ** 2)
                            / self.gauss_parametrs[crit]['ds_sigma'][2]);

        if membership == 2:
            if self.grades[crit][alt] <= self.gauss_parametrs[crit]['y'][3]:
                return 0

            if self.grades[crit][alt] >= self.gauss_parametrs[crit]['dominant_value'][2]:
                return 1

            return math.exp(-((self.grades[crit][alt]
                                - self.gauss_parametrs[crit]['dominant_value'][2]) ** 2)
                            / self.gauss_parametrs[crit]['ds_sigma'][3])
        return 0.0

    def getEffectMembership(self, crit1, crit2):
        if ((crit1 == 0 and crit2 == 0) or
            (crit1 == 0 and crit2 == 1) or
            (crit1 == 1 and crit2 == 0)):
            return 0

        if ((crit1 == 1 and crit2 == 1) or
            (crit1 == 0 and crit2 == 2) or
            (crit1 == 2 and crit2 == 0)):
            return 1

        if ((crit1 == 1 and crit2 == 2) or
            (crit1 == 2 and crit2 == 1) or
            (crit1 == 2 and crit2 == 2)):
            return 2

        return 0

    def getBestAlternative(self):
        #self.grades = [[0] * self.__alts for i in range(2)]
        fuzzy_grades = [[[0 for k in range(3)] for j in range(self.__alts)] for i in range(self.__crits)]
        print(fuzzy_grades)
        #double ***fuzzy_grades = new double**[crits];

       # for i in range(self.__crits):
       #     fuzzy_grades[i] = [] * self.__alts
       #     for j in range(self.__alts):
       #         fuzzy_grades[i][j] = [] * 3


        for i in range(self.__crits):
            #std::cout << "\n\nCrit #" << i+1 << ":\n";
            for j in range(self.__alts):
                for k in range(3):
                    fuzzy_grades[i][j][k] = self.gaussEstimate(i, j, k);
                    #std::cout << std::setw(20) << fuzzy_grades[i][j][k];
                #}
                #std::cout << "\n";
            #}
        #}
        print(fuzzy_grades)


        accum_table = [[0] * 3 for i in range(self.__alts)]
        print("accum_table:", accum_table)
        #fuzzy_grades = [[[0 for k in range(3)] for j in range(self.__alts)] for i in range(self.__crits)]
        compares = [[[0] for k in range(3)] for j in range(self.__alts)]
        print("compares: ", compares)
        #double **accum_table = new double*[alts];
        #std::vector<double> compares[alts][3];
        ind = 0

        for i in range(self.__alts):
            for c1 in range(3):
                for c2 in range(3):
                    ind = self.getEffectMembership(c1, c2);
                    compares[i][ind].append(min(fuzzy_grades[0][i][c1], fuzzy_grades[1][i][c2]))

            for t in range(3):
                accum_table[i][t] = compares[i][t][0];
                for k in range(len(compares[i][t])):
                    accum_table[i][t] = max(accum_table[i][t], compares[i][t][k])

            # std::cout << "Accumulation table:\n";
            # for (int i = 0; i < alts; i++) {
            #     for (int j = 0; j < 3; j++)
            #         std::cout << std::setw(20) << accum_table[i][j];
            #     std::cout << "\n";
            # }
        print(accum_table)

        alts_eff = [0 for i in range(self.__alts)]
            #double alts_eff[alts];
        best_alt = [0.0, 0]
            #std::pair<double, int> best_alt = std::make_pair(-1, -1);

        for i in range(self.__alts):
            alts_eff[i] = accum_table[i][0] * 0.1 + accum_table[i][1] * 0.5 + accum_table[i][2] * 0.9;
                #std::cout << "Alt #" << i+1 << ": " << alts_eff[i] << std::endl;
            if alts_eff[i] > best_alt[0]:
                best_alt = [alts_eff[i], i]


        print("alts effectivness: ", alts_eff)
            #std::cout << "\n\nBest alternative is alternative with #" << best_alt.second+1 << "\n\n";
        print("Best alt#", best_alt[1]+1)
#
#
# };
#
# int main()
# {
#     /*
#      *Программа не должна иметь ограничений на количество вводимых альтернатив,
#       критериев, состояний среды и прочих основных детерминант задачи
#      */
#
#     int alt_amount = 2, crit_amount = 2;
#     //system("chcp 1251 > nul");
#     std::cout << "Input alternatives amount: ";
#     std::cin >> alt_amount;
#
#     std::cout << "Amount:" << alt_amount << std::endl;
#
#     //std::cout << "Input criteria amount: ";
#     //std::cin >> crit_amount;
#
#     std::cout << "Criteria amount:" << crit_amount << std::endl;
#
#     gauss_parametrs *params = new gauss_parametrs[crit_amount];
#
#    for (int i = 0; i < crit_amount;i++) {
#        for (int j = 0; j < 3; j++) {
#            std::cout << "Input dominant  value #" << j+1 << ": ";
#            std::cin >> params[i].dominant_value[j];
#        }
#
#        for (int j = 0; j < 2; j++) {
#            std::cout << "Input boundary value of neighbour term #" << j+1 << ": ";
#            std::cin >> params[i].bound_neighb[j];
#        }
#
#        std::cout << "Input membership degree: ";
#        std::cin >> params[i].membership_deg[0];
#        params[i].membership_deg[1] = 1 - params[i].membership_deg[0];
#
#    }
#
#     double **grades = new double* [crit_amount];
#
#     for (int i = 0; i < crit_amount; i++) {
#         grades[i] = new double[alt_amount];
#         for (int j = 0; j < alt_amount; j++) {
#             std::cout << "Input grade of crit#" << i+1 << " alt #" << j+1 << ": ";
#             std::cin >> grades[i][j];
#         }
#     }
#
#     GaussExpert ge = GaussExpert(alt_amount, crit_amount, params, grades);
#
#     ge.getBestAlternative();
#     //delete[] params;
#
#    system("pause");
#     return 0;
# }


ge = GaussExpert()
ge.calculateParams()
ge.getBestAlternative()