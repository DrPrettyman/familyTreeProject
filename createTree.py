import pandas as pd
import numpy as np


def one_across(position, direction):
    return [position[0]+direction, position[1]]


class Family:
    def __init__(self, people_csv_path, unions_csv_path):
        self.people = pd.read_csv(people_csv_path, delimiter=';', index_col='code', parse_dates=['date_of_birth'])
        self.unions = pd.read_csv(unions_csv_path, delimiter=';', index_col=False, parse_dates=['date_of_union'])
        self.unions['children'] = self.unions['children'].apply(
            lambda names: names.split(' ') if type(names) == str else [])
        self.unions['members'] = self.unions['members'].apply(
            lambda names: names.split(' ') if type(names) == str else [])
        self.unions['separation'] = self.unions['separation'].apply(
            lambda s: s if s == 1 else 0)

        self.people_dict, self.index_dict = self._init_people_dict()
        # self.people_indices = [i for i in self.people.index]
        # self.people_codes = [self.people.code[i] for i in self.people_indices]
        self.children_dict = self._init_children_dict()
        self.unions_dict = self._init_unions_dict()
        self.parentunion_dict = self._init_parentunion_dict()
        self.parent_dict = self._init_parent_dict()
        self.siblings_dict = self._init_siblings_dict()
        self.spouse_dict = self._init_spouse_dict()
        self.relationship_dict = self._init_relationship_dict()
        self.positions_dict = {}
        self.branch_dict = {}

    def _init_people_dict(self):
        """
        returns two dictionaries:
        _people_dict maps indices to people, e.g. {0: 'Alice', 1: 'Bob', 2: 'Colin'}
        _index_dict does the opposite, e.g. {'Alice': 0, 'Bob': 1, 'Colin': 2}
        """
        _people_dict = {}
        _index_dict = {}
        _list_of_people = []
        for i in self.unions.index:
            for member in self.unions.members[i]:
                if member not in _list_of_people:
                    _list_of_people.append(member)
            for child in self.unions.children[i]:
                if child not in _list_of_people:
                    _list_of_people.append(child)
        for j in range(len(_list_of_people)):
            _people_dict[j] = _list_of_people[j]
            _index_dict[_list_of_people[j]] = j
        return _people_dict, _index_dict

    def _init_children_dict(self):
        """
        :return:
        children_dict maps a union's index to the children resulting from that union
        """
        children_dict = {}
        # For each union i
        for i in self.unions.index:
            # Find the indices of the children of that union
            children = self.unions.children[i]
            children_dict[i] = self.find_index(children)
        return children_dict

    def _init_unions_dict(self):
        """
        :return:
        unions_dict maps a union's index to the member/s of that union
        """
        unions_dict = {}
        # For each union i
        for i in self.unions.index:
            members = self.unions.members[i]
            unions_dict[i] = self.find_index(members)
        return unions_dict

    def _init_parentunion_dict(self):
        """
        :return:
        parent_uniondict maps a person's identifying index to their parental union
        """
        parentunion_dict = {}
        for union_index in self.children_dict:
            for child_index in self.children_dict[union_index]:
                parentunion_dict[child_index] = union_index
        return parentunion_dict

    def _init_parent_dict(self):
        """
        :return:
        parent_dict maps a person's identifying index to those of their parent/s
        """
        parent_dict = {i: [] for i in self.people_dict.keys()}
        for union_index in self.children_dict:
            for child_index in self.children_dict[union_index]:
                parent_dict[child_index] += self.unions_dict[union_index]
        return parent_dict

    def _init_siblings_dict(self):
        """
        :return:
        siblings_dict maps a person's identifying index to those of their siblings
        """
        siblings_dict = {i: [] for i in self.people_dict.keys()}
        for brood in self.children_dict.values():
            for child in brood:
                siblings_dict[child] += [i for i in brood if i != child]
        return siblings_dict

    def _init_spouse_dict(self):
        """
        :return:
        spouse_dict maps a person's identifying index to those of their spouse/s
        """
        spouse_dict = {i: [] for i in self.people_dict.keys()}
        for relationship in self.unions_dict.values():
            for member in relationship:
                spouse = [i for i in relationship if i != member]
                spouse_dict[member] += spouse
        return spouse_dict

    def _init_relationship_dict(self):
        """
        :return:
        spouse_dict maps a person's identifying index to those of their spouse/s
        """
        relationship_dict = {i: [] for i in self.people_dict.keys()}
        for _union in self.unions_dict.keys():
            for _member in self.unions_dict[_union]:
                relationship_dict[_member].append(_union)
        return relationship_dict

    def find_index(self, list_of_people_names):
        list_of_indices = [self.index_dict[name] for name in list_of_people_names]
        return list_of_indices

    def find_unions(self, list_of_people):
        _l = []
        for person in list_of_people:
            _l += self.relationship_dict[person]
        _l = [_l[i] for i in range(len(_l)) if _l[i] not in _l[:i]]
        return _l

    def find_person_and_spouses(self, person: int, direction: int):
        # get a list of the spouses
        _l = self.spouse_dict[person]
        # If there are 0 or 1 spouses we want to add them in the order [person, spouse1]
        # If there are >1 spouses we add in the order [spouse1, person, spouse2, ...]
        if len(_l) <= 1:
            _l.insert(0, person)
        else:
            _l.insert(1, person)
        # if we are adding on the left (direction == -1) we reverse the list
        if direction == -1:
            _l.reverse()
        return _l

    def create_first_branch(self):
        first_branch_index = 0
        self.branch_dict[first_branch_index] = 0
        return first_branch_index

    def create_new_branch(self, current_branch, direction):
        new_branch_index = current_branch + 1
        current_branch_position = self.branch_dict[current_branch]
        new_branch_position = current_branch_position + direction
        if direction == -1:
            for _k in self.branch_dict.keys():
                if self.branch_dict[_k] <= new_branch_position:
                    self.branch_dict[_k] -= 1
        elif direction == 1:
            for _k in self.branch_dict.keys():
                if self.branch_dict[_k] >= new_branch_position:
                    self.branch_dict[_k] += 1
        self.branch_dict[new_branch_index] = new_branch_position
        return new_branch_index

    def edge_of_level(self, branch, level: int, direction: int):
        """
        gives the position vector either one to the left of the current left-most position,
        or one to the right of the current right-most position
        :param level:     The level to be examined
        :param direction: -1 for left, 1 for right
        :return:          position vector as a list of coordinates [x, y]
        """
        if len(self.positions_dict.keys()) < 1:
            return [0, 0]
        _dummy_list = []
        for _pos in self.positions_dict.values():
            # If the y coordinate is ==level, add the x coordinate to the list
            if _pos[1] == level:
                _dummy_list.append(_pos[0])
            # Now we have a list of all the occupied x coordinates on the current level
        _x = 0
        if len(_dummy_list) > 0:
            if direction == -1:
                _x = min(_dummy_list)  # the leftmost (lowest) x coordinate
            elif direction == 1:
                _x = max(_dummy_list)  # the rightmost (largest) x coordinate
        return [_x + direction, level]

    def add_person(self, person: int, branch, level, direction: int):
        """
        Add a person on either the left or right of the given level
        The index of he person, and the position will be added to
        self.positions_dict
        :param person:    index of the person to add
        :param branch:    index of current branch
        :param level:     index of the level on which to add the person
        :param direction: -1 for left, 1 for right
        """
        self.positions_dict[person] = self.edge_of_level(branch, level, direction)

    def add_children_of_union(self, union: int, branch, level, direction: int):
        for sibling in self.children_dict[union]:
            self.add_sibling(sibling, level=level-1, direction=direction)

    def add_parents(self):
        pass

    def add_sibling(self, sibling: int, branch, level, direction: int):
        #  get a list of the sibling and his/her spouse/s
        _sibling_and_spouses = self.find_person_and_spouses(sibling, direction)
        # Add the position of the sibling and spouses at the edge of the level
        for _p in _sibling_and_spouses:
            self.add_person(_p, level=level, direction=direction)
        # Now we get a list of any unions containing the sibling and his/her spouse/s
        # and finally add the children of each union
        for _u in self.find_unions(_sibling_and_spouses):
            self.add_children_of_union(union=_u, level=level, direction=direction)

    def explore_outward(self, person: int, direction: int):
        current_position = self.positions_dict[person]
        # Find siblings
        for _sibling in self.siblings_dict[person]:
            self.add_sibling(_sibling, level=current_position[1], direction=direction)

    def explore_upward(self, person: int):
        _parents = self.parent_dict[person]

    def create_tree(self, initial_person=0):
        branch = self.create_first_branch()



























