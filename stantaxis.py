import stanza
import conllu

txt = input('Введите текст: \n')
pipeline = stanza.Pipeline(lang='ru',processors='lemma,tokenize,pos,depparse')
doc = pipeline(txt)

#res = CoNLL.doc2conll_text(doc) #Преобразуем пайплайн в conllu
res = "{:C}".format(doc)
#print(res)
sents = conllu.parse_tree(res) #Преобразуем conllu в дерево
#sents[0].print_tree()
root = sents[0].token
print(f'Корень: {root}.')

root = sents[0]
root_token = root.token
root_lemma = root.token['form']
root_children = root.children
root_children_tokens = [x.token for x in root_children]
#print([root_token])

#Заводим два массива
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
[print(item) for item in result] #Печатаем, что получилось

    


