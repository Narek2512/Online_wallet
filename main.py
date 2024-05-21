import requests
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sql import add_user, delete_user, update_password, update_balance, get_user, get_user_by_id, update_country


while True:
    command = input(f"""
For registration Enter 'r'
To login Enter 'l':
""")

    if command == "r":
        #COUNTRY
        #####################################################################
        ip_address = requests.get('https://api.ipify.org').text
        location = requests.get(f'https://ipinfo.io/{ip_address}/json').json()
        #####################################################################
        #SYMBOL AND VALUE
        res = requests.get(f'https://restcountries.com/v3.1/alpha/{location["country"]}').json()
        currencies = res[0]['currencies']
        currencies_code = currencies.keys()




        for code in currencies_code:
            currencies_code = code
        #####################################################################

        user_name = input("Enter your name: ")
        user_surname = input("Enter your surname: ")
        ##############################################
        user_email = input("Enter your email: ")
        message = MIMEMultipart()
        message["from"] = 'python2512@mail.ru'
        message["To"] = user_email
        message["Subject"] = 'Password check'
        random_code = random.randint(100000, 999999)
        message.attach(MIMEText(f'Your code {random_code}', "plain"))
        try:
            with smtplib.SMTP_SSL('smpt.mail.ru', 465) as server:
                server.login('python2512@mail.ru', 'eGZy8vBNzGfd5EZ1e3zA')

                server.sendmail('python2512@mail.ru', user_email, message.as_string())
            password_check = int(input("Enter code we sent to your email: "))
            if password_check == random_code:
                user_password = int(input("Create a password: "))
                add = add_user(user_name, user_surname, user_email, user_password, 0, location["country"], currencies[currencies_code]["symbol"], currencies_code)
                if add:
                    print("Registration successed! ")

                else:
                    print("Registration Error!")

            else:
                print("Invalid code!")
        except:
            print("Registration Error!")


    elif command == "l":
        user_info = get_user()
        email = input("Enter your email: ")
        password = int(input("Enter your password: "))
        for i in user_info:

            if email == i[3] and password == i[4]:
                balance = i[5]
                print(f"Welcome {i[1]}!")
                print("-" * 20)

                print(f"Your Balance: {i[7]}{balance}")
                print("**Commands**")
                print("To cash in enter '+'")
                print("To cash out Enter '-'")
                print("To transfer money Enter 't'")
                print("To check history Enter 'h'")
                print("To change password Enter 'c'")
                print("To delete account Enter 'del'")
                print("To log out Enter 'log out'")
                print("To change country Enter 'change country'")
                print("-" * 20)
                while True:
                    command = input("Enter command: ")
                    #Cash in
                    if command == '+':
                        cash_in = int(input("Enter sum to cash in: "))
                        if cash_in <= 0:
                            print("Cash in Error!")
                        else:
                            balance = balance + cash_in
                            update_balance(i[0], balance)

                            message = MIMEMultipart()
                            message["from"] = 'python2512@mail.ru'
                            message["To"] = i[3]
                            message["Subject"] = 'Online Wallet'
                            message.attach(MIMEText(f'You cash in ${cash_in}', "plain"))
                            try:
                                with smtplib.SMTP_SSL('smpt.mail.ru', 465) as server:
                                    server.login('python2512@mail.ru', 'eGZy8vBNzGfd5EZ1e3zA')
                                    server.sendmail('python2512@mail.ru', i[3], message.as_string())
                                    print("Cash in seccessed!")
                            except:
                                print("Cash in Error!")
                    #Cash out
                    elif command == "-":
                        cash_out = int(input("Enter sum to cash out: "))
                        if cash_out <= 0 or cash_out > balance:
                            print("Error!")
                        else:
                            balance = balance - cash_out
                            update_balance(i[0], balance)

                            message = MIMEMultipart()
                            message["from"] = 'python2512@mail.ru'
                            message["To"] = i[3]
                            message["Subject"] = 'Online Wallet'
                            message.attach(MIMEText(f'You cash out ${cash_out}', "plain"))
                            try:
                                with smtplib.SMTP_SSL('smpt.mail.ru', 465) as server:
                                    server.login('python2512@mail.ru', 'eGZy8vBNzGfd5EZ1e3zA')
                                    server.sendmail('python2512@mail.ru', i[3], message.as_string())
                                    print("Cash out seccessed!")
                            except:
                                print("Cash out Error!")

                    #Transfer
                    elif command == "t":

                        transfer_to = int(input("Enter user id to transfer cash: "))
                        if transfer_to == i[0] or get_user_by_id(transfer_to) == None:
                            print("Invalid Id!")

                        else:

                            send_money = int(input("Enter sum to transfer: "))
                            if send_money <= 0 or send_money > balance:
                                print("Transfer Error!!")
                            else:
                                #Transfer_to_user_balance update
                                data = requests.get(f'https://open.er-api.com/v6/latest/{i[8]}').json()
                                a = data["rates"][get_user_by_id(transfer_to)[8]]
                                print(a)

                                balance_2 = get_user_by_id(transfer_to)[5]
                                balance_2 += send_money
                                update_balance(transfer_to, balance_2)
                                #User balance update
                                balance -= send_money
                                update_balance(i[0], balance)
                                print("Transfer successed!")
                                #send email
                                message = MIMEMultipart()
                                message["from"] = 'python2512@mail.ru'
                                message["To"] = i[3]
                                message["Subject"] = 'Online Wallet'
                                message.attach(MIMEText(f'You transferred to Id:{get_user_by_id(transfer_to)[0]} - ${send_money}'))
                                try:
                                    with smtplib.SMTP_SSL('smpt.mail.ru', 465) as server:
                                        server.login('python2512@mail.ru', 'eGZy8vBNzGfd5EZ1e3zA')
                                        server.sendmail('python2512@mail.ru', i[3], message.as_string())
                                except:
                                    print("Mail Error!")

                                #mail2
                                message = MIMEMultipart()
                                message["from"] = 'python2512@mail.ru'
                                message["To"] = get_user_by_id(transfer_to)[3]
                                message["Subject"] = 'Online Wallet'
                                message.attach(
                                    MIMEText(f'You got ${send_money} from Id: {i[3]}'))
                                try:
                                    with smtplib.SMTP_SSL('smpt.mail.ru', 465) as server:
                                        server.login('python2512@mail.ru', 'eGZy8vBNzGfd5EZ1e3zA')
                                        server.sendmail('python2512@mail.ru', get_user_by_id(transfer_to)[3], message.as_string())
                                except:
                                    print("Mail Error!")



                    # elif command == "h":
                    #
                    #
                    #     print(f"Today you cash in ${cash_in}")
                    #     print(f"Today you cash out ${cash_out}")
                    #     print(f"You transfer to {get_user_by_id(transfer_to)[1]} ${send_money}")

                    elif command == "c":
                        password = int(input("Enter your account password: "))
                        if password == i[4]:
                            new_password = int(input("Create new password: "))
                            new_password_again = int(input("Enter new password again: "))



                            if new_password == i[4] and new_password_again == new_password:
                                update_password(i[0], new_password)
                                print("The password changed successfully!")

                            else:
                                print("Update error!")


                        else:
                            print("Incorrect password")



                    elif command == "del":
                        sure = input("Are you sure that you want to delete your account?(Yes/No): ")
                        if sure == "Yes":
                            check_password = int(input("Enter your account password: "))
                            if check_password == i[4]:

                               delete_user(i[0])
                               print("Deleted successfully!")
                            else:
                                print("Incorrect password!")

                    elif command == "change country":
                        country_name = input("Enter the name of the country code where you are located: ")
                        res = requests.get(f'https://restcountries.com/v3.1/alpha/{country_name}').json()
                        currencies = res[0]['currencies']
                        currencies_code = currencies.keys()
                        for code in currencies_code:
                            currencies_code = code

                        print(country_name)
                        print(currencies[currencies_code]['symbol'])
                        print(currencies_code)
                        if currencies[currencies_code]["symbol"] == "" or currencies_code == "":
                            print("Country change Error!")

                        else:
                            update_country(i[0], currencies[currencies_code]['symbol'], country_name.upper(), currencies_code)
                            print("Country changed")


                    elif command == "log out":
                        break

                    else:
                        print("Command Error!")



                print("-" * 20)




            else:
                print("Login Error")


