[← Home](Home.md) | [Main Home](../Home.md) | [Next: Java Cursors →](Java_Cursors.md)

# Java Collections Framework

## Overview
The Java Collections Framework provides a unified architecture for representing and manipulating collections. It contains interfaces, implementations, and algorithms that allow collections to be manipulated independently of implementation details.

## List Interface Implementations

### ArrayList
- **Default capacity**: 10
- **Growth formula**: (capacity * 3/2) + 1
- **Null elements**: Allowed
- **Special features**:
  - Implements RandomAccess interface (marker interface with 0 methods)
  - Present in java.util package
- **Performance characteristics**:
  - Best for retrieval operations (O(1) time complexity)
  - Worst for insertion and deletion in between (O(n) time complexity)
- **Example initialization**: `ArrayList a1 = new ArrayList(1)` - initializes with capacity 1
- **Internal structure**: Backed by a resizable array
- **Thread safety**: Not thread-safe
- **Usage scenarios**: 
  - When frequent access to elements is needed
  - When mostly adding elements at the end
  - When you need fast iteration

### LinkedList
- **Implementation**: Doubly-linked list
- **Null elements**: Allowed
- **Special features**:
  - Implements both List and Deque interfaces
  - Can function as a queue or stack
- **Performance characteristics**:
  - O(1) insertion and deletion at both ends
  - O(1) insertion and deletion in the middle (after finding position)
  - O(n) for random access
- **Internal structure**: Each element is a separate node with references to previous and next elements
- **Thread safety**: Not thread-safe
- **Memory overhead**: Higher than ArrayList due to storage of node references
- **Usage scenarios**:
  - When frequent insertion/deletion operations are needed
  - When implementing queues or stacks
  - When random access is rare

### Vector
- **Default capacity**: 10
- **Growth formula**: capacity * 2
- **Null elements**: Allowed
- **Special features**:
  - Implements RandomAccess interface
  - Thread-safe (all methods synchronized)
  - Legacy class, has been in Java since JDK 1.0
- **Performance characteristics**:
  - Similar to ArrayList but with thread safety overhead
  - O(1) for random access
  - O(n) for insertion/deletion in the middle
- **Internal structure**: Backed by a resizable array
- **Thread safety**: Thread-safe
- **Usage scenarios**:
  - Legacy code
  - When thread safety is required (though better alternatives exist in java.util.concurrent)

### Stack
- **Implementation**: Child class of Vector
- **Access pattern**: LIFO (Last-In-First-Out)
- **Special features**:
  - Inherits thread safety from Vector
  - Provides specific methods for stack operations
- **Key methods**:
  - `push(E item)`: Adds an item to the top of the stack
  - `pop()`: Removes and returns the item from the top
  - `peek()`: Returns but doesn't remove the top item
  - `empty()`: Checks if stack is empty
  - `search(Object o)`: Returns 1-based position from the top
- **Performance characteristics**:
  - O(1) for push and pop operations
  - Inherits Vector's performance characteristics
- **Internal structure**: Extends Vector, so backed by a resizable array
- **Thread safety**: Thread-safe (inherited from Vector)
- **Usage scenarios**:
  - When LIFO behavior is needed in a thread-safe context
  - For algorithms requiring stack data structure
  - *Note*: For modern applications, `Deque` implementations like `ArrayDeque` are preferred

## Set Interface Implementations

### Set
- **Key characteristic**: No duplicate elements
- **Implementation options**: HashSet, LinkedHashSet, TreeSet
- **Special features**:
  - Implements Collection interface
  - Modeling mathematical set abstraction
  - Can't access elements by index
- **Common operations**:
  - Add, remove, contains (element presence check)
  - Union, intersection, and difference of sets
- **Performance characteristics**:
  - Performance varies by implementation
  - HashSet: O(1) for basic operations
  - TreeSet: O(log n) for basic operations
- **Usage scenarios**:
  - When uniqueness of elements must be ensured
  - When performing set-algebraic operations
  - When order is not important (HashSet) or specific ordering is needed (TreeSet, LinkedHashSet)

## Utility Classes

### Array
- **Characteristics**: Fixed-size, primitive or object containers
- **Declaration syntax**: `type[] arrayName` or `type arrayName[]`
- **Key features**:
  - Direct memory allocation (continuous memory blocks)
  - Fixed size once initialized
  - Can store primitives or objects
  - Zero-based indexing
- **Limitations**:
  - Fixed size
  - No built-in methods
  - Manual array copying
- **Usage scenarios**:
  - When size is known and fixed
  - When direct access to elements by position is required
  - When maximum performance is needed

### Arrays
- **Type**: Utility class in java.util package
- **Purpose**: Provides static methods for array manipulation
- **Key methods**:
  - `sort()`: Sorts array elements
  - `binarySearch()`: Searches for element in sorted array
  - `equals()`: Compares arrays for equality
  - `fill()`: Assigns specified value to each element
  - `copyOf()`: Creates a new array copy with specified length
  - `asList()`: Returns a fixed-size List backed by the array
- **Performance characteristics**:
  - `sort()`: O(n log n) using dual-pivot Quicksort
  - `binarySearch()`: O(log n) for sorted arrays
- **Usage scenarios**:
  - Sorting and searching arrays
  - Converting between arrays and collections
  - Filling and manipulating array contents
  - Comparing arrays for equality

## Additional List Types

### Serialized List
- Lists that implement the Serializable interface
- Allows the list and its contents to be written to a stream and reconstructed later
- All standard collection implementations in Java are serializable
- **Key methods**:
  - `writeObject()`: Custom serialization
  - `readObject()`: Custom deserialization
- **Usage scenarios**:
  - Persisting collections to disk
  - Sending collections over a network
  - Deep copying collections

### Doubly Linked List
- Implemented in Java as the LinkedList class
- Each node contains references to both previous and next nodes
- **Special features**:
  - Allows traversal in both directions
  - Efficient insertion/deletion at both ends
  - Can serve as a Deque (double-ended queue)
- **Performance characteristics**:
  - O(1) time complexity for add/remove from beginning and end
  - O(n) time complexity for finding elements
- **Usage scenarios**:
  - When navigation in both directions is required
  - When implementing advanced data structures like LRU caches

## Cloneable Collections
- Collections that implement the Cloneable interface
- Standard collection implementations provide shallow cloning
- **Clone behavior**:
  - Collection structure is duplicated
  - References to contained objects are copied (not the objects themselves)
- **Deep cloning**:
  - Must be implemented manually
  - Often achieved through serialization/deserialization
- **Examples**:
  - ArrayList, LinkedList, Vector, and HashSet all implement Cloneable
- **Usage scenarios**:
  - When you need to modify a collection without affecting the original
  - Creating independent copies of collections

## Summary Comparison

| Collection | Random Access | Insertion/Deletion | Thread-Safe | Null Elements | Growth Strategy | Special Features |
|------------|---------------|-------------------|-------------|--------------|-----------------|-----------------|
| ArrayList  | O(1) - Fast   | O(n) - Slow       | No          | Yes          | (c*3/2)+1      | RandomAccess    |
| LinkedList | O(n) - Slow   | O(1) - Fast       | No          | Yes          | N/A             | Deque operations |
| Vector     | O(1) - Fast   | O(n) - Slow       | Yes         | Yes          | capacity*2     | Legacy, synchronized |
| Stack      | O(1) - Fast   | O(n) - Slow       | Yes         | Yes          | capacity*2     | LIFO operations |
| HashSet    | O(1) - Fast   | O(1) - Fast       | No          | Yes (one)    | N/A            | No duplicates   |

## Best Practices
- Choose ArrayList when random access is frequent
- Choose LinkedList when insertion/deletion is frequent
- Avoid Vector in new code unless thread safety is specifically needed
- Use interface types in variable declarations (e.g., `List<String>` instead of `ArrayList<String>`)
- Consider thread-safe alternatives from java.util.concurrent for multi-threaded environments

---

[← Home](Home.md) | [Main Home](../Home.md) | [Next: Java Cursors →](Java_Cursors.md) | [Back to Top](#java-collections-framework) 