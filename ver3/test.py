import marker

file = 'output.jpg'
[[dc_y_EHUFCO],[dc_y_EHUFSI]] = marker.readfile(file, 'DHT', 0, True)
[[ac_y_EHUFCO],[ac_y_EHUFSI]] = marker.readfile(file, 'DHT', 1, True)
[[dc_c_EHUFCO],[dc_c_EHUFSI]] = marker.readfile(file, 'DHT', 2, True)
[[ac_c_EHUFCO],[ac_c_EHUFSI]] = marker.readfile(file, 'DHT', 3, True)
print('\nDC\n', dc_y_EHUFCO, '\nAC\n', dc_y_EHUFSI)
print('\nDC\n', ac_y_EHUFCO, '\nAC\n', ac_y_EHUFSI)
print('\nDC\n', dc_c_EHUFCO, '\nAC\n', dc_c_EHUFSI)
print('\nDC\n', ac_c_EHUFCO, '\nAC\n', ac_c_EHUFSI)