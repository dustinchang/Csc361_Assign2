import os
import copy

import file_util
import nat_util
import html_util

class nat:
	def __init__(self,question_library_path,question_path):
		self.question_library_path = question_library_path
		self.question_path = question_path

		config = file_util.dynamic_import(os.path.join(
		 question_library_path,question_path,'cqg_config.py'))
		self.public_ip_address = config.public_ip_address
		self.starting_port = config.starting_port

		self.traffic_list = config.traffic_list
		self.traffic_hotspots = config.traffic_hotspots
		self.conntrack_hotspots = config.conntrack_hotspots

	'''
	purpose
		return question_library_path passed in constructor
	preconditions
		None
	'''
	def get_question_library_path(self):
		return self.question_library_path

	'''
	purpose
		return question_path passed in constructor
	preconditions
		None
	'''
	def get_question_path(self):
		return self.question_path

	'''
	purpose
		return a CSS string which will be placed in the HTML <head> tag
	preconditions
		None
	'''
	def get_css(self,answer):
		return ''

	'''
	purpose
		return a string containing the html to be displayed
		by abstract_question, including answers
	preconditions
		for each key K in get_input_element_ids():
			K is also in answer
			if K was not in submitted answer
				answer[K] == None
	'''
	def get_html(self,answer): 
		s = str(len(self.traffic_list))
		html = '<b>Private Network:10/24 ' '\tPublic IP Address:'+ self.public_ip_address + \
		'<br></br>\nNAT port allocated sequentially starting at ' + self.starting_port + '<br></br></b>'
		#This is where to start doing table stuff
		html += '<center>'
		html += '<table border=1>'
		html += '<tr><td align=center colspan=7> Traffic Table </td></tr>'
		html += '<tr><td align=center colspan=5> 5-tuple </td><td align=center>Direction</td><td align=center>Action</td></tr>'
		counter = 0;
		for row in self.traffic_list:
			html += '<tr>'
			for cell in row:
				if type(cell) is list:
					for a in cell:
						html += '<td>%s</td>'%a
				else:
					html += '<td>%s</td>'%cell
			html += '<td>Accept: <input type=radio name=button_%s value="accept">'%counter	
			html += 'Drop: <input type=radio name=button_%s value="drop"></td>'%counter
			html +='</tr>'
			counter = counter + 1;
		html += '</table>'
		#END OF FIRST TABLE

		Rcount = 0
		Lcount = 0
		Icount = 0
		html += '<br></br><br></br><table border=1>'
		html += '<tr><td align=center colspan=10> Connection tracking table </td></tr>'
		html += '<tr><td align=center colspan=5>Private 5-tuple</td><td align=center colspan=5>Public 5-tuple</td><tr>'

		(T,C) = nat_util.generate_tables(self.traffic_list, self.public_ip_address, self.starting_port)

		for row in C:
			Lcount = 0
			Icount = 0
			html += '<tr>'
			for cell in row:
				Icount = 0
				if type(cell) is list:
					for item in cell:
						RLI = [Rcount, Lcount, Icount]
						if RLI == self.conntrack_hotspots[0]:
							conntrack_nums = 'conntrack_{}_{}_{}'.format(str(Rcount), str(Lcount), str(Icount))
							html += '<td><input type="text" value="" style="width:100%" \
							size="3" name={}></input></td>'.format(conntrack_nums)
						else:
							html += '<td>%s</td>'%item
						Icount += 1
				else:
					html += '<td>%s</td>'%cell
				Lcount += 1
			html += '</tr>'
			Rcount += 1

		html += '</table>'
		html += '</center>'

		return html


	'''
	purpose
		return a list containing the names of the HTML
		input elements returned by get_html()
	preconditions
		None
	'''
	def get_input_element_ids(self):
		
		temp = []
		count = 0
		for k in self.traffic_list:
			temp.append(traffic_button_name(count))
			count += 1
		temp.append(conntrack_textbox_name(self.conntrack_hotspots[0][0], self.conntrack_hotspots[0][1], self.conntrack_hotspots[0][2]))

		print temp
		return temp

	'''
	purpose
		return True iff answer is correct
	preconditions
		for each key K in get_input_element_ids():
			K is also in answer
			if K was not in submitted answer
				answer[K] == None
	'''
	def check_answer(self,answer):
		
		#sanity check to see if radio buttons or textbox unchecked/null
		button_count = 0
		button = 0
		keys = answer.values()
		print keys
		for key in keys:
			print key
			if key == None or key == '':
				return False

		#check to see if radio button correct
		(T,C) = nat_util.generate_tables(self.traffic_list, self.public_ip_address, self.starting_port)
		print T
		print C
		#iterate through radio buttons
		t_count = 0
		for t in T:
			key = 'button_%s' %str(t_count)
			print key
			print answer
			print answer.get(key)
			print 'after getKey'
			if T[t_count][2] != answer.get(key):
				print 'enter if loop'
				return False 
			t_count += 1
		print answer
		return True

# return name of text box in traffic table at row/col
def traffic_textbox_name(row,col):
	return 'traffic_' + str(row) + '_' + str(col)

# return name of radio button in traffic table at row
def traffic_button_name(row):
	return 'button_' + str(row)

# return string name of text box in connection tracking table at row/public_private/col
def conntrack_textbox_name(row,public_private,col):
	return 'conntrack_' + str(row) + '_' + str(public_private) + '_' + str(col)
