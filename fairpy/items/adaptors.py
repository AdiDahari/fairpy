"""
This module implements Adaptor functions for fair division algorithms.

The functions accept a division algorithm as an argument.

They allow you to call the algorithm with convenient input types,
such as: a list of values, or a dict that maps an item to its value.

Author: Erel Segal-Halevi
Since: 2022-10
"""

from typing import Callable, Any
from fairpy import AgentList, Allocation
from dicttools import stringify


def divide(
    algorithm: Callable,
    instance: Any,
    **kwargs
):
    """
    An adaptor function for item allocation.

    :param algorithm: a specific fair item allocation algorithm. Should accept (at least) the following parameters: 
        agents: List[Agent]

    :param instance: can be one of the following:
       * dict of dicts mapping agent names to their valuations, e.g.: {"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}}
       * list of dicts, e.g. [{"x":1,"y":2}, {"x":3,"y":4}]. Agents are called by their number: "Agent #0", "Agent #1", etc.
       * list of lists, e.g. [[1,2],[3,4]]. Agents and items are called by their number.
       * numpy array, e.g.: np.ones([2,4])). 
       * list of Valuation objects, e.g. [AdditiveValuation([1,2]), BinaryValuation("xy")]
       * list of Agent objects, e.g. [AdditiveAgent([1,2]), BinaryAgent("xy")]

    :param kwargs: any other arguments expected by `algorithm`.

    :return: an allocation of the items among the agents.

    >>> import fairpy

    ### List of lists of values, plus an optional parameter::
    >>> divide(algorithm=fairpy.items.round_robin, instance=[[11,22,44,0],[22,11,66,33]], agent_order=[1,0])
    Agent #0 gets {0,1} with value 33.
    Agent #1 gets {2,3} with value 99.
    <BLANKLINE>

    ### Dict mapping agent names to lists of values
    >>> divide(algorithm=fairpy.items.round_robin, instance={"Alice": [11,22,44,0], "George": [22,11,66,33]})
    Alice gets {1,2} with value 66.
    George gets {0,3} with value 55.
    <BLANKLINE>

    ### Dict mapping agent names to lists of values:
    >>> divide(algorithm=fairpy.items.utilitarian_matching, instance={"Alice": [11,22,44,0], "George": [22,11,66,33]})
    Alice gets {1} with value 22.
    George gets {2} with value 66.
    <BLANKLINE>

    ### Dict mapping agent names to dicts of values:
    >>> divide(algorithm=fairpy.items.iterated_maximum_matching, instance={"Alice": {"w":11,"x":22,"y":44,"z":0}, "George": {"w":22,"x":11,"y":66,"z":33}})
    Alice gets {w,x} with value 33.
    George gets {y,z} with value 99.
    <BLANKLINE>

    >>> divide(algorithm=fairpy.items.undercut, instance={"Alex":{"a": 1,"b": 2, "c": 3, "d":4,"e": 5, "f":14},"Bob":{"a":1,"b": 1, "c": 1, "d":1,"e": 1, "f":7}})
    Alex gets {a,b,c,d,e} with value 15.
    Bob gets {f} with value 7.
    <BLANKLINE>

    >>> divide(algorithm=fairpy.items.three_quarters_MMS_allocation, instance={"Alice": {"w":11,"x":22,"y":44,"z":0}, "George": {"w":22,"x":11,"y":66,"z":33}})
    Alice gets {y} with value 44.
    George gets {w,x,z} with value 66.
    <BLANKLINE>

    >>> prefs = AgentList({"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}})
    >>> alloc = divide(fairpy.items.utilitarian_matching, prefs, item_capacities={"x":2, "y":2})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x'], beni:['y'], gadi:['x']}"
    >>> stringify(alloc.map_item_to_agents())
    "{x:['avi', 'gadi'], y:['beni']}"
    >>> agent_weights = {"avi":1, "gadi":10, "beni":100}
    >>> stringify(alloc.map_item_to_agents(sortkey=lambda name: -agent_weights[name]))
    "{x:['gadi', 'avi'], y:['beni']}"

    >>> alloc = divide(fairpy.items.utilitarian_matching, prefs, item_capacities={"x":2, "y":2}, agent_capacities={"avi":2,"beni":1,"gadi":1})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x', 'y'], beni:['y'], gadi:['x']}"

    >>> prefs = AgentList([[5,4],[3,2]])
    >>> alloc = divide(fairpy.items.utilitarian_matching, prefs)
    >>> stringify(alloc.map_agent_to_bundle())
    '{Agent #0:[1], Agent #1:[0]}'
    >>> stringify(alloc.map_item_to_agents())
    "{0:['Agent #1'], 1:['Agent #0']}"

    >>> agents = AgentList({"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}})
    >>> alloc = divide(fairpy.items.iterated_maximum_matching, agents, item_capacities={"x":1,"y":1,"z":1,"w":1})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x', 'y'], beni:['w', 'z']}"
    >>> stringify(alloc.map_item_to_agents())
    "{w:['beni'], x:['avi'], y:['avi'], z:['beni']}"
    """
    if "agents" in algorithm.__annotations__:
        agents = AgentList(instance)
        allocation = algorithm(agents, **kwargs)
    else:
        allocation = algorithm(instance, **kwargs)
    if isinstance(allocation, Allocation):
        return allocation
    else:
        return Allocation(agents, allocation)


if __name__ == "__main__":
    # from fairpy.items.round_robin import round_robin
    # print(divide(algorithm=round_robin, instance = [[11,22,44,0],[22,11,66,33]]))
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True)
    print(f"{failures} failures, {tests} tests")
    # if failures > 0:
    #     sys.exit(1)