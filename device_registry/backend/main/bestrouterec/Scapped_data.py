from selenium import webdriver
from time import sleep
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as sp
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,ElementNotVisibleException

#CTM Bot
class CTMBot(object):
	"""docstring for CTMBot"""
	def __init__(self):
		self.driver = webdriver.Chrome("C:/Program Files/operadriver.exe")
		self.out = open('CTM_trips.csv','a')
		self.driver.maximize_window()

	def search(self,origin,destination):
		self.driver.get('http://www.ctm.ma/home/index')
		sleep(2)
		prices = []
		times = []
		self.driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/div[2]/div/form/div[2]/div[1]/div/input").click()
		self.driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/div[2]/div/form/div[2]/div[1]/div/input").send_keys(origin)
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[7]/h1').click()
		sleep(1)
		self.driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/div[2]/div/form/div[2]/div[2]/div/input").click()
		self.driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/div[2]/div/form/div[2]/div[2]/div/input").send_keys(destination)
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[7]/h1').click()
		sleep(1)
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[7]/div[2]/div/form/div[2]/div[3]/div/div/input').click()
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[7]/div[2]/div/form/div[2]/div[3]/div/div/input').send_keys("20-03-2020")
		sleep(1)
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[7]/div[2]/div/form/div[4]/div[2]/button').click()
		sleep(10)
		try:
			timeList = self.driver.find_elements_by_xpath("//span[contains(@class, 'horaires-tab')]")
			priceList = self.driver.find_elements_by_xpath("//span[contains(@class, 'cell-price')]")
			prices.extend([price.text for price in priceList])
			times.extend([time.text for time in timeList])
			for i in range(len(prices)):
				self.out.write(origin+";"+destination+";"+times[2*i]+";"+times[2*i+1]+";"+prices[i]+'\n')
		except UnexpectedAlertPresentException :
			self.driver.switch_to.alert.accept()
		
	def close(self):
		self.driver.close()
		self.driver.quit()
		self.out.close()


bot = CTMBot()
gares = ['Agadir','Al Hoceima','Azrou','Beni Mellal','Fkih Ben Salah','Berkane','Casablanca FAR','Casablanca Ain Sebaa','Casablanca Maarif','Chefchaouen','Dakhla','El Hajeb','Errachidia','Essaouira','Fes','Fnidek','Guelmim','Ifrane','Kasbat Tadla','Kelaa Sraghna','Khemisset','Khenifra','Khouribga','Ksar El Kébir','Laayoune','Larache','Marrakech','Meknes','Midelt','Mrirt','Nador','Ouarzazate','Oujda','Rabat','Safi','Saidia','Sidi Kacem','Souk Larbaa','Tan Tan','Tanger','Taounate','Taza','Tetouan','Tiflet']
nbGares = len(gares)
for i in range(32,nbGares):
	print(i)
	for j in range(nbGares):
		if i != j:
			print(gares[i],gares[j])
			bot.search(gares[i],gares[j])
bot.close()


class COVBot(object):
	"""docstring for COVBot"""
	def __init__(self):
		self.driver = webdriver.Chrome("C:/Program Files/operadriver.exe")
		#self.out = open('COVTrips.csv','a')
		self.driver.maximize_window()
		self.driver.get('https://www.comobila.com/covoiturage/trajet/rechercher')
		
		self.drivers = []
		self.from_to = []
		self.dates_times = []
		self.prices = []


	def get_infos(self):
		while(1):
			self.driver.execute_script("window.scrollTo(0, 0);")
			sleep(10)
			try:
				driversinfos = self.driver.find_elements_by_xpath('//div[@class = "recent-ride-row-img"]')
				tripinfos =  self.driver.find_elements_by_xpath('//div[@class = "recent-ride-row-info"]')
				tripprice = self.driver.find_elements_by_xpath('//div[@class = "recent-ride-row-price"]')
				for i in range(len(driversinfos)):
					self.drivers.append(driversinfos[i].text.split('\n'))
					self.from_to.append(tripinfos[i].text.split('\n')[0].split(' '))
					if tripinfos[i].text.split('\n')[1].startswith('Date'):
						self.dates_times.append(tripinfos[i].text.split('\n')[1].split(': ')[1].split(' - '))
					else:
						self.dates_times.append(tripinfos[i].text.split('\n')[2].split(': ')[1].split(' - '))
					self.prices.append(tripprice[i].text.split('\n')[0])
					self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				sleep(2)
				print(1)
				self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[4]/ul/li[13]/a").click()
			except ElementNotVisibleException :
				break

	def close(self):
		self.driver.close()
		self.driver.quit()

	def saveinfos(self):
		out = open('COV_trips.csv','w')
		out.write('driver_name;driver_sex;driver_age;driver_is_smoking;from;to;date;time;price\n')
		for i in range(len(bot.drivers)):
			out.write(bot.drivers[i][0]+';'+bot.drivers[i][1].split(' | ')[0]+';'+bot.drivers[i][1].split(' | ')[1]+';'+bot.drivers[i][2].split(' : ')[1]+';'+bot.from_to[i][0]+';'+bot.from_to[i][1]+';'+bot.dates_times[i][0]+';'+bot.dates_times[i][1]+';'+bot.prices[i]+'\n');



bot = COVBot()
bot.get_infos()
bot.saveinfos()
bot.close()

#ONCF Bot

class ONCFBot(object):
	"""docstring for ONCFBot"""
	def __init__(self):
		self.driver = webdriver.Chrome("C:/Program Files/operadriver.exe")
		self.driver.maximize_window()
		self.out = open('ONCF_trips.csv','a')
		#self.out.write('from;to;depart_time;arrival_time;price\n')
		

	def get_all_gares(self):
		self.driver.get("https://www.oncf-voyages.ma")
		self.driver.maximize_window()
		self.driver.find_element_by_xpath("//div[@id='origin']").click()
		gareList = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/ul")
		gares = gareList.find_elements_by_xpath('//li')
		gares = [gare.text for gare in gares]
		return gares[22:]

	def search(self,origin,destination):
		self.driver.get("https://www.oncf-voyages.ma")
		sleep(2)
		prices = []
		times = []
		self.driver.find_element_by_xpath("//div[@id='origin']").click()
		self.driver.find_element_by_xpath("//input[@id='origin']").send_keys(origin)
		self.driver.find_element_by_xpath("//h2[@class='SearchForm_title']").click()
		sleep(1)
		self.driver.find_element_by_xpath("//div[@id='destination']").click()
		self.driver.find_element_by_xpath("//input[@id='destination']").send_keys(destination)
		self.driver.find_element_by_xpath("//h2[@class='SearchForm_title']").click()
		sleep(1)
		self.driver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div/div[1]/div[4]/div/div/div[1]/div/div/input").click()
		sleep(1)
		self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[4]").click()
		sleep(1)
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/label[1]/span[2]').click()
		sleep(1)
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()
		sleep(1)
		self.driver.find_element_by_xpath("/html/body/div/section/div[1]/div[2]/main/div[1]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div/div[3]/div/button").click()
		while(1):
			sleep(10)
			try:
				tripbox = self.driver.find_element_by_xpath("//div[@class='ant-card trip-card-wrapper']")
				trips = tripbox.find_elements_by_xpath("//label[contains(@class, 'date')]")
				pricess = tripbox.find_elements_by_xpath("//label[contains(@class,'price')]")
				prices.extend([price.text for price in pricess])
				times.extend([trip.text for trip in trips])
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				sleep(2)
				self.driver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/a").click()
			except NoSuchElementException :
				break
		for i in range(len(prices)):
			self.out.write(origin+";"+destination+";"+times[2*i]+";"+times[2*i+1]+";"+prices[i]+'\n')
	def close(self):
		self.driver.close()
		self.driver.quit()
		self.out.close()


bot = ONCFBot()
# gares = bot.get_all_gares() # all gars are a lot 
gares = ['AEROPORT MED V', 'AGADIR  (SUPRAT.)', 'AIN SEBAA', 'AIN-TAOUJDATE',  'ASILAH', 'BENGUERIR', 'BENI-MELLAL', 'BERRECHID', 'BOUZNIKA', 'CASA PORT', 'CASA VOYAGEURS', 'CHEFCHAOUEN', 'EL JADIDA', 'EL KHEMISSET', 'EL KSAR EL KEBIR',  'ERFOUD (SUPRAT.)', 'ERRACHIDIA (SUPRAT.)', 'ESSAOUIRA', 'FACULTES', 'FES', 'FNIDEQ (SUPRA.)', 'FQUIH BEN SALAH', 'GUELMIMA', 'GUELMIME',  'JORF EL MELHA', 'KELAA  DES  SRAGHNAS', 'KENITRA', 'KHENIFRA (SUPRAT.)', 'KHOURIBGA', 'LAAYOUNE', 'LARACHE', "L'OASIS", 'MARRAKECH', 'MARTIL' , 'MEKNES', 'MEKNES AL AMIR',  'MERS SULTAN', 'MIDELT (SUPRAT.)', 'MOHAMMEDIA', 'NADOR VILLE', 'OUARZAZATE', 'OUEZZANE', 'OUJDA', 'RABAT AGDAL', 'RABAT VILLE',  'SAFI', 'SALE', 'SALE TABRIQUET', 'SEBAA-AIOUN', 'SETTAT', 'SIDI KACEM',  'SIDI SLIMANE MEDINA', 'SKHIRAT', 'SOUK EL ARBAA', 'TANGER VILLE', 'TAZA', 'TEMARA', 'TETOUAN', 'TIZNIT',  'YOUSSOUFIA']
nbGares = len(gares)
for i in range(43,nbGares):
	print(i)
	for j in range(nbGares):
		if i != j:
			print(gares[i],gares[j])
			bot.search(gares[i],gares[j])
bot.close()

