from enum import Enum
from openpyxl.styles import PatternFill

# {'red':'ffc7ce', 'yellow': 'ffeb9c', 'green': 'c6efce'}
class Color(Enum):
    RED = r'99001A'
    GREEN = r'66FF7F'
    YELLOW = r'E1FF4D'

'''
给excel cell上色
'''
final_status_fill = {'已达标': PatternFill('solid', start_color=Color.GREEN.value),
                     '未达标': PatternFill('solid', start_color=Color.RED.value),
                     '达标，但不满足0.7K': PatternFill('solid', start_color=Color.YELLOW.value),
                     '不满足0.7K': PatternFill('solid', start_color=Color.RED.value)}
