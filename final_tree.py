class Label:
    def __init__(self) :
        self.key = ""
        self.value = []

class Node:
    def __init__(self):
        self.labels = []
        self.data_list = []
        self.next_nodes = []
        
class SearchTree:
    def __init__(self,data_list):
        self.categories_type_list = []
        self.price_type_list = []
        self.rating_type_list = []
        self.closed_type_list = [True,False]
        self.data_list = []

        for item in data_list:

            if 'price' not in item:
                continue
            if len(item['categories']) > 0:
                item['category'] = item['categories'][0]['title']


            if item['price'] == '££':
                item['price'] = '$$'

            if item['category'] not in self.categories_type_list:
                self.categories_type_list.append(item['category'])
            if item['price'] not in self.price_type_list:
                self.price_type_list.append(item['price'])
            if item['rating'] not in self.rating_type_list:
                self.rating_type_list.append(item['rating'])
            
            self.data_list.append(item)
        self.tree = self.create_tree()

    
    def create_tree(self):

        category_label = Label()
        category_label.key = "category"
        category_label.value = self.categories_type_list[:]

        price_label = Label()
        price_label.key = "price"
        price_label.value = self.price_type_list[:]

        rating_label = Label()
        rating_label.key = "rating"
        rating_label.value = self.rating_type_list[:]

        closed_label = Label()
        closed_label.key = "is_closed"
        closed_label.value = self.closed_type_list[:]

        root_node = Node()
        root_node.labels = [category_label,price_label,rating_label,closed_label]
        root_node.data_list = self.data_list[:]
        self.add_sub_node(root_node)
        return root_node

    def add_sub_node(self,node:Node):
        if len(node.labels) == 0:
            return
        label:Label = node.labels[0]
        next_node_data_list = list()
        for i in range(len(label.value)):
            next_node_data_list.append([])
        for data in node.data_list:
            value_index = label.value.index(data[label.key])
            next_node_data_list[value_index].append(data)
        
        for item in next_node_data_list:
            next_node = Node()
            next_node.labels = node.labels[1:]
            next_node.data_list = item
            node.next_nodes.append(next_node)
            self.add_sub_node(next_node)

    def search_data(self,filter_list,node = None,):
        if node == None:
            node = self.tree
        if len(filter_list) == 0:
            return node.data_list
        else:
            label = node.labels[0]
            value_index = label.value.index(filter_list[0])
            return self.search_data(filter_list = filter_list[1:],node = node.next_nodes[value_index])
        