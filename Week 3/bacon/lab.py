"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!
# write docstrings for each code to get full points
# also write comments for documentation


def transform_data(raw_data):
    """
    Transforms data by converting tuples to keys being the actor
    and values being the set of actors actor in keys acted with.
    Movie dictionary maps the movie ID as the keys and the values are
    the set of actors that acted in the movie
    """
    dictionary = dict()
    movie_dict = dict()
    for elem in raw_data:
        if elem[0] != elem[1]:
            dictionary.setdefault(elem[0], set()).add(elem[1])
            dictionary.setdefault(elem[1], set()).add(elem[0])
        movie_dict.setdefault(elem[2], set()).add(elem[0])
        movie_dict.setdefault(elem[2], set()).add(elem[1])
    return dictionary, movie_dict


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Returns true or false if two actors acted together based on transformed_data
    """
    if actor_id_1 == actor_id_2:
        return True
    return bool(
        actor_id_2 in transformed_data[0][actor_id_1]
        or actor_id_1 in transformed_data[0][actor_id_2]
        )


def actors_with_bacon_number(transformed_data, n):
    """
    Returns a set of actors with given bacon number by having a while loop
    that keeps going until the iterator reaches n. Gets neighbors by calling
    the values that correspond to the keys in the transformed_data.
    Prevents the same actor from being added by making sure it's not in the
    tracker set. Have working_set as the set of actors for bacon number i,
    new_set as the set of actors for bacon number i+1
    """

    i = 0
    tracker_set = set()
    #set keeps track of all actor_IDs that we go through
    new_set = set()
    #initialize set as empty set
    if n == 0:
        return {4724}
    #Only Kevin Bacon (ID=4724) has Bacon number 0
    while i < n:
        new_set = set()
        #redefine set as empty set each time for while loop
        bacon_ID = 4724
        if i == 0:
            working_set = {bacon_ID}
            tracker_set = {bacon_ID}
            #start with Kevin Bacon as the center
        for name in working_set:
            #Iterate through the list of actors at i
            for actor in transformed_data[0][
                name
            ]:
                #iterate through list of neighbors of actors at i
                if actor not in tracker_set:
                    #do not want to add same actor again
                    new_set.add(actor)
                    tracker_set.add(actor)
                    #keeps tracks of things
        working_set = new_set
        #redefine working set as set for the next iteration
        if working_set == set():
            return (
                set()
            )
        #takes into account extremely large bacon numbers which is empty set
        i += 1
        #increase count by 1 to end the while loop
    return new_set


def bacon_path(transformed_data, actor_id):
    """
    Gives the list of actors from Kevin Bacon (4724) to the desired actor
    """
    path = actor_to_actor_path(transformed_data, 4724, actor_id)
    return path


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Returns a list of actors with given bacon number by having a while loop
    that keeps going until the tracker_set has actor_id_2. Gets neighbors by calling
    the values that correspond to the keys in the transformed_data.
    Prevents the same actor from being added by making sure it's not in the
    tracker set. Will return none if there is no possible path for two actors. Use a
    dictionary to keep track of the actor_path_list (value) for each corresponding
    actor (key)
    """

    def actor_boolean(actor_id):
        return actor_id == actor_id_2

    actor_list = actor_path(transformed_data, actor_id_1, actor_boolean)
    return actor_list


def movie_path(raw_data, transformed_data, actor_id_1, actor_id_2):
    """
    Use actor_to_actor_path to get actor list. Adds movies to movie_list if
    actor at bacon number i and actor at bacon number i+1 acted together by
    going through the raw data to find the movie id from the raw data. If
    true, then append to the movie list
    """
    actor_list = actor_to_actor_path(transformed_data, actor_id_1, actor_id_2)
    movie_list = []
    for i in range(len(actor_list) - 1):
        for value in raw_data:
            if actor_list[i] in value and actor_list[i + 1] in value:
                movie = value[2]
                movie_list.append(movie)
    return movie_list


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    While loop keeps running if the goal_test_function is false and
    will stop running once goal_test_function is true. If no path is
    possible, return None
    """
    working_set = {actor_id_1}
    tracker_set = {actor_id_1}
    #set keeps track of all actor_IDs that we go through
    actor_path_list = [actor_id_1]
    new_dict = {actor_id_1: [actor_id_1]}
    #actor_id_1: [actor_id_1]
    boolean_variable = goal_test_function(actor_id_1)
    #initialize variable to boolean
    if boolean_variable is True:
        return actor_path_list
    #skips while loop if boolean is true
    while boolean_variable is False:
        new_set = set()
        #redefine set as empty set each time for while loop
        for name in working_set:
            #Iterate through the list of actors at i
            for actor in transformed_data[0][name]:
                #iterate through list of neighbors of actors at i
                if actor not in tracker_set:
                    #do not want to add same actor again
                    new_set.add(actor)
                    tracker_set.add(actor)
                    #keeps tracks of things
                    actor_path_list = new_dict[name] + [actor]
                    new_dict[actor] = actor_path_list
                if goal_test_function(actor) is True:
                    return new_dict[
                        actor
                    ]
                #finish while loop because reaches the path, finds actor
        working_set = new_set
        #redefine working set as set for the next iteration
        if working_set == set():
            return None
        #takes into account extremely large bacon numbers which is empty set


def actors_connecting_films(transformed_data, film1, film2):
    """
    Get set of actors from film 1 and another set of actors from
    film 2. Then use nested for loop to go through each set,
    adding each list. Then find the shortest list by finding the length.
    If it is the shortest, then return the list of actors
    """
    tracker_list = []
    length_list = []
    movie_dictionary = transformed_data[1]
    actor_1_set = movie_dictionary[film1]
    actor_2_set = movie_dictionary[film2]
    for actor_1 in actor_1_set:
        for actor_2 in actor_2_set:
            path_list = actor_to_actor_path(transformed_data, actor_1, actor_2)
            tracker_list.append(path_list)
            length_list.append(len(path_list))
    for tracker in tracker_list:
        if len(tracker) == min(length_list):
            return tracker


if __name__ == "__main__":
    with open("large.pickle", "rb") as f:
        db_large = pickle.load(f)
    pass
