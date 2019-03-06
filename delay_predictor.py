import tkinter as tk
import sys
from data_manager import *


class main_window(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.frames={'home':home,'config':config}
		self.show_page('home')
	def show_page(self,page_name):
		self.frames[page_name](self).pack()

class home(tk.Frame):
	def __init__(self,parent):
		tk.Frame.__init__(self,parent)
		self.parent=parent
		self.selector=Select_popup(container=self.parent,parent=self)
		self.response={'station':'','train':''}#,'date':''}

		stationL=tk.Label(self,text='Select The station')
		stationL.pack()

		self.stationB=tk.Button(self,text='Click to select station',command=self.station_fun)
		self.stationB.pack()

		trainL=tk.Label(self,text='Select The Train')
		trainL.pack()

		self.trainB=tk.Button(self,text='Click to select train',command=self.train_fun)
		self.trainB.pack()

		'''dateL=tk.Label(self,text='Select The Date')
		dateL.pack()

		self.dateB=tk.Button(self,text='Click to select date',command=self.date_fun)
		self.dateB.pack()'''

		self.statusL=tk.Label(self,text='')
		self.statusL.pack()

		get_delayB=tk.Button(self,text='Get Delay',command=self.get_delay_fun)
		get_delayB.pack()

		configB=tk.Button(self,text='Config',command=self.config_fun)
		configB.pack()

	
	def station_fun(self):
		self.response['train']=''
		self.trainB.configure(text='Click to select train')

		global avg_delays,stations
		self.selector.data=[code+' | '+stations[code] for code in avg_delays.keys() if code in stations]
		self.selector.responseB=self.stationB
		self.selector.response_label='station'
		self.selector.update_list()
		self.pack_forget()
		self.selector.pack()

	def train_fun(self):
		if(self.response['station']==''):
			self.statusL.configure(text='Please select a station')
			return
		global trains,avg_delays
		self.selector.data=[code+' | '+trains[code] for code in avg_delays[self.response['station']].keys() if code in trains]
		self.selector.responseB=self.trainB
		self.selector.response_label='train'
		self.selector.update_list()
		self.pack_forget()
		self.selector.pack()


	def get_delay_fun(self):
		for label in self.response.keys(): 
			if(self.response[label]==''):
				self.statusL.configure(text='Please select a '+label)
				return
		global avg_delays
		self.statusL.configure(text=f'''The expected delay  is:{int(avg_delays[self.response['station']][self.response['train']])} minutes''')

	def config_fun(self):
		self.pack_forget()
		self.destroy()
		self.parent.show_page('config')


class config(tk.Frame):
	def __init__(self,parent):
		tk.Frame.__init__(self,parent)
		self.parent=parent

		backB=tk.Button(self,text='Back',command=self.back_fun)
		backB.pack()

		update_stationsB=tk.Button(self,text="Update Stations List",command=self.update_stations_fun)
		update_stationsB.pack()

		update_trainsB=tk.Button(self,text='Update Trains List',command=self.update_trains_fun)
		update_trainsB.pack()

		update_avg_delaysB=tk.Button(self,text='Update Delays',command=self.update_avg_delays_fun)
		update_avg_delaysB.pack()

	def update_stations_fun(self):
		global stations
		stations=update_stations_trains('stations')
	def update_trains_fun(self):
		global trains
		trains=update_stations_trains('trains')
	def update_avg_delays_fun(self):
		global stations,avg_delays
		avg_delays=update_avg_delays(stations)
	def back_fun(self):
		self.pack_forget()
		self.destroy()
		self.parent.show_page('home')

class Select_popup(tk.Frame):

    def __init__(self,container,parent):
        tk.Frame.__init__(self,container)

        self.parent=parent
        #self.pack()

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        self.entry = tk.Entry(self, textvariable=self.search_var, width=13)
        self.lbox = tk.Listbox(self, width=45, height=15)

        self.entry.grid(row=0, column=0, padx=10, pady=3)
        self.lbox.grid(row=1, column=0, padx=10, pady=3)

        proceedB=tk.Button(self,text="Proceed",command=self.proceed_fun)
        proceedB.grid(row=2,column=0,padx=10,pady=3)

        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.

    def update_list(self):
        search_term = self.search_var.get()
        #global lbox_list
        self.lbox.delete(0, tk.END)
        self.cur_list=[]
        for item in self.data:
                if search_term.lower() in item.lower():
                    self.lbox.insert(tk.END, item)
                    self.cur_list.append(item)

    def proceed_fun(self):
    	selections=self.lbox.curselection()
    	if(len(selections)!=0):
    		response=self.cur_list[selections[0]]
    		self.responseB.configure(text=response)
    		self.parent.response[self.response_label]=response.split(' | ')[0]
    	self.entry.delete(0,tk.END)
    	self.pack_forget()
    	self.parent.pack()
        


stations=filefetch_stations_trains('stations')
trains=filefetch_stations_trains('trains')
avg_delays=filefetch_avg_delays()
main_window()
tk.mainloop()
