"""
6.1010 Spring '23 Lab 4: Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    recipe_dict = {}
    # initialize an empty dictionary
    for recipe in recipes:
        if recipe[0] == "compound":  # will only do this if it is a compound recipe
            recipe_dict.setdefault(recipe[1], []).append(recipe[2])
            # creates a new dictionary with key being food name
            # value being ingredient list
    return recipe_dict


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    recipe_dict = {}
    for recipe in recipes:
        if recipe[0] == "atomic":
            recipe_dict.setdefault(recipe[1], recipe[2])
    return recipe_dict


def lowest_cost(recipes, food_item, forbidden=None):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    recipe_dict = make_recipe_book(recipes)
    atomic_dict = make_atomic_costs(recipes)
    if forbidden is None:
        pass
    else:
        for (
            forbidden_item
        ) in forbidden:  # can have more than one item in forbidden, list
            if forbidden_item in atomic_dict:
                del atomic_dict[forbidden_item]
            elif forbidden_item in recipe_dict:
                del recipe_dict[forbidden_item]
            else:
                pass

    def lowest_cost_recursion(food):
        if food in atomic_dict:  # base case
            cost = atomic_dict[food]  # return cost which is dict value
            return cost
        elif food in recipe_dict:  # perform recursion for the compound food items
            # check food in recipe_dict
            # is this line of code redundant
            recipe_list = recipe_dict[food]
            cost_list = []
            for recipe in recipe_list:
                # add an outer for loop, all possible ways to make the food
                # after iterate through all the ways, find lowest cost method
                # only looked at one method, should iterate through recipe_dict[food][0]
                total_cost = (
                    0  # initialize in the scale of changing not inside for loop
                )
                broken = False
                for item, scale in recipe:
                    lowest_cost = lowest_cost_recursion(item)  # call function only once
                    if lowest_cost is None:
                        broken = True  # use boolean to remember if broken
                        break
                    else:
                        total_cost += scale * lowest_cost
                if broken:
                    continue
                cost_list.append(
                    total_cost
                )  # append once finish going through items in the ingredients
                # for else loop with if else inside
            if cost_list == []:
                return None
            else:
                return min(cost_list)
        else:
            return None

    return lowest_cost_recursion(food_item)


def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    scale_recipe_dict = {key: flat_recipe[key] * n for key in flat_recipe.keys()}
    return scale_recipe_dict


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    grocery_dict = {}
    for recipe in flat_recipes:
        for key in recipe.keys():
            # enumerate has index, value while dictionary has items too
            if (
                key in grocery_dict.keys()
            ):  # if the key is already in the growing grocery_dict
                grocery_dict[key] += recipe[
                    key
                ]  # add the recipe's value to the grocery's value
            else:
                grocery_dict.setdefault(
                    key, recipe[key]
                )  # create a new value to grocery_dict
    return grocery_dict
    # setdefault used only when it doesn't exist. returns a value
    # once it exists if it reappears we don't want it to append
    # doesn't exist will set the value.


def cheapest_flat_recipe(recipes, food_item, forbidden=None):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    recipe_dict = make_recipe_book(recipes)
    atomic_dict = make_atomic_costs(recipes)
    if forbidden is None:
        pass
    else:
        for (
            forbidden_item
        ) in forbidden:  # can have more than one item in forbidden, list
            if forbidden_item in atomic_dict:
                del atomic_dict[forbidden_item]
            elif forbidden_item in recipe_dict:
                del recipe_dict[forbidden_item]
            else:
                pass

    def flat_recipe_recursion(food):
        mini_dict = dict()
        if food in atomic_dict:  # base case
            cost = atomic_dict[food]  # return cost which is dict value
            mini_dict.setdefault(food, 1)
            return (cost, mini_dict)
        elif food in recipe_dict:
            recipe_list = recipe_dict[food]
            tuple_list = []
            for recipe in recipe_list:
                total_cost = 0
                broken = False
                recipe_dict_list = []
                for food, scale in recipe:
                    cost_recipe_tuple = flat_recipe_recursion(food)
                    if cost_recipe_tuple is None:
                        broken = True
                        break
                    else:
                        total_cost += scale * cost_recipe_tuple[0]
                        # dictionary 0 but 0 doesn't exist
                        scaled_recipe = scale_recipe(cost_recipe_tuple[1], scale)
                        recipe_dict_list.append(scaled_recipe)
                final_grocery_dict = make_grocery_list(recipe_dict_list)
                if broken:
                    continue
                tuple_list.append((total_cost, final_grocery_dict))
            if tuple_list == []:
                return None
            else:
                minimum = tuple_list[0]
                print(minimum)
                for i in range(len(tuple_list)):
                    if tuple_list[i][0] < minimum[0]:
                        minimum = tuple_list[i]
                return minimum
            # looping through a tuple need to do carefully.
        else:
            return None

    if flat_recipe_recursion(food_item) is None:
        return None
    else:  # additional if else statement because of the tuple need to index
        return flat_recipe_recursion(food_item)[1]


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes make a certain ingredient as part of a recipe, compute all
    combinations of the flat recipes.
    """
    mix_list = []
    if len(flat_recipes) == 1:
        return flat_recipes[0]  # base case is when the length is 1
    else:
        sub_list = flat_recipes[1:]  # list not including first food
        intermediate = ingredient_mixes(sub_list)  # list of the mixed ingredients
        for combinations in intermediate:  # loop through all combinations
            for food in flat_recipes[0]:  # go through the items in first list
                mix_list.append(
                    make_grocery_list([food, combinations])
                )  # append item to the list
    return mix_list

    # does this require recursion or something?
    # combinations happens when you have recursion like subsequences


def all_flat_recipes(recipes, food_item, forbidden=None):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    recipe_dict = make_recipe_book(recipes)
    atomic_dict = make_atomic_costs(recipes)
    if forbidden is None:
        pass
    else:
        for (
            forbidden_item
        ) in forbidden:  # can have more than one item in forbidden, list
            if forbidden_item in atomic_dict:
                del atomic_dict[forbidden_item]
            elif forbidden_item in recipe_dict:
                del recipe_dict[forbidden_item]
            else:
                pass

    def all_flat_recursion(food):  # should return a list of dictionaries
        if food in atomic_dict:  # base case
            return [{food: 1}]  # not sure if return mini_dict
        elif food in recipe_dict:
            recipe_combinations = []
            recipe_list = recipe_dict[food]
            for recipe in recipe_list:
                big_list = []
                for food, scale in recipe:
                    flat_recipe_list = all_flat_recursion(food)
                    recipe_dict_list = []
                    print(flat_recipe_list)
                    for item in flat_recipe_list:
                        scaled_dict = scale_recipe(
                            item, scale
                        )  # list comprehension or for loop
                        recipe_dict_list.append(scaled_dict)
                    print(recipe_dict_list)
                    big_list.append(recipe_dict_list)
                print(big_list)
                recipe_combinations.extend(
                    ingredient_mixes(big_list)
                )  # takes in a list of list of dictionaries

                # dictionary 0 but 0 doesn't exist
                # extend doesn't have an extra layer
            return recipe_combinations
            # looping through a tuple need to do carefully.
        else:
            return []

    # additional if else statement because of the tuple need to index
    return all_flat_recursion(food_item)

    # use ingredient mixes as helper function


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    cookie_recipes = [
        ("compound", "cookie sandwich", [("cookie", 2), ("ice cream scoop", 3)]),
        ("compound", "cookie", [("chocolate chips", 3)]),
        ("compound", "cookie", [("sugar", 10)]),
        ("atomic", "chocolate chips", 200),
        ("atomic", "sugar", 5),
        ("compound", "ice cream scoop", [("vanilla ice cream", 1)]),
        ("compound", "ice cream scoop", [("chocolate ice cream", 1)]),
        ("atomic", "vanilla ice cream", 20),
        ("atomic", "chocolate ice cream", 30),
    ]

    dairy_recipes = [
        ("compound", "milk", [("cow", 2), ("milking stool", 1)]),
        ("compound", "cheese", [("milk", 1), ("time", 1)]),
        ("compound", "cheese", [("cutting-edge laboratory", 11)]),
        ("atomic", "milking stool", 5),
        ("atomic", "cutting-edge laboratory", 1000),
        ("atomic", "time", 10000),
        ("atomic", "cow", 100),
    ]
    new_recipes = make_recipe_book(cookie_recipes)
    atomic_dict = make_atomic_costs(cookie_recipes)
    print(new_recipes)
    print(atomic_dict)
    # ingredient_mixes(cake_recipes, icing_recipes)
