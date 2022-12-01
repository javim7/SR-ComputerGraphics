class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.tvertices = []
        self.faces = []

        for line in self.lines:
            if not line:
                continue

            if (len(line) == 1):
                pass
            else:
                prefix, value = line.strip().split(' ', 1)

                if prefix == 'v':
                    self.vertices.append(
                        list(
                            map(float, value.split(' '))
                        )
                    )
                if prefix == 'vt':
                    self.tvertices.append(
                        list(
                            map(float, value.strip().split(' '))
                        )
                    )
                if prefix == 'f':
                    try:
                        self.faces.append([
                            list(map(int, face.split('/')))
                            for face in value.split(' ')
                        ])
                    except:
                        self.faces.append([
                            list(map(int, face.split('//')))
                            for face in value.split(' ')
                        ])
