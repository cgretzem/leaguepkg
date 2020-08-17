from requests_html import HTMLSession
import runes

class UGG():
    def __init__(self, champ):
        self.session = HTMLSession()
        self.page = self.session.get(f'https://u.gg/lol/champions/{champ}/build')
        print('Loading page')
        self.page.html.render(wait = 5, retries = 7)
        print('Page Loaded')

    def getRunes(self):
        divs = self.page.html.find('div')
        rune_list = []
        all_runes = []
        for rune in divs:
            if 'class' in rune.attrs:
                if rune.attrs['class'] == ('perk', 'perk-active'):
                    rune_list.append(rune.find('img'))
        for rune in rune_list:
            all_runes.append(runes.Rune(rune[0].attrs['alt'],rune[0].attrs['src'] ))
        return all_runes
                
    def getBuild(self):
        divs = self.page.html.find('div')
        skills = []
        levels = []
        for skill in divs:
            if 'class' in skill.attrs:
                #print (skill.attrs)
                if skill.attrs['class'] == ('skill-order-row',):
                    skills.append(skill)
        for skill in skills:
            levels.append(skill.find('div'))
        print (levels)

if __name__ == '__main__':
    ugg = UGG('lux')
    ugg.getBuild()
   