[← Collections Framework](Java_Collections_Framework.md) | [Home](Home.md) | [Main Home](../Home.md)

# Java Cursors

## Overview
Java cursors are interfaces that provide mechanisms to traverse through elements in collections. They allow sequential access to collection elements without exposing the underlying structure. Each cursor implementation has different capabilities and is designed for specific use cases.

## Types of Cursors

### Enumeration

- **Package**: `java.util.Enumeration`
- **Applicable for**: Legacy collections (primarily Vector and Hashtable)
- **Direction**: Forward-only
- **Operations**: Read-only access
- **Creation method**: Obtained via `elements()` method
- **Thread-safety**: Not fail-fast (doesn't throw ConcurrentModificationException)
- **Status**: Legacy interface, still supported but generally replaced by Iterator

#### Key Methods
- **`hasMoreElements()`**: Returns true if there are more elements to iterate
- **`nextElement()`**: Returns the next element in the collection
- **`asIterator()`**: Converts this Enumeration to an Iterator (Java 9+)

#### Usage Example
```java
public static void main(String[] args) {
    Vector v1 = new Vector<>();

    for (int i=1; i<=10; i++) {
        v1.add(i);
    }

    Enumeration e1 = v1.elements();
    do {
        Integer i1 = (Integer) e1.nextElement();
        System.out.println(i1);
    } while(e1.hasMoreElements());
}
```

#### Limitations
- Only supports read operations
- No remove functionality
- Limited to legacy collections
- Lacks support for generics (in original form)

### Iterator

- **Package**: `java.util.Iterator`
- **Applicable for**: All Collection implementations
- **Direction**: Forward-only
- **Operations**: Read and remove
- **Creation method**: Obtained via `iterator()` method
- **Thread-safety**: Fail-fast (throws ConcurrentModificationException if collection modified during iteration)
- **Status**: Standard iterator interface since Java 1.2

#### Key Methods
- **`hasNext()`**: Returns true if the iteration has more elements
- **`next()`**: Returns the next element in the iteration
- **`remove()`**: Removes the last element returned by next() (optional operation)
- **`forEachRemaining(Consumer<? super E> action)`**: Performs the given action for each remaining element (Java 8+)

#### Usage Example
```java
public static void main(String[] args) {
    ArrayList a1 = new ArrayList();
    a1.add(10);
    a1.add(20);
    a1.add(30);

    Iterator i1 = a1.iterator();

    do {
        Integer i2 = (Integer) i1.next();
        if(i2 % 5 == 0) {
            i1.remove();
        } else {
            System.out.println(i2);
        }
    } while (i1.hasNext());
}
```

#### Key Features
- Universal support across Java Collections Framework
- Supports element removal during iteration
- Provides fail-fast behavior
- Supports generics for type safety
- Enhanced with functional programming methods in Java 8+

### ListIterator

- **Package**: `java.util.ListIterator`
- **Applicable for**: List implementations only
- **Direction**: Bidirectional (forward and backward)
- **Operations**: Read, add, remove, and replace
- **Creation method**: Obtained via `listIterator()` or `listIterator(int index)` method
- **Thread-safety**: Fail-fast (throws ConcurrentModificationException if collection modified during iteration)
- **Status**: Extended iterator interface for Lists

#### Key Methods
- **Inherited methods**: All methods from Iterator
- **`hasPrevious()`**: Returns true if there are elements before the current position
- **`previous()`**: Returns the previous element in the list
- **`nextIndex()`**: Returns the index of the element that would be returned by a call to next()
- **`previousIndex()`**: Returns the index of the element that would be returned by a call to previous()
- **`add(E e)`**: Inserts the specified element into the list
- **`set(E e)`**: Replaces the last element returned by next() or previous()

#### Key Features
- Most powerful cursor in Java
- Bidirectional traversal
- Position-aware (can report indices)
- Supports element modification, addition, and removal
- List-specific functionality

## Comparison of Cursors

| Feature | Enumeration | Iterator | ListIterator |
|---------|-------------|----------|--------------|
| Package | java.util | java.util | java.util |
| Applicable Collections | Legacy (Vector, Hashtable) | All Collections | Lists only |
| Direction | Forward | Forward | Bidirectional |
| Read Operation | Yes | Yes | Yes |
| Remove Operation | No | Yes | Yes |
| Replace Operation | No | No | Yes |
| Add Operation | No | No | Yes |
| Method for Next Check | hasMoreElements() | hasNext() | hasNext() |
| Method for Next Element | nextElement() | next() | next() |
| Method for Previous Check | Not Available | Not Available | hasPrevious() |
| Method for Previous Element | Not Available | Not Available | previous() |
| Fail-Fast | No | Yes | Yes |
| Legacy Status | Yes | No | No |

## Best Practices

1. **General use**: Prefer Iterator over Enumeration for most cases
2. **Modern code**: Use enhanced for-loop where possible (uses Iterator behind the scenes)
3. **List traversal**: Use ListIterator when bidirectional traversal or element modification is needed
4. **Legacy code**: Continue using Enumeration when working with older APIs that return it
5. **Functional approach**: For Java 8+, consider Stream API as an alternative to traditional cursors
6. **Concurrent collections**: Use specialized iterators from java.util.concurrent for thread-safety

## Stream API as Modern Alternative

For Java 8 and later, the Stream API often provides a more elegant and functional approach to collection traversal and manipulation:

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// Using Stream API instead of iterator
numbers.stream()
       .filter(n -> n % 2 == 0)
       .map(n -> n * n)
       .forEach(System.out::println);
```

---

[← Collections Framework](Java_Collections_Framework.md) | [Home](Home.md) | [Main Home](../Home.md) | [Back to Top](#java-cursors) 