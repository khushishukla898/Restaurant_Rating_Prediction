import pickle
from tkinter import Tk, X, Frame, messagebox, IntVar
from tkinter.ttk import Label, Entry, Spinbox, Combobox, Checkbutton, Button
from pandas import DataFrame
import time
import logging
import os

def details_input():
    restaurant_name = entry_name.get()
    logging.info("Entered Value of Restaurant Name is %s", restaurant_name)
    votes = entry_vote.get()
    logging.info("Entered Value of Votes is %s", votes)
    r_type = entry_type.get()
    logging.info("Entered Value of Restaurant Type is %s", r_type)
    location = entry_location.get()
    logging.info("Entered Value of Location is %s", location)
    cost = entry_cost.get()
    logging.info("Entered Value of Cost is %s", cost)
    cuisines = entry_cuisines.get()
    logging.info("Entered Value of Cuisines is  %s", cuisines)
    online_order = chk_button_online.get()
    logging.info("Entered Value of Online Order is %s", online_order)
    book_table = chk_button_booktable.get()
    logging.info("Entered Value of Book Table is %s", book_table)
    #verification
    if len(votes) == 0 or len(r_type) == 0 or len(location) == 0 or len(cost) == 0 or len(cuisines) == 0:
        logging.info("Required Field is Empty")
        return messagebox.showwarning("Field Empty", "Required Field is Empty")
    if not votes.isdigit():
        logging.info("Unacceptable value of Votes")
        return messagebox.showerror("Invalid Value", "Votes has Invalid Value")
    if not cost.isdigit():
        logging.info("Unacceptable value of Cost")
        return messagebox.showerror("Invalid Value", "Cost has Invalid Value")
    if r_type not in options_type:
        logging.info("Unacceptable value of Restaurant Type")
        return messagebox.showerror("Invalid Value", "Select valid Restaurant type")
    if location not in options_location:
        logging.info("Unacceptable value of Location ")
        return messagebox.showerror("Invalid Value", "Select valid Location")

    rating.config(text="Predicted Rating: " + str(
        predictor(online_order=online_order, book_table=book_table, votes=votes, cuisines=cuisines, Cost=cost,
                  rest_type=r_type,
                  City=location)))


def predictor(**kwargs):    #Model and Encoder
    logging.info("Values Heading For Encoding")

    features_df = DataFrame(kwargs, index=[0])

    with open("saves/encoder_rest_type.sav", "rb") as file:
        encoder = pickle.load(file)
        features_df.rest_type = encoder.transform(features_df.rest_type)
    with open("saves/encoder_city.sav", "rb") as file:
        encoder = pickle.load(file)
        features_df.City = encoder.transform(features_df.City)
    with open("saves/encoder_cuisines.sav", "rb") as file:
        encoder = pickle.load(file)
        try:
            features_df.cuisines = encoder.transform(features_df.cuisines)
        except:
            logging.info("Unacceptable value of Cuisines")
            messagebox.showerror("Invalid Value", "Select valid cuisines")
            return ""

    logging.info("Model Recieved The values")
    with open("saves/best_model.sav", "rb") as file:
        model = pickle.load(file)
        rate = model.predict(features_df)

    rate = rate[0]
    if rate > 5:
        rate = 5
    elif rate < 0:
        rate = 0
    logging.info(f"Model Predicted the Rating Value :{rate}")
    return round(rate, 1)


if __name__ == "__main__":
    if not os.path.isdir("logs/"):
        os.mkdir("logs")
    logfile_name = "logs/LOG" + time.strftime("%y%m%d%H%M%S") + ".log"
    logging.basicConfig(filename=logfile_name, filemode="w", level=logging.INFO,
                        format='%(process)d-%(levelname)s-%(asctime)s-%(message)s')
    logging.info("Program has been started")

    root = Tk()
    root.title("Restaurant Rating Predictor")
    root.iconbitmap("cutlery.ico")
    # root.geometry("700x400")

    mainframe = Frame(root, padx=30, pady=30)
    mainframe.pack()
    frame = Frame(mainframe)  # , background="red")
    label = Label(frame, text="Restaurant Rating Prediction", font="LucidSans 15 bold", padding=(5, 0, 0, 20))

    frame.pack(fill=X)
    label.pack(side="left")

    frame2 = Frame(mainframe)  # , background="green")
    frame2.pack(fill=X)

    label_name = Label(frame2, text="Restaurant Name:")
    label_name.grid(sticky="W", columnspan=2, row=1, column=1, padx=5, pady=(10, 2))
    entry_name = Entry(frame2, width=49)
    entry_name.grid(sticky="W", columnspan=2, row=2, column=1, padx=5)

    label_vote = Label(frame2, text="Votes:")
    label_vote.grid(sticky="W", row=1, column=3, padx=5, pady=(10, 2))
    entry_vote = Spinbox(frame2, from_=0, to=1000)
    entry_vote.grid(sticky="W", row=2, column=3, padx=5)

    options_type = ['Buffet', 'Cafes', 'Delivery', 'Desserts', 'Dine-out',
                    'Drinks & nightlife', 'Pubs and bars']
    label_type = Label(frame2, text="Type:")
    label_type.grid(sticky="W", column=1, row=3, padx=5, pady=(10, 2))
    entry_type = Combobox(frame2, values=options_type)
    entry_type.grid(sticky="W", column=1, row=4, padx=5)

    options_location = ['Banashankari', 'Bannerghatta Road', 'Basavanagudi', 'Bellandur',
                        'Brigade Road', 'Brookefield', 'BTM', 'Church Street',
                        'Electronic City', 'Frazer Town', 'HSR', 'Indiranagar',
                        'Jayanagar', 'JP Nagar', 'Kalyan Nagar', 'Kammanahalli',
                        'Koramangala 4th Block', 'Koramangala 5th Block',
                        'Koramangala 6th Block', 'Koramangala 7th Block', 'Lavelle Road',
                        'Malleshwaram', 'Marathahalli', 'MG Road', 'New BEL Road',
                        'Old Airport Road', 'Rajajinagar', 'Residency Road',
                        'Sarjapur Road', 'Whitefield']

    label_location = Label(frame2, text="Location:")
    label_location.grid(sticky="W", column=2, row=3, padx=5, pady=(10, 2))
    entry_location = Combobox(frame2, values=options_location)
    entry_location.grid(sticky="W", column=2, row=4, padx=5)

    label_cost = Label(frame2, text="Cost:")
    label_cost.grid(sticky="W", row=3, column=3, padx=5, pady=(10, 2))
    entry_cost = Spinbox(frame2, from_=0, to=5000)
    entry_cost.grid(sticky="W", row=4, column=3, padx=5)

    label_cuisines = Label(frame2, text="Cuisines")
    label_cuisines.grid(sticky="W", row=5, column=1, padx=5, pady=(10, 2))
    entry_cuisines = Entry(frame2, width=74)
    entry_cuisines.grid(sticky="W", row=6, columnspan=3, column=1, padx=5)
    chk_button_online = IntVar()
    chk_button_booktable = IntVar()
    checkbox_online = Checkbutton(frame2, text="Online Order", variable=chk_button_online)
    checkbox_online.state(['!alternate'])
    checkbox_online.grid(sticky="W", row=7, column=1, padx=5, pady=(10, 2))
    checkbox_booktable = Checkbutton(frame2, text="Book Table", variable=chk_button_booktable)
    checkbox_booktable.state(['!alternate'])
    checkbox_booktable.grid(sticky="W", row=7, column=2, padx=5, pady=(10, 2))

    rating = Label(frame2, text="Predicted Rating:", font=("", 10, "bold"))
    rating.grid(sticky="W", row=8, column=1, padx=5, pady=(10, 2))

    button_predict = Button(mainframe, text="Predict", command=details_input)
    button_predict.pack(side="bottom", anchor="se")
    root.mainloop()
    logging.info("Program Ended")
