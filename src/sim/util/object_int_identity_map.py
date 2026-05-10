from typing import TypeVar, Generic, Iterator, Optional

T = TypeVar('T')


class _IdentityKey:
    __slots__ = ('obj',)

    def __init__(self, obj):
        self.obj = obj

    def __hash__(self) -> int:
        return id(self.obj)

    def __eq__(self, other) -> bool:
        return isinstance(other, _IdentityKey) and self.obj is other.obj


class ObjectIntIdentityMap(Generic[T]):
    def __init__(self):
        self._identity_map: dict[_IdentityKey, int] = {}
        self._object_list: list[Optional[T]] = []

    def put(self, key: T, value: int) -> None:
        self._identity_map[_IdentityKey(key)] = value
        while len(self._object_list) <= value:
            self._object_list.append(None)
        self._object_list[value] = key

    def get(self, key: T) -> int:
        result = self._identity_map.get(_IdentityKey(key))
        return -1 if result is None else result

    def get_by_value(self, value: int) -> Optional[T]:
        if 0 <= value < len(self._object_list):
            return self._object_list[value]
        return None

    def __iter__(self) -> Iterator[T]:
        return (obj for obj in self._object_list if obj is not None)
