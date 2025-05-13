class Property:
    def __init__(self, property_id, title, location, price, property_type):
        # simple class to represent a real estate property with basic attributes
        # keeps track of essential info that any property listing would need
        self.id = property_id
        self.title = title
        self.location = location
        self.price = price
        self.property_type = property_type

class PropertyListingEngine:
    def __init__(self):
        # main engine class that manages all property operations
        # using multiple data structures for efficient lookups:
        # - list for sequential access
        # - hash maps for O(1) lookups by location and id
        self.properties = []  # main list to store all properties
        self.location_map = {}  # hash map for location-based searches
        self.id_map = {}  # hash map for direct id access
        self.next_id = 1  # auto-increment id counter

    def add_property(self, title, location, price, property_type):
        # creates and adds a new property to the system
        # maintains all our data structures to ensure consistency
        property_id = self.next_id
        self.next_id += 1

        new_property = Property(property_id, title, location, price, property_type)
        self.properties.append(new_property)

        # update our location map for efficient location-based searches
        location_key = self._hash_location(location)
        if location_key not in self.location_map:
            self.location_map[location_key] = []
        self.location_map[location_key].append(new_property)

        # update our id map for O(1) lookups by id
        self.id_map[property_id] = new_property

        return property_id

    def delete_property(self, property_id):
        # removes a property from all data structures
        # returns true if successful, false if property not found
        if property_id not in self.id_map:
            return False

        deleted_property = self.id_map[property_id]

        # remove from our id lookup map
        del self.id_map[property_id]

        # remove from main properties list
        self.properties = [prop for prop in self.properties if prop.id != property_id]

        # remove from location map
        location_key = self._hash_location(deleted_property.location)
        if location_key in self.location_map:
            self.location_map[location_key] = [
                prop for prop in self.location_map[location_key]
                if prop.id != property_id
            ]

        return True

    def search_by_location(self, location):
        # constant time search by location using our hash map
        # returns properties in the specified location
        location_key = self._hash_location(location)
        if location_key in self.location_map:
            return self.location_map[location_key]
        return []

    def search_by_price_range(self, min_price, max_price):
        # find properties within a price range using binary search
        # first sort by price, then find boundaries of the range
        sorted_properties = self.sort_properties_by_price(True)

        # find first property >= min_price and last property <= max_price
        start_idx = self._binary_search_min_price(sorted_properties, min_price)
        end_idx = self._binary_search_max_price(sorted_properties, max_price)

        if start_idx <= end_idx and start_idx < len(sorted_properties):
            return sorted_properties[start_idx:end_idx + 1]
        return []

    def sort_properties_by_price(self, ascending=True):
        # sorts properties by price using quicksort
        # returns a new list without modifying original
        if not self.properties:
            return []

        result = self.properties.copy()
        self._quick_sort_by_price(result, 0, len(result) - 1)

        if not ascending:
            return result[::-1]

        return result

    def _quick_sort_by_price(self, items, low, high):
        # standard quicksort implementation specialized for price sorting
        # chose quicksort for average O(n log n) performance
        # base case: if the range is invalid or has one item, do nothing
        if low >= high:
            return

        # choose middle item as pivot index to avoid worst-case with sorted data
        mid_index = (low + high) // 2
        pivot_index = mid_index

        # move pivot to end for simplicity
        items[pivot_index], items[high] = items[high], items[pivot_index]
        pivot_price = items[high].price

        # partitioning step
        left_pointer = low
        for current in range(low, high):
            if items[current].price <= pivot_price:
                items[left_pointer], items[current] = items[current], items[left_pointer]
                left_pointer += 1

        # place pivot in its correct sorted position
        items[left_pointer], items[high] = items[high], items[left_pointer]

        # recursively sort left and right subarrays
        self._quick_sort_by_price(items, low, left_pointer - 1)
        self._quick_sort_by_price(items, left_pointer + 1, high)

    def get_all_properties(self):
        # simple accessor method to return all properties
        return self.properties

    def _hash_location(self, location):
        # custom hash function for location strings
        # normalizes locations by removing spaces and casing
        # uses a polynomial rolling hash algorithm
        clean_location = location.lower().replace(" ", "")
        hash_value = 0
        prime = 31

        for char in clean_location:
            hash_value =  (prime * hash_value + ord(char)) & 0xFFFFFFFF
        return hash_value

    def _binary_search_min_price(self, sorted_properties, min_price):
        # binary search to find first property with price >= min_price
        # more efficient than linear search for large datasets
        left, right = 0, len(sorted_properties) - 1
        result = len(sorted_properties)

        while left <= right:
            mid = (left + right) // 2
            if sorted_properties[mid].price >= min_price:
                result = mid
                right = mid - 1
            else:
                left = mid + 1

        return result

    def _binary_search_max_price(self, sorted_properties, max_price):
        # binary search to find last property with price <= max_price
        # paired with min_price search to efficiently find price ranges
        left, right = 0, len(sorted_properties) - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2
            if sorted_properties[mid].price <= max_price:
                result = mid
                left = mid + 1
            else:
                right = mid - 1

        return result

    def display_properties_table(self, properties):
        print(f"{'ID':<5} {'Title':<20} {'Location':<15} {'Price':<10} {'Type':<10}")
        print("-" * 65)
        for p in properties:
            print(f"{p.id:<5} {p.title:<20} {p.location:<15} ${p.price:<9.2f} {p.property_type:<10}")


def main():
    # entry point for the application
    # simple console-based menu for interaction
    engine = PropertyListingEngine()

    while True:
        print("\n=== WELCOME TO GLOBAL REAL ESTATES - PROPERTY LISTING ENGINE ===")
        print("1. Add Property")
        print("2. Delete Property")
        print("3. Search by Location")
        print("4. Search by Price Range")
        print("5. Sort Properties by Price")
        print("6. Display All Properties")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == "1":
            # add new property with input validation
            title = input("Enter property title: ")
            location = input("Enter location: ")

            while True:
                try:
                    price = float(input("Enter price: $"))
                    if price < 0:
                        print("Price cannot be negative. Please try again.")
                        continue
                    break
                except ValueError:
                    print("Invalid price. Please enter a number.")

            property_type = input("Enter property type (apartment, house, plot, etc.): ")

            property_id = engine.add_property(title, location, price, property_type)
            print(f"Property added successfully with ID: {property_id}")

        elif choice == "2":
            # delete property with basic error handling
            try:
                property_id = int(input("Enter property ID to delete: "))
                if engine.delete_property(property_id):
                    print(f"Property with ID {property_id} deleted successfully.")
                else:
                    print(f"Property with ID {property_id} not found.")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "3":
            # search by location feature
            location = input("Enter location to search: ")
            results = engine.search_by_location(location)

            if results:
                print(f"\nFound {len(results)} properties in {location}:")
                engine.display_properties_table(results)
            else:
                print(f"No properties found in {location}.")

        elif choice == "4":
            # search by price range with validation
            try:
                min_price = float(input("Enter minimum price: $"))
                max_price = float(input("Enter maximum price: $"))

                if min_price > max_price:
                    print("Minimum price cannot be greater than maximum price.")
                    continue

                results = engine.search_by_price_range(min_price, max_price)

                if results:
                    print(f"\nFound {len(results)} properties between ${min_price:.2f} and ${max_price:.2f}:")
                    engine.display_properties_table(results)
                else:
                    print(f"No properties found between ${min_price:.2f} and ${max_price:.2f}.")
            except ValueError:
                print("Invalid price. Please enter a number.")

        elif choice == "5":
            # sorting feature with direction option
            sort_order = input("Sort by price (A)scending or (D)escending? ").upper()

            if sort_order not in ['A', 'D']:
                print("Invalid choice. Please enter 'A' or 'D'.")
                continue

            ascending = (sort_order == 'A')
            sorted_properties = engine.sort_properties_by_price(ascending)

            if sorted_properties:
                print(f"\nProperties sorted by price ({'ascending' if ascending else 'descending'}):")
                engine.display_properties_table(sorted_properties)
            else:
                print("No properties to sort.")

        elif choice == "6":
            # display all properties
            properties = engine.get_all_properties()

            if properties:
                print(f"\nAll Properties ({len(properties)}):")
                engine.display_properties_table(properties)
            else:
                print("No properties found.")

        elif choice == "7":
            # exit the application
            print("Thank you for using Global Real Estates Property Listing Engine. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()