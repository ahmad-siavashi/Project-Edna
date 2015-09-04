# Developer: Ahmad Siavashi
# Email: ahmad.siavashi@gmail.com
from bluetooth import *
from multiprocessing import *
from threading import *
from Tkinter import *


service_uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
messages = dict()
devices_list = []

def broadcaster(my_messages):
    global service_uuid
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)
    advertise_service(server_sock, "Project Edna",
                      service_id=service_uuid,
                      service_classes=[service_uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE], description=my_messages)
    # import tkMessageBox
    # tkMessageBox.showinfo('H', my_messages)
    server_sock.accept()


def update():
    global messages
    global messages_list
    global recently_seen_devices_list
    messages_list.delete(0, END)
    recently_seen_devices_list.delete(0, END)
    last_seen_list = []
    list_of_messages = []
    for key in messages.keys():
        recv = messages[key].split('|')
        try:
            recv.remove('')
        except Exception as e:
            print e.message
        last_seen_list.append((key, recv[0]))
        for i in xrange(len(recv)/2):
            print recv
            try:
                list_of_messages += [(key, recv[i*2+1], recv[i*2+2])]
            except Exception as e:
                print e.message
    list_of_messages = sorted(list_of_messages, key=lambda x: x[2])
    for item in list_of_messages:
        print item[0] + ': ' + item[1] + ' (' + item[2] + ')'
        messages_list.insert(END, item[0] + ': ' + item[1] + ' (' + item[2] + ')')
    last_seen_list = sorted(last_seen_list, key=lambda x: x[1], reverse=True)
    for item in last_seen_list:
        print item[0] + ': ' + item[1]
        recently_seen_devices_list.insert(END, item[0] + ': ' + item[1])

def receiver():
    global service_uuid
    global messages
    global devices_list
    receive_list = devices_list[:]
    search_list = []
    while True:
        if len(devices_list) != 0:
            if receive_list != devices_list:
                receive_list = devices_list[:]
                nearby_devices = discover_devices(lookup_names=True)
                for device in nearby_devices:
                    if device[1].upper() in receive_list:
                        search_list.append(device[0])
        else:
            search_list = discover_devices()
        #nearby_devices = ['5C:93:A2:A0:51:1C']

        for device in search_list:
            services = find_service(address=device)
            for service in services:
                if service['name'] != 'Project Edna':
                    continue
                name = lookup_name(device)
                messages[name] = service['description']
                print name, service['description']
        # nearby_devices = discover_devices(duration=8, lookup_names=True)
        # for device in nearby_devices:
        #     name = device[1]
        #     service = find_service(address=device[0], uuid=service_uuid)
        #     if len(service) != 0:
        #         time = str(datetime.datetime.now().time())
        #         messages[name] = time + service[0]['description']
        #         print name, service[0]['description']
                update()


def sendButtonCallBack():
    global message_textbox
    global broadcaster_process
    global messages
    import datetime
    time = str(datetime.datetime.now().time())
    time = time[:time.index('.')]
    messages['Me'] = messages.get('Me', time) + '|' + (message_textbox.get()) + '|' + time
    messages['Me'] = messages['Me'][messages['Me'].index('|'):]
    messages['Me'] = time + messages['Me']
    message_textbox.delete(0, END)
    broadcaster_process.terminate()
    broadcaster_process = Process(target=broadcaster, args=(messages.get('Me', '|'),))
    broadcaster_process.start()
    update()

def focusButtonCallBack():
    global focus_textbox
    global  broadcaster_process
    global devices_list
    for device in focus_textbox.get().split(','):
        devices_list.append(device.strip().upper())

root = Tk()
root.wm_title('Project Edna')
root.geometry('500x500')

def onMainWindowExit():
    global broadcaster_process
    try:
        broadcaster_process.terminate()
    except Exception as e:
        print e.message
    root.destroy()
    import os
    os._exit(0)

root.protocol('WM_DELETE_WINDOW', onMainWindowExit)

focus_button = Button(root, text="Focus", command=focusButtonCallBack)
focus_button.pack(side=BOTTOM, fill=X)

focus_textbox = Entry(root, bd=5)
focus_textbox.pack(side=BOTTOM, fill=X)

focus_label = Label(root, text='Focus on devices(Hint: <empty> == All, [Device1, Device2, ...]): ')
focus_label.pack(side=BOTTOM, fill=X, pady='10')

send_button = Button(root, text="Send", command=sendButtonCallBack)
send_button.pack(side=BOTTOM, fill=X)

message_textbox = Entry(root, bd=5)
message_textbox.pack(side=BOTTOM, fill=X)
message_textbox.bind("<Return>", lambda x: sendButtonCallBack())

message_label = Label(root, text='Message Box')
message_label.pack(side=BOTTOM, fill=X, pady='10')

scrollbar = Scrollbar(root)
scrollbar.pack(side=LEFT, fill=Y)

messages_list = Listbox(root, yscrollcommand=scrollbar.set)

messages_list.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar.config(command=messages_list.yview)

scrollbar2 = Scrollbar(root)
scrollbar2.pack(side=LEFT, fill=Y)

recently_seen_devices_list = Listbox(root, yscrollcommand=scrollbar2.set)

recently_seen_devices_list.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar2.config(command=recently_seen_devices_list.yview)

if __name__ == '__main__':
    import datetime
    time = str(datetime.datetime.now().time())
    time = time[:time.index('.')]
    broadcaster_process = Process(target=broadcaster, args=(time + messages.get('Me', '|'),))
    broadcaster_process.start()
    receiver_thread = Thread(target=receiver)
    receiver_thread.start()
    message_textbox.focus_set()
    mainloop()
