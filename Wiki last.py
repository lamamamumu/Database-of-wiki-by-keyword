import wikipediaapi
import sqlite3
import re

def clear_all_data():
    conn = sqlite3.connect('D:/Getting and cleanning/dynasties_history.db')
    c = conn.cursor()
    countries = ["thailand", "china", "japan", "vietnam", "france"]
    for country in countries:
        c.execute(f'DROP TABLE IF EXISTS dynasties_{country}')
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS dynasties_{country} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                NameL TEXT,
                summary TEXT,
                content TEXT
            )
        ''')
    conn.commit()
    conn.close()
    print("เริ่มอัพเดท...")

def fetch_wiki_content(title, language='th'):
    wiki_wiki = wikipediaapi.Wikipedia(
        language=language,
        user_agent='Wiki/1.0 (siwatninlachat@gmail.com)'
    )
    page = wiki_wiki.page(title)
    if page.exists():
        full_title = page.title
        summary = page.summary
        content = page.text
        
        nameL_match = re.search(r'\((.*?)\)', summary)
        nameL = nameL_match.group(1) if nameL_match else None
        
        return full_title, nameL, summary, content
    else:
        return None, None, None, None

dynasty_titles = {
    "thailand" : [
        "ราชวงศ์ลาว",
        "รายพระนามผู้ปกครองแคว้นหริภุญชัย",
        "ราชวงศ์ภูคา",
        "ราชวงศ์ศรีธรรมาโศกราช",
        "พ่อขุนศรีนาวนำถุม",
        "ราชวงศ์พระร่วง",
        "ราชวงศ์ศรีวังสา",
        "ราชวงศ์มังราย",
        "ราชวงศ์อู่ทอง",
        "ราชวงศ์สุพรรณภูมิ",
        "ราชวงศ์สุโขทัย",
        "ราชวงศ์ปราสาททอง",
        "ราชวงศ์บ้านพลูหลวง",
        "ราชวงศ์ติ๋นมหาวงศ์",
        "ตระกูลเจ้าเจ็ดตน",
        "ราชวงศ์ธนบุรี",
        "ราชวงศ์แสนซ้าย",
        "ราชวงศ์จักรี"
    ],

    "china": [
        "ราชวงศ์เซี่ย",
        "ราชวงศ์ซาง",
        "ราชวงศ์โจวตะวันตก",
        "ราชวงศ์โจวตะวันออก",
        "ราชวงศ์ฮั่นตะวันตก",
        "ราชวงศ์ซิน",
        "ราชวงศ์ฮั่นตะวันออก",
        "ยุคสามก๊ก",
        "ราชวงศ์จิ้นตะวันตก",
        "ราชวงศ์จิ้นตะวันออก",
        "ยุคราชวงศ์เหนือ-ใต้",
        "ราชวงศ์สุย",
        "ราชวงศ์ถัง",
        "ห้าราชวงศ์และสิบอาณาจักร",
        "ราชวงศ์ซ่งเหนือ",
        "ราชวงศ์ซ่งใต้",
        "ราชวงศ์เหลียว",
        "ราชวงศ์จิน",
        "ราชวงศ์เซี่ยตะวันตก",
        "ราชวงศ์หยวน",
        "ราชวงศ์หมิง",
        "ราชวงศ์ชิง",
        "สาธารณรัฐจีน",
        "สาธารณรัฐประชาชนจีน"
    ],

    "japan": [
        "ยุคยะโยะอิ",
        "ยุคยะมะโตะ",
        "ยุคนะระ",
        "ยุคเฮอัง",
        "ยุคคะมะกุระ",
        "ยุคมุโระมะจิ",
        "ยุคอะซุชิ-โมะโมะยะมะ",
        "ยุคเอโดะ",
        "ยุคเมจิ",
        "ยุคไทโช",
        "ยุคโชวะ",
        "ยุคเฮเซ",
        "ยุคเรวะ"
    ],

    "vietnam": [
        "ราชวงศ์โชซ็อน",
        "ราชวงศ์เฉิน",
        "ราชวงศ์เหงียน"
    ],

    "france": [
        "ราชวงศ์การอแล็งเฌียง",
        "ราชวงศ์กาเปเซียง",
        "ราชวงศ์บูร์บง",
        "ราชวงศ์โบนาปาร์ต"
    ]
}

def insert_dynasties_to_db(country, titles, language):
    conn = sqlite3.connect('D:/Getting and cleanning/dynasties_history.db')
    c = conn.cursor()
    
    for title in titles:
        wiki_title, nameL, wiki_summary, wiki_content = fetch_wiki_content(title, language)
        if wiki_title:
            c.execute(f'''
                INSERT INTO dynasties_{country} (title, NameL, summary, content) VALUES (?, ?, ?, ?)
            ''', (wiki_title, nameL, wiki_summary, wiki_content))
            conn.commit()
            print(f"เพิ่ม '{wiki_title}' เข้าไปในฐานข้อมูลของ {country} แล้ว")
        else:
            print(f"ไม่มีหัวข้อนี้ในวิกิพีเดีย '{title}' ({country})")
    
    conn.close()

def clean_nameL_column():
    conn = sqlite3.connect('D:/Getting and cleanning/dynasties_history.db')
    c = conn.cursor()

    countries = ["thailand", "china", "japan", "vietnam", "france"]
    for country in countries:
        c.execute(f'SELECT id, NameL FROM dynasties_{country}')
        rows = c.fetchall()
        for row in rows:
            nameL = row[1]
            if nameL:
                if len(re.findall(r'\d', nameL)) >= 3:
                    c.execute(f'UPDATE dynasties_{country} SET NameL = NULL WHERE id = ?', (row[0],))
                    print(f"ลบข้อมูล '{nameL}' ที่มีตัวเลขออกจากฐานข้อมูลของ {country}")
    
    conn.commit()
    conn.close()
    print("เสร็จสิ้นการลบข้อมูล")

def display_dynasties_from_db(country):
    conn = sqlite3.connect('D:/Getting and cleanning/dynasties_history.db')
    c = conn.cursor()
    
    c.execute(f'SELECT * FROM dynasties_{country}')
    rows = c.fetchall()

    print(f"ราชวงศ์ใน {country.capitalize()}:")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Title: {row[1]}")
        print(f"NameL: {row[2]}")
        print(f"Summary: {row[3][:50]}...")
        print(f"Content: {row[4][:100]}...")
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    
    conn.close()

clear_all_data()

for country, titles in dynasty_titles.items():
    insert_dynasties_to_db(country, titles, 'th')

clean_nameL_column()

print("------------------------------------------------------------------------------------------------------------------------------------------------------")
for country in dynasty_titles.keys():
    display_dynasties_from_db(country)

print("ฐานข้อมูลอยู่ที่ ( D:/Getting and cleanning/dynasties_history.db )")
