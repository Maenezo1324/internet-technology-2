def check_relation(net: tuple, first: str, second: str) -> bool:
    """Проверяет, существует ли связь между двумя пользователями."""
    graph: dict = {}
    for person_a, person_b in net:
        if person_a not in graph:
            graph[person_a] = set()
        if person_b not in graph:
            graph[person_b] = set()
        graph[person_a].add(person_b)
        graph[person_b].add(person_a)

    if first not in graph or second not in graph:
        return False

    visited = set()
    queue = [first]

    while queue:
        current_node = queue.pop(0)
        if current_node == second:
            return True
        if current_node not in visited:
            visited.add(current_node)
            queue.extend(list(graph[current_node]))

    return False


if __name__ == '__main__':
    users_net = (
        ('Ваня', 'Лёша'), ('Лёша', 'Катя'),
        ('Ваня', 'Катя'), ('Вова', 'Катя'),
        ('Лёша', 'Лена'), ('Оля', 'Петя'),
        ('Стёпа', 'Оля'), ('Оля', 'Настя'),
        ('Настя', 'Дима'), ('Дима', 'Маша'),
    )

    assert check_relation(users_net, 'Петя', 'Стёпа') is True
    assert check_relation(users_net, 'Маша', 'Петя') is True
    assert check_relation(users_net, 'Ваня', 'Дима') is False
    assert check_relation(users_net, 'Лёша', 'Настя') is False
    assert check_relation(users_net, 'Стёпа', 'Маша') is True
    assert check_relation(users_net, 'Лена', 'Маша') is False
    assert check_relation(users_net, 'Вова', 'Лена') is True
    print('Все тесты пройдены успешно!')