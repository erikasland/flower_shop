from django.core.management.base import BaseCommand, CommandError
from apps.flower.models import Flower
from bs4 import BeautifulSoup
import requests

class Command(BaseCommand):

    help = 'Takes information from webpage'

    def handle(self, *args, **options):
        self.insert_into_db()

    def scrape_flowers(self):  #scrapes flowers from website
        r = requests.get("http://www.pbase.com/hjsteed/just_flowers_pz&page=all")
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        flowers = []

        for name in soup.find_all('td', {'class': "thumbnail"}):
            flowers.append(name.b.string.strip(':').encode('ascii', 'ignore').decode('ascii'))
        return flowers

    def scrape_imgs(self): #scrapes img urls from website
        r = requests.get("http://www.pbase.com/hjsteed/just_flowers_pz&page=all")
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        links = []

        for link in soup.find_all('a', {'class': "thumbnail"}):
            links.append(link.img['src'].encode('ascii', 'ignore').decode('ascii'))
        return links

    def insert_into_db(self): #inserts flowers and links into database 
        flowers_list = self.scrape_flowers()
        url_list = self.scrape_imgs()

        count = 0
        while count < len(flowers_list):
            Flower.objects.get_or_create(name = flowers_list[count], link = url_list[count])
            count+=1


        