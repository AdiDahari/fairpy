import os  # for os.system - system commands

import random # for random.randrange - random numbers within a range

import time # for time.time - time measurement



# def cython_prepare():
#     '''
#     Prepares the cython code for the time comparison.
#     '''
#     print('Preparing cython...')
#     # compiles the cython code to c code
#     os.system('cython cython_improvement/cy_compensation_procedure.pyx -o cython_improvement/cy_compensation_procedure.c')

#     # compiles the c code to a shared library
#     os.system('python cython_improvement/setup.py build_ext --inplace cython_improvement/')

def prepare_cython(): 
    print('Preparing cython...')
    # compiles the cython code to c code
    os.system('cython -v cython_improvement/cy_compensation_procedure.pyx')

    # compiles the c code to a shared library
    os.system('python cython_improvement/setup.py build_ext --inplace')

prepare_cython()

from fairpy.items.bidding_for_envy_freeness import bidding_for_envy_freeness as base

from cython_improvement.bidding_for_envy_freeness import bidding_for_envy_freeness as cython_improvement

from multithreading_improvement.bidding_for_envy_freeness import bidding_for_envy_freeness as multithreading_improvement

GITHUB_URL = 'https://github.com/AdiDahari/fairpy.git' # URL of the github repository

IMPLEMENTATIONS = ['base', 'cython', 'multithreading'] # branches to compare

SIZES = [4, 10, 100, 200, 500] # matrix sizes to compare

def create_bidding_matrix(n: int):
    '''
    Creates a random bidding matrix of size n x n.
    '''
    print(f'Creating random bidding matrix of size {n}x{n}...')
    bidding_matrix = list()
    
    # creates a random bidding matrix
    for _ in range(n): 
        row = list()
        for _ in range(n):
            row.append(random.randrange(0, 60, 2))
        bidding_matrix.append(row)
    
    return bidding_matrix

def plot_times(times, implementations = ['base', 'cython', 'multithreading'], sizes=SIZES):
    '''
    Plots the times of the time comparison.
    '''

    import matplotlib.pyplot as plt

    # plots the times
    for key in implementations:
        plt.plot(sizes, times[key], label=key)

    # sets the plot's title, x and y labels and legend
    plt.xlabel('Matrix size')
    plt.ylabel('Time (sec)')
    plt.title('Time comparison')
    
    plt.legend()
    plt.show()

def compare(implementations=IMPLEMENTATIONS, sizes=SIZES):
    '''
    Runs the time comparison.
    '''
    times = {}  # list of times for each branch

    bidding_matrixes = [create_bidding_matrix(size) for size in sizes] # creates a random bidding matrix



    # intitalize_enviroment() # initializes the enviroment
    # runs the time comparison

    print(implementations)
    for key in implementations:

        
        times.setdefault(key, [])

        print(f'Timimg implementation: {key}...')

        for bidding_matrix in bidding_matrixes:


            start = time.time()
            if key == 'base':
                base(bidding_matrix=bidding_matrix)
            elif key == 'multithreading':
                multithreading_improvement(bidding_matrix=bidding_matrix)
            else:
                cython_improvement(bidding_matrix=bidding_matrix)
            end = time.time()
            
            times[key].append(end - start)

    plot_times(times, implementations=implementations, sizes=sizes)

if __name__ == '__main__':
    # compare(implementations=['base', 'cython']) # compares the base and cython implementations
    # compare(implementations=['base', 'multuthreading']) # compares the base and cython implementations
    # compare(implementations=['cython', 'multuthreading']) # compares the base and cython implementations
    compare()