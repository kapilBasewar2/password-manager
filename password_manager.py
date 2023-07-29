from distutils.cmd import Command
from tkinter import CENTER, PhotoImage, Tk,Label, Button, Entry,Frame,END, Toplevel,messagebox
from tkinter import ttk
from turtle import bgcolor
from db_operations import DbOperations
import tkinter as tk
from PIL import Image, ImageTk
import string,random


class root_window:

    def __init__(self,root,db):
        self.db=db
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("1100x650")
        self.root.configure(bg='pink')
        
        head_title = Label(self.root, text="Password Manager",width=30,font=("Algerian", 24, "bold"),padx=5,pady=10, justify=CENTER, anchor="center").grid(columnspan=4, padx=100,pady=20)

        self.crud_frame= Frame(self.root, highlightbackground="black",highlightthickness=1,padx=60,pady=30,bg='pink')
        self.crud_frame.grid()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()
        self.col_no+=1
        
        
        self.create_records_tree()

    def create_entry_labels(self):
        self.col_no, self.row_no=0, 0
        labels_info =('Email or Phone (Optional)','Website Name','Username','Password')
        for label_info in labels_info:
            Label(self.crud_frame,text=label_info ,bg='yellow',fg='black',font=('Ariel',12), padx=5, pady=2).grid(row=self.row_no,column=self.col_no, padx=5, pady=2)
            self.col_no+=1


    def create_crud_buttons(self):
        self.row_no += 1
        self.col_no = 0
        crud_buttons_frame = Frame(self.crud_frame, bg='pink')
        crud_buttons_frame.grid(row=self.row_no, column=0, columnspan=4, padx=5, pady=10)

        buttons_info = (('Save', 'green', self.save_record), ('Update', 'blue', self.update_record), ('Delete', 'red', self.delete_record), ('Copy Password', 'violet', self.copy_password), ('Clear Record','Black',self.create_new_record))

        for idx, btn_info in enumerate(buttons_info):
       
            if btn_info[0] == 'Update':
                Button(crud_buttons_frame, text=btn_info[0], bg=btn_info[1], fg='white', font=('Ariel', 12), width=19, command=lambda btn_info=btn_info: self.get_id_input()).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)
            elif btn_info[0] == 'Delete':
                Button(crud_buttons_frame, text=btn_info[0], bg=btn_info[1], fg='white', font=('Ariel', 12), width=19, command=lambda btn_info=btn_info: self.get_id_inputid()).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)
            elif btn_info[0] == 'Clear Record':
                Button(crud_buttons_frame, text=btn_info[0], bg=btn_info[1], fg='white', font=('Ariel', 12), width=19, command=lambda btn_info=btn_info: self.create_new_record()).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)
            else:
                Button(crud_buttons_frame, text=btn_info[0], bg=btn_info[1], fg='white', font=('Ariel', 12), width=19, command=btn_info[2]).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)

            self.col_no += 1

    
        self.row_no += 1

    
        additional_buttons_frame = Frame(self.crud_frame, bg='pink')
        additional_buttons_frame.grid(row=self.row_no, column=0, columnspan=4, padx=5, pady=10)

   
        Button(additional_buttons_frame, text="Show All Records", bg='purple', fg='white', font=('Ariel', 12), width=19, command=self.show_records).grid(row=0, column=0, padx=5, pady=10)

    
        Button(additional_buttons_frame, text="Delete All Record", bg='dark red', fg='white', font=('Ariel', 12), width=19, command=self.delete_all_record).grid(row=0, column=1, padx=5, pady=10)
        
        Button(additional_buttons_frame, text="Search", bg="orange", fg="white", font=("Ariel", 12), width=19, command=self.open_search_popup).grid(row=0, column=2, padx=5, pady=10)

        Button(additional_buttons_frame, text="Generate Password", bg="grey", fg="white", font=("Ariel", 12), width=19, command=self.generate_password).grid(row=0, column=3, padx=5, pady=10)
           
        self.col_no += 1 

    def create_entry_boxes(self):
        self.row_no+=1
        self.entry_boxes = []
        self.col_no = 0
        for i in range(4):
            show=""
            entry_box = Entry(self.crud_frame, width=20 ,background="lightgrey", font=("Ariel", 12),show=show)
            entry_box.grid(row=self.row_no,column=self.col_no, padx=5 ,pady=2)
            self.col_no+=1
            self.entry_boxes.append(entry_box)

    #CRUD FUNTIONS

    def save_record(self):
        gmail_id = self.entry_boxes[0].get()
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()
        if not website or not username or not password:
            self.showmessage("Error", "Please fill all the fields")
            return
        data = {'gmail_id': gmail_id, 'website': website, 'username': username, 'password': password}
        self.db.create_record(data)
        self.show_records()
        self.clear_input_fields()

    def update_record(self, id_value):
  
        gmail_id = self.entry_boxes[0].get()
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()
        if not website or not username or not password:
            self.showmessage("Error", "Please fill all the fields")
            return
        data ={'ID': id_value,'gmail_id':gmail_id,'website':website,'username':username,'password':password}
        self.db.update_record(data)
        self.show_records()
        self.clear_input_fields()


    def show_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        records_list = self.db.show_records()
        for record in records_list:
            self.records_tree.insert('', END, values=record)


    def create_records_tree(self):
        columns = ('ID', 'Email', 'website', 'username', 'password')
        self.records_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.records_tree.heading('ID', text="Record ID")
        self.records_tree.heading('Email', text="Email or Phone")
        self.records_tree.heading('website', text="Website Name")
        self.records_tree.heading('username', text="Username")
        self.records_tree.heading('password', text="Password")
        self.records_tree['displaycolumns'] = ('ID', 'Email', 'website', 'username','password')


        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                record = item['values']
            for entry_box, item in zip(self.entry_boxes[0:], record[1:]):
                entry_box.delete(0, END)
                entry_box.insert(0, item)

        self.records_tree.bind('<<TreeviewSelect>>',item_selected)

        self.records_tree.grid()


    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entry_boxes[3].get())
        message = "Password Copied"
        title = "Copy"
        if self.entry_boxes[3].get()=="":
            message="Box is Empty"
            title="Error"
        self.showmessage(title, message)

    def showmessage(self, title_box:str=None, message:str=None):
        TIME_TO_WAIT = 900 
        root = Toplevel(self.root)
        background ="green"
        if title_box == "Error":
            background="red"
        root.geometry("200x30+600+200")
        root.title(title_box)
        Label(root,text=message, background=background,font=("Ariel",15),fg='white').pack(pady=2)
        try:
            root.after(TIME_TO_WAIT,root.destroy)
        except Exception as e:
            print("Error occured", e)

    def delete_record(self):
        record_id = self.entry_boxes[0].get()  
        if record_id:
        
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
            if confirm:
                self.db.delete_record(record_id)
                self.show_records()
        else:
            self.showmessage("Error", "Please enter an ID to delete.")

    def get_id_input(self):
 
        top = Toplevel(self.root)
        top.title("Enter ID")
    
   
        entry_id = Entry(top, font=("Ariel", 12), width=20)
        entry_id.grid(row=0, column=0, padx=10, pady=5)

   
        def update_with_id():
            id_value = entry_id.get()
            if id_value:
            
                self.update_record(id_value)
                top.destroy()

        button_update = Button(top, text="Update", bg="blue", fg="white", font=("Ariel", 12), command=update_with_id)
        button_update.grid(row=0, column=1, padx=10, pady=5)

    



    def get_id_inputid(self):
    
        top = Toplevel(self.root)
        top.title("Enter ID")
        top.geometry("250x100")

    
        Label(top, text="Enter ID to delete:", font=("Arial", 12)).pack(pady=10)
        id_entry = Entry(top, font=("Arial", 12))
        id_entry.pack(pady=0)

   
        delete_btn = Button(top, text="Delete", bg="red", fg="white", font=("Arial", 12),
                        command=lambda: self.delete_record_by_id(id_entry.get(), top))
        delete_btn.pack(pady=0)

    def delete_record_by_id(self, id_value, top):
        if id_value.strip() == "":
            messagebox.showerror("Error", "Please enter a valid ID.")
        else:
          
            if not self.db.is_record_exists(id_value):
                messagebox.showerror("Error", "Record with the given ID does not exist.")
            else:
                self.db.delete_record(id_value)
                self.show_records()
                messagebox.showinfo("Success", "Record deleted successfully.")

        top.destroy()

    def delete_all_record(self):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all records?")
        if confirm:
            self.db.delete_all_record()
            self.show_records()
    
    def open_search_popup(self):
        top = Toplevel(self.root)
        top.title("Search Records")
        top.geometry("300x150")
        
    
        Label(top, text="Website:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        website_entry = Entry(top, font=("Arial", 12))
        website_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(top, text="Username:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        username_entry = Entry(top, font=("Arial", 12))
        username_entry.grid(row=1, column=1, padx=10, pady=5)


        Button(top, text="Search", bg="orange", fg="white", font=("Arial", 12), command=lambda: self.search_records_popup(website_entry.get(), username_entry.get(), top)).grid(row=2, columnspan=2, padx=10, pady=5)

    def search_records_popup(self, website, username, top):
        top.destroy()  


        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        records_list = self.db.search_records(website, username)

        for record in records_list:
            self.records_tree.insert('', END, values=record)

    def clear_input_fields(self):
        for entry_box in self.entry_boxes:
            entry_box.delete(0, END)

    def generate_password(self):
        
        password_length = 10
        characters = string.ascii_letters + string.digits + string.punctuation
        generated_password = ''.join(random.sample(characters, password_length))
        self.entry_boxes[3].delete(0, END)
        self.entry_boxes[3].insert(0, generated_password)

    def create_new_record(self):
        for entry_box in self.entry_boxes:
            entry_box.delete(0, END)
# ... (existing code)

#if __name__=="__main__":

#create table if doesn't exist
    #db_class=DbOperations()
    #db_class.create_table()

    #create tkinter window
    #root = Tk()
    #root_class =root_window(root,db_class)
    #root.mainloop() 