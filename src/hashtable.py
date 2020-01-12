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
        self.storage = [None] * capacity

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key) % self.capacity

    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        pass

    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)
        lp = LinkedPair(key, value)

        # if there is collision,
        if self.storage[index]:
            # store the value of the colliding key in the next linked list node
            lp.next = self.storage[index]

        self.storage[index] = lp

    def remove(self, key):
        index = self._hash(key)

        # if hash table index has values
        if self.storage[index]:
            lp = self.storage[index]
            # and you found the key,
            if lp.key == key:
                # replace that value with the next key's value
                self.storage[index] = lp.next
            else:
                # else loop through linked list until you find the key
                while lp.next is not None:
                    if lp.next.key == key:
                        lp.next = lp.next.next
                    else:
                        lp = lp.next
        else:
            print("This value doesn't exist in the hash table.")

    def retrieve(self, key):
        index = self._hash(key)

        # if hash table index has values,
        if self.storage[index]:
            # loop through linked list until key is found
            lp = self.storage[index]
            if lp.key == key:
                return lp.value
            else:
                # else loop through linked list until you find the key
                while lp.next is not None:
                    if lp.next.key == key:
                        return lp.next.value
                    else:
                        lp = lp.next
        else:
            # return None if key is not found
            return None

    def resize(self):
        # double hash table size
        ht = HashTable(2 * self.capacity)

        # copy old hash table into new one
        for item in self.storage:
            cur_item = item
            while cur_item is not None:
                ht.insert(cur_item.key, cur_item.value)
                cur_item = cur_item.next

        # replace old hash table with the new
        self.capacity *= 2
        self.storage = ht.storage


if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
