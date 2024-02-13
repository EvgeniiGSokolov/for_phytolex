import stanza, conllu, chardet, docx
from tkinter.filedialog import askopenfilenames as ask

def gettext(file):
    try:
        #print(f'{file}')
        if file.endswith('.txt'):
            text = open(rf'{file}','rb')
            text_body = text.read()
            enc = chardet.detect(text_body).get("encoding")
            #print(enc)
            if enc and enc.lower() != "utf-8" and enc.lower() != "windows-1251":
                text_body = text_body.decode(enc)
                text_body = text_body.encode("utf-8")
                text_body = text_body.decode("utf-8")
                #print('Открыт текст!')
                return text_body
            elif enc and enc.lower() == "windows-1251":
                text = open(rf'{file}', 'r', encoding = 'windows-1251')
                text_body = text.read()
                text.close()
                #print('Открыт текст!')
                return text_body
            else:
                text = open(rf'{file}', 'r', encoding = 'UTF-8')
                text_body = text.read()
                text.close()
                #print('Открыт текст!')
                return text_body
        elif file.endswith('.docx'):
            doc = docx.Document(rf'{file}')
            text = (paragraph.text for paragraph in doc.paragraphs)
            text_body = '\n'.join(text)
            return text_body
        else:
            #print('Неподдерживаемый формат!')
            pass
    except:
        pass 

files = ask()
pipeline = stanza.Pipeline(lang='ru',processors='lemma,tokenize,pos,depparse')

def process(file):
    global pipeline
    text = gettext(file)
    doc = pipeline(text)
    res = "{:C}".format(doc)
    sents = conllu.parse_tree(res) #Преобразуем conllu в дерево
    for sent in range(0,len(sents)):
        #root = sents[sent].token
        #print(f'Корень: {root}.')

        root = sents[sent]
        root_token = root.token
        root_children = root.children

        inp = [] #Входной; здесь у нас будут поддеревья.
        outp = [] #Выходной; здесь будут словари со вхождениями.
        outp.append(root_token) #Добавляем в выходной массив вхождение корневого узла
        [inp.append(subtree) for subtree in root_children] #Добавляем во входной массив все поддеревья, возглавляемые дочерьми корневого узла
        while inp != []: #Пока входной массив не пуст, продолжается цикл:
            for elt in inp: #Для каждого элемента elt во входном массиве
                outp.append(elt.token) #-добавить в выходной массив вхождение элемента elt
                elt_children = elt.children #-определить множество дочерей элемента elt
                [inp.append(child) for child in elt_children] #Добавляем каждую дочь во входной массив
                inp.remove(elt) #Удаляем из входного массива их маму
                inp = [item for item in inp if item != []] #Оставляем во входном массиве только непустые элементы

        #Дальше преобразуем выходной массив в результативный массив словарей, содержащих данные о каждом токене в предложении
        result = [{'id':elt['id'],'form':elt['form'],'lemma':elt['lemma'],'head':elt['head'],'deprel':elt['deprel']} for elt in outp]
        result = sorted(result, key=lambda x: x['id']) #Сортируем по id 
        print(sent)
        [print(item) for item in result] #Печатаем, что получилось
    
[process(file) for file in files]