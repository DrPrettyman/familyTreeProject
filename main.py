import createTree
import initCSV

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initCSV.init_prettycrew()
    prettycrew = createTree.Family('ft_people.csv', 'ft_unions.csv')
    print('children dict:    ', prettycrew.children_dict)
    print('unions dict:      ', prettycrew.unions_dict)
    print('parent dict:      ', prettycrew.parent_dict)
    print('siblings dict:    ', prettycrew.siblings_dict)
    print('parentunion_dict: ', prettycrew.parentunion_dict)
    print('spouse_dict:      ', prettycrew.spouse_dict)
    print('relationship_dict:', prettycrew.relationship_dict)



    # createTree.write_html()
    # createTree.draw_family_tree()
    # createTree.add_positions(ft_people, ft_unions)


