import unittest


class Person:
    def __init__(self, unique_id, name=""):
        self.unique_id = unique_id
        self.name = name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.unique_id}, {self.name})'

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __eq__(self, other):
        return self.unique_id == other.unique_id


class Client(Person):
    pass


class Employee(Person):
    def __init__(self, unique_id, name="", salary=0):
        super().__init__(unique_id, name)
        self.salary = salary

    def __repr__(self):
        return f'{self.__class__.__name__}({self.unique_id}, {self.name}, {self.salary})'


class Group:
    def __init__(self, person_list):
        self.person_list = person_list.copy()
        self.current_person = 0

    def __repr__(self):
        return f'Group({self.person_list})'

    def __iter__(self):
        self.current_person = 0
        return self

    def __next__(self):
        if self.current_person >= len(self.person_list):
            raise StopIteration
        index = self.current_person
        self.current_person += 1
        return self.person_list[index]


#########
# Testing


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.people = [
            Client(7, 'Sally'),
            Employee(3, 'Bob', 100),
            Client(9, 'Alice'),
            Employee(2, 'George', 110)]

    def test_init(self):
        self.assertTrue(self.people[3].unique_id == 2)
        self.assertTrue(self.people[3].name == 'George')
        self.assertTrue(self.people[0].unique_id == 7)
        self.assertTrue(self.people[0].name == 'Sally')
        other_person = Person(1)
        self.assertTrue(other_person.unique_id == 1)
        self.assertTrue(other_person.name == '')

    def test_repr(self):
        person_repr = self.people[0].__repr__()
        self.assertTrue(person_repr.find('Client') == 0)
        self.assertTrue(person_repr.find('Sally') > 0)
        self.assertTrue(person_repr.find('7') > 0)
        person_repr = self.people[1].__repr__()
        self.assertTrue(person_repr.find('Employee') == 0)
        self.assertTrue(person_repr.find('Bob') > 0)
        self.assertTrue(person_repr.find('3') > 0)

    def test_sortable(self):
        self.assertTrue(self.people[0].unique_id == 7)
        self.people.sort()
        self.assertTrue(self.people[0].unique_id == 2)

    def test_equality(self):
        self.assertTrue(self.people[0] != self.people[2])
        self.assertTrue(self.people[2] == self.people[2])
        self.assertTrue(self.people[0] in self.people)
        other_person = Employee(3)
        self.assertTrue(other_person in self.people)
        other_person = Employee(6)
        self.assertTrue(other_person not in self.people)


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.people = [
            Client(7, 'Sally'),
            Employee(3, 'Bob'),
            Client(9, 'Alice'),
            Employee(2, 'George', 110)]

    def test_init(self):
        self.assertTrue(self.people[3].salary == 110)
        self.assertTrue(self.people[3].name == 'George')
        self.assertTrue(self.people[1].salary == 0)
        self.assertTrue(self.people[1].name == 'Bob')


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.people = [
            Client(7, 'Sally'),
            Employee(3, 'Bob', 100),
            Client(9, 'Alice'),
            Employee(2, 'George', 110)]

    def test_init(self):
        group = Group(self.people)
        self.assertTrue(len(group.person_list) == 4)
        person = self.people.pop(1)
        self.assertTrue(len(group.person_list) == 4)
        self.assertTrue(person not in self.people)
        self.assertTrue(person in group.person_list)

    def test_iterable(self):
        group = Group(self.people)
        for i, person in enumerate(group):
            if i == 2:
                self.assertTrue(person.name == 'Alice')


if __name__ == '__main__':
    unittest.main()
