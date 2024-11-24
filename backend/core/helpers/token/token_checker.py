"""Token checker
Used to rotate refresh tokens.
"""

import random


class TokenChecker:
    def __init__(self) -> None:
        """
        Initialize a new instance of the TokenChecker class.

        Attributes:
            tree (dict): A dictionary representing the token tree.
            range (int): The range of the token IDs.
        """
        self.tree = {}
        self.range = 1329227995784915872903807060280344576 # 16**30

        self.exc_msg_conflict = "Id key already exists"

    def __repr__(self):
        output = []
        for key, value in self.tree.items():
            output.append(f"'{key}': {value}")
        return "\n".join(output)

    def generate_add(self, prev_id: str = None) -> str:
        """
        Generate a new token ID and add it to the token tree.

        Args:
            prev_id (str): The ID of the previous token in the tree (optional).

        Returns:
            str: The newly generated token ID.
        """
        # https://stackoverflow.com/questions/2782229/most-lightweight-way-to-create-a-random-string-and-a-random-hexadecimal-number
        id_ = "%030x" % random.randrange(self.range)

        try:
            self.add(id_, prev_id)
        except ValueError as e:
            # Techincally possible for an infinite loop to appear
            if str(e) == self.exc_msg_conflict:
                return self.generate_add(prev_id)
            else: 
                raise e

        return id_

    def add(self, id_: str, prev_id: str = None):
        """
        Add a new token ID to the token tree.

        Args:
            id (str): The token ID to add.
            prev_id (str): The ID of the previous token in the tree (optional).

        Raises:
            ValueError: If the ID already exists in the tree.
            KeyError: If the previous ID does not exist in the tree.
        """
        if self._get(id_):
            raise ValueError(self.exc_msg_conflict)

        if prev_id:
            prev = self._get(prev_id)

            if not prev:
                raise KeyError("Previous Id does not exist")

            if prev["next"]:
                self._remove_tree(prev_id)
                raise ValueError("Id already has a next id. Removing tree...")

            self._set(prev_id, id_)

        self.tree[id_] = {"prev": prev_id, "next": None}

    def _get(self, id_: str):
        """
        Get the node with the given ID from the token tree.

        Args:
            id (str): The ID of the node to get.

        Returns:
            dict: A dictionary representing the node if found, None otherwise.
        """
        try:
            return self.tree[id_]
        except KeyError:
            return None

    def _set(self, id_: str, next_id: str):
        """
        Set the 'next' attribute of the node with the given ID to the given next ID.

        Args:
            id (str): The ID of the node to set.
            next_id (str): The ID of the next node in the tree.
        """
        self.tree[id_]["next"] = next_id

    def _remove_tree(self, id_: str):
        """
        Remove a node and all its children from the token tree.

        Args:
            id (str): The ID of the node to remove.
        """
        cur = self._get(id_)

        if cur["prev"]:
            prev = self._get(cur["prev"])

            if prev and prev["next"] == id_:
                prev_id = cur["prev"]
                self.tree[prev_id]["next"] = None
                self._remove_tree(prev_id)

        if cur["next"]:
            next = self._get(cur["next"])

            if next and next["prev"] == id_:
                next_id = cur["next"]
                self.tree[next_id]["prev"] = None
                self._remove_tree(next_id)
                
        del self.tree[id_]


token_checker = TokenChecker()
