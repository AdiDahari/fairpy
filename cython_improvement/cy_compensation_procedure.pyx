import numpy as np
cimport numpy as np


#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION


cpdef compensation_procedure(np.ndarray[long, ndim=2] assessment_matrix, int MC, int num_of_agents):
    cdef int players = len(assessment_matrix) - 1
    cdef int i
    compansations = np.empty((players,))
    result = np.ndarray(shape=(players, players)) 

    if all([all([x <= assessment_matrix[player][player] for x in assessment_matrix[player]]) for player in range(players)]):
        result = np.empty_like(assessment_matrix)
        np.copyto(result, assessment_matrix)
        result[-1, :] += int((MC - sum(assessment_matrix[-1, :])) / num_of_agents)
        return result
    else:
        result = np.empty_like(assessment_matrix)
        np.copyto(result, assessment_matrix)
        for i in range(players):
            compansations[i] = max(assessment_matrix[i]) - assessment_matrix[i][i] if any([x > assessment_matrix[i][i] for x in assessment_matrix[i]]) else 0
        for i in range(players):
            result[:, i] += int(compansations[i])
        if MC and sum(result[-1, :]) > MC:
            raise Exception('No fair division exists for the given bidding matrix')
        return compensation_procedure(result, MC, num_of_agents)
