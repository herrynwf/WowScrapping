from bs4 import BeautifulSoup
import requests

#define url template for each class type region
url_template="https://www.pvpleaderboard.com/leaderboards/filter/results?class={class_value}&leaderboard={type}&region={region}&current-rating=2200"

#define classes types regions
classes=["death-knight","demon-hunter","druid","hunter","mage","monk","paladin","priest","rogue","shaman","warlock","warrior"]
types=["2v2","3v3"]
regions=["us","eu"]

#define race counts dictionary
race_counts = {"dwarf": 0, "night elf": 0,"blood elf": 0,"orc": 0,"human": 0,"worgen": 0,"tauren": 0,"troll": 0,"draenei": 0,"zandalari troll": 0,"undead": 0,"kul tiran": 0,"void elf": 0,"goblin": 0,"mechagnome": 0,"gnome": 0,"nightborne": 0,"vulpera": 0,"mag'har orc": 0,"dark iron dwarf": 0,"lightforged draenei": 0,"highmountain tauren": 0,"dracthyr": 0,"pandaren": 0}

#Generate urls based on templates
class_urls={}

for class_name in classes:
    class_urls[class_name]={}
    for type_name in types:
        class_urls[class_name][type_name]={}
        for region_name in regions:
            class_urls[class_name][type_name][region_name]=url_template.format(
                class_value=class_name, type=type_name, region=region_name)

#function to get race counts for specific class type region
def get_race_counts(class_urls,race_counts):
    class_race_counts={class_name:{}for class_name in class_urls.keys()}
    for class_name, types in class_urls.items():
        for type_name,regions in types.items():
            for region_name,url in regions.items():
                response = requests.get(url)
                response.raise_for_status()  # Check for any request errors
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")
                image_elements = soup.select("img.img-responsive.center.inline-block")

                for element in image_elements:
                    alt_text = element.get("alt", "").lower()
                    for race in race_counts:
                        if race in alt_text:
                            class_race_counts[class_name][race]=class_race_counts[class_name].get(race,0)+1
                            race_counts[race] += 1
                            break
    return class_race_counts

#get race counts for all classes types regions
class_race_counts=get_race_counts(class_urls,race_counts)

#print top three races for each class
for class_name, race_counts in class_race_counts.items():
    print(f"Top races for {class_name.capitalize()}:") 
    sorted_races=sorted(race_counts,key=race_counts.get,reverse=True)
    for race in sorted_races[:3]:
        count=race_counts[race]
        print(f"{race.capitalize()}: {count}")
    print()


