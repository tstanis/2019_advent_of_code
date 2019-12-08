image_width = 25
image_height = 6

pixels = ''
with open('day8.txt') as file:
    lines = []
    for line in file:
        lines.append(line.rstrip())
    pixels = ''.join(lines)

#print("Pixels: " + str(len(pixels)))
layer_sz = image_width * image_height
layers = []
for i in range(0, len(pixels), layer_sz):
    layers.append(pixels[i:i+layer_sz])

#print("Num Layers: " + str(len(layers)))
#print(str(len(layers[0])))
best_zeros = 100000
best_product = 0
for layer in layers:
    num_zeros = layer.count('0')
    if num_zeros < best_zeros:
        num_ones = layer.count('1')
        num_two = layer.count('2')
        #print("Num Zero " + str(num_zeros) + " Num Ones " + str(num_ones) + " Num Twos " + str(num_two))
        best_product = num_ones * num_two
        best_zeros = num_zeros

print("Best Zeros: " + str(best_zeros))
print("Best Product: " + str(best_product))

decoded_layer = [0] * layer_sz
for i in range(0, layer_sz):
    for layer in layers:
        if layer[i] != '2':
            decoded_layer[i] = layer[i]
            break

for y in range(0, image_height):
    start = y * image_width
    print(''.join(decoded_layer[start:start+image_width]))
