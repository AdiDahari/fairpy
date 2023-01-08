import os  # for os.system - system commands

import random # for random.randrange - random numbers within a range

import time # for time.time - time measurement

GITHUB_URL = 'https://github.com/AdiDahari/fairpy.git' # URL of the github repository

BRANCHES = ['master', 'cython', 'Multi-Threading'] # branches to compare

SIZES = [4, 10, 100, 200, 500, 1000, 2000] # matrix sizes to compare

def intitalize_enviroment():
    '''
    Initializes the enviroment for the time comparison.
    initializes a virtual enviroment, installs the requirements and installs fairpy enviroment.
    '''
    print('Initializing enviroment...')
    os.system('virtualenv .venv') # creates a virtual enviroment
    os.system('source .venv/bin/activate') # activates the virtual enviroment

    os.system(f'pip install -r requirements.txt') # installs the requirements
    os.system(f'pip install -e .') # installs fairpy

def cython_prepare():
    '''
    Prepares the cython code for the time comparison.
    '''
    print('Preparing cython...')
    os.system('pip install cython') # installs cython
    # compiles the cython code to c code
    os.system('cython -v fairpy/items/cy_compensation_procedure.pyx -o fairpy/items/cy_compensation_procedure.c')

    # compiles the c code to a shared library
    os.system('python3 fairpy/items/setup.py build_ext --inplace')

def switch_branch(branch):
    '''
    Switches to a branch.
    '''
    print(f'Switching to branch: {branch}...')
    os.system(f'git switch -f {branch}')

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

def plot_times(times, branches=BRANCHES, sizes=SIZES):
    '''
    Plots the times of the time comparison.
    '''

    import matplotlib.pyplot as plt

    # plots the times
    for index, branch in enumerate(branches):
        plt.plot(sizes, times[index], label=branch)

    # sets the plot's title, x and y labels and legend
    plt.xlabel('Matrix size')
    plt.ylabel('Time (sec)')
    plt.title('Time comparison')
    
    plt.legend()
    plt.show()

def compare(branches=BRANCHES, sizes=SIZES):
    '''
    Runs the time comparison.
    '''
    times = []  # list of times for each branch

    bidding_matrixes = [create_bidding_matrix(size) for size in sizes] # creates a random bidding matrix



    # intitalize_enviroment() # initializes the enviroment
    # runs the time comparison
    for index, branch in enumerate(branches):

        
        times.append([])
        switch_branch(branch)

        if branch == 'cython':
            cython_prepare()

        print(f'Timimg branch: {branch}...')

        for bidding_matrix in bidding_matrixes:
            from fairpy.items.bidding_for_envy_freeness import bidding_for_envy_freeness
            

            start = time.time()
            bidding_for_envy_freeness(bidding_matrix)
            end = time.time()
            
            times[index].append(end - start)

    switch_branch('master')
    plot_times(times, branches, sizes)

if __name__ == '__main__':
    # compare(branches=['master', 'cython']) # compares the master and cython branches
    # compare(branches=['master', 'Multi-Threading']) # compares the master and Multi-Threading branches
    compare()