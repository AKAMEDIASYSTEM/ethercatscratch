installed = [
{
	'name':'EK1100',
	'phase_offsets': []

},
{
	'name':'EL4024',
	'phase_offsets': [1,2,3,4]
},
{
	'name':'EK1100',
	'phase_offsets': []

},
{
	'name':'EL4008',
	'phase_offsets': [5,6,7,8,9,10,11,12]
},
{
	'name':'EK1100',
	'phase_offsets': []

},
{
	'name':'EL4008',
	'phase_offsets': [13,14,15,16,17,18,19,20]
},
{
	'name':'EL4024',
	'phase_offsets': [21,22,23,24]
}
]



'''
each wave_index_counter, do this

for this_slave in slaves:
	output_buffer = []
	for this_channel in this_slave['channels']:
		the_value = lut[wave_index_counter]+this_slave['phase_offsets']
		output_buffer.push(the_value)
	master.slaves[this_slave].output = struct.pack(
            'Bx' + ''.join(['H' for i in range(len(output_buffer))]), len(output_buffer), *output_buffer)

'''