import PySimpleGUI as SG
import queue
import os
import threading
import settings
import img2txt
from selenium import webdriver

stop_event = threading.Event()
stop_thread_flag = False


def clear_cookies():
    cookies = "cookies"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=" + cookies)
    driver2 = webdriver.Chrome('chromedriver.exe', options=options)
    driver2.delete_all_cookies()


def long_operation_thread(gui_queue, stop_event):
    while not stop_event.is_set():
        img2txt.start_convert(gui_queue, stop_event)


def update_output(new_row):
    # Append text to the Logs frame
    current_logs_text = window['user_text'].get()
    window['user_text'].update(current_logs_text + new_row)


gui_queue = queue.Queue()


def the_gui():
    SG.ChangeLookAndFeel('lightpurple')
    gui_queue = queue.Queue()

    output = [
        [SG.Frame(layout=[
            [SG.Output(size=(42, 8), pad=(0, 0))],
        ], title='Output', title_color="#3C323D")], ]
    layout = [
        [SG.Frame(layout=[
            [SG.Text('Platform:', size=(17, 1), font=("Roboto", 8)),
             SG.Text('Messenger', key="source", size=(25, 1))],
            [SG.Text('conversation name:', size=(17, 1), font=("Roboto", 8)),
             SG.Multiline('', key="conversation name", size=(27, 1))],
            [SG.Text('Username/Email:', size=(17, 1), font=("Roboto", 8)),
             SG.InputText('', key="username_email", size=(27, 1))],
            [SG.Text('Password:', size=(17, 1), font=("Roboto", 8)),
             SG.InputText('', key="password", password_char='*', size=(27, 1))],
        ],
            title='Login', title_color="#3C323D"), SG.Column(output)],
        [SG.Frame(layout=[
            [SG.Multiline(default_text='logs...', size=(91, 10), key='user_text')],
        ], title='Logs', title_color="#3C323D")],
        [SG.Button('Run', size=(10, 1), key="Run"), SG.Button('Exit', size=(10, 1))]
    ]
    global window
    window = SG.Window('Messenger - Low Data Mode', layout, default_element_size=(40, 1), grab_anywhere=False,
                       location=(5, 5))
    while True:
        event, values = window.read(timeout=1000)
        window['password'].update(disabled=False)
        window['user_text'].update(disabled=False)
        # If exit button is clicked
        if event in (None, 'Exit'):
            stop_event.set()
            print("closing...")
            window['Run'].update(disabled=False)

        # If run button is clicked
        elif event == 'Run':
            stop_event.clear()
            window['Run'].update(disabled=True)
            settings.password = values['password']
            settings.username_email = values['username_email']
            settings.conversation_name = values['conversation name'].split('\n')
            if values['username_email']:
                clear_cookies()
            # Calls the long_operation_thread

            try:
                thread = threading.Thread(target=long_operation_thread, args=(gui_queue, stop_event), daemon=True)
                thread.start()
                # Now, wait for messages from the thread
                while True:
                    try:
                        message = gui_queue.get(timeout=1)  # Adjust the timeout as needed
                        if message:
                            # Process the message, e.g., update the "Logs" frame
                            update_output(message)
                    except queue.Empty:
                        # If no more messages are queued up, break from the loop
                        break
            except Exception as e:
                print('Error')

        # Checks for incoming messages from threads
        try:
            # get_nowait() will get exception when Queue is empty
            message = gui_queue.get_nowait()
        except queue.Empty:
            # break from the loop if no more messages are queued up
            message = None
        # if message received from queue, display the message in the Window
        if message:
            print('Got a message back from the thread: ', message)
    # if user exits the window, then close the window and exit the GUI


if __name__ == '__main__':
    gui_queue = None
    the_gui()
    print('Exiting Program')
