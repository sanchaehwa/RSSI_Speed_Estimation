put = input('문자 입력: ')
ongoing = ""
memory = ""
for char in put:
    if char == " " and memory == " ":
        continue
    ongoing += char
    memory = char

print(ongoing)
output = list(ongoing)
print(output)