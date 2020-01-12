# '''
# Linked List hash table key/value pair
# '''
import hashlib


class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''

    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        # Used for limiting hash table shrinking to never go below the original size
        self.orig_capacity = capacity
        self.storage = [None] * capacity
        self.num_items = 0  # For calculating load factor, which is num_items / capacity

    def __hash_djb2(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key) % self.capacity

    def __hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2

        Reference: http://www.cse.yorku.ca/~oz/hash.html
        '''
        hash = 5381
        for char in key:
            hash = ((hash << 5) + hash) + ord(char)

        return hash

    def __hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self.__hash_djb2(key) % self.capacity

    def load_factor(self):
        return self.num_items / self.capacity

    def insert(self, key, value):

        # If key exists in hash table, remove it so we can replace with updated value
        if self.retrieve(key):
            self.remove(key)

        index = self.__hash_mod(key)
        item = LinkedPair(key, value)

        # if there is a collision,
        if self.storage[index]:
            # store the value of the colliding key in the next linked list node
            item.next = self.storage[index]

        self.storage[index] = item

        # Resize hash table if high load factor
        self.num_items += 1
        if self.load_factor() > 0.7:
            self.resize()

    def remove(self, key):
        if self.retrieve(key) is None:
            return

        index = self.__hash_mod(key)

        # if hash table index has values
        if self.storage[index]:
            item = self.storage[index]
            # and you found the key,
            if item.key == key:
                # replace that value with the next key's value
                self.storage[index] = item.next
                self.num_items -= 1
            else:
                # else loop through linked list until you find the key
                while item.next is not None:
                    if item.next.key == key:
                        # set pointer to skip over item, effectively removing it
                        item.next = item.next.next
                        self.num_items -= 1
                        break
                    else:
                        item = item.next

        # Shrink hash table if low load factor and hash table is larger than its original size
        if self.load_factor() < 0.2 and self.capacity > self.orig_capacity:
            self.resize()

    def retrieve(self, key):
        index = self.__hash_mod(key)

        # if hash table index has values,
        if self.storage[index]:
            # loop through linked list until key is found
            item = self.storage[index]
            if item.key == key:
                return item.value
            else:
                while item.next is not None:
                    if item.next.key == key:
                        return item.next.value
                    else:
                        item = item.next

        # return None if key is not found
        return None

    def resize(self):
        new_capacity = self.capacity
        # double hash table size if high load factor
        if self.load_factor() > 0.7:
            new_capacity *= 2
            # print("Growing to ", new_capacity)
        # or halve if low load factor and larger than original size
        elif self.load_factor() < 0.2 and self.capacity > self.orig_capacity:
            new_capacity //= 2
            # print("Shrinking to ", new_capacity)

        # if neither enlarging or shrinking, return with no other action
        if new_capacity == self.capacity:
            return

        # create new hash table
        ht = HashTable(new_capacity)

        # copy old hash table into new one
        for node in self.storage:
            cur_node = node
            while cur_node is not None:
                ht.insert(cur_node.key, cur_node.value)
                cur_node = cur_node.next

        # replace old hash table with the new
        self.capacity = new_capacity
        self.storage = ht.storage


if __name__ == "__main__":
    ht = HashTable(2)

    old_capacity = len(ht.storage)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))
