def reverse(string):
    if len(string) in [0, 1]:
        return string
    else:
        return reverse(string[1:]) + string[0]

print(reverse('augah'))
