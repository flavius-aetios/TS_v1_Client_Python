import serial
import PySimpleGUI as sg
from serial.tools.list_ports import comports

#Проверка на доступность порта
def portIsUsable(portName):
    try:
       ser = serial.Serial(port=portName)
       return True
    except:
       return False

#Создание списка доступных COM портов
def getComPortsList():
    list = comports()
    connected = []
    connected.append('-------')
    for element in list:
        connected.append(element.device)
    return connected

sg.theme('LightGrey1')

combo_list = ['REF', '1dB', '2dB', '3dB', '4dB', '5dB', '6dB', '7dB', '8dB', '9dB', '10dB', '11dB', '12dB', '13dB', '14dB', '15dB', '16dB', '17dB']

text_to_value = {
    'REF': '4095',
    '1dB': '4095',
    '2dB': '4095',
    '3dB': '3935',
    '4dB': '3740',
    '5dB': '3550',
    '6dB': '3360',
    '7dB': '3155',
    '8dB': '2910',
    '9dB': '2620',
    '10dB': '2255',
    '11dB': '1855',
    '12dB': '1443',
    '13dB': '1125',
    '14dB': '862',
    '15dB': '630',
    '16dB': '402',
    '17dB': '169',
}

layout = [
    [sg.Text('Порт:', size=(16, 1)), sg.Text('Ослабление:', size=(10, 1)),],
    [sg.Combo(getComPortsList(), size=(6, 5), readonly=True, key='COM'), sg.Button('Обновить', button_color=('black', '#DCDCDC')),
     sg.Combo(combo_list, size=(6, 10), readonly=True, key='ATT'), sg.Radio('Значение ослабления из списка', "RADIO1", key='Radio_combo', default=True)],
    [sg.Text('DAC Value (0-4095):', size=(16, 1)), sg.InputText(size=(8, 1), key='text_DAC_val'), sg.Radio('Значение ЦАП', "RADIO1", key='Radio_dac_val')],
    [sg.Output(size=(66, 10))],
    [sg.Submit('Подтвердить', pad=((405,0),1))]
]

sg.set_global_icon(icon = r'Terminal.ico')
window = sg.Window('TS_v1 COM Terminal', layout)

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break
    if event == 'Обновить':
        window.FindElement('COM').Update(values=getComPortsList())
        print('Список портов обновлён')
        continue
    if event == 'Подтвердить':
        if values['COM'] == '' or values['COM'] == '-------':
            print('Выберите COM порт!')
            continue
        if values['Radio_combo'] is True and values['ATT'] == '':
            print('Выберите величину ослабления!')
            continue
        if values['Radio_dac_val'] is True and values['text_DAC_val'] == '':
            print('Введите значение DAC value!')
            continue
        if values['text_DAC_val'].isdigit() == False or int(values['text_DAC_val']) < 0 or int(values['text_DAC_val']) > 4095:
            print('Введите корректное значение DAC value (0-4095) !')
            continue

        #Инициализация COM порта
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = values['COM']

        #Проверка на доступность порта
        if not portIsUsable(ser.port):
            print("Порт " + values['COM'] + " недоступен!")
            window.FindElement('COM').Update(values=getComPortsList())
            continue

        ser.open()

        if values['Radio_combo'] is True:
            msg = bytes(text_to_value[values['ATT']].encode('utf-8'))
            try:
                ser.write(msg)
                ser.close()
            except:
                print("При передаче возникла ошибка! Порт " + values['COM'] + " недоступен!")
                continue

            print("Сигнал ослаблен на: " + values['ATT'])
            continue


        if values['Radio_dac_val'] is True:
            msg = bytes(values['text_DAC_val'].encode('utf-8'))
            try:
                ser.write(msg)
                ser.close()
            except:
                print("При передаче возникла ошибка! Порт " + values['COM'] + " недоступен!")
                continue

            print("Задано значение ЦАП: " + values['text_DAC_val'])
            continue

window.close()
