import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"


class ConvexHullOnline:
    def __init__(self):
        self.points = []
        self.hull = []

    def add_point(self, new_point):
        """Добавляет новую точку и обновляет выпуклую оболочку"""
        print(f"\n--- Добавляем точку {new_point} ---")
        self.points.append(new_point)

        if len(self.points) <= 2:
            # Для 1-2 точек оболочка - все точки
            self.hull = self.points.copy()
            print(f"Только {len(self.points)} точки, оболочка: {self.hull}")
            return

        if len(self.hull) == 0:
            # Начальная оболочка - треугольник из первых трех точек
            self.hull = self.points[:3]
            # Убедимся, что оболочка выпуклая и обход против часовой стрелки
            self._make_counter_clockwise()
            print(f"Построили начальную оболочку: {self.hull}")
            return

        # Проверяем, находится ли точка внутри текущей оболочки
        if self._is_point_inside_hull(new_point):
            print(f"Точка {new_point} ВНУТРИ оболочки, не меняем")
            return
        else:
            print(f"Точка {new_point} СНАРУЖИ оболочки, перестраиваем...")

        # Находим левую и правую касательные
        left_tangent, right_tangent = self._find_tangents(new_point)
        print(f"Левая касательная: вершина {left_tangent} = {self.hull[left_tangent]}")
        print(f"Правая касательная: вершина {right_tangent} = {self.hull[right_tangent]}")

        # Строим новую оболочку
        self._rebuild_hull(new_point, left_tangent, right_tangent)
        print(f"Новая оболочка: {self.hull}")

    def _is_point_inside_hull(self, point):
        """Проверяет, находится ли точка внутри выпуклой оболочки"""
        n = len(self.hull)
        print("Проверка положения точки относительно оболочки:")

        for i in range(n):
            p1 = self.hull[i]
            p2 = self.hull[(i + 1) % n]
            cross = self._cross_product(p1, p2, point)

            print(f"  Ребро {p1}→{p2}: cross = {cross}", end="")

            if cross < 0:
                print(" → точка СПРАВА (снаружи!)")
                return False
            elif cross > 0:
                print(" → точка СЛЕВА")
            else:
                print(" → на линии")

        print("Точка слева от всех рёбер → ВНУТРИ")
        return True

    def _find_tangents(self, point):
        """Находит левую и правую касательные из точки к выпуклой оболочке"""
        n = len(self.hull)
        left_tangent = 0
        right_tangent = 0

        print("Поиск правой касательной (все точки слева от луча):")
        # Ищем правую касательную (все точки оболочки слева от луча)
        for i in range(n):
            if self._is_right_tangent(point, i):
                print(f"  Вершина {i}: {self.hull[i]} - ПРАВАЯ касательная ✓")
                right_tangent = i
                break
            else:
                print(f"  Вершина {i}: {self.hull[i]} - не подходит")

        print("Поиск левой касательной (все точки справа от луча):")
        # Ищем левую касательную (все точки оболочки справа от луча)
        for i in range(n):
            if self._is_left_tangent(point, i):
                print(f"  Вершина {i}: {self.hull[i]} - ЛЕВАЯ касательная ✓")
                left_tangent = i
                break
            else:
                print(f"  Вершина {i}: {self.hull[i]} - не подходит")

        return left_tangent, right_tangent

    def _is_right_tangent(self, point, vertex_index):
        """Проверяет, является ли луч из точки к вершине правой касательной"""
        n = len(self.hull)
        prev_vertex = self.hull[(vertex_index - 1) % n]
        vertex = self.hull[vertex_index]
        next_vertex = self.hull[(vertex_index + 1) % n]

        cross_prev = self._cross_product(point, vertex, prev_vertex)
        cross_next = self._cross_product(point, vertex, next_vertex)

        # Все точки должны быть слева от луча point→vertex (cross >= 0)
        result = cross_prev >= 0 and cross_next >= 0

        print(f"    Проверка вершины {vertex}: prev_cross={cross_prev}, next_cross={cross_next} → {result}")
        return result

    def _is_left_tangent(self, point, vertex_index):
        """Проверяет, является ли луч из точки к вершине левой касательной"""
        n = len(self.hull)
        prev_vertex = self.hull[(vertex_index - 1) % n]
        vertex = self.hull[vertex_index]
        next_vertex = self.hull[(vertex_index + 1) % n]

        cross_prev = self._cross_product(point, vertex, prev_vertex)
        cross_next = self._cross_product(point, vertex, next_vertex)

        # Все точки должны быть справа от луча point→vertex (cross <= 0)
        result = cross_prev <= 0 and cross_next <= 0

        print(f"    Проверка вершины {vertex}: prev_cross={cross_prev}, next_cross={cross_next} → {result}")
        return result

    def _rebuild_hull(self, new_point, left_tangent_idx, right_tangent_idx):
        """Перестраивает выпуклую оболочку с добавлением новой точки"""
        n = len(self.hull)
        new_hull = []

        print(f"Перестраиваем оболочку от вершины {right_tangent_idx} до {left_tangent_idx}")

        # Добавляем точки от правой касательной до левой
        i = right_tangent_idx
        while True:
            new_hull.append(self.hull[i])
            print(f"  Добавляем вершину {i}: {self.hull[i]}")
            if i == left_tangent_idx:
                break
            i = (i + 1) % n

        # Вставляем новую точку между точками касания
        insert_position = new_hull.index(self.hull[left_tangent_idx])
        print(f"Вставляем новую точку {new_point} после позиции {insert_position}")
        new_hull.insert(insert_position + 1, new_point)

        self.hull = new_hull

    def _make_counter_clockwise(self):
        """Убеждается, что оболочка обходится против часовой стрелки"""
        if len(self.hull) < 3:
            return

        # Вычисляем площадь (для определения направления)
        area = 0
        n = len(self.hull)
        for i in range(n):
            j = (i + 1) % n
            area += (self.hull[j].x - self.hull[i].x) * (self.hull[j].y + self.hull[i].y)

        # Если площадь положительная, меняем порядок
        if area > 0:
            print("Исправляем направление обхода на против часовой стрелки")
            self.hull.reverse()

    def _cross_product(self, a, b, c):
        """Векторное произведение AB × AC"""
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    def get_hull(self):
        """Возвращает текущую выпуклую оболочку"""
        return self.hull

    def plot(self, show=True):
        """Визуализирует точки и выпуклую оболочку"""
        plt.figure(figsize=(10, 8))

        # Рисуем все точки
        x_all = [p.x for p in self.points]
        y_all = [p.y for p in self.points]
        plt.scatter(x_all, y_all, color='blue', alpha=0.6, label='Все точки', s=100)

        # Подписываем точки
        for i, p in enumerate(self.points):
            plt.annotate(f'P{i + 1}({p.x},{p.y})', (p.x, p.y), xytext=(5, 5),
                         textcoords='offset points', fontsize=9)

        # Рисуем выпуклую оболочку
        if len(self.hull) > 1:
            x_hull = [p.x for p in self.hull] + [self.hull[0].x]
            y_hull = [p.y for p in self.hull] + [self.hull[0].y]
            plt.plot(x_hull, y_hull, 'r-', linewidth=2, label='Выпуклая оболочка')
            plt.scatter([p.x for p in self.hull], [p.y for p in self.hull],
                        color='red', s=80, zorder=5)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Пошаговое построение выпуклой оболочки')
        plt.legend()
        plt.grid(True, alpha=0.3)

        if show:
            plt.show()


def interactive_demo():
    """Интерактивная демонстрация с ручным вводом точек"""
    ch = ConvexHullOnline()

    print("=" * 60)
    print("ИНТЕРАКТИВНОЕ ПОСТРОЕНИЕ ВЫПУКЛОЙ ОБОЛОЧКИ")
    print("=" * 60)
    print("Вводите точки в формате: x y")
    print("Пример: 2 3")
    print("Для завершения введите: end")
    print("Для отображения графика введите: plot")
    print("Для очистки введите: clear")
    print("=" * 60)

    point_counter = 0

    while True:
        try:
            user_input = input(f"\nВведите точку {point_counter + 1} (или команду): ").strip()

            if user_input.lower() == 'end':
                print("Завершение работы.")
                break

            elif user_input.lower() == 'plot':
                if len(ch.points) > 0:
                    print("Отображаем график...")
                    ch.plot()
                else:
                    print("Нет точек для отображения!")

            elif user_input.lower() == 'clear':
                ch = ConvexHullOnline()
                point_counter = 0
                print("Очищено! Начинаем заново.")

            elif user_input.lower() == 'help':
                print("Доступные команды:")
                print("  x y - добавить точку (например: 2 3)")
                print("  plot - показать график")
                print("  clear - очистить все точки")
                print("  end - завершить работу")
                print("  help - показать эту справку")

            else:
                # Пытаемся разобрать координаты точки
                parts = user_input.split()
                if len(parts) == 2:
                    x = float(parts[0])
                    y = float(parts[1])

                    new_point = Point(x, y)
                    ch.add_point(new_point)
                    point_counter += 1

                    print(f"\n★ Текущее состояние:")
                    print(f"Всего точек: {len(ch.points)}")
                    print(f"Текущая оболочка ({len(ch.hull)} вершин): {ch.hull}")

                else:
                    print("Ошибка: введите две координаты через пробел!")

        except ValueError:
            print("Ошибка: координаты должны быть числами!")
        except KeyboardInterrupt:
            print("\nЗавершение работы.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    interactive_demo()
