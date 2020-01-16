#!/usr/bin/env python3
# commande permetant au robot de comprendre quel environement utiliser.

# importation de a premiere bibliotheque ev3
from ev3dev.ev3 import *
# importation de la seconde bibliotheque ev3
from ev3dev2.motor import *
# importation des fonction capable de gerer le temps
import time

# indique que la variable tank correspondra aux sorties A et D de la btique que nous avons branche aux moteurs
tank = MoveTank(OUTPUT_A, OUTPUT_D)
# indique que la variable lever correspondra au soulevement de la pelle
lever = motor(OUTPUT_B)
# indique que la variable porte correspondra a l'ouvertur de la porte
porte = motor(OUTPUT_B)
# indique que la variable csL correspondra a l'entree 1 que nous avons branche au capteur de couleur gauche
csL = ColorSensor('in1')
# indique que la variable csR correspondra a l'entree 4 que nous avons branche au capteur de couleur droit
csR = ColorSensor('in4')

# indique que les deux capteur devront utiliser le mode col-color au demarage
csR.mode = 'COL-COLOR'
csL.mode = 'COL-COLOR'

# indique que la variable usav correspondra a l'entree 2 que nous avons branche au capteur a ultrason avant
usav = UltrasonicSensor('in2')
# indique que la variable usar correspondra a l'entree 3 que nous avons branche au capteur a ultrason arriere
usar = UltrasonicSensor('in3')
# indique aux capteurs a ultrason de mesurer la distance qu'il y a entre eux et le prochain obstacle
usav.mode = 'US-DIST-CM'
usar.mode = 'US-DIST-CM'

# creation et initialisation de deux variables servant pour la partie bille
timerbase = 0
timertest = 0

# global permet aux variables de rester les mains quelle que soit la fonction
global timertest, timerbase


def compte(sec):
    """
    Patiente une seconde et en ajoute une a celle entree.
    :param sec: Seconde passee a laquelle doit etre ajoute une seconde.
    :return: Seconde.
    """
    # fait patienter le programme une seconde avant de continuer
    time.sleep(1)
    # fait augmenter la variable sec d'une unite
    sec += 1
    # renvoie la variable sec la ou la fonction a ete appelee
    return (sec)


def bille():  # creation de la fonction(bille) charger de ramasser les billes
    global timertest, timerbase  # global permet aux variables de rester les mains quelle que soit la fonction
    sound.tone()  # le robot va biper legerment pour inidquer qu'il a changer de mode
    while usav.value() / 10 > 4:  # tant que le capteur a ultrason avant ne detecte pas d'obstacle a moins de 4 cm( la fonction .value donne les distance ne mm d'ou la division par 10)
        tank.on(SpeedPercent(15), SpeedPercent(
            15))  # les deux roues avancent a 15% de leurs vitesses maximal jusqu'a ce qu'elles recoivent un contre ordre
    tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(-15),
                        4)  # les deux roues reculent a 15% de leurs vitesses maximal pendant 4 secondes
    tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15),
                        1.8)  # les deux roues bouges de maniere independantes pour permettre au robot de faire des virage sur place pour que cela soit plus pratique
    # comme vu ci dessus la fonction tank.on permet de faire avancer les deux roues en meme temps mais sans qu'elle n'avancent exactement de la meme maniere
    # la fonction tank.on_for_seconds permet de faire la meme chose mais aussi de limiter ce mouvement de roue dans le temps
    # Ces deux fonctions proviennent de la bibliotheque ev3 importer en debut de programme
    while usav.value() / 10 > 4:  # tant que le capteur a ultrason avant ne detecte pas d'obstacle a moins de 4 cm
        tank.on(SpeedPercent(15), SpeedPercent(
            15))  # les deux roues avancent a 15% de leurs vitesses maximal jusqu'a ce qu'elles recoivent un contre ordre
    tank.on_for_seconds(SpeedPercent(-10), SpeedPercent(-10), 2)
    tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.9)
    while usav.value() / 10 > 4:  # tant que le capteur a ultrason avant ne detecte pas d'obstacle a moins de 4 cm
        tank.on(SpeedPercent(15), SpeedPercent(15))
    tank.on_for_seconds(SpeedPercent(-10), SpeedPercent(-10), 2)
    tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.9)
    # tout la partie ci dessus avait pour but de placer le robot au bon endroit c'est a dire le coin a gauche de l'entree
    # ainsi le robot siat ou il est par rapport au coin ou il doit placer les billes
    while usav.value() / 10 > 4:  # tant que le capteur a ultrason avant ne detecte pas d'obstacle a moins de 4 cm
        tank.on(SpeedPercent(15), SpeedPercent(15))
        timerbase = compte(timerbase)  # la variable timerbase augmente de 1 a chaque seconde
    timerbase += 2  # augmentation de deux pour plus de securite
    # ainsi le robot ne risque pas de croire qu'il est arrive au coin car sa trajectoire n'est pas droite
    for i in range(10):  # repetition de la boucle de ramassage de bille 11 fois pour etre sur de toute les ramasser
        timertest = 0  # reinitialisation de la variable a chaque passage pour qu'elle puisse faire les tests a chaque fois
        while timertest < timerbase:  # tant que le temps de test est plsu petit que le temps de depart le robot va continuer a faire la boucle
            while usav.value() / 10 > 4:  # tant que le capteur a ultrason avant ne detecte pas d'obstacle a moins de 4 cm
                tank.on(SpeedPercent(10), SpeedPercent(10))  # le robot avance a 10% de sa vitesse maximal
            if timertest < timerbase:  # tant  que la variable timertest est plus petite que le temps de timerbase le robot n'est pas bloque il n'est donc pas dans le coin
                # cela permet de savoir quand il arrive dans le coin car il roulera bien plus longtemps que d'habitude
                tank.on(SpeedPercent(-10),
                        SpeedPercent(-10))  # le robot avance jusuqu'a ce qu'il recoive un contre-ordre
                timertest = compte(
                    timertest)  # le timertest augmente d'une unite car une seconde c'est passe
                tank.on_for_seconds(SpeedPercent(-10), SpeedPercent(-10), 2)
                tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.9)
                tank.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 1)
                tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.9)
                # les commandes au dessus permettent au robot de faire un demi tour
                lever.on(SpeedPercent(-50))
                lever.on(SpeedPercent(50))
                # ces commande permettent de lever la pelle pour deposer les billes dans le bac puis de rabaisser la pelle
                timertest = 0  # reinitialisation de la variable pour pouvoir reeffectuer un test
            else:  # si le robot entre dans ce sinon c'est qu'il est bloque contre la zone de recuperation des billes
                tank.on_for_seconds(SpeedPercent(-10), SpeedPercent(-10), 2)
                tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 3.8)
                # le robot recule puis effectue un demi-tour
                while usar.value() / 10 < 4:  # tant que le robot est assez eloignee du mur arriere
                    tank.on(SpeedPercent(-10), SpeedPercent(-10))  # il recule
                porte.on(SpeedPercent(-50))  # la porte s'ouvre
                time.sleep(1)  # le robot attend une seconde le temps que les billes tombent
                porte.on(SpeedPercent(-50))  # la porte se referme
        tank.on_for_seconds(SpeedPercent(-10), SpeedPercent(-10), 2)
        tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.9)  # le robot est arrive face au mur il tourne juste


def evitement():
    """
    Contourne l'obstacle de dimensions connus a l'avence.
    """
    tank.on_for_seconds(SpeedPercent(-10), SpeedPercent(-10), 2)
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(-5), 1.7)
    # if usav.value()/10<4:
    #    bille()
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(15), 1)
    tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.8)
    tank.on_for_seconds(SpeedPercent(20), SpeedPercent(20), 4)
    tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.9)
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(15), 1.1)
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(-5), 1.8)
    tank.on_for_seconds(SpeedPercent(-10), SpeedPercent(-10), 1)
    # toute les focntion de deplacemetn ci dessus permettent au robot de contourner l'obstacle et de se remttre juste derriere pour continuer a suivre la ligne
    # cette fonction a ete modifie plusieurs fois pour s'adapter aux obstacle de chaque parcours

def noirD():
    """
    Inverse de :func:`noirG`
    Verifie que le capteur csR (ColorSensorRight) detecte la couleur noir (1).
    Puis tourne gauche jusqu'a que le capteur ne voit plus de noir.
    """

    # si le capteru de couleur droit voit du noir il renverra la valeur 1
    if csR.value() == 1:
        # le robot va se decaler pour continuer suivre la ligne noir de la maniere la plus precise possible
        tank.on(SpeedPercent(20), SpeedPercent(-10))

        ''' les deux test suivant servent a eviter que la rectification de trajectoire ne soit trop
         vuiolente et permet au roobot de se corriger en cas d'erreur
        '''
        if csR.value() == 1:
            tank.on(SpeedPercent(20), SpeedPercent(-10))
        elif csL.value() == 1:
            tank.on(SpeedPercent(-10), SpeedPercent(20))


def noirG():
    """
    Inverse de :func:`noirD`
    Verifie que le capteur csL (ColorSensorLeft) detecte la couleur noir (1).
    Puis tourne droite jusqu'a que le capteur ne voit plus de noir.
    """
    if csL.value() == 1:
        tank.on(SpeedPercent(-20), SpeedPercent(40))
        if csR.value() == 1:
            tank.on(SpeedPercent(20), SpeedPercent(-10))
        elif csL.value() == 1:
            tank.on(SpeedPercent(-10), SpeedPercent(20))


def follow():
    """
    Verifie les valeurs de capteurs pour decider quelle actions doit etre entreprise.
    Noir lancera les fonctions :func:`noirG` et :func:`noirD`.
    Vert, avec une verification supplementaire, tournera en direction du carre vert.
    """
    if csL.value() == 3 and csR.value() == 3:  # si le capteur gauche et le capteur droit voit du vert il renvoie le nombre trois
        tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(15), 1.8)  # le robot effectue un demi tou
        # cette partie ne fonctionnasi pas parce que le robot ne detectais jamasi les deux vert en mleme temps 

    elif csL.value() == 3:  # sinon si le capteur gauche voie du vert
        csL.mode = 'RGB-RAW'  # le capteru change de mode pour une deuxieme vveirfication pour eviter les faux positif
        if 13 <= csL.value() <= 20:  # si la valeur dasn el deuxieme mode est comprise entre 13 et 20
            # c'est valeur changeait en fonction du moment de la journee et de la reflection de la salle
            tank.on_for_seconds(SpeedPercent(5), SpeedPercent(5), 0.5)
            tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.6)
        # le robot avance un peut et tourne ne direction du carre vert
        csL.mode = 'COL-COLOR'  # le capteur repasse dans son mode normal
    elif csR.value() == 3:  # sinon si le capteur droit voie du vert
        csR.mode = 'RGB-RAW'  # le capteru change de mode pour une deuxieme vveirfication pour eviter les faux positif
        if 13 <= csR.value() <= 20:  # si la valeur dasn el deuxieme mode est comprise entre 13 et 20
            tank.on_for_seconds(SpeedPercent(5), SpeedPercent(5), 0.5)
            tank.on_for_seconds(SpeedPercent(5), SpeedPercent(-15), 1.6)
            # le robot avance un peut et tourne ne direction du carre vert
        csR.mode = 'COL-COLOR'  # le capteur repasse dans son mode normal

    elif csR.value() == 1 or csL.value() == 1:  # si jamasi un des capteurs vooit du noir il lance les deux fonctions noirG et noirD pour quil suivent la ligne sans etre trop brusque
        noirG()
        noirD()
    # en dessus il y a de nouveau la meme verifiaction pour le vert car il arrivati que le capteur ne le detece pas
    elif csL.value() == 3:
        csL.mode = 'RGB-RAW'
        if 13 <= csL.value() <= 20:
            tank.on_for_seconds(SpeedPercent(5), SpeedPercent(5), 0.5)
            tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1.6)
        csL.mode = 'COL-COLOR'
    elif csR.value() == 3:
        csR.mode = 'RGB-RAW'
        if 13 <= csR.value() <= 20:
            tank.on_for_seconds(SpeedPercent(5), SpeedPercent(5), 0.5)
            tank.on_for_seconds(SpeedPercent(5), SpeedPercent(-15), 1.6)
        csR.mode = 'COL-COLOR'
    # elif csL.value() == 4 or csR.value() == 4:
    #   csL.mode = 'RGB-RAW'
    #  csR.mode = 'RGB-RAW'
    # if  87 <= csL.value() <=100 or 87 <= csL.value() <= 100:
    #    Sound.tone(1500, 2000).wait()
    #   csL.mode = 'COL-COLOR'
    #  csR.mode = 'COL-COLOR'
    # bille()

    else:
        # tant que le capteur a ultrason avant ne detecte pas d'obstacle a moins de 4 cm
        if usav.value() / 10 <= 4:
            # apelle de la fonction evitemetn pour esquiver l'obstacle
            evitement()

        # if usar.value()/10<4:
        # time.sleep(1)
        # tank.on_for_seconds(SpeedPercent(100), SpeedPercent(100), 2)

        # si il ne detecte rien le robot continue d'avancer tout droit
        tank.on(SpeedPercent(12), SpeedPercent(12))


''' se repetera toujours ce qui permettra au programme de ne jamasi s'arreter 
et au robot de toujour rouler
'''
while 1:
    # apelle la fonction follow
    follow()
