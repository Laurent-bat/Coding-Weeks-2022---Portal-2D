import numpy as np

"""
    Dans ce fichier :
        fun distance (point 1 , point 2) -> distance*
        class Rayon (x,y,dx,dy)
"""

def distance(p1,p2):
    """
    Paramêtres : point_1 (x,y) , point_2 (x,y)
    Renvoie la distance (float)
    """
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
def angle(x,y):
    """
    Paramêtres : x,y 
    Renvoie la distance l'angle en degré et trigonométrique (float)
    """
    return np.arctan2(y,x)*180/np.pi

# Test des fonctions

if __name__ == '__main__':
    print("Test de calcul d'angle : ")
    assert angle(50,0)==0
    assert angle(0,50)==90
    assert angle(0,-50)==-90
    assert angle(-50,0)==180
    assert angle(50,50)==45.0
    print("Test Reussi")
