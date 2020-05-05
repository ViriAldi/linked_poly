# Implementation of the Polynomial ADT using a sorted linked list.


class Polynomial :
    # Create a new polynomial object.
    def __init__(self, degree = None, coefficient = None):
        if degree is None :
            self._polyHead = None
        else :
            self._polyHead = _PolyTermNode(degree, coefficient)
        self._polyTail = self._polyHead

    # Return the degree of the polynomial.
    def degree(self):
        if self._polyHead is None :
            return -1
        else :
            return self._polyHead.degree

    # Return the coefficient for the term of the given degree.
    def __getitem__(self, degree):
        assert self.degree() >= 0, "Operation not permitted on an empty polynomial."
        curNode = self._polyHead
        while curNode is not None and curNode.degree > degree :
            curNode = curNode.next

        if curNode is None or curNode.degree != degree :
            return 0.0
        else :
            return curNode.coefficient

    # Evaluate the polynomial at the given scalar value.
    def evaluate(self, scalar):
        assert self.degree() >= 0, "Only non -empty polynomials can be evaluated."
        result = 0.0
        curNode = self._polyHead
        while curNode is not None :
            result += curNode.coefficient * (scalar ** curNode.degree)
            curNode = curNode.next
        return result

    # Polynomial addition: newPoly = self + rhsPoly.
    def __add__(self, rhsPoly):
        return self.simple_add(rhsPoly, 1)

    # Polynomial subtraction: newPoly = self - rhsPoly.
    def __sub__(self, rhsPoly):
        return self.simple_add(rhsPoly, -1)

    # Polynomial multiplication: newPoly = self * rhsPoly.
    def __mul__(self, rhsPoly):
        cur_node1 = self._polyHead
        ans = Polynomial()

        while cur_node1:
            cur_node2 = rhsPoly._polyHead
            while cur_node2:
                if cur_node1.coefficient * cur_node2.coefficient != 0:
                    ans._appendTerm(degree=cur_node1.degree + cur_node2.degree,
                                    value=cur_node1.coefficient * cur_node2.coefficient)
                cur_node2 = cur_node2.next
            cur_node1 = cur_node1.next

        return ans

    def simple_add(self, rhsPoly, k):
        newPoly = Polynomial()
        if self.degree() > rhsPoly.degree():
            maxDegree = self.degree()
        else:
            maxDegree = rhsPoly.degree()

        i = maxDegree
        while i >= 0:
            value = self[i] + rhsPoly[i] * k
            newPoly._appendTerm(i, value)
            i -= 1
        return newPoly

    def _appendTerm(self, degree, value):
        if degree < 0:
            raise ValueError

        if degree <= self.degree():
            cur_node = self._polyHead
            while cur_node.degree != degree:
                cur_node = cur_node.next
            cur_node.coefficient += value
            while self._polyHead.coefficient == 0 and self.degree() > 1:
                self._polyHead = self._polyHead.next
            return

        if value == 0:
            return

        cur_node = _PolyTermNode(degree, value)
        fst = cur_node
        while cur_node.degree != self.degree() + 1:
            cur_node.next = _PolyTermNode(cur_node.degree - 1, 0.0)
            cur_node = cur_node.next
        cur_node.next = self._polyHead
        self._polyHead = fst

    def __str__(self):
        ans = ""
        cur_node = self._polyHead

        while cur_node:
            if cur_node.coefficient:
                ans += str(cur_node) + " + "
            cur_node = cur_node.next

        return ans[:-2]


# Class for creating polynomial term nodes used with the linked list.
class _PolyTermNode(object):
    def __init__(self, degree, coefficient):
        self.degree = degree
        self.coefficient = coefficient
        self.next = None

    def __str__(self):
        """
        Prints the value stored in self.
        __str__: Node -> Str
        """
        return str(self.coefficient) + "x" + str(int(self.degree))
