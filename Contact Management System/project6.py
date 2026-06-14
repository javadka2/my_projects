import csv
import os
from datetime import datetime

CONTACTS_FILE = 'Contacts.csv'

def load_file():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE , 'w',encoding='utf-8', newline='') as f:
            writers = csv.writer(f)
            writers.writerow(['Name', 'Phone', 'Email', 'Created_at'])

def get_contacts_from_file():
    load_file()

    contacts = []
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                print(f"Warning: '{CONTACTS_FILE}' seems empty or missing headers.")
                return []
            for row in reader:
                contacts.append(row)
        return contacts
    except FileNotFoundError:
        print(f"Error: Contact file '{CONTACTS_FILE}' not found during read.")
        return []
    except Exception as e:
        print(f'Error reading contacts: {e}')
        return []   

def find_contacts_by_name(name):
    all_contacts = get_contacts_from_file()
    found_contacts = []
    if not all_contacts:
        print("No contacts available to search.")
        return []
        
    for contact in all_contacts:
        if isinstance(contact,dict):
            if name.lower() in contact.get('Name', '').lower():
                found_contacts.append(contact)

    if not found_contacts:
            print(f"No contacts found matching '{name}'.")
    return found_contacts    
        
def add_contact():
    load_file()

    print('\n--- Add a new contact ---')
    contact_name = input('Enter contact name: ').strip()
    if not contact_name:
        print('Error: Contact name cannot be empty.')
        return

    contact_phone = input('Enter contact phone number: ').strip()
    if not contact_phone:
        print('Error: Contact phone number cannot be empty.')
        return

    contact_email = input('Enter contact email (optional): ').strip()  
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Contact = {
        'Name': contact_name,
        'Phone': contact_phone,
        'Email': contact_email,
        'Created_at': current_time
    }

    try:
        with open(CONTACTS_FILE, 'a',encoding='utf-8', newline='') as f:
            fieldnames = ['Name', 'Phone', 'Email', 'Created_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(Contact)
        print(f'Contact {contact_name} added successfully')
    except Exception as e:
        print(f'Error {e}')
def show_contacts():
    print('\n ----- All Contacts -----')
    all_contacts = get_contacts_from_file()
    if not all_contacts:
        print('No contacts found in the address book.')
        return

    headers = ['Name', 'Phone', 'Email', 'Created at']
    col_widths = {header: len(header) for header in headers}
    for contact in all_contacts:
        col_widths['Name'] = max(col_widths['Name'], len(contact.get('Name', '')))
        col_widths['Phone'] = max(col_widths['Phone'], len(contact.get('Phone', '')))
        col_widths['Email'] = max(col_widths['Email'], len(contact.get('Email', '')))
        col_widths['Created at'] = max(col_widths['Created at'], len(contact.get('Created_at', '')))

    header_line = "  ".join(f"{h:<{col_widths[h]}}" for h in headers)
    print(header_line)
    print('-' * len(header_line))

    rows_found = False
    for contact in all_contacts:
        rows_found = True
        name = contact.get('Name', 'N/A')
        phone = contact.get('Phone', 'N/A')
        email = contact.get('Email', '') if contact.get('Email') else '-'
        created_at = contact.get('Created_at', 'N/A')
        
        print(f"{name:<{col_widths['Name']}}  {phone:<{col_widths['Phone']}}  {email:<{col_widths['Email']}}  {created_at:<{col_widths['Created at']}}")
    
    if not rows_found:
        print('No entries found for contacts')

def search_contact():
    print('\n--- Search Contacts ---')
    search_term = input('Enter the name: ').strip()
    if not search_term:
        print('Search term cannot be empty.')
        return

    found_contacts = find_contacts_by_name(search_term)

    if found_contacts:
        print(f"\nFound {len(found_contacts)} contact(s):")
        col_widths = {
                'Name': len('Name'),
                'Phone': len('Phone'),
                'Email': len('Email'),
                'Created_at': len('Created_at')
                }
        for contact in found_contacts:
            col_widths['Name'] = max(col_widths['Name'], len(contact.get('Name', '')))
            col_widths['Phone'] = max(col_widths['Phone'], len(contact.get('Phone', '')))
            col_widths['Email'] = max(col_widths['Email'], len(contact.get('Email', '')))
            col_widths['Created_at'] = max(col_widths['Created_at'], len(contact.get('Created_at', '')))

        header = (f"{'Name'.ljust(col_widths['Name'])} | {'Phone'.ljust(col_widths['Phone'])} | {'Email'.ljust(col_widths['Email'])} | {'Created_at'.ljust(col_widths['Created_at'])}")
        print(header)
        print("-" * len(header))

    for contact in found_contacts:
        name = contact.get('Name', 'N/A')
        phone = contact.get('Phone', 'N/A')
        email = contact.get('Email', '') if contact.get('Email') else '-'
        created_at = contact.get('Created_at', 'N/A')
            
        print(f"{name.ljust(col_widths['Name'])} | {phone.ljust(col_widths['Phone'])} | {email.ljust(col_widths['Email'])} | {created_at.ljust(col_widths['Created_at'])}")
def update_contact():
    name_to_update = input('Please enter a name to update: ')
    contacts = get_contacts_from_file()
    
    updated_contacts = []
    found = False

    for contact in contacts:
        if contact.get('Name', '').lower() == name_to_update.lower():
            found = True

            print(f"Name: {contact.get('Name')}, "
                  f"Phone: {contact.get('Phone')}, "
                  f"Email: {contact.get('Email')} found")

            print("\nWhat do you want to do?")
            print("1. Edit contact normally")
            print("2. Add new phone number")
            choice = input("Choose (1-2): ").strip()

            if choice == '2':
                current_phones = contact.get('Phone', '')
                phones_list = current_phones.split('|') if current_phones else []
                new_phone = input("Enter new phone number to add: ").strip()

                if new_phone:
                    if new_phone in phones_list:
                        print("This phone number already exists for this contact.")
                        updated_phone = current_phones
                    else:
                        phones_list.append(new_phone)
                        updated_phone = "|".join(phones_list)
                        print("Phone number added successfully.")
                else:
                    print("No phone entered. Nothing changed.")
                    updated_phone = current_phones

                updated_contacts.append({
                    'Name': contact.get('Name'),
                    'Phone': updated_phone,
                    'Email': contact.get('Email'),
                    'Created_at': contact.get('Created_at')
                })

            else:
                new_name = input(f"New name ({contact.get('Name')}): ") or contact.get('Name')
                new_phone = input(f"New phone number ({contact.get('Phone')}): ") or contact.get('Phone')
                new_email = input(f"New email ({contact.get('Email')}): ") or contact.get('Email')

                if not new_name or not new_phone:
                    print('Name and phone number cannot be empty')
                    updated_contacts.append(contact)
                    continue

                updated_contacts.append({
                    'Name': new_name,
                    'Phone': new_phone,
                    'Email': new_email if new_email else 'N/A',
                    'Created_at': contact.get('Created_at')
                })

                print(f'Contact: {name_to_update} updated successfully ✅')

        else:
            updated_contacts.append(contact)

    if not found:
        print(f'Contact: {name_to_update} not found.')
        return

    try:
        with open(CONTACTS_FILE, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Phone', 'Email', 'Created_at']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # ✅ بهتره هدر هم نوشته بشه
            writer.writerows(updated_contacts)

    except Exception as e:
        print(f'Error: {e}')

def delete_contact():
    name_to_delete = input('Enter contact name to delete: ')
    contacts = get_contacts_from_file()
    
    initial_count = len(contacts)
    contacts_after_delete = [contact for contact in contacts if contact.get('Name', '').lower() != name_to_delete.lower()]
    
    final_count = len(contacts_after_delete)
    
    if initial_count == final_count:
        print(f'contact: {name_to_delete} didnt find.')
        return

    try:
        with open(CONTACTS_FILE, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Phone', 'Email', 'Created_at']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(contacts_after_delete)
        print(f'contact: {name_to_delete} deleted successfully.')
    except Exception as e:
        print(f'Error: {e}')
def display_menu():
    print('\n==== Contacts Manager ====')
    print('1. Add a contact')
    print('2. Update a contact')
    print('3. Show all the contacts')
    print('4. search for a contact')
    print('5. Delete a contact')
    print('6. Exit')

if __name__ == '__main__':
    load_file()

while True:
    display_menu()
    choice = input('Choose an option(1-6): ')
    if choice == '1':
        add_contact()
    elif choice == '2':
        update_contact()
    elif choice == '3':
        show_contacts()
    elif choice == '4':
        search_contact()
    elif choice == '5':
        delete_contact()
    elif choice == '6':
        print('GoodBye.')
        break
    else:
        print('Please enter a number between 1-6')