'''
To the Max GUI front-end.

Filename: 
    - tothemaxhome.py 

Contains: 
- Classes: FrontEnd
- Methods: browse, run, clear, helper, about, finish, sel_perc, sel_deg,  
           sel_perc_and_deg, sel_northern, sel_southern and unchecked
'''
import tkinter as tk
from tkinter import filedialog
import subprocess
import surface

class FrontEnd():
    '''
    Setup of To the Max GUI home page
    
    Calls tothemaxmain.py with any parameters entered.
    
    Updateable label field
        - File name 
            (URL returned from browse button activation)

    Data entry fields:
        - Resolution / Cell size
            (Optional, integer, > 0, auto poputlated from raster ascii file)
        - Lower left corner Cartesian map reference (x axis)
            (Optional, integer, auto populated from raster ascii file)
        - Lower left corner Cartesian map reference (y axis)
            (Optional, integer, auto populated from raster ascii file)

    Check Buttons
        - Fill sinks cells when no downhill slope
            (optional, translated to single byte text, default=off)
        - Create aspect map
            (optional, translated to single byte text, default=off)
        - Display Parameter Data
            (optional, translated to single byte text, default=off)

    Radio Buttons
        - Create slope map - as a percentage, in degrees or both
            (translated to single byte text, default=D)
        - Specify hemisphere of lower left corner Cartesian map reference
            (translated to single byte text, default=N)
        
    Buttons:
        - Run 
            (Transfers control to tothemaxmain.py with data entry fiels as
             arguments, if entered or selected)
        - Reset
            (Reset input fields)
        - Exit
            (Terminate application)
            
    Display field
        - Run information
            (Displays any information (help, validation errosr etc) returned
             from modelmain.py or the command prompt)

    Menu bar 
        - File > Run 
            (Transfers control to tothemaxmain.py with data entry fiels as
             arguments, if entered)
        - File > Reset
            (Reset fields)
        - File > Exit
            (Terminate application)
        - Help > Input
            (Displays information generated from tothemaxmain.py -h)
        - Help > About
            (Displays general information of the To the Max application)
    '''
    def __init__(self, home):
        '''
        Initialisation of the application GUI front end with:
            - Variables
            - 3 x Entry field
            - 2 x Set Radio buttons
            - 3 x Check buttons
            - 4 x Buttons
            - 1 x Updateable label field
            - 1 x Text field (read only)
            - Menu bar (with cascading items)
        '''
        #-------------------------------------------------
        # Create GUI page
        #-------------------------------------------------
        self.home = home
        
        # Fields for Radio and Check buttons
        self.file_name = tk.StringVar()
        self.resolution = tk.StringVar()
        self.fill_sinks = tk.StringVar()
        self.slope_map = tk.StringVar()
        self.aspect_map = tk.StringVar()
        self.hemisphere = tk.StringVar()
        self.disp_params = tk.StringVar()
        
        # Other general field before we start contructing the layout
        self.menu_bar = tk.Menu(self.home)
        self.home.config(menu=self.menu_bar)
        self.home.geometry('950x850')
        self.home.wm_title('To the Max! - Student 201388212')
        
        #-------------------------------------------------
        # Setup Keyboard shortcuts that can be used
        # irrespective  of where the cursor is located
        #-------------------------------------------------
        self.home.bind('<Alt-b>', self.browse)
        self.home.bind('<Alt-r>', self.run)
        self.home.bind('<Alt-x>', self.finish)
        self.home.bind('<Alt-s>', self.clear)
        
        #-------------------------------------------------
        # Set up Menu Bar and cascading options.
        #-------------------------------------------------
        self.menu_item_1 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_item_2 = tk.Menu(self.menu_bar, tearoff=1)
        self.menu_item_3 = tk.Menu(self.menu_bar, tearoff=2)

        self.menu_bar.add_cascade(label='File', menu=self.menu_item_1)
        self.menu_bar.add_cascade(label='Help', menu=self.menu_item_2)
       
        self.menu_item_1.add_command(
                label='Run...', command=self.run, underline=0)
        self.menu_item_1.add_command(
                label='Reset', command=self.clear, underline=2)
        self.menu_item_1.add_command(
                label='Exit', command=self.finish, underline=1)
        self.menu_item_2.add_command(
                label='Inputs...', command=self.helper)
        self.menu_item_2.add_command(
                label='About...', command=self.about)
        
        #-------------------------------------------------
        # Set up frames for individual screen fields
        #-------------------------------------------------
        frame0 = tk.Frame(self.home)
        frame0.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame1 = tk.Frame(self.home)
        frame1.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame2 = tk.Frame(self.home)
        frame2.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame3 = tk.Frame(self.home)
        frame3.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame4 = tk.Frame(self.home)
        frame4.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame5 = tk.Frame(self.home)
        frame5.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame6 = tk.Frame(self.home)
        frame6.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame7 = tk.Frame(self.home)
        frame7.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame8 = tk.Frame(self.home)
        frame8.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame9 = tk.Frame(self.home)
        frame9.pack(fill=tk.X, expand=False, padx=30, pady=20)

        #-------------------------------------------------
        # Set up screen fields.  There are:
        # 3 x Entry fieds
        # 2 x Radio button sets (2 option and 3 option)
        # 3 x Check buttons
        # 4 x Buttons
        # 1 x Updatable label
        # 1 x Scrollable text box (This will be protected) 
        #-------------------------------------------------
        
        # Frame 0
        l0 = tk.Label(frame0, width=200, height=3, anchor=tk.CENTER, 
                      text='To the Max\nSnowboard Holiday Planners', 
                      font=('Wide Latin', 14), bg='royalblue', fg='White')
        l0.pack(side=tk.LEFT, expand=False)
        
        # Frame 1
        l1 = tk.Label(frame1, width=25, anchor=tk.W, text='File')
        l1.pack(side=tk.LEFT, expand=False)
        
        self.l11 = tk.Label(frame1, anchor=tk.W)
        self.l11.pack(side=tk.LEFT, expand=False)
        
        self.b1 = tk.Button(frame1, text='Browse...', underline=0, width=6,
                            command=self.browse)
        self.b1.bind('<Return>', self.browse)
        self.b1.pack(side=tk.LEFT, expand=False)

        # Frame 2
        l2 = tk.Label(frame2, width=25, anchor=tk.W, 
                      text='Resolution (metres)')
        l2.pack(side=tk.LEFT, expand=False)
        
        self.e1 = tk.Entry(frame2, width=10, textvariable=self.resolution) 
        self.e1.pack(side=tk.LEFT, expand=False)
        
        # Frame 3
        l3 = tk.Label(frame3, width=25, anchor=tk.W, text='Fill sinks')
        l3.pack(side=tk.LEFT, expand=False) 
        
        self.cb1 = tk.Checkbutton(frame3, offvalue=tk.N, onvalue=tk.Y, 
                                  variable=self.fill_sinks, text='')
        self.cb1.pack(side=tk.LEFT, expand=False)
        
        # Frame 4
        l4 = tk.Label(frame4, width=25, anchor=tk.W, 
                      text='Generate slope map')
        l4.pack(side=tk.LEFT, expand=False)
        
        self.rb1 = tk.Radiobutton(frame4, variable=self.slope_map, value='P',
                                  text='Percentage', command=self.sel_perc) 
        self.rb1.pack(side=tk.LEFT, expand=False, padx=10)
        
        self.rb2 = tk.Radiobutton(frame4, variable=self.slope_map, value='D',
                                  text='Degrees', command=self.sel_deg) 
        self.rb2.pack(side=tk.LEFT, expand=False, padx=10)
        
        self.rb3 = tk.Radiobutton(frame4, variable=self.slope_map, value='B',
                                  text='Both', command=self.sel_perc_and_deg) 
        self.rb3.pack(side=tk.LEFT, expand=False, padx=10)
        
        # Frame 5
        l5 = tk.Label(frame5, width=25, anchor=tk.W, 
                      text='Generate aspect map')
        l5.pack(side=tk.LEFT, expand=False) 
        
        self.cb2 = tk.Checkbutton(frame5, offvalue=tk.N, onvalue=tk.Y, 
                                  variable=self.aspect_map, text='')
        self.cb2.pack(side=tk.LEFT, expand=False)
        
        # Frame 6
        l6 = tk.Label(frame6, width=25, anchor=tk.W, 
                      text='Starting extent (metres)')
        l6.pack(side=tk.LEFT, expand=False)
        
        l61 = tk.Label(frame6, anchor=tk.W, text='X:')
        l61.pack(side=tk.LEFT, expand=False)
        self.e2 = tk.Entry(frame6, width=10) 
        self.e2.pack(side=tk.LEFT, expand=False, padx=20)
        
        l62 = tk.Label(frame6, anchor=tk.W, text='Y:')
        l62.pack(side=tk.LEFT, expand=False)
        self.e3 = tk.Entry(frame6, width=10) 
        self.e3.pack(side=tk.LEFT, expand=False, padx=20)

        l63 = tk.Label(frame6, anchor=tk.W, text='Hemisphere:')
        l63.pack(side=tk.LEFT, expand=False)
        self.rb4 = tk.Radiobutton(frame6, variable=self.hemisphere, value='N',
                                  text='Northern', command=self.sel_northern) 
        self.rb4.pack(side=tk.LEFT, expand=False, padx=10)
        
        self.rb5 = tk.Radiobutton(frame6, variable=self.hemisphere, value='S', 
                                  text='Southern', command=self.sel_southern) 
        self.rb5.pack(side=tk.LEFT, expand=False, padx=10)
                
        # Frame 7
        l7 = tk.Label(frame7, width=25, anchor=tk.W, 
                      text='Display parameter data')
        l7.pack(side=tk.LEFT, expand=False)
        

        self.cb4 = tk.Checkbutton(frame7, offvalue=tk.N, onvalue=tk.Y, 
                                  variable=self.disp_params)
        self.cb4.pack(side=tk.LEFT, expand=False)

        # Frame 8
        l7 = tk.Label(frame8, width=25, anchor=tk.W, text=None)
        l7.pack(side=tk.LEFT, expand=False)

        self.b2 = tk.Button(frame8, text='Run', underline=0, width=6,
                            command=self.run)
        self.b2.bind('<Return>', self.run)
        self.b2.pack(side=tk.LEFT, expand=False)
        
        self.b3 = tk.Button(frame8, text='Reset', underline=2, width=6,
                            command=self.clear)
        self.b3.bind('<Return>', self.clear)
        self.b3.pack(side=tk.LEFT, expand=False, padx=20)
        
        self.b4 = tk.Button(frame8, text='Exit', underline=1, width=6,
                            command=self.finish)
        self.b4.bind('<Return>', self.finish)
        self.b4.pack(side=tk.LEFT, expand=False)
        
        # Frame 9
        l9 = tk.Label(frame9, width=25, anchor=tk.W, text='Run information')
        l9.pack(side=tk.LEFT, expand=False)
        
        self.sb1 = tk.Scrollbar(frame9, orient=tk.VERTICAL)
        self.sb1.pack(side=tk.RIGHT, expand=False, padx=10, fill=tk.BOTH)

        self.t1 = tk.Text(frame9, width=600, fg='red', state=tk.DISABLED,
                          yscrollcommand=self.sb1.set)
        self.t1.pack(side = tk.LEFT, expand=False)
        
        #-------------------------------------------------
        # Initialise all input fields.
        #-------------------------------------------------
        self.clear()


    def browse(self, event=None):

        self.file_name = filedialog.askopenfilename(
                                initialdir='/', title='Select A File', 
                                filetype=(('ascii files','*.asc'),
                                          ('all files','*.*')))
        self.l11.configure(text=self.file_name)
        
        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)
        self.e3.delete(0, tk.END)

        if self.file_name == '':
            self.clear()
        else:
            self.b2.configure(state=tk.NORMAL)
            self.menu_item_1.entryconfigure(0, state=tk.NORMAL)
            self.terrain = surface.SurfaceRaster(self.file_name)
            
            try:
                self.terrain.read_raster()
            except:
                self.terrain.close_raster()
                return

            self.terrain.close_raster()

            if self.terrain.cellsize > 0:
                self.e1.insert(0, self.terrain.cellsize)
        
            if self.terrain.xllcorner > 0:
                self.e2.insert(0, self.terrain.xllcorner)

            if self.terrain.yllcorner > 0:
                self.e3.insert(0, self.terrain.yllcorner)
        

    def run(self, event=None):
        '''
        Link to the main To the Max module with any parameters entered.
        
        Display any returned information, errors, help etc.
        
        Note 1: Only parameters that have been entered via the GUI front-end 
        will be passed as arguments to modelhome.py.  
        
        Note 2: Radio and Check button will always have a value.
        '''
        call_string = ''.join(
            ['python tothemaxmain.py',
             ' --filename ' +  '\"' + self.file_name + '\"',
             ' --resolution ' +  self.e1.get() if self.e1.get() != '' else '',
             ' --fillsinks ' +  self.fill_sinks.get(),           # check button
             ' --slopemap ' +  self.slope_map.get(),             # radio button
             ' --aspectmap ' +  self.aspect_map.get(),           # check button
             ' --xref ' +  self.e2.get() if self.e2.get() != '' else '',  
             ' --yref ' +  self.e3.get() if self.e3.get() != '' else '',  
             ' --hemisphere ' +  self.hemisphere.get(),          # radio button
             ' --dispparams ' +  self.disp_params.get()          # check button
            ])
        print(call_string)
        self.b2.focus_set()
        self.t1.configure(state=tk.NORMAL)  
        self.t1.delete(1.0, tk.END)
        self.t1.configure(state=tk.DISABLED)
        
        ret_code, ret_output = subprocess.getstatusoutput(call_string)
        
        self.t1.configure(state=tk.NORMAL)  
        self.t1.insert(tk.END, ret_output)
        self.sb1.config(command=self.t1.yview)
        self.t1.configure(state=tk.DISABLED)

    
    def clear(self, event=None):
        '''
        Set / Reset input fields to their initial values.
        '''
        self.b1.focus_set()
        self.l11.configure(text='')
        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)
        self.e3.delete(0, tk.END)
        self.rb1.deselect()
        self.rb2.select()
        self.sel_deg()
        self.sel_northern()
        self.t1.configure(state=tk.NORMAL)  
        self.t1.delete(1.0, tk.END)
        self.t1.configure(state=tk.DISABLED)
        self.unchecked()
        self.b2.configure(state=tk.DISABLED)
        self.menu_item_1.entryconfigure(0, state=tk.DISABLED)
    
    
    def helper(self):
        '''
        Get the main To the Max help information.
        
        Display information in a popup window.
        '''
        help_return = subprocess.getoutput('python tothemaxmain.py -h') 
        
        help_info = tk.Tk()
        help_info.geometry('900x500')
        help_info.wm_title('Help - To The Max - Student 201388212')
        help_text = tk.Text(help_info)
        help_text.pack(padx=30, pady=30)
        help_text.insert(tk.END, help_return)
        
        b2 = tk.Button(help_info, text='OK', command=help_info.destroy)
        b2.pack()


    def about(self):
        '''
        Display general information about the Agents model in a popup window.
        '''
        about_return = 'To the Max v1.0' \
                       + '\n\nAuthor: 201388212' \
                       + '\n\nCourse: MSc - Geographical Information Science' \
                       + '\n\nUnit: GEOG5003M' \
                       + '\n\nAssignment: 2' \
                       + '\n\nDate: 8 May 2020'
        
        about_info = tk.Tk()
        about_info.geometry('600x450')
        about_info.wm_title('About - To The Max - Student 201388212')
        about_text = tk.Text(about_info)
        about_text.pack()
        about_text.insert(tk.END, about_return)
        
        b2 = tk.Button(about_info, text='OK', command=about_info.destroy)
        b2.pack()
        
    
    def finish(self, event=None):
        '''
        Exit the program.
        '''
        exit()
        
        
    def sel_perc(self):
        '''
        Set the Slope Map radio button to Percentage.
        '''
        self.slope_map.set('P')
            
            
    def sel_deg(self):
        '''
        Set the Slope Map radio button to Degrees.
        '''
        self.slope_map.set('D')

            
    def sel_perc_and_deg(self):
        '''
        Set the Slope Map radio button to Both.
        '''
        self.slope_map.set('B')

            
    def sel_northern(self):
        '''
        Set the Hemishphere radio button to Northern.
        '''
        self.hemisphere.set('N')
            
            
    def sel_southern(self):
        '''
        Set the Hemishphere radio button to Southern.
        '''
        self.hemisphere.set('S')

            
    def unchecked(self):
        '''
        Set all of the Check Buttons off.
        '''
        self.fill_sinks.set(tk.N)
        self.aspect_map.set(tk.N)
        self.disp_params.set(tk.N)
            
            
#-------------------------------------------------
# Main program
#-------------------------------------------------
root = tk.Tk()
window = FrontEnd(root)      
        
#-------------------------------------------------
# Wait for interactions.
#-------------------------------------------------
tk.mainloop() 
        
