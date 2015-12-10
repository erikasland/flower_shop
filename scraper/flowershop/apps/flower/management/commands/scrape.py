from django.core.management.base import BaseCommand, CommandError
from apps.flower.models import Flower
from bs4 import BeautifulSoup
import requests

class Command(BaseCommand):

    help = 'Takes information from webpage'

    def handle(self, *args, **options):
        r = requests.get("http://www.all-my-favourite-flower-names.com/list-of-flower-names.html")
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        links = []
        flowers = []
        for flower in soup.find_all('b'):  #Finds flower names and appends them to the flowers list
            flower = flower.string
            if (flower != None and flower[0] == "A"):
                flowers.append(flower.strip('.()'))
            
        for link in soup.find_all('img'):  #Finds 'src' in <img> tag and appends 'src' to the links list
            links.append(link['src'].strip('https://'))

        for stragler in soup.find_all('a'):  #Finds the only flower name that doesn't follow the pattern of the other names and inserts it into flowers list
            floss = stragler.string
            if floss != None and floss == "Ageratum houstonianum.":
                flowers.insert(3, floss)

        counter = 0
        while counter < len(flowers):  #Creates flowers/links in the database
            if len(Flower.objects.all()) == len(flowers):
                break
            else:
                Flower.objects.create(name=flowers[counter], link=links[counter])
                counter += 1



