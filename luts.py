luts=[{
	'name':'sin_lut',
	# involves is a bitfield describing which muscles are used in the animation
	'involves':[[],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1,1,1,1,1],[],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]], 
	'lut':[16383, 17411, 18436, 19452, 20457, 21445, 22413, 23358, 24275, 25161, 26012, 26825, 27597, 28325, 29006, 29637, 30215, 30739, 31206, 31615, 31964, 32251, 32475, 32636, 32733, 32766, 32733, 32636, 32475, 32251, 31964, 31615, 31206, 30739, 30215, 29637, 29006, 28325, 27597, 26825, 26012, 25161, 24275, 23358, 22413, 21445, 20457, 19452, 18436, 17411, 16382, 15354, 14329, 13313, 12308, 11320, 10352, 9407, 8490, 7604, 6753, 5940, 5168, 4440, 3759, 3128, 2550, 2026, 1559, 1150, 801, 514, 290, 129, 32, 0, 32, 129, 290, 514, 801, 1150, 1559, 2026, 2550, 3128, 3759, 4440, 5168, 5940, 6753, 7604, 8490, 9407, 10352, 11320, 12308, 13313, 14329, 15354, 0]
},
{
	'name':'tri_lut',
	'involves':[[],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1,1,1,1,1],[],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]], 
	'lut':[0, 655, 1310, 1965, 2621, 3276, 3931, 4587, 5242, 5897, 6553, 7208, 7863, 8519, 9174, 9829, 10485, 11140, 11795, 12451, 13106, 13761, 14417, 15072, 15727, 16383, 17038, 17693, 18348, 19004, 19659, 20314, 20970, 21625, 22280, 22936, 23591, 24246, 24902, 25557, 26212, 26868, 27523, 28178, 28834, 29489, 30144, 30800, 31455, 32110, 32766, 32110, 31455, 30800, 30144, 29489, 28834, 28178, 27523, 26868, 26212, 25557, 24902, 24246, 23591, 22936, 22280, 21625, 20970, 20314, 19659, 19004, 18348, 17693, 17038, 16382, 15727, 15072, 14417, 13761, 13106, 12451, 11795, 11140, 10485, 9829, 9174, 8519, 7863, 7208, 6553, 5897, 5242, 4587, 3931, 3276, 2621, 1965, 1310, 655, 0]
},
{
	'name':'testo_lut',
	'involves':[[],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1,1,1,1,1],[],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]], 
	'lut':[ 32036, 31133, 29847, 28735, 27519, 26303, 24809, 22863, 21821, 20917, 18346, 15740, 15115, 14107, 12821, 11223, 9312, 6637, 4726, 3370, 2502, 1946, 1355, 1077, 938, 903, 903, 1355, 8582, 25712, 26929, 27971, 28353, 28492, 28492, 28388, 28179, 27485, 26338, 19423, 12370, 8200, 7505, 6880, 6532, 6463, 6254, 6081, 6011, 6220, 6532, 7262, 7783, 8582, 10841, 22967, 23906, 24809, 24879, 24774, 24566, 24357, 23975, 23419, 22238, 20222, 18311, 9590, 6880, 5490, 4552, 3961, 3579, 3301, 3127, 3092, 3336, 3787, 4413, 5177, 6880, 9451, 12544, 15636, 17999, 19597, 20605, 21508, 22029, 22203, 22203, 22203, 22203, 22099, 21890, 21647, 21195, 20813, 20361, 18972, 17304, 13794, 11605, 7332, 4969, 3822, 3023, 2502, 1842, 1529, 1390, 1216, 1147, 1112, 1077, 1077, 1077, 1077, 0 ]
},
{
	'name':'chunk_lut',
	'involves':[[],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1,1,1,1,1],[],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]], 
	'lut':[ 0, 1080, 3755, 16852, 28682, 29480, 30184, 30513, 29902, 28823, 27368, 23096, 20608, 14224, 11970, 9858, 2676, 1549, 1033, 751, 1127, 2065, 6760, 13519, 15632, 17791, 19716, 21359, 22345, 23988, 25349, 26523, 27743, 28588, 29809, 30372, 30607, 30794, 30794, 30794, 30794, 30560, 30043, 29433, 28494, 26476, 24316, 23331, 22626, 21688, 20749, 19622, 18261, 17510, 16430, 15256, 14411, 12393, 8872, 6901, 5398, 4084, 3333, 2582, 2206, 1831, 1596, 1455, 1127, 1033, 1033, 1267, 1690, 3051, 4882, 7464, 9389, 10844, 13519, 16336, 17510, 19200, 20514, 21406, 22345, 23143, 24175, 24927, 25865, 26851, 27461, 28353, 29104, 29480, 29902, 30231, 30466, 30466, 30466, 30466, 30372, 30090, 29809, 29339, 28870, 28025, 27321, 26194, 25584, 24269, 22392, 20749, 19716, 18448, 4882, 3896, 3286, 2535, 1784, 1080, 704, 0 ]
},
{
	'name':'long_lut',
	'involves':[[],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1,1,1,1,1],[],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]], 
	'lut':[ 329, 516, 1127, 1596, 2065, 2535, 2957, 3333, 3755, 4225, 4647, 5070, 5539, 6196, 6760, 7464, 7980, 8825, 9342, 10093, 10656, 11360, 11970, 12956, 13848, 14787, 15397, 16712, 18214, 19528, 20749, 21969, 22626, 23424, 24175, 24974, 25725, 26663, 27227, 27696, 28353, 28729, 29104, 29621, 30043, 30419, 30607, 30747, 30982, 31123, 31123, 31123, 31123, 31123, 31123, 31076, 31076, 30888, 30794, 30794, 30654, 30654, 30607, 30607, 30607, 30607, 30607, 30607, 30607, 30607, 30607, 30701, 30701, 30747, 30794, 30888, 30935, 30982, 30982, 30982, 30982, 30982, 30982, 30982, 30841, 30701, 30466, 30325, 29949, 29856, 29668, 29198, 29104, 28964, 28541, 28260, 28025, 27837, 27415, 27039, 26663, 26194, 25537, 24786, 24035, 23377, 22345, 20843, 19059, 17557, 16336, 15022, 13707, 11125, 8919, 6196, 3755, 610, 0, 0, 0 ]
},
{
	'name':'decay_lut',
	'involves':[[],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1,1,1,1,1],[],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]],
	'lut':[ 28400, 28353, 28119, 27978, 27790, 27743, 27649, 27602, 27415, 27227, 27180, 27086, 26898, 26851, 26710, 26663, 26663, 26523, 26476, 26288, 26100, 25959, 25912, 25865, 25772, 25725, 25537, 25537, 25349, 25349, 25161, 25114, 25020, 24974, 24833, 24645, 24645, 24598, 24598, 24551, 24410, 24410, 24363, 24363, 24363, 24269, 24222, 24175, 24175, 24175, 24175, 24175, 24082, 24035, 23988, 23988, 23988, 23988, 23988, 23988, 23988, 23894, 23847, 23847, 23659, 23612, 23471, 23331, 23143, 23049, 22908, 22720, 22532, 22392, 22298, 22157, 21969, 21828, 21734, 21547, 21359, 21077, 20889, 20702, 20514, 20232, 19904, 19669, 19481, 19153, 18824, 18448, 18167, 17838, 17463, 17087, 16571, 16148, 15585, 14975, 14411, 13848, 13144, 12721, 12158, 11642, 11078, 10515, 10140, 9576, 8872, 8121, 7135, 6196, 5211, 4131, 2770, 1925, 1314, 0 ]
},
{
	'name':'silence_lut',
	'involves':[[],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1,1,1,1,1],[],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]],
	'lut': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}]