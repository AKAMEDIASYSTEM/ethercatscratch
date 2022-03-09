installed = [
{
	'name':'EK1100',
	'phase_offsets': []

},
{
	'name':'EL4024',
	'phase_offsets': [0,0,20,20]
},
{
	'name':'EL4024',
	'phase_offsets': [0,0,20,20]
},
{
	'name':'EL4024',
	'phase_offsets': [10,10,0,0]
},
{
	'name':'EL4024',
	'phase_offsets': [30,30,0,0]
},
{
	'name':'EL4008',
	'phase_offsets': [20,20,30,30,10,10,5,5]
},
{
	'name':'EK1100',
	'phase_offsets':[]
},
{
	'name':'EL4008',
	'phase_offsets': [30,30,10,10,7,7,40,40]
},
{
	'name':'EL4008',
	'phase_offsets': [23,23,0,0,23,23,0,0]
},
{
	'name':'EL4008',
	'phase_offsets': [0,0,25,25,0,0,25,25]
},
{
	'name':'EL4008',
	'phase_offsets': [0,0,27,27,0,0,17,17]
},
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