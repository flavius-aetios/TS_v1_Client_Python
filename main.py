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
    '3dB': '3900',
    '4dB': '3700',
    '5dB': '3510',
    '6dB': '3305',
    '7dB': '3090',
    '8dB': '2830',
    '9dB': '2470',
    '10dB': '1950',
    '11dB': '1350',
    '12dB': '950',
    '13dB': '700',
    '14dB': '530',
    '15dB': '395',
    '16dB': '265',
    '17dB': '120',
}

layout = [
    [sg.Text('Порт:', size=(16, 1)), sg.Text('Ослабление:', size=(10, 1)),],
    [sg.Combo(getComPortsList(), size=(6, 5), readonly=True, key='COM'), sg.Button('Обновить', button_color=('black', '#DCDCDC')),
     sg.Combo(combo_list, size=(6, 10), readonly=True, key='ATT'), sg.Radio('Значение ослабления из списка', "RADIO1", key='Radio_combo', default=True)],
    [sg.Text('DAC Value (0-4095):', size=(15, 1), pad=((5,15),0)), sg.InputText(size=(8, 1), key='text_DAC_val'), sg.Radio('Значение ЦАП', "RADIO1", key='Radio_dac_val')],
    [sg.Output(size=(66, 10))],
    [sg.Submit('Подтвердить', pad=((405,0),1))]
]

icon_base64 = b'iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAP1BMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABHcEyWpW0nAAAAFXRSTlP/+AyyWWb74i4Giqbrcw0R9SPHUAClWLX2AAACEklEQVR42u3b25KDIAwGYOyqnNTWuu//rLvWqdqpToH8kN2Z5Kp3+QYBEyrqmzmUAAQggL8CsJfCYfcAa3r/VTh8b+wTMDrdqvKh3bgAzF0xxd3MAL78D4EavGIMP6ip4wR0k2IdgN8hUJoXoNW6ANuisWbdnoZrCoZ/33i0KfkGmCpmQC0AAQhAAAIQgAD+F8CagRdQazdwAhqtbmhBBMDWc+GOFkQA6qVxAAvCAc2zccEKQgG23honqCAU8NK6IwXBI9B0eQTBcyCXIHwSZhLE7ANZBDE7YRZB1FacQxD5NsQLIusBvCC2IIELoisitCC+JAMLEmpCrCClKIUKkqpipCCtLAcKEvsCnCC1MYEJkjsjlCC9NQMJCL2hbW4vAssLqNyF9RG07so6CavU/KBlmJ4fsxER8kO2Ykp+xMuIlB/wOqblpxckxPzkkoyan1qUkvMTy3J6flpjAshPas0Q+SnNKSQ/oT3H5E8/oADlTz6iOchvQwJ1SHWQ/+r85+gt5pjuaPzHkE9AfDJgvH96/pkB+6Pa4/mXGbATnMz/3ID1uPxs/eUHLH8YnK7/AoB5DM73nxKA+U+r0/2vCMCa8/13aPrPMREBGUIAAhCAAAQgAAEI4ADQ9XXBcNun3euvqmTsPm5n/7yf/YID+xUP9ksu7Nd8+C86cV31aterXvyX3R4G1ut+nCEAAQiAHfAD1PNjIYVXmu0AAAAASUVORK5CYII='

sg.set_global_icon(icon_base64)
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
        if values['Radio_dac_val'] is True and \
                (values['text_DAC_val'].isdigit() == False or int(values['text_DAC_val']) < 0 or int(values['text_DAC_val']) > 4095):
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
