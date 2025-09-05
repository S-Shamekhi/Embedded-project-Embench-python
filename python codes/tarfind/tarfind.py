import random

# This scale factor will be changed to equalize the runtime of the benchmarks.
CPU_MHZ = 100
LOCAL_SCALE_FACTOR = 47

# Number of files in the simulated archive
ARCHIVE_FILES = 35

# Number of searches to perform per run
N_SEARCHES = 5


class TarHeader:
    """
    A Python class to represent the C tar_header_t struct.
    We only really need the filename for this benchmark.
    """

    def __init__(self, filename=""):
        self.filename = filename
        # The other fields from the C struct are not needed for the logic,
        # but are conceptually part of the object.
        self.mode = ""
        self.uID = ""
        self.gID = ""
        self.size = "0"
        self.mtime = ""
        self.checksum = ""
        self.isLink = '0'
        self.linkedFile = ""


def benchmark_body(rpt):
    """
    The main body of the benchmark. It simulates creating TAR metadata
    and then searching for files within it.
    """
    final_found_count = 0

    for _ in range(rpt):
        # In the C code, a custom heap is initialized here. In Python, memory
        # management is automatic, so we just create a new list.
        archive = []

        # 1. Create the simulated archive headers
        for i in range(ARCHIVE_FILES):
            # Create a random filename of variable length
            flen = 5 + i % 94
            # Generate a list of random uppercase characters
            # ASCII 65 ('A') to 90 ('Z')
            random_chars = [chr(random.randint(65, 90)) for _ in range(flen)]
            filename = "".join(random_chars)

            # Create a header object and add it to our archive list
            header = TarHeader(filename=filename)
            archive.append(header)

        found_in_run = 0

        # 2. Search for N_SEARCHES files
        # The C code's memory access is noted as "inefficiently on purpose".
        for p in range(N_SEARCHES):
            # Pick a filename to search for from the middle of the generated list.
            # This ensures the file is always present.
            search_index = (p + ARCHIVE_FILES // 2) % ARCHIVE_FILES
            search_filename = archive[search_index].filename

            # Perform a linear search through the entire archive
            for header in archive:
                # The C code implements strcmp manually. In Python, the direct
                # and highly optimized equivalent is the '==' operator.
                if header.filename == search_filename:
                    found_in_run += 1
                    break  # Stop searching once found

        # The C code frees its custom heap here. Python's garbage collector
        # will handle the 'archive' list automatically when it goes out of scope.
        final_found_count = found_in_run

    # The benchmark returns true if the final run found all files.
    return final_found_count == N_SEARCHES


def verify_benchmark(r):
    """
    Verifies that the result is 1 (True), as all searched files should be found.
    """
    return r == 1


def main():
    """The main entry point of the program."""
    # A seed for the random number generator to ensure reproducibility,
    # similar to how the C benchmark framework would behave.
    random.seed(0)

    rpt = LOCAL_SCALE_FACTOR * CPU_MHZ
    result = benchmark_body(rpt)

    print(f"Final result indicates all files were found: {result}")

    if verify_benchmark(result):
        print("Verification: OK")
    else:
        print("Verification: FAIL")


if __name__ == "__main__":
    main()