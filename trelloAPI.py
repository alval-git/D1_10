
import uuid
import sys 
import requests    
base_url = "https://api.trello.com/1/{}" 
auth_params = {    
    'key': "929b8359f6b040a49015b6afb9e3f837",    
    'token': "07dbad1262cd52c72ebab58c7231293604986e66ac5b6768c4fe2010f3554b6d", }
board_id = "5fb2ae49fa8d91218d01bbe1" 
def column_check(column_name):  
    column_id = None  
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
    for column in column_data:  
        if column['name'] == column_name:  
            column_id = column['id']  
            return column_id
def getDublicate(task_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    dublicate_tasks = []
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in task_data:
            if task_name == task['name']:
                dublicate_tasks.append(task)
    return dublicate_tasks
def counterTasks():
    counter_tasks = {}
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        counter_tasks[column['id']] = len(task_data)
    return counter_tasks    
def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    counter_tasks = counterTasks()
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(str(counter_tasks[column['id']])+' '+ column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'] + " id задачи: " + task['id'])    


def create(name, column_name):      
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})

def createColumn( column_name):            
    return requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json() 

def move(name, column_name): 
    dublicate_tasks = getDublicate(name)   
    if len(dublicate_tasks) > 1:  
        print("Задач с таким названием несколько:")  
        for task in dublicate_tasks:  
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']  
            print("задача с id: {}\tНаходится в колонке: {}\t ".format(task['id'], task_column_name))  
        task_id = input("Пожалуйста, введите ID задачи, которую нужно переместить: ")  
    else:  
        task_id = duplicate_tasks[0]['id']        
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']    
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})
    
if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3]) 
    elif sys.argv[1] == 'createColumn':
        createColumn(sys.argv[2])