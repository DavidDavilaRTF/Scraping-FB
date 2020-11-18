import sys
sys.path.append('C:\\web_driver\\')
from web_driver import *
import pandas
import numpy
import time

class scrap_fb:
    def __init__(self,driver,config):
        self.lien_com = []
        self.comment = []
        self.posts = []
        self.nom_posts = []
        self.profil_posts = []
        self.profil = []
        self.nom = []
        self.lien_post = []
        self.profil_action = []
        self.nom_action = []
        self.label_action = []
        self.driver = driver
        self.config = config

    def tout_accepter(self):
        element = self.driver.find_element("//*[contains(text(),'Tout accepter')]")
        self.driver.click(element)
        try:
            element = driver.find_element("//*[contains(@placeholder,'Numéro de mobile')]")
        except:
            element = self.driver.find_element("//*[contains(@value,'Se connecter')]")
        self.driver.click(element)
        del element

    def fill_username(self):
        element = self.driver.find_element("//*[contains(@placeholder,'Mot de passe')]")
        self.driver.fill_form(element,self.config['mdp'])
        del element

    def fill_mdp(self):
        element = self.driver.find_element("//*[contains(@placeholder,'Numéro de mobile')]")
        self.driver.fill_form(element,self.config['username'])
        del element

    def finir_connexion(self):
        element = self.driver.find_element("//*[contains(@value,'Se connecter')]")
        self.driver.click(element)
        time.sleep(5)
        element = self.driver.find_element("//*[@value = 'OK']")
        self.driver.click(element)
        del element

    def connexion(self):
        self.driver.get_to_page('https://www.facebook.com/')
        time.sleep(5)
        self.tout_accepter()
        self.fill_mdp()
        self.fill_username()
        self.finir_connexion()

    def click_message_box(self):
        element = self.driver.find_element(self.config['xpath']['click_message_box'])
        self.driver.click(element)
        del element

    def send_message_box(self):
        element = self.driver.find_element(self.config['xpath']['send_message_box'])
        self.driver.click(element)
        del element


    def fill_message(self,message):
        element = self.driver.find_element(self.config['xpath']['fill_message'])
        self.driver.fill_form(element,message)
        del element

    def post(self,message):
        for l in self.config['page_message']:
            self.driver.get_to_page(l)
            time.sleep(5)
            self.click_message_box()
            time.sleep(5)
            self.fill_message(message)
            time.sleep(5)
            self.send_message_box()
            time.sleep(5)

    def get_nb_post(self):
        self.driver.get_to_page(self.config['page'])
        time.sleep(5)
        element = self.driver.find_elements("//*[contains(text(),'Commenter')]")
        nb_post_listed = len(element)
        nb_post_before = -1
        while nb_post_listed < float(self.config['nb_post']) and nb_post_before != nb_post_listed:
            self.driver.scroll()
            time.sleep(5)
            nb_post_before = nb_post_listed
            element = self.driver.find_elements("//*[contains(text(),'Commenter')]")
            nb_post_listed = len(element)
            if nb_post_listed == 0:
                nb_post_before = -1
            
        for e in element:
            self.lien_com.append(self.driver.find_attribute(e,'href'))
        del element
        del nb_post_listed
        del nb_post_before
        
    def access_to_action(self):
        element = self.driver.find_element("//div[@class = '_1w1k _5c4t']")
        self.driver.click(element)
        del element
        time.sleep(2)

    def scroll_action(self):
        try:
            element = self.driver.find_element("//div[@class = '_5p-o']//div[@class = 'title mfsm fcl']")
            self.driver.click(element)
            del element
            time.sleep(2)
        except:
            pass

    def get_profil_action(self):
        element = self.driver.find_elements("//div[contains(@class,'_1uja')]")
        for e in element:
            p = self.driver.find_element_in_box(e,".//a")
            p = self.driver.find_attribute(p,'href')
            self.profil_action.append(p)
            del p
            n = self.driver.find_element_in_box(e,".//strong")
            n = self.driver.find_attribute(n,'innerHTML')
            self.nom_action.append(n)
            del n
            l = ''
            for r in self.config['reaction']:
                try:
                    xpath = ".//i[@class = " + "'" + self.config['reaction'][r] + "']"
                    i = self.driver.find_element_in_box(e,xpath)
                    l = r
                    del i
                except:
                    pass
            self.label_action.append(l)
            del l
        del element

    def list_action(self):
        for l in self.lien_com:
            self.driver.get_to_page(l)
            time.sleep(5)
            try:
                self.access_to_action()
                for i in range(int(self.config['nb_scroll_action'])):
                    self.scroll_action()
                self.get_profil_action()
            except:
                pass
            self.write_action()

    def delete_com(self,box):
        element = self.driver.find_element_in_box(box,".//a[text() = 'Plus']")
        time.sleep(1)
        self.driver.click(element)
        element = self.driver.find_element("//span[text() = 'Supprimer le commentaire et bloquer l’utilisateur']")
        del element
        time.sleep(10)

    def list_com(self):
        for l in self.lien_com:
            self.driver.get_to_page(l)
            time.sleep(5)
            try:
                element = self.driver.find_element("//div[@class = '_5rgt _5nk5']")
                post = self.driver.find_attribute(element,'')
            except:
                post = ''

            try:
                element = self.driver.find_element("//h3//a")
                nom_post = self.driver.find_attribute(element,'')
                profil_post = self.driver.find_attribute(element,'href')
            except:
                nom_post = ''
                profil_post = ''

            if int(self.config['is_all_com']):
                cont_loop = True
                k = 0
                while cont_loop and k <= 20:
                    try:
                        element = self.driver.find_element("//*[contains(text(),'Commentaires précédents')]")
                        self.driver.click(element)
                        time.sleep(5)
                    except:
                        cont_loop = False
                    k += 1
                element = self.driver.find_elements("//a[contains(text(),'Voir')]")
                k = 0
                while len(element) > 0 and k <= 20:
                    for e in element:
                        try:
                            self.driver.click(e)
                            time.sleep(1)
                        except:
                            pass
                    element = self.driver.find_elements("//a[contains(text(),'Voir')]")
                    k += 1
                element = self.driver.find_elements("//span[@class = '_4ayk']")
                for e in element:
                    try:
                        self.driver.click(e)
                        time.sleep(1)
                    except:
                        pass
            try:
                ok = diver.find_element("//a[text() = 'OK']")
                self.driver.click(ok)
            except:
                pass
            lp = self.driver.get_current_url()
            bloc = self.driver.find_elements("//div[@class = '_2b04']")
            for b in bloc:
                element_com = self.driver.find_element_in_box(b,".//*[@data-sigil = 'comment-body']")
                com = self.driver.find_attribute(element_com,'')
                is_extract = False
                for kw in self.config['key_words']:
                    is_extract += (com.find(kw) != -1)
                if is_extract:
                    element_nom = self.driver.find_element_in_box(b,".//div[@class = '_2b05']//a")
                    self.profil.append(self.driver.find_attribute(element_nom,'href'))
                    self.nom.append(self.driver.find_attribute(element_nom,''))
                    self.comment.append(com)
                    self.posts.append(post)
                    self.nom_posts.append(nom_post)
                    self.profil_posts.append(profil_post)
                    self.lien_post.append(lp)
            self.write_com()

    def envoyer_message(self,text):
        df = pandas.read_csv(self.config['output_path'], sep = ';', engine = 'python')
        df = df['profils'].unique()
        for d in df:
            self.driver.get_to_page(d)
            time.sleep(5)
            try:
                element = self.driver.find_element("//a[contains(@href,'profile_message')]")
                lien = self.driver.find_attribute(element,'href')
                time.sleep(5)
                self.driver.get_to_page(lien)
                time.sleep(5)
                element = self.driver.find_element("//textarea")
                self.driver.fill_form(element,text)
                element = self.driver.find_element("//button[@name = 'send']")
                self.driver.click(element)
                del element
                del lien
            except:
                pass
        del df

    def write_com(self):
        recap = pandas.DataFrame()
        recap['noms'] = self.nom
        recap['profils'] = self.profil
        recap['com'] = self.comment
        recap['posts'] = self.posts
        recap['nom_posts'] = self.nom_posts
        recap['profil_posts'] = self.profil_posts
        recap['lien_posts'] = self.lien_post
        recap.to_csv(self.config['output_path'],sep = ';',index = False)
        del recap

    def write_action(self):
        recap = pandas.DataFrame()
        recap['noms'] = self.nom_action
        recap['profils'] = self.profil_action
        recap['label'] = self.label_action
        recap = recap.drop_duplicates(subset = ['profils'])
        recap.to_csv(self.config['output_path'],sep = ';',index = False)
        del recap

    def run(self):
        self.connexion()
        if self.config['action'] == 'reaction':
            self.get_nb_post()
            self.list_action()
            self.write_action()
        elif self.config['action'] == 'com':
            self.get_nb_post()
            self.list_com()
            self.write_com()
        elif self.config['action'] == 'message':
            self.envoyer_message(self.config['message'])

arg = sys.argv[1]
arg = arg.split(',')
config = {}
for a in arg:
    cle = a.split('|')[0]
    info = a.split('|')[1]
    if cle != 'message':
        info = info.split(';')
    if len(info) == 1:
        config[cle] = info[0]
    else:
        config[cle] = info
    del cle
    del info
del arg

config['reaction'] = {}
config['reaction']['lol'] = '_59aq img sp_yP8gT9Lyb8L sx_1f73b4'
config['reaction']['whoa'] = '_59aq img sp_yP8gT9Lyb8L sx_d81791'
config['reaction']['solidaire'] = '_59aq img sp_yP8gT9Lyb8L sx_4cc9ee'
config['reaction']['love'] = '_59aq img sp_yP8gT9Lyb8L sx_091c53'
config['reaction']['thumbs_up'] = '_59aq img sp_yP8gT9Lyb8L sx_c5e132'
config['reaction']['cry'] = '_59aq img sp_yP8gT9Lyb8L sx_7294bf'
config['reaction']['angry'] = '_59aq img sp_yP8gT9Lyb8L sx_b0d007'

driver = web_driver_selenium()
driver.create_browser()
sf = scrap_fb(driver = driver,
            config = config)
sf.run()
driver.close_browser()
del sf
del driver
