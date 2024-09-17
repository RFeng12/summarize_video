from flask import Flask, request
from flask import render_template
import requests
import time
import json
import jsonpickle
import funct_videomaker
import nltk
nltk.download('stopwords')

string='''
A coelacanth is a rare and ancient type of lobe-finned fish belonging to the class Sarcopterygii, which includes the lineage that led to the first land vertebrates. Coelacanths are notable for their distinct, lobed pectoral and pelvic fins, which are thought to resemble the early evolutionary adaptations of fins that enabled vertebrates to move onto land. Once believed to be extinct and known only from fossils dating back about 360 million years, coelacanths were unexpectedly discovered alive off the coast of South Africa in 1938. This discovery was significant because it provided a living example of a lineage that had seemingly vanished. Coelacanths have a unique, oil-filled organ in their tails that aids in buoyancy, and they possess a pair of thick, bony scales covering their bodies. Their discovery has provided scientists with valuable insights into vertebrate evolution and the history of ancient fish.

'''

funct_videomaker.make_video(string.replace("123 -1..43gg3", "?"), "Ceolocanth")


