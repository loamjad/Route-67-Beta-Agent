from typing import Optional, TypeVar

V = TypeVar('V')


class LongHashMap:

    class _Entry:
        __slots__ = ('key', 'value', 'next_entry', 'hash')

        def __init__(self, hash_val: int, key: int, value, next_entry: Optional['LongHashMap._Entry']):
            self.hash = hash_val
            self.key = key
            self.value = value
            self.next_entry = next_entry

        def get_key(self) -> int:
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other) -> bool:
            if not isinstance(other, LongHashMap._Entry):
                return False
            return self.key == other.key and self.value == other.value

        def __hash__(self) -> int:
            return LongHashMap._get_hashed_key(self.key)

        def __str__(self) -> str:
            return f"{self.key}={self.value}"

    def __init__(self):
        self._hash_array: list = [None] * 4096
        self._num_hash_elements: int = 0
        self._mask: int = len(self._hash_array) - 1
        self._capacity: int = 3072
        self._percent_useable: float = 0.75
        self._mod_count: int = 0

    @staticmethod
    def _get_hashed_key(original_key: int) -> int:
        original_key = original_key & 0xFFFFFFFFFFFFFFFF
        val = (original_key ^ (original_key >> 32)) & 0xFFFFFFFF
        return LongHashMap._hash(val)

    @staticmethod
    def _hash(integer: int) -> int:
        integer = integer & 0xFFFFFFFF
        integer = integer ^ (integer >> 20) ^ (integer >> 12)
        integer = integer & 0xFFFFFFFF
        return (integer ^ (integer >> 7) ^ (integer >> 4)) & 0xFFFFFFFF

    @staticmethod
    def _get_hash_index(hashed_key: int, mask: int) -> int:
        return hashed_key & mask

    def get_num_hash_elements(self) -> int:
        return self._num_hash_elements

    def get_value_by_key(self, key: int):
        i = self._get_hashed_key(key)
        entry = self._hash_array[self._get_hash_index(i, self._mask)]
        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next_entry
        return None

    def contains_item(self, key: int) -> bool:
        return self._get_entry(key) is not None

    def _get_entry(self, key: int) -> Optional['LongHashMap._Entry']:
        i = self._get_hashed_key(key)
        entry = self._hash_array[self._get_hash_index(i, self._mask)]
        while entry is not None:
            if entry.key == key:
                return entry
            entry = entry.next_entry
        return None

    def add(self, key: int, value) -> None:
        i = self._get_hashed_key(key)
        j = self._get_hash_index(i, self._mask)
        entry = self._hash_array[j]
        while entry is not None:
            if entry.key == key:
                entry.value = value
                return
            entry = entry.next_entry
        self._mod_count += 1
        self._create_key(i, key, value, j)

    def _resize_table(self, new_size: int) -> None:
        if len(self._hash_array) == 1073741824:
            self._capacity = 2147483647
        else:
            new_array = [None] * new_size
            self._copy_hash_table_to(new_array)
            self._hash_array = new_array
            self._mask = len(self._hash_array) - 1
            self._capacity = int(new_size * self._percent_useable)

    def _copy_hash_table_to(self, new_array: list) -> None:
        old_array = self._hash_array
        new_len = len(new_array)
        for j in range(len(old_array)):
            entry1 = old_array[j]
            if entry1 is not None:
                old_array[j] = None
                while True:
                    entry2 = entry1.next_entry
                    k = self._get_hash_index(entry1.hash, new_len - 1)
                    entry1.next_entry = new_array[k]
                    new_array[k] = entry1
                    entry1 = entry2
                    if entry2 is None:
                        break

    def remove(self, key: int):
        entry = self._remove_key(key)
        return None if entry is None else entry.value

    def _remove_key(self, key: int) -> Optional['LongHashMap._Entry']:
        i = self._get_hashed_key(key)
        j = self._get_hash_index(i, self._mask)
        entry = self._hash_array[j]
        entry1 = entry
        while entry1 is not None:
            entry2 = entry1.next_entry
            if entry1.key == key:
                self._mod_count += 1
                self._num_hash_elements -= 1
                if entry is entry1:
                    self._hash_array[j] = entry2
                else:
                    entry.next_entry = entry2
                return entry1
            entry = entry1
            entry1 = entry2
        return entry1

    def _create_key(self, hash_val: int, key: int, value, index: int) -> None:
        existing = self._hash_array[index]
        self._hash_array[index] = LongHashMap._Entry(hash_val, key, value, existing)
        count = self._num_hash_elements
        self._num_hash_elements += 1
        if count >= self._capacity:
            self._resize_table(2 * len(self._hash_array))
