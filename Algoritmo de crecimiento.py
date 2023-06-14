import pygame
from math import sqrt
from random import uniform
from random import randint 

class Vector2D:
    def __init__(self, x, y):
        """
        Constructor de la clase Vector2D
        Entradas y restricciones:
        - x, y: dos números componentes del vector.
        """
        if type(x) not in (int, float):
            raise Exception("x debe ser un escalar.")
        if type(y) not in (int, float):
            raise Exception("y debe ser un escalar.")
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other):
        """Función booleana que retorna True si ambos vectores son iguales y False sino."""
        return self.x == other.x and self.y == other.y

    def checkVector2D(v):
        """Subrutina que busca las restricciones para ser un vector."""
        if type(v) != Vector2D:
            raise Exception("Debe ser un objeto Vector2D")

    def checkScalar(s):
        """Subrutina que busca las restricciones para ser un escalar."""
        if type(s) not in (int, float):
            raise Exception("Debe ser un escalar.")

    def sum(self, other):
        """Función que suma dos vectores y modifica el primero: A + B = A'"""
        Vector2D.checkVector2D(other)
        self.x += other.x
        self.y += other.y

    def sub(self, other):
        """Función que resta dos vectores y modfica el primero: A - B = A'"""
        Vector2D.checkVector2D(other)
        self.x -= other.x
        self.y -= other.y

    def mult(self, s):
        """Función que multiplica dos vectores y modifica el primero: A * B = A'"""
        Vector2D.checkScalar(s)
        self.x *= s
        self.y *= s

    def div(self, s):
        """Función que divide dos vectores y modifica el primero: A / B = A'."""
        Vector2D.checkScalar(s)
        self.mult(1 / s)

    def mag(self):
        """Función que retorna la magnitud del vector."""
        return sqrt(self.x**2 + self.y**2)

    def normal(self):
        """Función que normaliza el vector (cambia su magnitud siempre a 1)."""
        self.div(self.mag())

    def copy(self):
        """Función que copia un vector."""
        return Vector2D(self.x, self.y)

class Circle:
    def __init__(self, x, y, radio, color, surface):
        """
        Constructor de la clase Vector2D
        Entradas y restricciones:
        - x, y: dos números componentes de las coordenadas del círculo.
        - radio: tamaño del círculo.
        - color: tupla con el rgb del color del círculo.
        - surface: superficie en la que se presenta el círculo.
        """
        self.pos = Vector2D(x, y)
        self.radio = radio 
        self.color = color
        self.surface = surface
    def display(self):
        """Función encargada de dibujar el o los círculos."""
        self.colored()
        pygame.draw.circle(self.surface, self.color, (self.pos.x, self.pos.y), self.radio)
    def setPos(self, newPos):
        """Función que cambia la posición del círculo a un lugar diferente.
        - newPos: Es el vector nuevo, pero con los mismos datos.
        """
        self.pos = newPos.copy()
    def dist(self, other):
        """Función que calcula la distancia entre dos círculos."""
        dif = self.pos.copy()
        dif.sub(other.pos)
        return dif.mag()
    def touch(self, other):
        """Función que se encarga de saber si dos círculos se están tocando o no."""
        return self.dist(other) <= self.radio + other.radio
    def findClosest(self, circles): 
        """Función que encuentra el círculo más cercano al círculo creado más reciente (Algoritmo de búsqueda).
        - circles: Lista de círculos.
        """
        closest = circles[0]
        for c in circles[1:]:
            if self.dist(c) < self.dist(closest):
                closest = c
        return closest
    def move(self, other):
        """Función que mueve el círculo creado más reciente al más cercano."""
        dif = other.pos.copy()
        dif.sub(self.pos)
        distance = dif.mag()
        dif.normal()
        dif.mult(distance - self.radio - other.radio)
        self.pos.sum(dif)
    def colored(self):
        """Función que se encarga de crerar los colores para todos los círculos."""
        r, g, b = self.color
        b = (b + 3)  % 256
        self.color = r, g, b
    def createdCircle(surface): 
        """Función que crea los datos de todos los círculos."""
        x = randint(0, surface.get_width())
        y = randint(0, surface.get_height())
        radio = 2
        color = (0, 0, 255)
        return Circle(x, y, radio, color, surface)
    def createdFirstCircle(surface):
        """Función que crea los datos del primer círculo."""
        x = surface.get_width() // 2
        y = 0
        radio = 2
        color = (0, 0, 255)
        return Circle(x, y, radio, color, surface)
    def createSeparatedCircle(surface, circles):
        """Función que crea los círculos llamando a la función "createdCircle", sin embargo, antes vela que no esté junto a ningún  otro."""
        contact = True 
        while contact:
            newCircle = Circle.createdCircle(surface)
            contact = False 
            for c in circles:
                if c.touch(newCircle):
                    contact = True
        return newCircle  

def main():
    """Función principal que hace los llamados necesarios ppara poner en función la simulación."""
    pygame.init()
    window = pygame.display.set_mode((600, 500))
    loop = True 
    circles = []
    circles.append(Circle.createdFirstCircle(window))
    while loop:
        pygame.time.delay(16)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False 
        newCircle = Circle.createSeparatedCircle(window, circles)
        closest = newCircle.findClosest(circles)
        newCircle.move(closest)
        circles.append(newCircle)
        window.fill((0, 0, 0))
        for c in circles:
            c.display()
        pygame.display.update()
    pygame.quit()
main() 