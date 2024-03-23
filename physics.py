import numpy as np

# DIM is a vector which contains dimensions of the environment
# dt is time of one step of simulation
class Environment():
    def __init__(self, DIM, GRAVITY, dt):
        self.DIM = DIM
        self.GRAVITY = GRAVITY
        self.dt = dt
        self.particles = []

    def update(self):
        for p1 in self.particles:
            p1.stateUpdate()
            self.bounce(p1)
            for p2 in self.particles:
                if p1!=p2:
                    self.elasticCollision(p1, p2)


    def addParticle(self, p):
        self.particles += [p]
        # default acceleration is gravity
        p.addAcceleration(self.GRAVITY)

    def bounce(self, p):
        for p in self.particles:
            for i, x in enumerate(p.X):
                if x > self.DIM[i] - p.radius:
                    dist = p.radius - (self.DIM[i] - x)
                    p.addPosition(-dist)
                    # returns a zero-filled array of the set size
                    tmp = np.zeros(np.size(p.X))
                    tmp[i] = -2 * p.V[i]
                    p.addVelocity(tmp)
                elif x < p.radius:
                    dist = p.radius - x
                    p.addPosition(dist)
                    tmp = np.zeros(np.size(p.X))
                    tmp[i] = -2 * p.V[i]
                    p.addVelocity(tmp)


    def elasticCollision(self, p1, p2):
        dX = p1.X - p2.X
        # a*a + b*b = c*c
        dist = np.sqrt(np.sum(dX ** 2))
        if dist < p1.radius + p2.radius:
            # if there started entering each other
            # offset is clipping distance
            offset = dist - p1.radius - p2.radius
            p1.addPosition((-dX / dist) * offset / 2)
            p2.addPosition((dX / dist) * offset / 2)
            totalMass = p1.mass + p2.mass
            dv1 = -2 * p2.mass / totalMass * np.inner(p1.V - p2.V, p1.X - p2.X) / np.sum((p1.X - p2.X) ** 2) * (
                        p1.X - p2.X)
            dv2 = -2 * p1.mass / totalMass * np.inner(p2.V - p1.V, p2.X - p1.X) / np.sum((p2.X - p1.X) ** 2) * (
                        p2.X - p1.X)
            p1.addVelocity(dv1)
            p2.addVelocity(dv2)

    def plasticCollision(self):
        pass


# X position
# V velocity
# A acceleration
class Particle():
    def __init__(self, env, X, V, A, radius, mass, density):
        self.env = env
        self.X = X
        self.V = V
        self.A = A
        self.radius = radius
        self.mass = mass
        self.density = density
        self.color = (0, 0, int((density - 5) / 95 * 240 + 15))

    def addForce(self, F):
        # The second Newton's law
        self.A += F / self.mass

    def addAcceleration(self, acc):
        self.A += acc

    def addVelocity(self, vel):
        self.V += vel

    def addPosition(self, pos):
        self.X += pos

    def attract(self, particle):
        pass

    def stateUpdate(self):
        # because acceleration is velocity-changer
        # and density is also velocity-changer
        self.V += self.A * self.env.dt
        self.X += self.V * self.env.dt