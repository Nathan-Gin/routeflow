
class APQBinaryHeap:
    """ Maintain an collection of items, popping by lowest key.

        This implementation maintains the collection using a binary heap.
        Uses an internally-defined class Element to store the items as a
        key (i.e. priority) and value (i.e. the actual item) pair.
        Use this class by typing PQBinaryHeap.Element() etc.
    """
    class Element:
        """ An element with a key and value. """
        
        def __init__(self, k, v, i):
            self._key = k
            self._value = v
            self._index = i
            

        def __eq__(self, other):
            """ Return True if this key equals the other key. """
            return self._key == other._key

        def __lt__(self, other):
            """ Return True if this key is less than the other key. """
            return self._key < other._key

        def _wipe(self):
            """ Set the instance variables to None. """
            self._key = None
            self._value = None
            self._index = None

    def __init__(self):
        """ Create a PQ with no elements. """

        # this is an array-based heap, so you need to create
        # an empty python list, and then maintain it
        # properly in the add and remove-min methods.
        self._heap = []
        self._size = 0
        self._locations = {}
        self._items_removed = 0
        
    def __str__(self):
        """ Return a breadth-first string of the values. """
        outstr = '['
        index = 0
        for elt in self._heap:
            outstr += str(index) + ' stored index' + str(elt._index) \
                      + ':' + str(elt._value) \
                      + ':' + str(elt._key) + ','
            index += 1
        return outstr + ']'

    def add(self, key, value):
        """ Add Element(key,value) to the heap. """
        e = APQBinaryHeap.Element(key, value, self._size)
        self._heap.append(e)
        self._upheap(self._size)
        self._size += 1
        self._locations[value] = e
        return e

    def min(self):
        """ Return the min priority key,value. """
        if self._size:
            return self._heap[0]._key, self._heap[0]._value
        return None, None

    def remove_min(self):
        """ Remove and return the min priority key,value. """
        returnvalue = None
        returnkey = None
        if self._size > 0:
            returnkey = self._heap[0]._key
            returnvalue = self._heap[0]._value
            self._heap[0]._wipe()
            self._locations.pop(returnvalue)
            self._items_removed += 1
            if self._size > 1: #if other items, restructure
                self._heap[0] = self._heap.pop()
                self._heap[0]._index = 0
                self._size -= 1
                self._downheap(0)
            else:
                self._heap.pop()
                self._size -= 1
        return returnkey, returnvalue
    
    def update_key(self, item, newkey):
        element = self._locations[item]
        oldkey = element._key
        element._key = newkey

        #checking if the new key is smaller then we call upheap to check if parent is smaller
        if newkey < oldkey:
            self._upheap(element._index)
        else: # otherwise we check if we need to bubble down as it was bigger
            self._downheap(element._index)

    def get_key(self, item):
        if item in self._locations:
            return self._locations[item]._key
        return None
    
    def remove(self, item):
        returnvalue = None
        returnkey = None
        if item in self._locations:
            element = self._locations[item]
            #swap item with last and update index of swapped item
            swap_index = element._index
            returnkey = element._key
            returnvalue = element._value
            self._heap[swap_index], self._heap[-1] = self._heap[-1], self._heap[swap_index]
            self._heap[swap_index]._index = swap_index
            self._locations.pop(returnvalue)
            self._items_removed += 1
            self._heap[-1]._wipe()#clear and remove item
            self._heap.pop()
            self._size -= 1
            #We are only rebalncing the heap when its not the last item or last index
            if self._size > 0 and swap_index < self._size:
                if self._heap[swap_index]._key < returnkey:
                    self._upheap(swap_index)
                else: 
                    self._downheap(swap_index)
        return returnkey, returnvalue


            


 
    def length(self):
        """ Return the number of items in the heap. """
        return self._size

    # Private methods for the underlying heap

    def _left(self, posn):
        """ Return the index of the left child of elt at index posn. """
        return 1 + 2*posn

    def _right(self, posn):
        """ Return the index of the right child of elt at index posn. """
        return 2 + 2*posn

    def _parent(self, posn):
        """ Return the index of the parent of elt at index posn. """
        return (posn - 1)//2
    
    def _upheap(self, posn):
        """ Bubble the item in posn in the heap up to its correct place. """
        if posn > 0 and self._upswap(posn, self._parent(posn)):
            self._upheap(self._parent(posn))

    def _upswap(self, posn, parent):
        """ If heap elt at posn has lower key than parent, swap. """
        if self._heap[posn] < self._heap[parent]:
            self._heap[posn], self._heap[parent] = self._heap[parent], self._heap[posn]
            self._heap[posn]._index = posn
            self._heap[parent]._index = parent
            return True
        return False

    def _downheap(self, posn):
        """ Bubble the item in posn in the heap down to its correct place. """
        #find minchild position
        #if minchild is in the heap
        #    if downswap with minchild succeeded
        #        downheap minchild
        minchild = self._left(posn)
        if minchild < self._size:
            if (minchild + 1 < self._size and
                self._heap[minchild]._key > self._heap[minchild + 1]._key):
                minchild +=1
            if self._downswap(posn, minchild):
                self._downheap(minchild)

    def _downswap(self, posn, child):
        """ If healp elt at posn has lower key than child, swap; else return False. """
        #Note: this could be merged with _upswap to provide a general
        #heapswap(first, second) method, which swaps if the element
        #first has lower key than the element second
        if self._heap[posn]._key > self._heap[child]._key:
            self._heap[posn], self._heap[child] = self._heap[child], self._heap[posn]
            self._heap[posn]._index = posn
            self._heap[child]._index = child
            return True
        return False

    def _printstructure(self):
        """ Print out the elements one to a line. """
        for elt in self._heap:
            if elt is not None:
                print('(', elt._key, ',', elt._value, ')')
            else:
                print('*')

    def _testadd():
        print('Testing that we can add items to an array-based binary heap APQ')
        apq = APQBinaryHeap()
        print('pq has size:', apq.length(), '(should be 0)')
        apq.add(25,'25')
        apq.add(4, '4')
        print('pq has size:', apq.length(), '(should be 2)')
        print(apq, '(should be 4,25, could also show index and value)')
        apq.add(19,'19')
        apq.add(12,'12')
        print(apq, '(should be 4,12,19,25)')
        apq.add(17,'17')
        apq.add(8,'8')
        print(apq, '(should be 4,12,8,25,17,19)')
        print('pq length:', apq.length(), '(should be 6)')
        print('pq min item:', apq.min(), '(should be 4)')
        print()
        return apq

    def _test():
        print('Testing that we can add and remove items from an array-based binary heap APQ')
        apq = APQBinaryHeap()
        print('pq has size:', apq.length())
        loc = {}
        print('Adding ant with value 25')
        loc['ant'] = apq.add(25,'ant')
        print('pq has size:', apq.length())
        print(apq)
        print('Adding bed with value 4')
        loc['bed'] = apq.add(4, 'bed')
        print(apq)
        print('Adding cat with value 14')
        loc['cat'] = apq.add(14,'cat')
        print(apq)
        print('Adding dog with value 12')
        loc['dog'] = apq.add(12,'dog')
        print(apq)
        print('Removing first')
        min = apq.remove_min()
        print("Just removed", str(min))
        print(apq)
        print('Adding egg with value 17')
        loc['egg'] = apq.add(17,'egg')
        print(apq)
        print('Adding fox with value 8')
        loc['fox'] = apq.add(8,'fox')
        print(apq)
        print('pq length:', apq.length())
        print('pq min item:', apq.min())
        for i in range(apq.length()):
            key, value = apq.remove_min()
            print('removed min (', key, value, '):', apq)
if __name__ == '__main__':
    APQBinaryHeap._testadd()
    APQBinaryHeap._test()
