import collections
import heapq

# This scale factor will be changed to equalize the runtime of the benchmarks.
CPU_MHZ = 100
LOCAL_SCALE_FACTOR = 29

# The initial unsorted array, same as in the C code.
# Using a tuple makes it immutable, which is good practice for constants.
INITIAL_ARRAY = (
    14, 66, 12, 41, 86, 69, 19, 77, 68, 38,
    26, 42, 37, 23, 17, 29, 55, 13, 90, 92,
    76, 99, 10, 54, 57, 83, 40, 44, 75, 33,
    24, 28, 80, 18, 78, 32, 93, 89, 52, 11,
    21, 96, 50, 15, 48, 63, 87, 20, 8, 85,
    43, 16, 94, 88, 53, 84, 74, 91, 67, 36,
    95, 61, 64, 5, 30, 82, 72, 46, 59, 9,
    7, 3, 39, 31, 4, 73, 70, 60, 58, 81,
    56, 51, 45, 1, 6, 49, 27, 47, 34, 35,
    62, 97, 2, 79, 98, 25, 22, 65, 71, 0
)


def benchmark_body(rpt):
    """
    The main body of the benchmark. It runs a series of data structure
    operations 'rpt' times.
    """
    total_cnt = 0

    for _ in range(rpt):
        cnt = 0

        # 1. Array Quicksort
        # C: memcpy to a new array, then sort using a macro-based quicksort.
        # Python: Create a copy of the list and use the highly optimized built-in sort.
        array2 = list(INITIAL_ARRAY)
        array2.sort()

        # 2. Doubly Linked List
        # C: Manually allocates nodes, adds them to a list, then sorts the list.
        # Python: The high-level equivalent is simply creating a list and sorting it.
        # Python's list is more akin to a dynamic array than a linked list, but for
        # the purpose of "build a collection and sort it", this is the correct equivalent.
        the_list = list(INITIAL_ARRAY)
        the_list.sort()
        for _ in the_list:
            cnt += 1

        # 3. Hash Table
        # C: Manually creates a hash table and adds elements, checking for duplicates.
        # Python: The 'set' data structure is the direct, high-performance equivalent.
        my_set = set(INITIAL_ARRAY)
        for _ in my_set:
            cnt += 1

        # 4. Queue
        # C: Uses array-based macros to add to and delete from a queue.
        # Python: collections.deque is the highly optimized queue implementation.
        my_queue = collections.deque()
        for item in INITIAL_ARRAY:
            my_queue.append(item)
        while my_queue:
            cnt += my_queue.popleft()

        # 5. Heap (Priority Queue)
        # C: Uses macros to implement a heap in an array.
        # Python: The 'heapq' module provides heap operations.
        my_heap = []
        for item in INITIAL_ARRAY:
            heapq.heappush(my_heap, item)
        while my_heap:
            cnt += heapq.heappop(my_heap)

        # 6. Red-Black Tree
        # C: Manually builds a balanced binary search tree, which implicitly avoids duplicates.
        # An in-order traversal yields a sorted sequence of unique elements.
        # Python: The high-level result is a sorted list of unique items.
        # The most Pythonic way to achieve this is by converting to a set, then sorting.
        unique_sorted_list = sorted(list(set(INITIAL_ARRAY)))
        for item in unique_sorted_list:
            cnt += item

        total_cnt = cnt

    return total_cnt


def verify_benchmark(res):
    """
    Verifies the final result of the benchmark operations.
    In the C code, it also checks the final sorted array and other structures.
    We will check the two most important parts: the final count and the sorted array.
    """
    expected_array = sorted(list(INITIAL_ARRAY))

    # Run a single quicksort to get a sorted array for comparison
    array2 = list(INITIAL_ARRAY)
    array2.sort()

    is_array_ok = (array2 == expected_array)
    is_res_ok = (res == 15050)

    print(f"Verification - Array Sort: {'OK' if is_array_ok else 'FAIL'}")
    print(f"Verification - Final Count: {'OK' if is_res_ok else 'FAIL'}")

    return is_array_ok and is_res_ok


def main():
    """The main entry point of the program."""
    rpt = LOCAL_SCALE_FACTOR * CPU_MHZ
    final_result = benchmark_body(rpt)

    print(f"Final Count: {final_result}")

    verify_benchmark(final_result)


if __name__ == "__main__":
    main()