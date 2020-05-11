import colorama
import enum
import random

class Color(enum.Enum):
    white = 0
    red = 1
    blue = 2
    orange = 3
    green = 4
    yellow = 5

    def color(self):
        return COLORAMA_COLORS[self]

COLORAMA_COLORS = {
    Color.white: colorama.Fore.WHITE,
    Color.red: colorama.Fore.RED,
    Color.blue: colorama.Fore.BLUE,
    Color.orange: colorama.Fore.MAGENTA,
    Color.green: colorama.Fore.GREEN,
    Color.yellow: colorama.Fore.YELLOW,
}

#     012
#     345
#     678
#
#     UUU
#     UUU
#     UUU
# LLL FFF RRR BBB
# LLL FFF RRR BBB
# LLL FFF RRR BBB
#     DDD
#     DDD
#     DDD
class RubiksCube(object):

    def __init__(self, up=None, front=None, right=None, back=None, left=None, down=None):
        self.up = up if up else [[Color.white] * 3] * 3
        self.front = front if front else [[Color.red] * 3] * 3
        self.right = right if right else [[Color.blue] * 3] * 3
        self.back = back if back else [[Color.orange] * 3] * 3
        self.left = left if left else [[Color.green] * 3] * 3
        self.down = down if down else [[Color.yellow] * 3] * 3

        self.__check()

    # X clockwise, x counterclockwise

    # 012    630
    # 345 -> 741
    # 678    852

    OPS = [
        'U', 'u', 'F', 'f', 'R', 'r', 'B', 'b', 'L', 'l', 'D', 'd', 'X', 'x', 'Y', 'y', 'Z', 'z',
    ]
    INVERSE = {
        'U': 'u',
        'u': 'U',
        'F': 'f',
        'f': 'F',
        'R': 'r',
        'r': 'R',
        'B': 'b',
        'b': 'B',
        'L': 'l',
        'l': 'L',
        'D': 'd',
        'd': 'D',
        'X': 'x',
        'x': 'X',
        'Y': 'y',
        'y': 'Y',
        'Z': 'z',
        'z': 'Z',
    }

    def shuffle(self, n=40):
        ops = list()
        inverses = list()
        for i in range(n):
            op = random.choice(self.OPS)
            ops.append(op)
            inverses.append(self.INVERSE[op])
        return self.do(ops), ''.join(reversed(inverses))

    def do(self, ops):
        rubiks_cube = self
        for op in ops:
            if op in self.OPS:
                rubiks_cube = RubiksCube.__dict__[op](rubiks_cube)
        return rubiks_cube

    def indices(self):
        result = list()
        for face in [self.up, self.front, self.right, self.back, self.left, self.down]:
            for row in face:
                for square in row:
                    result.append(square.value)
        return result

    @staticmethod
    def simplify(solution):
        solution = solution.replace('UUU', 'u')
        solution = solution.replace('uuu', 'U')
        solution = solution.replace('FFF', 'f')
        solution = solution.replace('fff', 'F')
        solution = solution.replace('RRR', 'r')
        solution = solution.replace('rrr', 'R')
        solution = solution.replace('BBB', 'b')
        solution = solution.replace('bbb', 'B')
        solution = solution.replace('LLL', 'l')
        solution = solution.replace('lll', 'L')
        solution = solution.replace('DDD', 'd')
        solution = solution.replace('ddd', 'D')
        solution = solution.replace('XXX', 'x')
        solution = solution.replace('xxx', 'X')
        solution = solution.replace('YYY', 'y')
        solution = solution.replace('yyy', 'Y')
        solution = solution.replace('ZZZ', 'z')
        solution = solution.replace('zzz', 'Z')
        solution = solution.replace('Uu', '')
        solution = solution.replace('uU', '')
        solution = solution.replace('Ff', '')
        solution = solution.replace('fF', '')
        solution = solution.replace('Rr', '')
        solution = solution.replace('rR', '')
        solution = solution.replace('Bb', '')
        solution = solution.replace('bB', '')
        solution = solution.replace('Ll', '')
        solution = solution.replace('lL', '')
        solution = solution.replace('Dd', '')
        solution = solution.replace('dD', '')
        solution = solution.replace('Xx', '')
        solution = solution.replace('xX', '')
        solution = solution.replace('Yy', '')
        solution = solution.replace('yY', '')
        solution = solution.replace('Zz', '')
        solution = solution.replace('zZ', '')
        return solution

    def FURurf(self):
        return self.F().U().R().u().r().f()

    def U(self):
        return RubiksCube(
            up=self.__clockwise(self.up),
            front=[
                self.right[0],
                self.front[1],
                self.front[2],
            ],
            right=[
                self.back[0],
                self.right[1],
                self.right[2],
            ],
            back=[
                self.left[0],
                self.back[1],
                self.back[2],
            ],
            left=[
                self.front[0],
                self.left[1],
                self.left[2],
            ],
            down=self.down,
        )

    def u(self):
        return RubiksCube(
            up=self.__counterclockwise(self.up),
            front=[
                self.left[0],
                self.front[1],
                self.front[2],
            ],
            right=[
                self.front[0],
                self.right[1],
                self.right[2],
            ],
            back=[
                self.right[0],
                self.back[1],
                self.back[2],
            ],
            left=[
                self.back[0],
                self.left[1],
                self.left[2],
            ],
            down=self.down,
        )

    def F(self):
        return RubiksCube(
            up=[
                self.up[0],
                self.up[1],
                [self.left[2][2], self.left[1][2], self.left[0][2]],
            ],
            front=self.__clockwise(self.front),
            right=[
                [self.up[2][0], self.right[0][1], self.right[0][2]],
                [self.up[2][1], self.right[1][1], self.right[1][2]],
                [self.up[2][2], self.right[2][1], self.right[2][2]],
            ],
            back=self.back,
            left=[
                [self.left[0][0], self.left[0][1], self.down[0][0]],
                [self.left[1][0], self.left[1][1], self.down[0][1]],
                [self.left[2][0], self.left[2][1], self.down[0][2]],
            ],
            down=[
                [self.right[2][0], self.right[1][0], self.right[0][0]],
                self.down[1],
                self.down[2],
            ],
        )

    def f(self):
        return RubiksCube(
            up=[
                self.up[0],
                self.up[1],
                [self.right[0][0], self.right[1][0], self.right[2][0]],
            ],
            front=self.__counterclockwise(self.front),
            right=[
                [self.down[0][2], self.right[0][1], self.right[0][2]],
                [self.down[0][1], self.right[1][1], self.right[1][2]],
                [self.down[0][0], self.right[2][1], self.right[2][2]],
            ],
            back=self.back,
            left=[
                [self.left[0][0], self.left[0][1], self.up[2][2]],
                [self.left[1][0], self.left[1][1], self.up[2][1]],
                [self.left[2][0], self.left[2][1], self.up[2][0]],
            ],
            down=[
                [self.left[0][2], self.left[1][2], self.left[2][2]],
                self.down[1],
                self.down[2],
            ],
        )

    def R(self):
        return RubiksCube(
            up=[
                [self.up[0][0], self.up[0][1], self.front[0][2]],
                [self.up[1][0], self.up[1][1], self.front[1][2]],
                [self.up[2][0], self.up[2][1], self.front[2][2]],
            ],
            front=[
                [self.front[0][0], self.front[0][1], self.down[0][2]],
                [self.front[1][0], self.front[1][1], self.down[1][2]],
                [self.front[2][0], self.front[2][1], self.down[2][2]],
            ],
            right=self.__clockwise(self.right),
            back=[
                [self.up[2][2], self.back[0][1], self.back[0][2]],
                [self.up[1][2], self.back[1][1], self.back[1][2]],
                [self.up[0][2], self.back[2][1], self.back[2][2]],
            ],
            left=self.left,
            down=[
                [self.down[0][0], self.down[0][1], self.back[2][0]],
                [self.down[1][0], self.down[1][1], self.back[1][0]],
                [self.down[2][0], self.down[2][1], self.back[0][0]],
            ],
        )

    def r(self):
        return RubiksCube(
            up=[
                [self.up[0][0], self.up[0][1], self.back[2][0]],
                [self.up[1][0], self.up[1][1], self.back[1][0]],
                [self.up[2][0], self.up[2][1], self.back[0][0]],
            ],
            front=[
                [self.front[0][0], self.front[0][1], self.up[0][2]],
                [self.front[1][0], self.front[1][1], self.up[1][2]],
                [self.front[2][0], self.front[2][1], self.up[2][2]],
            ],
            right=self.__counterclockwise(self.right),
            back=[
                [self.down[2][2], self.back[0][1], self.back[0][2]],
                [self.down[1][2], self.back[1][1], self.back[1][2]],
                [self.down[0][2], self.back[2][1], self.back[2][2]],
            ],
            left=self.left,
            down=[
                [self.down[0][0], self.down[0][1], self.front[0][2]],
                [self.down[1][0], self.down[1][1], self.front[1][2]],
                [self.down[2][0], self.down[2][1], self.front[2][2]],
            ],
        )

    def B(self):
        return RubiksCube(
            up=[
                [self.right[0][2], self.right[1][2], self.right[2][2]],
                self.up[1],
                self.up[2],
            ],
            front=self.front,
            right=[
                [self.right[0][0], self.right[0][1], self.down[2][2]],
                [self.right[1][0], self.right[1][1], self.down[2][1]],
                [self.right[2][0], self.right[2][1], self.down[2][0]],
            ],
            back=self.__clockwise(self.back),
            left=[
                [self.up[0][2], self.left[0][1], self.left[0][2]],
                [self.up[0][1], self.left[1][1], self.left[1][2]],
                [self.up[0][0], self.left[2][1], self.left[2][2]],
            ],
            down=[
                self.down[0],
                self.down[1],
                [self.left[0][0], self.left[1][0], self.left[2][0]],
            ],
        )

    def b(self):
        return RubiksCube(
            up=[
                [self.left[2][0], self.left[1][0], self.left[0][0]],
                self.up[1],
                self.up[2],
            ],
            front=self.front,
            right=[
                [self.right[0][0], self.right[0][1], self.up[0][0]],
                [self.right[1][0], self.right[1][1], self.up[0][1]],
                [self.right[2][0], self.right[2][1], self.up[0][2]],
            ],
            back=self.__counterclockwise(self.back),
            left=[
                [self.down[2][0], self.left[0][1], self.left[0][2]],
                [self.down[2][1], self.left[1][1], self.left[1][2]],
                [self.down[2][2], self.left[2][1], self.left[2][2]],
            ],
            down=[
                self.down[0],
                self.down[1],
                [self.right[2][2], self.right[1][2], self.right[0][2]],
            ],
        )

    def L(self):
        return RubiksCube(
            up=[
                [self.back[2][2], self.up[0][1], self.up[0][2]],
                [self.back[1][2], self.up[1][1], self.up[1][2]],
                [self.back[0][2], self.up[2][1], self.up[2][2]],
            ],
            front=[
                [self.up[0][0], self.front[0][1], self.front[0][2]],
                [self.up[1][0], self.front[1][1], self.front[1][2]],
                [self.up[2][0], self.front[2][1], self.front[2][2]],
            ],
            right=self.right,
            back=[
                [self.back[0][0], self.back[0][1], self.down[2][0]],
                [self.back[1][0], self.back[1][1], self.down[1][0]],
                [self.back[2][0], self.back[2][1], self.down[0][0]],
            ],
            left=self.__clockwise(self.left),
            down=[
                [self.front[0][0], self.down[0][1], self.down[0][2]],
                [self.front[1][0], self.down[1][1], self.down[1][2]],
                [self.front[2][0], self.down[2][1], self.down[2][2]],
            ],
        )

    def l(self):
        return RubiksCube(
            up=[
                [self.front[0][0], self.up[0][1], self.up[0][2]],
                [self.front[1][0], self.up[1][1], self.up[1][2]],
                [self.front[2][0], self.up[2][1], self.up[2][2]],
            ],
            front=[
                [self.down[0][0], self.front[0][1], self.front[0][2]],
                [self.down[1][0], self.front[1][1], self.front[1][2]],
                [self.down[2][0], self.front[2][1], self.front[2][2]],
            ],
            right=self.right,
            back=[
                [self.back[0][0], self.back[0][1], self.up[2][0]],
                [self.back[1][0], self.back[1][1], self.up[1][0]],
                [self.back[2][0], self.back[2][1], self.up[0][0]],
            ],
            left=self.__counterclockwise(self.left),
            down=[
                [self.back[2][2], self.down[0][1], self.down[0][2]],
                [self.back[1][2], self.down[1][1], self.down[1][2]],
                [self.back[0][2], self.down[2][1], self.down[2][2]],
            ],
        )

    def D(self):
        return RubiksCube(
            up=self.up,
            front=[
                self.front[0],
                self.front[1],
                self.left[2],
            ],
            right=[
                self.right[0],
                self.right[1],
                self.front[2],
            ],
            back=[
                self.back[0],
                self.back[1],
                self.right[2],
            ],
            left=[
                self.left[0],
                self.left[1],
                self.back[2],
            ],
            down=self.__clockwise(self.down),
        )

    def d(self):
        return RubiksCube(
            up=self.up,
            front=[
                self.front[0],
                self.front[1],
                self.right[2],
            ],
            right=[
                self.right[0],
                self.right[1],
                self.back[2],
            ],
            back=[
                self.back[0],
                self.back[1],
                self.left[2],
            ],
            left=[
                self.left[0],
                self.left[1],
                self.front[2],
            ],
            down=self.__counterclockwise(self.down),
        )

    def X(self):
        return RubiksCube(
            up=self.front,
            front=self.down,
            right=self.__clockwise(self.right),
            back=self.__clockwise(self.__clockwise(self.up)),
            left=self.__counterclockwise(self.left),
            down=self.__clockwise(self.__clockwise(self.back)),
        )

    def x(self):
        return RubiksCube(
            up=self.__clockwise(self.__clockwise(self.back)),
            front=self.up,
            right=self.__counterclockwise(self.right),
            back=self.__clockwise(self.__clockwise(self.down)),
            left=self.__clockwise(self.left),
            down=self.front,
        )

    def Y(self):
        return RubiksCube(
            up=self.__clockwise(self.up),
            front=self.right,
            right=self.back,
            back=self.left,
            left=self.front,
            down=self.__counterclockwise(self.down),
        )

    def y(self):
        return RubiksCube(
            up=self.__counterclockwise(self.up),
            front=self.left,
            right=self.front,
            back=self.right,
            left=self.back,
            down=self.__clockwise(self.down),
        )

    def Z(self):
        return RubiksCube(
            up=self.__clockwise(self.left),
            front=self.__clockwise(self.front),
            right=self.__clockwise(self.up),
            back=self.__counterclockwise(self.back),
            left=self.__clockwise(self.down),
            down=self.__clockwise(self.right),
        )

    def z(self):
        return RubiksCube(
            up=self.__counterclockwise(self.right),
            front=self.__counterclockwise(self.front),
            right=self.__counterclockwise(self.down),
            back=self.__clockwise(self.back),
            left=self.__counterclockwise(self.up),
            down=self.__counterclockwise(self.left),
        )

    def __check(self):
        count = dict()
        for face in [self.up, self.front, self.right, self.left, self.back, self.down]:
            for row in face:
                for square in row:
                    count[square] = count.setdefault(square, 0) + 1
        for key, value in count.items():
            if value != 9:
                 raise ValueError('%s has incorrect value %d' % (key, value))

    def __clockwise(self, face):
        return [
            [face[2][0], face[1][0], face[0][0]],
            [face[2][1], face[1][1], face[0][1]],
            [face[2][2], face[1][2], face[0][2]],
        ]

    def __counterclockwise(self, face):
        return [
            [face[0][2], face[1][2], face[2][2]],
            [face[0][1], face[1][1], face[2][1]],
            [face[0][0], face[1][0], face[2][0]],
        ]

    def __repr__(self):
        rows = [
            '\n   '.join(map(self.__repr_colors, self.up)),
            ''.join(map(self.__repr_color, self.left[0] + self.front[0] + self.right[0] + self.back[0])),
            ''.join(map(self.__repr_color, self.left[1] + self.front[1] + self.right[1] + self.back[1])),
            ''.join(map(self.__repr_color, self.left[2] + self.front[2] + self.right[2] + self.back[2])),
            '   ' + '\n   '.join(map(self.__repr_colors, self.down)),
        ]
        return 'RubiksCube(\n   %s\n)' % '\n'.join(rows)

    def __repr_colors(self, colors):
        return ''.join(map(self.__repr_color, colors)) + colorama.Style.RESET_ALL

    def __repr_color(self, color):
        return color.color() + '\u25A0'
