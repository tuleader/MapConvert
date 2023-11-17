import unicodedata
from unidecode import unidecode
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    without_accents = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    # Replace specific characters like 'đ' with their non-accented counterparts
    without_accents = without_accents.replace('đ', 'd')
    without_accents = without_accents.replace('Đ', 'D')
    return without_accents

# Test the function
input_str = "Thẹ giới đầy rẫy những định kiến."
result = remove_accents(input_str)
print(result)
