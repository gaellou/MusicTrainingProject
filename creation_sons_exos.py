import os
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as io
import os
from pydub import AudioSegment
from pydub.playback import play

from periodo import *

REP_exos = "./exos/"
REP_wav = "./wav/"
LILYPOND ='/usr/bin/lilypond --png '
RATE = 44100
DIAPASON = 440   ### provisoire


###### fonctions de base pour synthétiser un son, convertir en wav
def NormaliserSon(x):
    M = np.max(abs(x)); ## la plus grande valeur absolue du signal
    return  x/M;

def ConvertirWav(name_file,signal):
    signal = 0.7*NormaliserSon(signal)  ##pour protéger vos oreilles des saturations de vos enceintes 
    scaled = np.round(32767*signal)
    signal = scaled.astype(np.int16)
    io.write(name_file, RATE, signal)
    os.system('mv '+name_file+' '+REP_wav+name_file)

def SonSimple(f0,duree_note):   ### duree_note en secondes
    te = 1/RATE
    t= np.arange(0, duree_note, te)
    return np.cos(2*(np.pi)*f0*t)*2* np.sin(t*(np.pi)/duree_note)



def GenererSignal(liste_indice_note,rythme,tempo, diapason): ### liste_note en Hz et rythme notation anglaise
    #### conversion en Hertz
    a=2**(1/12)
    indices=np.array(liste_indice_note)
    liste_note =diapason*(a**indices)
    ### conversion rythme en secondes
    te = 1/RATE
    FreqNOIRE = tempo/60 #Hz
    d_NOIRE = 1/FreqNOIRE
    liste_duree_note = []
    liste_duree_note[:] = [4*d_NOIRE/x for x in rythme]
    ### création signal
    x_total = []
    for i in range (len(liste_note)):
        t= np.arange(0, liste_duree_note[i], te)
        x_tampon = SonSimple(liste_note[i],liste_duree_note[i])
        x_total = np.concatenate((x_total,x_tampon))
    somme_duree_note = 0
    for k in range (len(liste_duree_note)):
        somme_duree_note += liste_duree_note[k]
    time = np.arange(0,somme_duree_note,te)
    return x_total


def karaoke(liste_note, liste_duree,tempo):
    #liste_note = creation_liste_note(220,liste_note)
    duree_total = sum(liste_duree)*RATE
    kara = []
    FreqNOIRE = tempo/60 #Hz
    d_NOIRE = 1/FreqNOIRE
    for k in range (len(liste_duree)):
        for i in range(int(liste_duree[k]*d_NOIRE*20)):
            kara.append(liste_note[k])
        print(liste_duree[k]*d_NOIRE)
    return kara

def CreerFichier(FileName ,liste_indice,rythme,tempo,diapason):
    x = GenererSignal(liste_indice,rythme,tempo, diapason);
    ConvertirWav(FileName,x)

def JouerWav(fileName):
    song = AudioSegment.from_wav(REP_wav+fileName)
    play(song)

##############################################################################
class Instruments:
    Nom = 'Nom'
    NoteBasse = 57 #numero MIDI
    NoteHaute = 71 #Numéro MIDI
    Clef = 'violon' #violin, french, alto, bass
    Diapasion = 440 #frequence
    Pmax = 1 #float
    Pmin = 1 #float

    def étalonnage() :
        pass
        #code


class Exercices:

    Nom = "nom_fichier"
    Activite = "activité"
    Tempo = 60

    def ChargerExercice(exo) : #Génère les fichiers liers aux exercices
        nom_exercice = exo.Nom
        activite = exo.Activite
        tempo = exo.Tempo
        os.chdir(REP_exos)
        print(nom_exercice)
        if os.path.isfile( nom_exercice +'_prov.ly'):
            os.remove(nom_exercice+'_prov.ly')
        if os.path.isfile(nom_exercice+'_prov-unnamed-staff.notes'):
            os.remove(nom_exercice+'_prov-unnamed-staff.notes')

        #### duplication du fichier tierce.ly 
        ##### Attention! ce n'est peut-être pas la syntaxe pour Windows
        os.system('cp ' +nom_exercice+ '.ly '+nom_exercice+'_prov.ly')

########  On transpose 
        fichier = open(nom_exercice+'_prov.ly','a') ####### l'option 'a' : append

### on choisit de transposer du do (c) à une autre note 
### on choisit cette dernière au hasard (on monte d'un eoctave éventuellement)
        notes=["do", "reb","re" ,"mib","mi","fa","sol","lab","la","lad","sib","si" ]
        note_trans = np.random.choice(notes)
        clef = "\\clef alto"
        octavier = ["", "\'"]
        note_trans= note_trans+np.random.choice(octavier)
        fichier.write("\\transpose do "+note_trans+'{'+clef+" \\notes"+"}"+ "\n")   
###
        fichier.close()

######## lancement de lilypond
        os.system(LILYPOND + nom_exercice+ '_prov.ly')



#######  extraction de l'information utile du fichier généré par event-listener.ly
####### attention! ce code ne gère pas encore les silences
#######   ni les notes situées au-dessus du numéro 99 (environ le ré7 : très très aigü...)
        fichier = open(nom_exercice+'_prov-unnamed-staff.notes','r')
        lines = fichier.readlines()
        fichier.close()
        nb_notes = len(lines)
        indices = np.zeros(nb_notes)  ### le tableau des nombres de 1/2 tons par rapport au la4
        rythme = np.zeros(nb_notes) ### le tableau des rythmes associés (notation anglo-saxonne : 4-> noire 2->croche, etc.)
# Itérer sur les lignes
        no=0
        for line in lines:
        ### print(line.strip()) ### pour afficher le contenu du fichier ligne à ligne
            indices[no]=int(line[16:19])
            rythme[no]= round(1/float(line[21:31]))
            no=no+1
        
        indices = indices-69
        os.chdir('./../')
        #### ici : créer un fichier .wav
        CreerFichier(nom_exercice+'.wav' ,indices,rythme,tempo,DIAPASON)
        Nom_Image =  './exos/' + nom_exercice +'_prov.png'
        Nom_Son =  nom_exercice+'.wav'
        return(Nom_Image,Nom_Son,indices,rythme)
        
###########################################

    def JouerExercice(exo) :
        JouerWav(exo.Nom+'.wav')
        

    def AfficherExercice(exo) :
        pass
        #CODE


exercice1=Exercices()
exercice1.Nom='exercice1'
Exercices.ChargerExercice(exercice1)

