# Property Listing Engine

A lightweight, offline command-line application for Global Real Estates to manage property listings without external libraries or frameworks. This solution implements core data structures and custom algorithms to efficiently handle property data.

## Features

* Add property listings with auto-generated unique IDs
* Delete properties by ID
* Search properties by location (optimized with custom hash function)
* Search properties by price range (using binary search on sorted properties)
* Sort properties by price (ascending/descending) using custom QuickSort implementation
* Display all properties in a formatted table

## Data Structure Choices

1. **Primary Storage**:
   * List (`self.properties`) for storing all property objects
   * This allows for sequential access when displaying all properties

2. **Efficient Access**:
   * Location hashmap (`self.location_map`) for O(1) location lookups
   * ID hashmap (`self.id_map`) for O(1) property retrieval by ID

3. **Property Representation**:
   * Each property contains:
     * `id` (integer): Unique identifier (auto-incremented)
     * `title` (string): Property title
     * `location` (string): Property location
     * `price` (float): Property price
     * `property_type` (string): Type of property (apartment, house, plot, etc.)

## Algorithm Implementations

### Custom Hash Function for Locations
The hash function normalizes locations by converting to lowercase and removing spaces to handle minor variations in input. It uses a polynomial rolling hash algorithm with a prime multiplier (31) which provides good distribution for string data while minimizing collisions.

```python
def _hash_location(self, location):
    clean_location = location.lower().replace(" ", "")
    hash_value = 0
    prime = 31

    for char in clean_location:
        hash_value = prime * hash_value + ord(char) & 0xFFFFFFFF
    return hash_value
```

### Custom Sort Algorithm
The implementation uses QuickSort with the following characteristics:
* Uses middle element pivot selection to improve performance on partially sorted data
* Time Complexity: Average O(n log n), Worst-case O(n²)
* In-place sorting to minimize memory usage

### Binary Search for Price Range
The price range search works as follows:
1. Sort properties by price (using our custom sort)
2. Use binary search to find the lower bound of the price range
3. Use binary search to find the upper bound of the price range
4. Return all properties within those bounds

## User Interface

The application provides a simple console-based menu with the following options:
1. Add Property
2. Delete Property
3. Search by Location
4. Search by Price Range
5. Sort Properties by Price
6. Display All Properties
7. Exit

Each option includes input validation to handle potential user errors.

## Trade-offs and Limitations

1. **In-memory Storage**:
   * Fast access but data persists only during runtime
   * Limited by available system memory

2. **Hash Function**:
   * Simple collision handling using chaining 
   * Performance may degrade with many identical locations

3. **QuickSort Implementation**:
   * Uses middle element as pivot rather than median-of-three
   * Good average-case performance but has worst-case O(n²) for already sorted data

4. **Price Range Search**:
   * Requires sorting before searching by price range, adding O(n log n) overhead
   * For frequent price range searches, maintaining a continuously sorted copy would improve performance

5. **Exact Location Matching**:
   * The current implementation only supports exact location matches after normalization
   * No partial or fuzzy search capabilities

## Performance Analysis

* **Add Property**: O(1) amortized time
* **Delete Property**: O(n) due to list comprehension filtering
* **Search by Location**: O(1) average case using hashmap
* **Search by Price Range**: O(n log n) for sorting + O(log n) for binary search
* **Sort Properties**: O(n log n) using QuickSort

## How to Run

Simply execute the script:
```
python property_listing_engine.py
```

## Future Improvements

* Add data persistence via simple file I/O
* Implement fuzzy location search for better user experience
* Add more search criteria (property type, size, etc.)
* Optimize deletion operation to avoid O(n) list comprehensions
* Implement median-of-three pivot selection for better QuickSort performance# real
