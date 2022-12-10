

class GaussExpert:
    __crits = 0
    __alts = 0
    grades = [[]] * 1
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

                params[i].ds_sigma[j] = pow(params[i].bound_neighb[bn_ind] -
                                        params[i].dominant_value[dv_ind], 2) /
                                        (-std::log(params[i].membership_deg[md_ind]));
                params[i].y[j] = params[i].dominant_value[dv_ind] + pow(-1, j) *
                                 abs(sqrt(-params[i].ds_sigma[j] * std::log(0.05)));

                if (params[i].y[j] > params[i].dominant_value[2])
                    params[i].y[j] = params[i].dominant_value[2];
                if (params[i].y[j] < params[i].dominant_value[0])
                    params[i].y[j] = params[i].dominant_value[0];
            }
        }
    }
#
#         double gaussEstimate(int crit, int alt, int membership) {
#             if (membership == 0) {
#                 if (grades[crit][alt] < params[crit].dominant_value[0])
#                     return 1;
#
#                 if (grades[crit][alt] > params[crit].y[0])
#                     return 0;
#
#                 return exp(-pow(grades[crit][alt]
#                                 - params[crit].dominant_value[0], 2)
#                             / params[crit].ds_sigma[0]);
#             }
#
#             if (membership == 1) {
#                 if (params[crit].y[1] <= grades[crit][alt] &&
#                     grades[crit][alt] >= params[crit].y[2])
#                     return 0;
#
#                 if (grades[crit][alt] > params[crit].y[1] &&
#                     grades[crit][alt] < params[crit].dominant_value[1])
#                     return exp(-pow(grades[crit][alt]
#                                     - params[crit].dominant_value[1], 2)
#                                 / params[crit].ds_sigma[1]);
#
#                 return exp(-pow(grades[crit][alt]
#                                 - params[crit].dominant_value[1], 2)
#                             / params[crit].ds_sigma[2]);
#             }
#
#             if (membership == 2) {
#                 if (grades[crit][alt] <= params[crit].y[3])
#                     return 0;
#
#                 if (grades[crit][alt] >= params[crit].dominant_value[2])
#                     return 1;
#
#                 return exp(-pow(grades[crit][alt]
#                                 - params[crit].dominant_value[2], 2)
#                             / params[crit].ds_sigma[3]);
#             }
#
#             return 0.0;
#         }
#
#         int getEffectMembership(int crit1, int crit2) {
#             if ((crit1 == 0 && crit2 == 0) ||
#                 (crit1 == 0 && crit2 == 1) ||
#                 (crit1 == 1 && crit2 == 0))
#                 return 0;
#             if ((crit1 == 1 && crit2 == 1) ||
#                 (crit1 == 0 && crit2 == 2) ||
#                 (crit1 == 2 && crit2 == 0))
#                 return 1;
#             if ((crit1 == 1 && crit2 == 2) ||
#                 (crit1 == 2 && crit2 == 1) ||
#                 (crit1 == 2 && crit2 == 2))
#                 return 2;
#
#             return 0;
#         }
#     public:
#         GaussExpert(int alts_amount, int crit_amount,
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
#         ~GaussExpert() {
#             delete[] params;
#
#             for (int i = 0; i < alts; i++)
#                 delete[] grades[i];
#
#             delete[] grades;
#         }
#
#         void getBestAlternative() {
#             double ***fuzzy_grades = new double**[crits];
#
#             for (int i = 0; i < crits; i++) {
#                 fuzzy_grades[i] = new double*[alts];
#                 for (int j = 0; j < alts; j++)
#                     fuzzy_grades[i][j] = new double[3];
#             }
#
#
#             for (int i = 0; i < crits; i++) {
#                 std::cout << "\n\nCrit #" << i+1 << ":\n";
#                 for (int j = 0; j < alts; j++) {
#                     for (int k = 0; k < 3; k++) {
#                         fuzzy_grades[i][j][k] = gaussEstimate(i, j, k);
#                         std::cout << std::setw(20) << fuzzy_grades[i][j][k];
#                     }
#                  std::cout << "\n";
#                 }
#             }
#
#
#
#
#             double **accum_table = new double*[alts];
#             std::vector<double> compares[alts][3];
#             int ind = 0;
#             for (int i = 0; i < alts; i++) {
#                 accum_table[i] = new double[3];
#                 for (int c1 = 0; c1 < 3; c1++) {
#                     for (int c2 = 0; c2 < 3; c2++) {
#                         ind = getEffectMembership(c1, c2);
#                         compares[i][ind].push_back(std::min(fuzzy_grades[0][i][c1],
#                                                                fuzzy_grades[1][i][c2]));
#                     }
#                 }
#
#                 for (int t = 0; t < 3; t++) {
#                     accum_table[i][t] = compares[i][t][0];
#                     for (int k = 0; k < compares[i][t].size(); k++)
#                         accum_table[i][t] = std::max(accum_table[i][t], compares[i][t][k]);
#                 }
#
#             }
#
#             std::cout << "Accumulation table:\n";
#             for (int i = 0; i < alts; i++) {
#                 for (int j = 0; j < 3; j++)
#                     std::cout << std::setw(20) << accum_table[i][j];
#                 std::cout << "\n";
#             }
#
#
#             double alts_eff[alts];
#             std::pair<double, int> best_alt = std::make_pair(-1, -1);
#
#             for (int i = 0; i < alts; i++) {
#                 alts_eff[i] = accum_table[i][0] * 0.1 + accum_table[i][1] * 0.5 + accum_table[i][2] * 0.9;
#                 std::cout << "Alt #" << i+1 << ": " << alts_eff[i] << std::endl;
#                 if (alts_eff[i] > best_alt.first)
#                     best_alt = std::make_pair(alts_eff[i], i);
#             }
#
#             std::cout << "\n\nBest alternative is alternative with #" << best_alt.second+1 << "\n\n";
#
#
#             for (int i = 0; i < crits; i++) {
#                 for (int j = 0; j < alts; j++)
#                     delete[] fuzzy_grades[i][j];
#                 delete[] fuzzy_grades[i];
#             }
#
#             delete[] fuzzy_grades;
#         }
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
