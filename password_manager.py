#! python3

try:
	from AES_128 import AES_128
	from colorama import Fore, Back, Style
	import os, shutil, getpass, sys, ast, webbrowser
except Exception as Error:
	print(Error)
	
path_for_accounts = os.getcwd() + '/accounts'
current_path = os.getcwd()

'''
Github: https://www.github.com/m3r4j'
Author: m3r4j
'''

def banner():
	print(Fore.BLUE + '''

	██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
	██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
	██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
	██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
	██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
	╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝
	  
	███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
	████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
	██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
	██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
	██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
	╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
	
	''')

def get_file(filename):
	result = ''
	filename = open(str(filename),'r').readlines()
	for lines in filename:
		result += lines
	if result.split() == []:
		pass
	else:
		return result
		

def validate(password):
	if len(password) == 16:
		os.chdir(path_for_accounts)
		shutil.copy('accounts.txt',current_path)
		os.chdir(current_path)
		AES_128.decrypt('accounts.txt',password)
		result = get_file('accounts.txt')
		
		if result[0] == '{' and result[len(result)-1] == '}':
			os.remove('accounts.txt')
			return True
			
	return False
			
def encrypt_data(password):
	os.chdir(path_for_accounts)
	AES_128.encrypt('accounts.txt',password)
	os.chdir(current_path)
	
	
def decrypt_data(password):
	os.chdir(path_for_accounts)
	AES_128.decrypt('accounts.txt',password)
	os.chdir(current_path)
	
	
def unlock_accounts(password):
	decrypt_data(password)
	
def lock_accounts(password):
	encrypt_data(password)
	
	
def change_password(current_password,new_password):
	unlock_accounts(current_password)
	lock_accounts(new_password)
	
def create_files():
	os.chdir(path_for_accounts)
	with open('accounts.txt','a') as a:
		pass


def options():
	print(Fore.RED + '''
	1. Add Account
	2. Remove Account
	3. Search Account
	4. Change Password
	5. Exit
	''')
	print()


	

	
	
def check_if_new():
	os.chdir(path_for_accounts)
	if get_file('accounts.txt') == None or get_file('accounts.txt') == '{}':
		with open('accounts.txt','w') as w:
			w.write('{}')
		
		new_password = getpass.getpass(Fore.YELLOW + 'New Password: ')
		while not len(new_password) == 16:
			new_password = getpass.getpass(Fore.YELLOW + 'New Password: ')
		lock_accounts(new_password)
		print('Password-Manager configured.')
		print()
	
	
def add_account(dictionary,service,username,password):
	dictionary[service] = {'username':username,'password':password}
	save_changes(dictionary)

def save_changes(dictionary):
	os.chdir(path_for_accounts)
	with open('accounts.txt','w') as w:
		w.write(str(dictionary))
	
def search_account(dictionary,service):
	if dictionary.get(service):
		print(f'Service: {service}\nUsername: {dictionary[service]["username"]}\nPassword: {dictionary[service]["password"]}')
	else:
		print('Account not found.')
	
	
def remove_account(dictionary,service):
	if dictionary.get(service):
		dictionary.pop(service)
		save_changes(dictionary)
	else:
		print('Account not found.')
		
def main():
	if not os.path.exists(path_for_accounts) : os.mkdir(path_for_accounts)
	create_files()
	banner()
	check_if_new() 
	
	
	password = getpass.getpass(Fore.YELLOW + 'Password: ')
	while not validate(password):
		password = getpass.getpass(Fore.YELLOW + 'Password: ')
	print()
	
	key = password
	unlock_accounts(key)
	
	os.chdir(path_for_accounts)
	
	accounts = get_file('accounts.txt')
	accounts = ast.literal_eval(accounts)
	
	lock_accounts(key)
	
	while True:
		print()
		options()
		option = input(Fore.CYAN + 'Enter an option: ')
		print()
		
		if option == '1':
			service = input('Service: ').lower()
			username = input('Username: ')
			password = getpass.getpass()
			add_account(accounts,service,username,password)
			lock_accounts(key)
		
		elif option == '2':
			service = input('Service: ').lower()
			remove_account(accounts,service)
			lock_accounts(key)
			
		elif option == '3':
			service = input('Service: ').lower()
		      	print()
			search_account(accounts,service)
			
		elif option == '4':
			new_password = getpass.getpass(Fore.YELLOW + 'New Password: ')
			while len(new_password) != 16:
				new_password = getpass.getpass(Fore.YELLOW + 'New Password: ')
			change_password(key,new_password)
			key = new_password
			
		elif option == '5':
			sys.exit()
		      
		else:
		      	print('Invalid option.')

main()


