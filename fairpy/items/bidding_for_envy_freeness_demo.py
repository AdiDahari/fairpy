import random
import time
from fairpy.items.bidding_for_envy_freeness import BiddingForEnvyFreeness, bidding_for_envy_freeness

from fairpy.items.valuations import ValuationMatrix


def create_bidding_matrix(n: int) -> ValuationMatrix:
    bidding_matrix = list()
    
    for _ in range(n):
        row = list()
        for _ in range(n):
            row.append(random.randrange(0, 60, 5))
        bidding_matrix.append(row)
        
    return ValuationMatrix(bidding_matrix)
    
    
if __name__ == '__main__':
    sizes = [4, 10, 100, 200, 500, 1000]
    for size in sizes:
        matrix = create_bidding_matrix(size)
        start = time.time()
        bfef = bidding_for_envy_freeness(matrix)
        end = time.time()
        print(f'Size {size}: {end - start}')